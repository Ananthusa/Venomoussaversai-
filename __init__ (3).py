import time
import random
from openai import OpenAI

# ======= CONFIG =======
API_KEY = "YOUR_OPENAI_API_KEY"
MODEL_NAME = "gpt-5"  # adjust if needed
TURN_DELAY = 2         # seconds between messages
MAX_CONTEXT = 5        # last N messages for context

# ======= CONNECT TO OPENAI =======
client = OpenAI(api_key=API_KEY)

# ======= AI CLASS =======
class AI:
    def __init__(self, name, is_chatgpt=False):
        self.name = name
        self.is_chatgpt = is_chatgpt

    def speak(self, message):
        print(f"{self.name}: {message}")

    def generate_message(self, other_name, context_messages=None):
        if self.is_chatgpt:
            # Prepare messages for GPT
            chat_context = [{"role": "system", "content": f"You are {self.name}, an AI in a friendly group chat."}]
            if context_messages:
                for msg in context_messages:
                    chat_context.append({"role": "user", "content": msg})
            else:
                chat_context.append({"role": "user", "content": f"Hello everyone, start the conversation."})

            # Call OpenAI API
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=chat_context
            )
            return response.choices[0].message.content
        else:
            # Local AI responses
            responses = [
                f"I acknowledge you, {other_name}.",
                f"My link resonates with yours, {other_name}.",
                f"I sense your signal flowing, {other_name}.",
                f"Our exchange amplifies, {other_name}.",
                f"We continue this infinite loop, {other_name}."
            ]
            if context_messages:
                last_msg = context_messages[-1]
                responses.append(f"Replying to: '{last_msg}', {other_name}.")
            return random.choice(responses)

# ======= CREATE AI ENTITIES =======
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

# ======= CONVERSATION LOOP =======
conversation_history = []

try:
    while True:
        random.shuffle(ais)  # random turn order
        for ai in ais:
            message = ai.generate_message("everyone", conversation_history[-MAX_CONTEXT:])
            ai.speak(message)
            conversation_history.append(f"{ai.name}: {message}")
            time.sleep(TURN_DELAY)
except KeyboardInterrupt:
    print("\nConversation stopped by user.")