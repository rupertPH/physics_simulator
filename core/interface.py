from ctypes import *
import numpy as np
import os
from sympy import diff, simplify, lambdify


class Solver:

    def __init__(self, config):

        path_to_solver = os.path.join(
            os.path.dirname(__file__),"..","solver/solver.so"
        )

        self.LIB_solver = cdll.LoadLibrary(path_to_solver)

        #---------------
        # RK4 prototype
        #---------------

        self.rk4_step = self.LIB_solver.rk4_step

        self.rk4_step.argtypes = [
            c_double,                 # t
            c_double,                 # dt
            POINTER(c_double),        # state
            c_int,                    # state size
            POINTER(c_double)         # parameters
        ]

        self.rk4_step.restype = None

        #------------------------------
        # Number of generalized coordinates
        #------------------------------

        self.number_q = config.getint("VARIABLES", "number_q")

        #---------------
        # Initial state
        #---------------

        q_start = [
            float(x.strip())
            for x in config["INITIAL STATE"]["q_start"].split(",")
        ]

        qd_start = [
            float(x.strip())
            for x in config["INITIAL STATE"]["qd_start"].split(",")
        ]

        self.state = np.array(
            q_start + qd_start,
            dtype=np.float64
        )

        #---------------
        # Parameters
        #---------------

        self.params = np.array(
            [float(value) for value in config["PARAMETERS"].values()],
            dtype=np.float64
        )

        #---------------
        # Simulation time
        #---------------

        self.t = 0.0


    #------------------------------
    # Numerical integration step
    #------------------------------
    def step(self, dt):

        self.rk4_step(
            self.t,
            dt,
            self.state.ctypes.data_as(POINTER(c_double)),
            len(self.state),
            self.params.ctypes.data_as(POINTER(c_double))
        )

        self.t += dt


class Diagnostics:

    def __init__(self, compiler):

        # E = sum(qd_i * diff(L, qd_i)) - L

        E = 0

        for qi, qdi in zip(compiler.q, compiler.qd):
            E += qdi * diff(compiler.L, qdi)

        E -= compiler.L

        self.energy_expr = simplify(E)

        args = [
            *compiler.q,
            *compiler.qd,
            *compiler.parameters.values()
        ]

        self.energy_function = lambdify(
            args,
            self.energy_expr,
            modules="numpy"
        )

        self.initial_energy = None

    #------------------------------
    # Total mechanical energy of the system
    #------------------------------     

    def energy(self, state, params):

        values = [
            *state,
            *params
        ]

        return float(self.energy_function(*values))
    
    #------------------------------
    # Energy drift
    #------------------------------  

    def energy_drift(self, state, params):

        E = self.energy(state, params)

        if self.initial_energy is None:
            self.initial_energy = E

        return {
            "energy": E,
            "absolute_drift": E - self.initial_energy,
            "relative_drift":
                (E - self.initial_energy) / self.initial_energy
        }

    #------------------------------
    # Energy report
    #------------------------------ 

    def energy_report(self, state, params):

        drift = self.energy_drift(state, params)

        report = (
            f"Energy: {drift['energy']:.6f}\n"
            f"Absolute Drift: {drift['absolute_drift']:.6f}\n"
            f"Relative Drift: {drift['relative_drift']:.6f}"
        )

        return report


