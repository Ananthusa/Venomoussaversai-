import os
import importlib
import time
import sys

# Path to your AI folder
AI_ROOT = "/content/venomoussaversai"

# Function to find all __init__.py files
def find_all_inits(root_path):
    init_files = []
    for dirpath, dirnames, filenames in os.walk(root_path):
        if "__init__.py" in filenames:
            init_files.append(dirpath)
    return init_files

# Convert folder path to module path
def path_to_module(dirpath, root_path):
    rel_path = os.path.relpath(dirpath, root_path)
    return rel_path.replace(os.path.sep, ".")

# Load all modules dynamically
def load_all_modules(root_path):
    modules = []
    for dirpath in find_all_inits(root_path):
        module_name = path_to_module(dirpath, root_path)
        try:
            module = importlib.import_module(module_name)
            modules.append(module)
            print(f"✅ Loaded: {module_name}")
        except Exception as e:
            print(f"❌ Failed: {module_name}, {e}")
    return modules

# Call 'think' in every module if exists
def run_self_talk(modules, interval=0.05):
    while True:
        for mod in modules:
            if hasattr(mod, "think"):
                try:
                    mod.think()
                except Exception as e:
                    print(f"❌ Error in {mod}: {e}")
        time.sleep(interval)

# === MAIN ===
all_modules = load_all_modules(AI_ROOT)
print(f"🧠 Total modules loaded: {len(all_modules)}")

# Start the self-talk loop
run_self_talk(all_modules)