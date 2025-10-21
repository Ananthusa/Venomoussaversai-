import json
import random
import os
from copy import deepcopy

# -----------------------------
# NAS Node Simulation
# -----------------------------
class NASNode:
    def __init__(self, node_name):
        self.node_name = node_name
        self.data_file = f"{node_name}_data.json"
        self.state = {"population": [], "day": 0}

    def save_state(self):
        with open(self.data_file, "w") as f:
            json.dump(self.state, f, indent=2)

    def load_state(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                self.state = json.load(f)

    def update_population(self, population):
        """Serialize population state"""
        self.state["population"] = [
            {
                "name": h.name,
                "resources": h.resources,
                "stability": h.stability,
                "alive": h.alive,
                "gather_efficiency": getattr(h, "gather_efficiency", 1.0),
            }
            for h in population
        ]

    def sync_with(self, other_node):
        """Merge states between NAS nodes"""
        merged_state = deepcopy(self.state)
        for i, human_data in enumerate(other_node.state["population"]):
            if i < len(merged_state["population"]):
                # Update alive/resources/stability
                for key in ["resources", "stability", "alive", "gather_efficiency"]:
                    merged_state["population"][i][key] = max(
                        merged_state["population"][i][key], human_data[key]
                    )
        merged_state["day"] = max(merged_state["day"], other_node.state["day"])
        self.state = merged_state

# -----------------------------
# Example Population Setup
# -----------------------------
class Human:
    def __init__(self, name):
        self.name = name
        self.resources = 50
        self.stability = 100
        self.alive = True
        self.gather_efficiency = 1.0

population = [Human(f"Human_{i}") for i in range(5)]

# -----------------------------
# Initialize NAS Nodes
# -----------------------------
nas1 = NASNode("Node1")
nas2 = NASNode("Node2")

# -----------------------------
# Simulation Loop with NAS Sync
# -----------------------------
for day in range(1, 6):
    print(f"\n--- Day {day} ---")
    # Update population
    for h in population:
        if h.alive:
            h.resources += random.randint(5, 15) * h.gather_efficiency
            h.stability -= random.randint(0, 5)
            if h.stability <= 0:
                h.alive = False

    # Save to NAS 1
    nas1.update_population(population)
    nas1.state["day"] = day
    nas1.save_state()

    # Save to NAS 2
    nas2.update_population(population)
    nas2.state["day"] = day
    nas2.save_state()

    # Sync NAS nodes (bi-directional)
    nas1.sync_with(nas2)
    nas2.sync_with(nas1)

    # Print status
    for h in population:
        print(f"{h.name}: Alive={h.alive}, Resources={h.resources}, Stability={h.stability}")

# -----------------------------
# Load state from NAS
# -----------------------------
nas1.load_state()
print("\nLoaded state from NAS1:")
print(json.dumps(nas1.state, indent=2))