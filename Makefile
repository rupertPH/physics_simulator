#-----------------------------------
# Check python, gcc & dependencies
#-----------------------------------
check_python:
	@echo "Checking Python version..."
	@python3 --version

check_dependencies:
	@echo "Checking dependencies..."
	@python3 check_dependencies.py

install_dependencies:
	pip install -r requirements.txt

check_gcc:
	@echo "Checking GCC..."
	@command -v gcc >/dev/null 2>&1 || { echo "Error: gcc not found."; exit 1; }
	@gcc --version

check: check_python check_gcc check_dependencies

#-----------------------------------
# Run simulation
#-----------------------------------

compile_solver:
	@echo "Compiling solver..."
	gcc -O3 -Wall -shared -fPIC solver/solver.c solver/rk4.c -o solver/solver.so

CONFIG=config/config_double_pendulum.ini
#CONFIG=config/config_pendulum.ini
#CONFIG=config/config_spring_mass.ini
#CONFIG=config/config_multiple_spring_masses.ini

run:
	@echo "Running simulation..."
	@python main.py $(CONFIG)


#-----------------------------------
# Utilities
#-----------------------------------

clean:
	@echo "Cleaning up..."
	@rm -f solver/solver.so
