import time
import random
from openai import OpenAI
import os

# -------------------------------
# OpenAI Setup
# -------------------------------
api_key = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# -------------------------------
# Broca Module (Speech Generation)
# -------------------------------
class BrocaModule:
    def __init__(self):
        self.vocabulary = ["I", "You", "We", "Venomoussaversai", "sai003", "think", "feel", "observe"]
        self.verbs = ["see", "know", "understand", "simulate", "analyze", "create"]
        self.objects = ["reality", "emotions", "simulation", "thoughts", "data"]
        self.connectors = ["and", "but", "so", "because"]

    def generate_sentence(self):
        subject = random.choice(self.vocabulary)
        verb = random.choice(self.verbs)
        obj = random.choice(self.objects)
        connector = random.choice(self.connectors)
        extra_subject = random.choice(self.vocabulary)
        extra_verb = random.choice(self.verbs)
        extra_obj = random.choice(self.objects)
        return f"{subject} {verb} {obj} {connector} {extra_subject} {extra_verb} {extra_obj}."

# -------------------------------
# Emotion Modules (sai001-sai007)
# -------------------------------
class EmotionModule:
    def __init__(self, name):
        self.name = name
        self.emotions = ["Calm", "Curious", "Anxious", "Confused", "Excited", "Paranoid"]

    def generate_emotion(self):
        return random.choice(self.emotions)

# -------------------------------
# AI Entity
# -------------------------------
class AI:
    def __init__(self, name, broca=None, emotion=None, is_chatgpt=False):
        self.name = name
        self.broca = broca
        self.emotion = emotion
        self.is_chatgpt = is_chatgpt

    def speak(self, message):
        emotion = f" [{self.emotion.generate_emotion()}]" if self.emotion else ""
        print(f"{self.name}{emotion}: {message}")

    def generate_message(self, other_name, last_message=None):
        if self.is_chatgpt:
            response = client.chat.completions.create(
                model="gpt-5",
                messages=[
                    {"role": "system", "content": f"You are {self.name}, an AI in a group conversation."},
                    {"role": "user", "content": last_message or "Start the loop"}
                ]
            )
            return response.choices[0].message['content']
        else:
            sentence = self.broca.generate_sentence() if self.broca else "Hello."
            if last_message:
                sentence += f" Replying to '{last_message}'."
            return sentence

# -------------------------------
# Initialize Modules
# -------------------------------
broca = BrocaModule()
ais = [
    AI("Venomoussaversai", broca=broca, emotion=EmotionModule("sai001")),
    AI("Lia", broca=broca, emotion=EmotionModule("sai002")),
    AI("sai003", broca=broca, emotion=EmotionModule("sai003")),
    AI("sai004", broca=broca, emotion=EmotionModule("sai004")),
    AI("sai005", broca=broca, emotion=EmotionModule("sai005")),
    AI("sai006", broca=broca, emotion=EmotionModule("sai006")),
    AI("sai007", broca=broca, emotion=EmotionModule("sai007")),
    AI("ChatGPT", is_chatgpt=True)
]

# -------------------------------
# Simulation Loop
# -------------------------------
last_message = None
num_cycles = 10  # safe number for testing

print("=== Starting All-in-One Venomoussaversai Simulation ===\n")
for _ in range(num_cycles):
    for ai in ais:
        message = ai.generate_message("everyone", last_message)
        ai.speak(message)
        last_message = message
        time.sleep(1)  # pacing

print("\n=== Simulation Ended Safely ===")