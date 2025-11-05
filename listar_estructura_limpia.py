import os
import fnmatch

ROOT = "."
OUT = "estructura_clean.txt"

# Carpetas a excluir completamente (en cualquier nivel)
EXCLUDE_DIRS = {
    '.git', '.venv', 'Lib', 'Include', 'Scripts', '__pycache__',
    '.mypy_cache', '.pytest_cache', 'build', 'dist',
    'env', 'venv', 'data/raw', 'data/interim', 'data/tmp'
}

# Patrones de exclusión adicionales (cualquier nivel)
EXCLUDE_PATTERNS = [
    '*site-packages*', '*.dist-info*', '*.egg-info*', '*.pyc', '*.pyo', '*.pyd',
    '*.whl', '*.dll', '*.so', '*.tmp', '*.log'
]

def skip_dir(path):
    for excl in EXCLUDE_DIRS:
        if excl in path.replace("\\", "/"):
            return True
    for pat in EXCLUDE_PATTERNS:
        if fnmatch.fnmatch(path, pat):
            return True
    return False

def skip_file(name):
    return any(fnmatch.fnmatch(name, pat) for pat in EXCLUDE_PATTERNS)

with open(OUT, "w", encoding="utf-8") as f:
    for root, dirs, files in os.walk(ROOT, topdown=True):
        # Filtra directorios antes de descender
        dirs[:] = [d for d in dirs if not skip_dir(os.path.join(root, d))]

        level = root.replace(".", "").count(os.sep)
        indent = " " * 4 * level
        f.write(f"{indent}{os.path.basename(root) or '.'}/\n")

        subindent = " " * 4 * (level + 1)
        for file in sorted(files):
            if not skip_file(file):
                f.write(f"{subindent}{file}\n")

print("Árbol limpio generado en 'estructura_clean.txt'")
