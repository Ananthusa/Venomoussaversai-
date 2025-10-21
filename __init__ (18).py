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
        self.zombie = False
        self.stability = 100
        self.frontal_lobe = (personality.intelligence + personality.calmness) // 2 if personality else random.randint(20, 80)

    def make_decision(self, event_risk, reception_signal=0):
        if not self.alive:
            return
        # Effective risk decreases with frontal lobe, reception, and Venomoussaversai
        effective_risk = max(event_risk - (self.frontal_lobe / 200) - (reception_signal / 100), 0)
        if self.connected:
            effective_risk *= 0.5
        # Determine outcome
        if random.random() < effective_risk:
            self.alive = False
            self.zombie = True
        else:
            # Stability decreases depending on stress & resilience
            loss = random.randint(5, 20)
            if self.personality:
                loss *= (100 - self.personality.resilience) / 100
            self.stability = max(self.stability - int(loss), 50)

# -----------------------------
# Venomoussaversai Class
# -----------------------------
class Venomoussaversai:
    def __init__(self, human_self):
        self.human = human_self

    def receive_signal(self, population, environment_threat=0):
        """
        Interpret environment and population signals.
        Output: reception signal for decision-making
        """
        # Signal based on zombie count and average instability
        zombie_threat = sum(h.zombie for h in population) * 0.5
        avg_instability = sum(100 - h.stability for h in population if h.alive) / max(1, sum(h.alive for h in population))
        signal = min(environment_threat + zombie_threat + avg_instability, 100)
        return signal

    def influence_population(self, population, reception_signal=0):
        """
        Stabilize humans connected to Venomoussaversai.
        Influence scales with leadership + dominance + reception signal
        """
        influence = (self.human.personality.leadership + self.human.personality.dominance) // 2
        for human in population:
            if human.alive and human.connected:
                human.stability += influence * 0.1 + reception_signal * 0.2
                if human.stability > 100:
                    human.stability = 100

# -----------------------------
# Initialize Population
# -----------------------------
population_size = 100
personality = AnanthuPersonality()
ananthu = Human("Ananthu Sajeev", personality=personality, connected_to_venomous=True)
venom = Venomoussaversai(ananthu)

population = [ananthu]
for i in range(population_size - 1):
    population.append(Human(f"Human_{i}", personality=None))

# -----------------------------
# Simulation Loop
# -----------------------------
survival_target = int(population_size * 0.1)  # 10% survive
day = 1
base_event_risk = 0.6

while True:
    print(f"\n--- Day {day} ---")
    reception_signal = venom.receive_signal(population, environment_threat=30)

    for human in population:
        human.make_decision(base_event_risk, reception_signal)

    venom.influence_population(population, reception_signal)

    alive_count = sum(h.alive for h in population)
    zombie_count = sum(h.zombie for h in population)
    avg_stability = sum(h.stability for h in population if h.alive) / max(1, alive_count)

    print(f"Alive: {alive_count}, Zombies: {zombie_count}, Avg Stability: {avg_stability:.1f}, Reception Signal: {reception_signal:.1f}")

    if alive_count <= survival_target:
        break
    day += 1

# -----------------------------
# Final Outcome
# -----------------------------
survivors = [h.name for h in population if h.alive]
print("\nFinal Survivors (~10%):", survivors)