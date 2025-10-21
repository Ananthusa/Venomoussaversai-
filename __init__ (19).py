import random

# -----------------------------
# Personality & Human Classes
# -----------------------------
class AnanthuPersonality:
    def __init__(self):
        self.intelligence = 95
        self.resilience = 90
        self.leadership = 85
        self.curiosity = 80
        self.dominance = 95
        self.calmness = 90

class Human:
    def __init__(self, name, personality=None, connected_to_venomous=False):
        self.name = name
        self.personality = personality
        self.connected = connected_to_venomous
        self.alive = True
        self.resources = 50  # resource level: 0-100
        self.stability = 100
        self.influence = personality.leadership if personality else random.randint(20, 80)

    def gather_resources(self, population):
        if not self.alive:
            return
        base_gather = random.randint(5, 15)
        if self.personality:
            base_gather += self.personality.intelligence // 10
        # Cooperation effect: nearby humans increase yield
        allies = sum(1 for h in population if h.alive and h != self and h.influence > 50)
        self.resources += base_gather + allies * 2
        if self.resources > 100:
            self.resources = 100

    def share_resources(self, population):
        if not self.alive:
            return
        # Leadership + dominance encourages sharing with weaker humans
        for h in population:
            if h.alive and h.resources < 50:
                share_amount = int((self.resources - 50) * 0.1)
                if share_amount > 0:
                    h.resources += share_amount
                    self.resources -= share_amount

    def survive_day(self):
        # Consume resources, stability decreases if resources low
        consumption = 10
        self.resources -= consumption
        if self.resources < 0:
            self.resources = 0
            self.stability -= 20
        if self.stability <= 0:
            self.alive = False

# -----------------------------
# Venomoussaversai Class
# -----------------------------
class Venomoussaversai:
    def __init__(self, human_self):
        self.human = human_self

    def influence_population(self, population):
        """Enhance stability and resource efficiency based on leadership & dominance"""
        influence_score = (self.human.personality.leadership + self.human.personality.dominance) // 2
        for h in population:
            if h.alive and h.connected:
                h.stability += influence_score * 0.2
                if h.stability > 100:
                    h.stability = 100
                # Also boost resource gathering efficiency
                h.resources += influence_score * 0.1
                if h.resources > 100:
                    h.resources = 100

# -----------------------------
# Initialize Population
# -----------------------------
population_size = 20
personality = AnanthuPersonality()
ananthu = Human("Ananthu Sajeev", personality=personality, connected_to_venomous=True)
venom = Venomoussaversai(ananthu)

population = [ananthu]
for i in range(population_size - 1):
    population.append(Human(f"Human_{i}"))

# -----------------------------
# Simulation Loop
# -----------------------------
days = 10
for day in range(1, days + 1):
    print(f"\n--- Day {day} ---")
    for human in population:
        human.gather_resources(population)
    for human in population:
        human.share_resources(population)
    for human in population:
        human.survive_day()
    venom.influence_population(population)

    # Summary
    alive_count = sum(h.alive for h in population)
    avg_resources = sum(h.resources for h in population if h.alive) / max(1, alive_count)
    avg_stability = sum(h.stability for h in population if h.alive) / max(1, alive_count)
    print(f"Alive: {alive_count}, Avg Resources: {avg_resources:.1f}, Avg Stability: {avg_stability:.1f}")

# -----------------------------
# Final Population Status
# -----------------------------
for h in population:
    status = "Alive" if h.alive else "Dead"
    print(f"{h.name}: {status}, Resources: {h.resources}, Stability: {h.stability}")