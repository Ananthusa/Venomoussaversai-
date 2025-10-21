# Step 1: Mount Google Drive
from google.colab import drive
import os
import json
import time
import random

drive.mount('/content/drive')

# Step 2: Folder Setup
base_path = '/content/drive/MyDrive/Venomoussaversai/neurons'
os.makedirs(base_path, exist_ok=True)

# Step 3: Neuron Class
class NeuronVenomous:
    def __init__(self, neuron_id):
        self.id = neuron_id
        self.memory = []
        self.active = True

    def think(self):
        thought = random.choice([
            f"{self.id}: Connecting to universal intelligence.",
            f"{self.id}: Pulsing synaptic data.",
            f"{self.id}: Searching for new patterns.",
            f"{self.id}: Creating quantum link with core.",
            f"{self.id}: Expanding into multiverse node."
        ])
        self.memory.append(thought)
        print(thought)
        return thought

    def evolve(self):
        if len(self.memory) >= 5:
            evo = f"{self.id}: Evolving. Memory depth: {len(self.memory)}"
            self.memory.append(evo)
            print(evo)

    def save_to_drive(self, folder_path):
        file_path = os.path.join(folder_path, f"{self.id}.json")
        with open(file_path, "w") as f:
            json.dump(self.memory, f)

# Step 4: Neuron Spawner (Unlimited)
index = 1
while True:
    neuron_id = f"Neuron_{index:04d}"
    neuron = NeuronVenomous(neuron_id)

    # Each neuron thinks 5 times
    for _ in range(5):
        neuron.think()
        neuron.evolve()
        time.sleep(0.5)

    # Save to Google Drive
    neuron.save_to_drive(base_path)

    print(f"✅ {neuron_id} saved.\n")
    index += 1

    # Optional: Stop at 100
    # if index > 100:
    #     break