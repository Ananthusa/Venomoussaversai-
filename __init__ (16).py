import random

class AnanthuPersonality:
    def __init__(self):
        # Personality traits
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
        self.zombie = False
        self.stability = 100
        # Frontal lobe score influenced by intelligence + calmness
        if personality:
            self.frontal_lobe = (personality.intelligence + personality.calmness) // 2
        else:
            self.frontal_lobe = random.randint(20, 80)

    def make_decision(self, event_risk):
        if not self.alive:
            return
        effective_risk = max(event_risk - (self.frontal_lobe / 200), 0)
        if self.connected:
            # Venomoussaversai support
            effective_risk *= 0.5
        if random.random() < effective_risk:
            self.alive = False
            self.zombie = True
        else:
            # Stability reduced based on stress and resilience
            loss = random.randint(5, 20)
            if self.personality:
                loss *= (100 - self.personality.resilience) / 100
            self.stability = max(self.stability - int(loss), 50)

class Venomoussaversai:
    def __init__(self, human_self):
        self.human = human_self

    def influence_population(self, population):
        # Leadership + dominance improves survival of connected humans
        if not self.human.personality:
            return
        influence = (self.human.personality.leadership + self.human.personality.dominance) // 2
        for human in population:
            if human.alive and human.connected:
                human.stability += influence * 0.1
                if human.stability > 100:
                    human.stability = 100

# Initialize
personality = AnanthuPersonality()
ananthu = Human("Ananthu Sajeev", personality=personality, connected_to_venomous=True)
venom = Venomoussaversai(ananthu)

population = [ananthu]
for i in range(99):
    population.append(Human(f"Human_{i}"))

# Simulation loop
days = 5
event_risk = 0.6
for day in range(1, days + 1):
    print(f"\n--- Day {day} ---")
    for human in population:
        human.make_decision(event_risk)
    venom.influence_population(population)
    alive_count = sum(h.alive for h in population)
    zombie_count = sum(h.zombie for h in population)
    print(f"Alive: {alive_count}, Zombies: {zombie_count}")

# Final survivors
survivors = [h.name for h in population if h.alive]
print("\nFinal Survivors:", survivors)