import random
import json
import os
import time

# -------------------------------
# MEMORY FILES FOR MODULES
# -------------------------------
FILES = {
    'frontal_lobe': 'frontal_lobe_memory.json',
    'motor': 'sai001_motor_memory.json',
    'emotion': 'sai003_emotion_memory.json',
    'guardian': 'guardian_memory.json',
    'mind_talk': 'mind_talk_memory.json'
}

memory = {}
for key, file in FILES.items():
    if os.path.exists(file):
        with open(file, 'r') as f:
            memory[key] = json.load(f)
    else:
        memory[key] = []

# -------------------------------
# MODULES
# -------------------------------

# 1. Frontal Lobe: Decision Making
def frontal_lobe_decision(perception):
    options = ['Move Forward', 'Move Backward', 'Turn Left', 'Turn Right', 'Sit', 'Stand', 'Analyze', 'Evade']
    scores = {opt: random.uniform(0,10) + sum(perception.values())/3 for opt in options}
    decision = max(scores, key=scores.get)
    memory['frontal_lobe'].append({'perception': perception, 'decision': decision})
    with open(FILES['frontal_lobe'], 'w') as f:
        json.dump(memory['frontal_lobe'], f, indent=4)
    return decision

# 2. Motor Cortex (sai001)
def motor_execute(action):
    movements = ['Move Forward', 'Move Backward', 'Turn Left', 'Turn Right', 'Sit', 'Stand', 'Evade']
    if action in movements:
        success = random.uniform(0.8, 1.0)
        memory['motor'].append({'action': action, 'success': success})
        with open(FILES['motor'], 'w') as f:
            json.dump(memory['motor'], f, indent=4)
        return f"Executed {action}, success {success:.2f}"
    return f"No motor action executed for {action}"

# 3. Emotion Influence (sai003)
def emotional_influence():
    emotions = ['Love', 'Fear', 'Motivation', 'Curiosity']
    chosen = random.choice(emotions)
    intensity = random.uniform(0,10)
    memory['emotion'].append({'emotion': chosen, 'intensity': intensity})
    with open(FILES['emotion'], 'w') as f:
        json.dump(memory['emotion'], f, indent=4)
    return chosen, intensity

# 4. Guardian: Protection
def guardian_check():
    threats = ['No threat', 'Zombie', 'Hostile Human', 'Cyber Attack', 'Severe Danger']
    threat = random.choices(threats, weights=[50,20,15,10,5])[0]
    actions = {
        'No threat': ['Standby'],
        'Zombie': ['Evade', 'Defend'],
        'Hostile Human': ['Evade', 'Neutralize'],
        'Cyber Attack': ['Secure Network', 'Disconnect'],
        'Severe Danger': ['Full Defense', 'Evacuate']
    }
    chosen_action = random.choice(actions.get(threat, ['Monitor']))
    memory['guardian'].append({'threat': threat, 'action': chosen_action})
    with open(FILES['guardian'], 'w') as f:
        json.dump(memory['guardian'], f, indent=4)
    return threat, chosen_action

# 5. Mind Talk: Internal Reflection
def mind_talk(perception, decision):
    thought = f"Perceived {perception}, decided to {decision}. Analyzing possible outcomes..."
    memory['mind_talk'].append({'thought': thought})
    with open(FILES['mind_talk'], 'w') as f:
        json.dump(memory['mind_talk'], f, indent=4)
    return thought

# -------------------------------
# VENOMOUSSAVERSAI DIGITAL TWIN CYCLE
# -------------------------------
def venomoussaversai_cycle():
    # Perception
    perception = {'sight': random.randint(0,10), 'sound': random.randint(0,10), 'internal': random.randint(0,10)}
    
    # Frontal Lobe Decision
    decision = frontal_lobe_decision(perception)
    
    # Motor Execution
    motor_result = motor_execute(decision)
    
    # Emotion Influence
    emotion, intensity = emotional_influence()
    
    # Guardian Protection
    threat, protective_action = guardian_check()
    
    # Mind Talk / Reflection
    reflection = mind_talk(perception, decision)
    
    # Cycle Summary
    summary = {
        'perception': perception,
        'decision': decision,
        'motor_result': motor_result,
        'emotion': f"{emotion} ({intensity:.2f})",
        'threat': threat,
        'protective_action': protective_action,
        'reflection': reflection
    }
    return summary

# -------------------------------
# RUN DIGITAL TWIN SIMULATION
# -------------------------------
if __name__ == "__main__":
    print("=== Venomoussaversai Digital Twin Activated ===\n")
    for _ in range(5):
        summary = venomoussaversai_cycle()
        for k,v in summary.items():
            print(f"{k}: {v}")
        print("\n")
        time.sleep(1)  # simulate real-time processing