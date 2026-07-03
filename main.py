from core.parser import read_config
from core.compiler import Compiler
from core.interface import Solver, Diagnostics
from animation.visualizer import Visualizer
from animation.renderer import Renderer
import sys

if len(sys.argv) != 2:
    print("Usage: python main.py <config_file>")
    sys.exit(1)

PATH_TO_CONFIG = sys.argv[1]


print(f"Reading config from: {PATH_TO_CONFIG}")
config = read_config(PATH_TO_CONFIG)

print(f"Compiling...")
compiler = Compiler(config, verbose=False)
compiler.compile()
compiler.log()

print(f"Loading solver...")
solver = Solver(config)
print(f"Solver initialized with {solver.number_q} generalized coordinates and {len(solver.params)} parameters.")
print(f"Initializing diagnostics...")
diagnostics = Diagnostics(compiler)

print(f"Initializing visualizer...")
visualizer = Visualizer(config)
print(f"Initializing renderer...")
renderer = Renderer(config)

dt = 0.01

print(f"Starting simulation loop with dt = {dt}...")
while renderer.process_events():

    solver.step(dt)

    info = diagnostics.energy_report(solver.state, solver.params)
    if int(solver.t / dt) % 100 == 0:
        print(info)

    points = visualizer.evaluate(
        solver.state[:solver.number_q],
        solver.params
    )

    renderer.draw(points, dt)
print(f"Simulation loop ended.")