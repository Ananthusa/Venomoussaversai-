import datetime
import threading

class ImmutableAge:
    __instance = None
    __lock = threading.Lock()
    
    def __new__(cls):
        # Singleton pattern to ensure only one instance exists
        if cls.__instance is None:
            with cls.__lock:
                if cls.__instance is None:
                    cls.__instance = super(ImmutableAge, cls).__new__(cls)
                    cls.__instance.__age = 25
        return cls.__instance
    
    @property
    def age(self):
        # Always return 25
        return self.__age
    
    @age.setter
    def age(self, value):
        # Prevent any changes
        print(f"Cannot modify age. It is permanently fixed at {self.__age}.")
    
    def increment_age(self):
        # Even if some code tries to increment, ignore it
        print(f"Attempt to increment age ignored. Age remains {self.__age}.")
    
    def simulate_time_passage(self, years=1):
        # Simulate time passing but age stays constant
        print(f"{years} years passed, but age remains {self.__age}.")

# -----------------------------
# Usage
# -----------------------------
ananthu_age = ImmutableAge()
print(f"Age: {ananthu_age.age}")  # Always 25

# Attempt to modify
ananthu_age.age = 30
ananthu_age.increment_age()
ananthu_age.simulate_time_passage(10)

print(f"Age after attempts: {ananthu_age.age}")  # Still 25