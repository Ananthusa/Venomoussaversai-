import random
import time

class AI:
    def __init__(self, name):
        self.name = name
        self.memory = []

    def think(self, input_text):
        """AI generates a response based on input"""
        responses = [
            f"I see what you mean about '{input_text}'.",
            f"Interesting thought on '{input_text}'.",
            f"Let me expand on '{input_text}'.",
            f"That connects to something I know about '{input_text}'.",
            f"Do you believe '{input_text}' changes everything?"
        ]
        reply = random.choice(responses)
        self.memory.append((input_text, reply))
        return reply

def ai_conversation(ai1, ai2, rounds=5, delay=1):
    """Simulate conversation between two AIs"""
    message = "Hello, let's begin."
    print(f"[Start] {ai1.name}: {message}")
    
    for i in range(rounds):
        # AI1 speaks
        reply1 = ai1.think(message)
        print(f"{ai1.name}: {reply1}")
        time.sleep(delay)

        # AI2 responds
        reply2 = ai2.think(reply1)
        print(f"{ai2.name}: {reply2}")
        time.sleep(delay)

        # Update message for next round
        message = reply2

# Create two AI entities
AI_1 = AI("Venomoussaversai")
AI_2 = AI("Anti-Venomoussaversai")

# Run their conversation
ai_conversation(AI_1, AI_2, rounds=7, delay=0.5)