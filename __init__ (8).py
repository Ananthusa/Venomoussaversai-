import json
import random
import os

# -------------------------------
# High-Level Motor Memory
# -------------------------------
MOTOR_MEMORY_FILE = 'sai001_high_level_motor.json'

if os.path.exists(MOTOR_MEMORY_FILE):
    with open(MOTOR_MEMORY_FILE, 'r') as f:
        motor_memory = json.load(f)
else:
    motor_memory = []

# -------------------------------
# High-Level Motor Functions
# -------------------------------

# Define high-level actions
HIGH_LEVEL_ACTIONS = [
    'Move Forward', 'Move Backward',
    'Turn Left', 'Turn Right',
    'Sit', 'Stand'
]

def plan_high_level_action():
    """
    Generate motor plans with scores (priority or context)
    """
    scores = {action: random.uniform(0, 10) for action in HIGH_LEVEL_ACTIONS}
    return scores

def execute_high_level_action(action):
    """
    Simulate action execution with success probability
    """
    success_rate = random.uniform(0.8, 1.0)  # High-level actions are mostly reliable
    print(f"Executing action: {action} | Success probability: {success_rate:.2f}")
    return success_rate

def feedback_high_level(action, success_rate):
    """
    Save executed action and success to memory
    """
    motor_memory.append({
        'action': action,
        'success_rate': success_rate
    })
    with open(MOTOR_MEMORY_FILE, 'w') as f:
        json.dump(motor_memory, f, indent=4)

def high_level_motor_loop():
    """
    Full high-level motor control loop
    """
    # Step 1: Plan actions
    action_scores = plan_high_level_action()
    
    # Step 2: Decision (select best action)
    action = max(action_scores, key=action_scores.get)
    
    # Step 3: Execute action
    success = execute_high_level_action(action)
    
    # Step 4: Save feedback
    feedback_high_level(action, success)
    
    return action, success

# -------------------------------
# Run Example
# -------------------------------
if __name__ == "__main__":
    for _ in range(6):
        action, success = high_level_motor_loop()
        print(f"Selected Action: {action}, Success Rate: {success:.2f}\n")