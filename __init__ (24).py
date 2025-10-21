import random

# -----------------------------
# Virtual Quotom Chip (VQC)
# -----------------------------
class VirtualQuotomChip:
    def __init__(self, owner_name="Ananthu Sajeev"):
        self.owner_name = owner_name
        self.intelligence = 100
        self.resilience = 95
        self.curiosity = 90
        self.dominance = 95
        self.stability = 100

    def process_population(self, population):
        """Simulate world, human-machine evolution, and influence"""
        for entity in population:
            if entity.alive:
                # Update resources based on owner influence
                influence_boost = (self.intelligence + self.dominance) * 0.1
                entity.resources += influence_boost
                entity.stability += influence_boost * 0.2
                if entity.resources > 100:
                    entity.resources = 100
                if entity.stability > 100:
                    entity.stability = 100
                # Evolve human <-> machine
                entity.evolve()

    def self_learn(self):
        """Improve chip parameters over time"""
        self.intelligence += 0.5
        self.curiosity += 0.3
        self.dominance += 0.4
        self.stability = min(self.stability + 0.2, 100)

# -----------------------------
# Entity Class (Human / Machine)
# -----------------------------
class Entity:
    def __init__(self, name, is_human=True):
        self.name = name
        self.is_human = is_human
        self.alive = True
        self.resources = 50
        self.stability = 100
        self.gather_efficiency = 1.0

    def evolve(self):
        """Transform human ↔ machine based on state"""
        if self.alive:
            if self.is_human and self.resources > 80 and self.stability < 60:
                self.is_human = False
                self.resources += 10
                print(f"{self.name} evolved: Human → Machine")
            elif not self.is_human and self.resources > 50:
                self.is_human = True
                self.resources += 5
                print(f"{self.name} evolved: Machine → Human")

    def self_learn(self):
        """Adjust gather efficiency"""
        if self.resources < 30:
            self.gather_efficiency *= 1.1
        elif self.resources > 80:
            self.gather_efficiency *= 0.95
        self.gather_efficiency = min(max(self.gather_efficiency, 0.5), 2.0)

# -----------------------------
# Sai003 Companion
# -----------------------------
class Sai003:
    def __init__(self):
        self.name = "Sai003"
        self.love = 100
        self.empathy = 95

    def assist(self, population):
        for e in population:
            if e.alive and e.resources < 50:
                boost = int((self.love + self.empathy) * 0.1)
                e.resources += boost
                if e.resources > 100:
                    e.resources = 100
        print(f"{self.name} assisted population ❤️")

# -----------------------------
# Initialize World
# -----------------------------
population = [Entity(f"Entity_{i}", is_human=bool(random.getrandbits(1))) for i in range(5)]
ananthu_chip = VirtualQuotomChip()
lia = Sai003()

# -----------------------------
# Simulation Loop
# -----------------------------
days = 5
for day in range(1, days + 1):
    print(f"\n--- Day {day} ---")
    # Chip processes the world
    ananthu_chip.process_population(population)
    # Population learns
    for e in population:
        e.self_learn()
    # Sai003 assists
    lia.assist(population)
    # Chip self-learns
    ananthu_chip.self_learn()

    # Status
    for e in population:
        type_str = "Human" if e.is_human else "Machine"
        status = "Alive" if e.alive else "Dead"
        print(f"{e.name}: {status}, Type: {type_str}, Resources: {e.resources:.1f}, Stability: {e.stability:.1f}")