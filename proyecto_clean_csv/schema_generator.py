import os

# Carpetas y archivos a excluir
EXCLUDE_DIRS = {".venv", "venv", ".git", "__pycache__", ".pytest_cache", ".ruff_cache", ".vscode", ".python-version"}
EXCLUDE_FILES = {".DS_Store", ".gitignore", "README.md"}

# Profundidad máxima (None = sin límite)
MAX_DEPTH = None  # Cambia a un número como 3 si quieres limitar


def generate_tree(start_path=".", prefix="", depth=0):
    if MAX_DEPTH is not None and depth > MAX_DEPTH:
        return []

    entries = sorted(
        e for e in os.listdir(start_path)
        if e not in EXCLUDE_DIRS and e not in EXCLUDE_FILES
    )

    tree_lines = []

    for index, entry in enumerate(entries):
        path = os.path.join(start_path, entry)
        connector = "└── " if index == len(entries) - 1 else "├── "
        tree_lines.append(prefix + connector + entry)

        if os.path.isdir(path):
            extension = "    " if index == len(entries) - 1 else "│   "
            subtree = generate_tree(path, prefix + extension, depth + 1)
            tree_lines.extend(subtree)

    return tree_lines


if __name__ == "__main__":
    print("Estructura del proyecto:\n")
    print(".")
    tree = generate_tree(".")
    for line in tree:
        print(line)
