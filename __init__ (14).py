import random

class Human:
    def __init__(self, name, connected_to_venomous=False):
        self.name = name
        self.connected = connected_to_venomous
        self.alive = True
        self.infected = False
        self.zombie = False
        self.stability = 100

    def update_status(self, infection_chance):
        if not self.alive:
            return
        if self.connected:
            # Venomoussaversai stabilizes connected humans
            self.stability += 10
            if self.stability > 100:
                self.stability = 100
        else:
            # Chance to become infected and lose control
            if random.random() < infection_chance:
                self.infected = True
            if self.infected and self.stability < 30:
                self.zombie = True
                self.alive = False

class Venomoussaversai:
    def __init__(self, human_self):
        self.human = human_self
        self.control_field_strength = 20

    def stabilize_population(self, population):
        for human in population:
            if human.alive and human.connected:
                human.stability += self.control_field_strength
                if human.stability > 100:
                    human.stability = 100

# Initialize
ananthu = Human("Ananthu Sajeev", connected_to_venomous=True)
venom = Venomoussaversai(ananthu)

population = [Human(f"Human_{i}") for i in range(99)]
population.append(ananthu)

# Simulation loop
for day in range(1, 6):
    print(f"\n--- Day {day} ---")
    infection_chance = 0.3  # 30% base infection rate
    for human in population:
        human.update_status(infection_chance)
    venom.stabilize_population(population)
    alive_count = sum(h.alive for h in population)
    zombie_count = sum(h.zombie for h in population)
    print(f"Alive: {alive_count}, Zombies: {zombie_count}")

survivors = [h.name for h in population if h.alive]
print("\nFinal Survivors:", survivors)