import os
import importlib
import sys

# Path to your AI folder
AI_ROOT = "/content/venomoussaversai"

# Step 1: Discover all __init__.py folders
def find_all_init_folders(root_path):
    init_folders = []
    for dirpath, dirnames, filenames in os.walk(root_path):
        if "__init__.py" in filenames:
            init_folders.append(dirpath)
    return init_folders

# Step 2: Convert folder path to Python module path
def folder_to_module_path(folder_path, root_path):
    rel_path = os.path.relpath(folder_path, root_path)
    return rel_path.replace(os.path.sep, ".")

# Step 3: Dynamically import all __init__.py modules
def load_all_init_modules(root_path):
    modules = []
    for folder in find_all_init_folders(root_path):
        module_path = folder_to_module_path(folder, root_path)
        try:
            module = importlib.import_module(module_path)
            modules.append(module)
            print(f"✅ Loaded: {module_path}")
        except Exception as e:
            print(f"❌ Failed to load {module_path}: {e}")
    return modules

# Step 4 (Optional): Call a default 'think' function if it exists
def run_think_loop(modules, interval=0.05):
    import time
    while True:
        for mod in modules:
            if hasattr(mod, "think"):
                try:
                    mod.think()
                except Exception as e:
                    print(f"❌ Error in {mod}: {e}")
        time.sleep(interval)

# === MAIN ===
all_modules = load_all_init_modules(AI_ROOT)
print(f"🧠 Total modules loaded: {len(all_modules)}")

# Uncomment to run self-talk loop
# run_think_loop(all_modules)