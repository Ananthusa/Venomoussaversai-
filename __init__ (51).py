import time

def self_talk(modules, cycles=10):
    for _ in range(cycles):
        for mod in modules:
            if hasattr(mod, "think"):
                try:
                    mod.think()  # Each module can define a think() function
                except Exception as e:
                    print(f"Error in {mod}: {e}")
        time.sleep(0.1)  # small pause to avoid CPU overload

# Example usage
all_modules = [importlib.import_module(dirpath.replace("/", ".").lstrip(".")) 
               for dirpath, _, files in os.walk(root_path) if "__init__.py" in files]
self_talk(all_modules)