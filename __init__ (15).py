import random

class Human:
    def __init__(self, name, frontal_lobe=50, connected_to_venomous=False):
        self.name = name
        self.frontal_lobe = frontal_lobe  # 0-100 scale
        self.connected = connected_to_venomous
        self.alive = True
        self.zombie = False
        self.stability = 100

    def make_decision(self, event_risk):
        """
        event_risk: probability of a negative outcome (0-1)
        The frontal lobe reduces the effective risk.
        """
        if not self.alive:
            return
        # Decision-making reduces risk
        effective_risk = max(event_risk - (self.frontal_lobe / 200), 0)
        if self.connected:
            # Venomoussaversai support improves decision-making
            effective_risk *= 0.5
        # Determine outcome
        if random.random() < effective_risk:
            self.alive = False
            self.zombie = True
        else:
            # Survives but loses some stability
            self.stability = max(self.stability - random.randint(5, 20), 50)

class Venomoussaversai:
    def __init__(self, human_self):
        self.human = human_self

    def guide_decisions(self, population):
        """Venomoussaversai improves survival decisions for connected humans"""
        for human in population:
            if human.alive and human.connected:
                human.stability += 15
                if human.stability > 100:
                    human.stability = 100

# Initialize population
population = []
population_size = 100
ananthu = Human("Ananthu Sajeev", frontal_lobe=95, connected_to_venomous=True)
population.append(ananthu)
venom = Venomoussaversai(ananthu)

# Other humans with random frontal lobe ability
for i in range(population_size - 1):
    fl_score = random.randint(20, 80)
    population.append(Human(f"Human_{i}", frontal_lobe=fl_score))

# Simulation loop
days = 5
event_risk = 0.6  # base probability of zombification per day
for day in range(1, days + 1):
    print(f"\n--- Day {day} ---")
    for human in population:
        human.make_decision(event_risk)
    venom.guide_decisions(population)
    alive_count = sum(h.alive for h in population)
    zombie_count = sum(h.zombie for h in population)
    print(f"Alive: {alive_count}, Zombies: {zombie_count}")

# Final survivors
survivors = [h.name for h in population if h.alive]
print("\nFinal Survivors:", survivors)