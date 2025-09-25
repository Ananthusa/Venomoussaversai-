import os
import importlib

root_path = "/content/venomoussaversai"  # your AI folder

for dirpath, dirnames, filenames in os.walk(root_path):
    if "__init__.py" in filenames:
        # Convert folder path to Python module path
        module_path = dirpath.replace("/", ".").lstrip(".")
        try:
            module = importlib.import_module(module_path)
            print(f"✅ Loaded: {module_path}")
        except Exception as e:
            print(f"❌ Failed to load {module_path}: {e}")