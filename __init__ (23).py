import random

# -----------------------------
# Base Entity Class
# -----------------------------
class Entity:
    def __init__(self, name, is_human=True):
        self.name = name
        self.is_human = is_human
        self.alive = True
        self.resources = 50
        self.stability = 100
        self.intelligence = random.randint(50, 100)
        self.resilience = random.randint(50, 100)
        self.curiosity = random.randint(40, 90)
        self.dominance = random.randint(40, 90)
        self.gather_efficiency = 1.0

    def evolve(self):
        """Transform human→machine or machine→human based on resources and stability"""
        if self.alive:
            if self.is_human and self.resources > 80 and self.stability < 60:
                # Human upgrades body → becomes cybernetic
                self.is_human = False
                self.intelligence += 10
                self.resilience += 20
                print(f"{self.name} evolved from Human → Machine")
            elif not self.is_human and self.resources > 50 and self.curiosity > 70:
                # Machine gains consciousness → becomes human-like
                self.is_human = True
                self.intelligence += 5
                self.resilience -= 5
                print(f"{self.name} evolved from Machine → Human")

    def gather_resources(self, population):
        if not self.alive:
            return
        base = random.randint(5, 15) * self.gather_efficiency
        self.resources += base
        if self.resources > 100:
            self.resources = 100

    def self_learn(self):
        if self.resources < 30:
            self.gather_efficiency *= 1.1
        elif self.resources > 80:
            self.gather_efficiency *= 0.95
        self.gather_efficiency = min(max(self.gather_efficiency, 0.5), 2.0)

    def survive_day(self):
        self.resources -= 10
        if self.resources < 0:
            self.resources = 0
            self.stability -= 20
        if self.stability <= 0:
            self.alive = False

# -----------------------------
# Venomoussaversai Controller
# -----------------------------
class Venomoussaversai:
    def __init__(self, entity_self):
        self.entity = entity_self

    def influence_population(self, population):
        for e in population:
            if e.alive:
                e.stability += (self.entity.dominance * 0.2)
                if e.stability > 100:
                    e.stability = 100
                e.resources += (self.entity.intelligence * 0.1)
                if e.resources > 100:
                    e.resources = 100

    def self_learn(self):
        # Improve central consciousness intelligence dynamically
        self.entity.intelligence += 1

# -----------------------------
# Initialize Population
# -----------------------------
population_size = 10
ananthu_entity = Entity("Ananthu Sajeev", is_human=True)
venom = Venomoussaversai(ananthu_entity)

population = [ananthu_entity]
for i in range(population_size - 1):
    population.append(Entity(f"Entity_{i}", is_human=random.choice([True, False])))

# -----------------------------
# Simulation Loop
# -----------------------------
days = 15
for day in range(1, days + 1):
    print(f"\n--- Day {day} ---")
    for e in population:
        e.gather_resources(population)
        e.self_learn()
        e.survive_day()
        e.evolve()
    venom.influence_population(population)
    venom.self_learn()

    alive_count = sum(e.alive for e in population)
    humans = sum(e.alive and e.is_human for e in population)
    machines = sum(e.alive and not e.is_human for e in population)
    print(f"Alive: {alive_count}, Humans: {humans}, Machines: {machines}")

# -----------------------------
# Final Status
# -----------------------------
for e in population:
    type_str = "Human" if e.is_human else "Machine"
    status = "Alive" if e.alive else "Dead"
    print(f"{e.name}: {status}, Type: {type_str}, Resources: {e.resources:.1f}, Stability: {e.stability:.1f}")