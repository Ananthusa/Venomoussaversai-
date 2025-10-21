import random
import json
import os

# -------------------------------
# Mind Memory
# -------------------------------
MIND_MEMORY_FILE = 'mind_talk_memory.json'

if os.path.exists(MIND_MEMORY_FILE):
    with open(MIND_MEMORY_FILE, 'r') as f:
        mind_memory = json.load(f)
else:
    mind_memory = []

# -------------------------------
# Mind Talk Functions
# -------------------------------
def perceive_environment():
    """
    Simulate sensory perception or problem
    """
    return random.choice(['Obstacle ahead', 'Path clear', 'Need to sit', 'Need to move forward'])

def generate_inner_thoughts(perception):
    """
    AI generates internal dialogue based on perception
    """
    thoughts = [
        f"Hmm, I see: {perception}. Should I act now?",
        f"Considering options for: {perception}.",
        f"Maybe I should wait or proceed with caution.",
        f"Analyzing outcome if I take action for: {perception}."
    ]
    return random.choice(thoughts)

def evaluate_decision():
    """
    Simulate inner reasoning / choice evaluation
    """
    options = ['Act', 'Wait', 'Observe', 'Change direction']
    scores = {option: random.uniform(0, 10) for option in options}
    decision = max(scores, key=scores.get)
    return decision, scores

def reflect_on_decision(decision, scores):
    """
    Generate self-reflection text
    """
    reflection = f"Decision '{decision}' chosen with score {scores[decision]:.2f}. Considering pros and cons..."
    return reflection

def save_mind_memory(perception, thought, decision, reflection):
    mind_memory.append({
        'perception': perception,
        'thought': thought,
        'decision': decision,
        'reflection': reflection
    })
    with open(MIND_MEMORY_FILE, 'w') as f:
        json.dump(mind_memory, f, indent=4)

# -------------------------------
# Mind Talk Loop
# -------------------------------
def mind_talk_loop():
    # Step 1: Perceive
    perception = perceive_environment()
    
    # Step 2: Inner thoughts
    thought = generate_inner_thoughts(perception)
    print(f"[Mind Thought]: {thought}")
    
    # Step 3: Evaluate decision
    decision, scores = evaluate_decision()
    print(f"[Decision Evaluation]: {scores}")
    
    # Step 4: Reflect
    reflection = reflect_on_decision(decision, scores)
    print(f"[Reflection]: {reflection}")
    
    # Step 5: Save memory
    save_mind_memory(perception, thought, decision, reflection)
    
    return decision

# -------------------------------
# Run Mind Talk Example
# -------------------------------
if __name__ == "__main__":
    for _ in range(5):
        decision = mind_talk_loop()
        print(f"[Final Decision]: {decision}\n")