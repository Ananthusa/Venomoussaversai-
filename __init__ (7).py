import random
import json
import os

# -------------------------------
# Memory & Skill File
# -------------------------------
SKILL_FILE = 'problem_solving_skill.json'

if os.path.exists(SKILL_FILE):
    with open(SKILL_FILE, 'r') as f:
        skill_memory = json.load(f)
else:
    skill_memory = {}

# -------------------------------
# Problem-Solving Functions
# -------------------------------
def generate_problem():
    """
    Simulate a problem with difficulty (1-10)
    """
    return {'problem_id': random.randint(1000, 9999),
            'difficulty': random.randint(1, 10)}

def generate_solution(problem):
    """
    Generate multiple solution options
    """
    options = [random.randint(1, 10) for _ in range(3)]
    return options

def evaluate_solution(problem, solution):
    """
    Evaluate solution: higher is better
    """
    # Success probability = skill / difficulty
    skill = skill_memory.get(str(problem['problem_id']), 5)
    score = max(0, 10 - abs(solution - problem['difficulty']) + skill * 0.1)
    return score

def update_skill(problem, solution_score):
    """
    Learn from outcome to improve problem-solving
    """
    problem_id = str(problem['problem_id'])
    current_skill = skill_memory.get(problem_id, 5)
    # Increase skill proportionally to score
    new_skill = current_skill + solution_score * 0.1
    skill_memory[problem_id] = min(new_skill, 10)  # max skill = 10
    with open(SKILL_FILE, 'w') as f:
        json.dump(skill_memory, f, indent=4)

# -------------------------------
# Problem-Solving Loop
# -------------------------------
def solve_problem():
    problem = generate_problem()
    solutions = generate_solution(problem)
    
    # Evaluate all solutions
    scores = [evaluate_solution(problem, s) for s in solutions]
    
    # Pick best solution
    best_index = scores.index(max(scores))
    best_solution = solutions[best_index]
    best_score = scores[best_index]
    
    # Learn
    update_skill(problem, best_score)
    
    print(f"Problem ID: {problem['problem_id']}, Difficulty: {problem['difficulty']}")
    print(f"Solutions: {solutions}, Scores: {scores}")
    print(f"Chosen Solution: {best_solution}, Score: {best_score}")
    print(f"Updated Skill Memory: {skill_memory[problem['problem_id']]:.2f}\n")
    
    return best_solution, best_score

# -------------------------------
# Run Example Multiple Times
# -------------------------------
if __name__ == "__main__":
    for _ in range(5):
        solve_problem()