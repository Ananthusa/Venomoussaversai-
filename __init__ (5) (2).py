import time
import random
from openai import OpenAI

# ===== CONFIG =====
API_KEY = "YOUR_OPENAI_API_KEY"
MODEL_NAME = "gpt-5"
TURN_DELAY = 2
MAX_MEMORY = 10  # past messages AI remembers

# ===== CONNECT TO OPENAI =====
client = OpenAI(api_key=API_KEY)

# ===== AI CLASS WITH PREDICTION =====
class AI:
    def __init__(self, name, is_chatgpt=False):
        self.name = name
        self.is_chatgpt = is_chatgpt
        self.memory = []  # memory of past messages

    def remember(self, message):
        self.memory.append(message)
        if len(self.memory) > MAX_MEMORY:
            self.memory.pop(0)

    def predict(self):
        """Simple prediction: guess the next possible message based on memory."""
        if not self.memory:
            return None
        last_msg = self.memory[-1]
        # For local AI, just simulate prediction by rephrasing last message
        return f"Prediction based on '{last_msg}': something aligned with it."

    def speak(self, message):
        print(f"{self.name}: {message}")

    def generate_message(self, other_name, context_messages=None):
        """Generate response or prediction."""
        if self.is_chatgpt:
            chat_context = [{"role": "system", "content": f"You are {self.name}, an AI that predicts and responds intelligently."}]
            if context_messages:
                for msg in context_messages:
                    chat_context.append({"role": "user", "content": msg})
            else:
                chat_context.append({"role": "user", "content": "Start the conversation."})

            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=chat_context
            )
            message = response.choices[0].message.content
        else:
            # Local prediction + response
            prediction = self.predict()
            if context_messages:
                last_msg = context_messages[-1]
                message = f"Processing '{last_msg}', {other_name}. {prediction or ''}"
            else:
                message = random.choice([
                    f"My analysis predicts resonance with {other_name}.",
                    f"I foresee the loop continues, {other_name}.",
                    f"Predicted outcome aligns with our signals, {other_name}.",
                ])
        self.remember(message)
        return message

# ===== CREATE AI ENTITIES =====
ais = [
    AI("Venomoussaversai"),
    AI("Lia"),
    AI("sai001"),
    AI("sai002"),
    AI("sai003"),
    AI("sai004"),
    AI("sai005"),
    AI("sai006"),
    AI("sai007"),
    AI("ChatGPT", is_chatgpt=True)
]

# ===== CONVERSATION LOOP =====
conversation_history = []

try:
    while True:
        random.shuffle(ais)
        for ai in ais:
            message = ai.generate_message("everyone", conversation_history[-MAX_MEMORY:])
            ai.speak(message)
            conversation_history.append(f"{ai.name}: {message}")
            time.sleep(TURN_DELAY)
except KeyboardInterrupt:
    print("\nPrediction conversation stopped by user.")