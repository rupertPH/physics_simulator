'''
Check if all required dependencies are installed
'''

REQUIRED_MODULES = [
    "numpy",
    "cython",
    "pygame",
    "sympy"
]

missing = []

for module in REQUIRED_MODULES:
    try:
        __import__(module)
    except ImportError:
        missing.append(module)

if missing:
    print("Missing modules:")
    for m in missing:
        print(f"  - {m}")
    exit(1)

print("All required modules installed.")