import json
import random
import os

# -------------------------------
# Memory File
# -------------------------------
MEMORY_FILE = 'decision_memory.json'

# Load memory if exists
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, 'r') as f:
        memory = json.load(f)
else:
    memory = []

# -------------------------------
# Human Brain Decision Functions
# -------------------------------
def gather_sensory_data():
    # Simulate sensory input
    return random.randint(1, 10)

def retrieve_relevant_memories():
    if memory:
        return random.choice(memory)['decision']
    return None

def assess_emotional_response(inputs):
    # Random emotion factor
    return random.uniform(-1, 1)

def generate_possible_actions(inputs):
    # Generate 3 example options
    return ['Option A', 'Option B', 'Option C']

def estimate_reward(option):
    return random.uniform(0, 10)

def estimate_risk(option):
    return random.uniform(0, 5)

def option_emotion_factor(option):
    return random.uniform(0, 2)

def apply_heuristics(total_score):
    # Example: small random bias
    for key in total_score:
        total_score[key] += random.uniform(-0.5, 0.5)
    return total_score

def execute(decision):
    print(f"Executing decision: {decision}")

def monitor_feedback(decision):
    # Simulate outcome feedback
    return random.choice(['Success', 'Failure'])

# -------------------------------
# Main Decision-Making Loop
# -------------------------------
def human_brain_decision():
    # Step 1: Process input
    sensory_data = gather_sensory_data()
    past_memory = retrieve_relevant_memories()
    
    # Step 2: Emotional & rational assessment
    emotional_score = assess_emotional_response(sensory_data)
    
    # Step 3: Generate options
    options = generate_possible_actions(sensory_data)
    
    # Step 4: Evaluate options
    total_score = {}
    for option in options:
        reward = estimate_reward(option)
        risk = estimate_risk(option)
        emotional_weight = emotional_score * option_emotion_factor(option)
        total_score[option] = reward - risk + emotional_weight
    
    # Step 5: Apply heuristics
    total_score = apply_heuristics(total_score)
    
    # Step 6: Make decision
    decision = max(total_score, key=total_score.get)
    
    # Step 7: Execute & monitor
    execute(decision)
    outcome = monitor_feedback(decision)
    
    # Save to memory
    memory.append({
        'decision': decision,
        'score': total_score,
        'outcome': outcome
    })
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f, indent=4)
    
    return decision, outcome

# -------------------------------
# Run Example
# -------------------------------
if __name__ == "__main__":
    decision, outcome = human_brain_decision()
    print(f"Decision: {decision}, Outcome: {outcome}")