from sympy import (
    symbols,
    sympify,
    sin,
    cos,
    tan,
    exp,
    log,
    Matrix,
)
from sympy.physics.mechanics import dynamicsymbols, LagrangesMethod
from sympy import IndexedBase
from sympy import ccode
import subprocess


class Compiler:

    def __init__(self, config, verbose=False):

        self.config = config
        self.number_q = config.getint("VARIABLES", "number_q")
        self.verbose = verbose

        self.q = []
        self.qd = []
        self.qdd = []

        self.parameters = {}
        self.param_names = []

        self.rhs = []
        self.L = None
        self.mass_matrix = None
        self.forcing_vector = None
        self.accelerations = None
        self.rhs = None


    # -------------------------
    # SYMBOLS
    # -------------------------
    def create_symbols(self):

        self.q = []
        self.qd = []
        self.qdd = []

        for i in range(1, self.number_q + 1):

            qi = dynamicsymbols(f"q{i}")

            self.q.append(qi)
            self.qd.append(qi.diff())
            self.qdd.append(qi.diff().diff())

        # parameters
        self.parameters = {}
        self.param_names = []

        for name, value in self.config.items("PARAMETERS"):
            self.parameters[name] = symbols(name)
            self.param_names.append(name)

        # runtime arrays
        self.params = IndexedBase("params", shape=(len(self.param_names),))
        self.y = IndexedBase("y", shape=(2 * self.number_q,))

    # -------------------------
    # LAGRANGIAN
    # -------------------------
    def parse_lagrangian(self):

        local_dict = {}

        for i in range(self.number_q):

            local_dict[f"q{i+1}"] = self.q[i]
            local_dict[f"qd{i+1}"] = self.qd[i]

        local_dict.update(self.parameters)

        local_dict.update({
            "sin": sin,
            "cos": cos,
            "tan": tan,
            "exp": exp,
            "log": log,
        })

        lagrangian_text = self.config["LAGRANGIAN"]["L"]

        self.L = sympify(lagrangian_text, locals=local_dict)

    # -------------------------
    # EOM
    # -------------------------
    def solve_accelerations(self):

        LM = LagrangesMethod(self.L, self.q)
        LM.form_lagranges_equations()

        self.mass_matrix = LM.mass_matrix
        self.forcing_vector = LM.forcing

        self.accelerations = self.mass_matrix.LUsolve(self.forcing_vector)

    # -------------------------
    # RHS
    # -------------------------
    def build_rhs(self):

        self.rhs = Matrix([
            *self.qd,
            *self.accelerations
        ])

    # -------------------------
    # SYMBOL REPLACEMENT
    # -------------------------
    def replace_symbols(self):

        subs = {}

        y = self.y

        # q -> y[i]
        for i, qi in enumerate(self.q):
            subs[qi] = y[i]

        # qd -> y[n+i]
        for i, qdi in enumerate(self.qd):
            subs[qdi] = y[self.number_q + i]

        # params -> params[i]
        for i, name in enumerate(self.param_names):
            subs[self.parameters[name]] = self.params[i]

        return [expr.subs(subs) for expr in self.rhs]

    # -------------------------
    # C GENERATION
    # -------------------------
    def generate_solver_c(self):

        rhs = self.replace_symbols()

        with open("solver/solver.c", "w") as file:

            file.write("#include <math.h>\n\n")

            file.write(
                "void rhs(double t, const double y[], double dydt[], const double params[])\n{\n"
            )

            for i, expr in enumerate(rhs):

                code = ccode(expr, standard="C99")

                file.write(f"    dydt[{i}] = {code};\n")

            file.write("}\n")

    # -------------------------
    # BUILD
    # -------------------------
    def build_library(self):

        subprocess.run(
            [
                "gcc",
                "-O3",
                "-shared",
                "-fPIC",
                "solver/solver.c",
                "solver/rk4.c",
                "-o",
                "solver/solver.so"
            ],
            check=True
        )

    # -------------------------
    # COMPILIATION 
    # -------------------------
    def compile(self):

        self.create_symbols()

        self.parse_lagrangian()

        self.solve_accelerations()

        self.build_rhs()

        self.generate_solver_c()

        self.build_library()

    def log(self):

        if self.verbose == True:

            print("\n========== LAGRANGIAN ==========")
            print(self.L)

            print("PARAM MAP:")
            for i, name in enumerate(self.param_names):
                print(i, name)

            print("\n===== MASS MATRIX =====")
            print(self.mass_matrix)

            print("\n===== FORCING VECTOR =====")
            print(self.forcing_vector)

            print("\n===== ACCELERATIONS =====")

            for i, acc in enumerate(self.accelerations):
                print(f"qdd{i+1} = {acc}")

