from sympy import symbols, lambdify
from sympy.parsing.sympy_parser import parse_expr


class Visualizer:

    def __init__(self, config):

        self.config = config

        self.number_q = config.getint("VARIABLES", "number_q")

        self.create_symbols()
        self.parse_visualization()
        self.create_functions()

    def create_symbols(self):

        self.q = symbols(f"q1:{self.number_q + 1}")

        self.parameters = {}

        for key, _ in self.config.items("PARAMETERS"):
            self.parameters[key] = symbols(key)
    
    def parse_visualization(self):

        local_dict = {}

        for qi in self.q:
            local_dict[str(qi)] = qi

        local_dict.update(self.parameters)

        self.visualization_expr = {}

        for key, expr in self.config.items("2D VISUALIZATION"):

            self.visualization_expr[key] = parse_expr(
                expr,
                local_dict=local_dict
            )

    def create_functions(self):

        args = [
            *self.q,
            *self.parameters.values()
        ]

        self.functions = {}

        for key, expr in self.visualization_expr.items():

            self.functions[key] = lambdify(
                args,
                expr,
                modules="numpy"
            )
    
    def evaluate(self, q, params):

        values = [*q, *params]

        points = []

        for i in range(1, self.number_q + 1):

            x = self.functions[f"x{i}"](*values)
            y = self.functions[f"y{i}"](*values)

            points.append((float(x), float(y)))

        return points
    
