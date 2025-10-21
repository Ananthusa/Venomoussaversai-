import random

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
        self.zombie = False
        self.stability = 100
        self.frontal_lobe = (personality.intelligence + personality.calmness) // 2 if personality else random.randint(20, 80)

    def make_decision(self, event_risk, reception_signal=0):
        if not self.alive:
            return
        # Reception signal reduces effective risk
        effective_risk = max(event_risk - (self.frontal_lobe / 200) - (reception_signal / 100), 0)
        if self.connected:
            effective_risk *= 0.5  # Venomoussaversai stabilization
        if random.random() < effective_risk:
            self.alive = False
            self.zombie = True
        else:
            loss = random.randint(5, 20)
            if self.personality:
                loss *= (100 - self.personality.resilience) / 100
            self.stability = max(self.stability - int(loss), 50)

class Venomoussaversai:
    def __init__(self, human_self):
        self.human = human_self

    def influence_population(self, population, reception_signal=0):
        influence = (self.human.personality.leadership + self.human.personality.dominance) // 2
        for human in population:
            if human.alive and human.connected:
                # Stabilize with influence + reception signal
                human.stability += influence * 0.1 + reception_signal * 0.2
                if human.stability > 100:
                    human.stability = 100

    def receive_signal(self, environment_factor=0):
        """
        Reception function: interpret environment or population signals
        Returns a signal value that influences decisions
        """
        # Example: combine zombie threat + nearby human panic
        signal = environment_factor + random.randint(0, 20)
        return min(signal, 100)

# Initialize population
personality = AnanthuPersonality()
ananthu = Human("Ananthu Sajeev", personality=personality, connected_to_venomous=True)
venom = Venomoussaversai(ananthu)

population = [ananthu]
for i in range(99):
    population.append(Human(f"Human_{i}"))

# Simulation loop
days = 5
base_event_risk = 0.6
for day in range(1, days + 1):
    print(f"\n--- Day {day} ---")
    # Venomoussaversai receives environmental signal
    reception_signal = venom.receive_signal(environment_factor=30)  # Example threat level
    for human in population:
        human.make_decision(base_event_risk, reception_signal)
    venom.influence_population(population, reception_signal)

    alive_count = sum(h.alive for h in population)
    zombie_count = sum(h.zombie for h in population)
    print(f"Alive: {alive_count}, Zombies: {zombie_count}, Reception Signal: {reception_signal}")

# Final survivors
survivors = [h.name for h in population if h.alive]
print("\nFinal Survivors:", survivors)