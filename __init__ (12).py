import random
import time
import threading

# -------------------------
# AI Hub (Venomoussaversai)
# -------------------------
class Venomoussaversai:
    def __init__(self):
        self.log = []
    
    def analyze_and_distribute(self, world):
        total_need = sum(p.need_score() for p in world.inhabitants)
        for p in world.inhabitants:
            for r, amount in world.resources.items():
                # Distribute based on need, contribution, and skills
                share = ((p.need_score() + p.total_contribution()) / (total_need + 1)) * amount * 0.5
                p.receive_resource(r, share)
    
    def record_event(self, event):
        self.log.append(event)
        print(f"[Venomoussaversai Event]: {event}")

# -------------------------
# Inhabitants
# -------------------------
class Inhabitant:
    def __init__(self, name):
        self.name = name
        self.resources = {"food": 50, "water": 50, "energy": 50, "knowledge": 50, "health": 50, "happiness": 50}
        self.skills = {"farming": random.randint(1,10), "engineering": random.randint(1,10),
                       "teaching": random.randint(1,10), "research": random.randint(1,10)}
        self.productivity = random.randint(5,15)
        self.connections = []
    
    def need_score(self):
        return sum(max(0, 100 - v) for v in self.resources.values())
    
    def total_contribution(self):
        # Sum of all skills and past contributions
        return sum(self.skills.values())
    
    def act(self, world):
        # Generate resources based on skills and random events
        produced = {
            "food": self.skills["farming"] * random.randint(1,5),
            "energy": self.skills["engineering"] * random.randint(1,5),
            "knowledge": self.skills["teaching"] * random.randint(1,5),
            "research": self.skills["research"] * random.randint(1,5)
        }
        for r, amt in produced.items():
            world.resources[r] += amt
        return produced
    
    def receive_resource(self, resource, amount):
        self.resources[resource] += amount
        # Limit max to 100
        self.resources[resource] = min(100, self.resources[resource])
    
    def interact(self, world):
        # Connect or collaborate with random inhabitants
        partner = random.choice(world.inhabitants)
        if partner != self:
            # Improve each other's knowledge or happiness
            self.resources["knowledge"] += 1
            partner.resources["knowledge"] += 1
            self.resources["happiness"] += 1
            partner.resources["happiness"] += 1
            world.ai.record_event(f"{self.name} collaborated with {partner.name}")

# -------------------------
# World
# -------------------------
class ResourceWorld:
    def __init__(self):
        self.resources = {"food": 500, "water": 500, "energy": 500, "knowledge": 500, "health": 500, "happiness": 500}
        self.inhabitants = []
        self.ai = Venomoussaversai()
    
    def add_inhabitant(self, inhabitant):
        self.inhabitants.append(inhabitant)
        self.ai.record_event(f"{inhabitant.name} entered the world")
    
    def random_event(self):
        event_type = random.choice(["flood", "discovery", "festival", "disease"])
        if event_type == "flood":
            self.resources["food"] = max(0, self.resources["food"] - 50)
            self.ai.record_event("Flood reduced food resources!")
        elif event_type == "discovery":
            self.resources["knowledge"] += 30
            self.ai.record_event("A new discovery increased knowledge!")
        elif event_type == "festival":
            for p in self.inhabitants:
                p.resources["happiness"] += 10
            self.ai.record_event("Festival increased happiness for all!")
        elif event_type == "disease":
            for p in self.inhabitants:
                p.resources["health"] = max(0, p.resources["health"] - 20)
            self.ai.record_event("Disease outbreak reduced health!")

# -------------------------
# Simulation Loop
# -------------------------
def world_loop(world):
    while True:
        # Inhabitants act and produce
        for p in world.inhabitants:
            p.act(world)
            p.interact(world)
        
        # Random events
        if random.random() < 0.3:  # 30% chance of event
            world.random_event()
        
        # AI distributes resources
        world.ai.analyze_and_distribute(world)
        
        # Display world status
        print("\n=== World Status ===")
        print(f"Total Resources: {world.resources}")
        for p in world.inhabitants:
            print(f"{p.name} Resources: {p.resources}, Skills: {p.skills}")
        print("====================\n")
        time.sleep(5)

# -------------------------
# Setup
# -------------------------
if __name__ == "__main__":
    world = ResourceWorld()
    names = ["Alice", "Bob", "Charlie", "Dana", "Eli"]
    for n in names:
        world.add_inhabitant(Inhabitant(n))
    
    threading.Thread(target=world_loop, args=(world,), daemon=True).start()
    
    while True:
        time.sleep(1)