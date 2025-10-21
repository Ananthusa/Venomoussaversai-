import time
import random
from collections import deque

# --- Internal Monologue (Interactive Story) ---
def internal_monologue():
    print("Sai sat alone in the dimly lit room, the ticking of the old clock on the wall echoing his restless thoughts.")
    print("His internal monologue was a relentless torrent of self-venom, each word a dagger piercing his already fragile self-esteem.")
    print("\nYou are Sai. What do you do?")
    print("1. Continue with self-venom")
    print("2. Try to seek help")
    print("3. Reflect on past moments of hope")

    choice = input("Enter the number of your choice: ")

    if choice == '1':
        self_venom()
    elif choice == '2':
        seek_help()
    elif choice == '3':
        reflect_on_past()
    else:
        print("Invalid choice. Please try again.")
        internal_monologue()

def self_venom():
    print("\nYou clench your fists, feeling the nails dig into your palms. The physical pain is a distraction from the emotional turmoil raging inside you.")
    print("'You're worthless,' you whisper to yourself. 'Everyone would be better off without you.'")
    print("\nWhat do you do next?")
    print("1. Continue with self-venom")
    print("2. Try to seek help")
    print("3. Reflect on past moments of hope")

    choice = input("Enter the number of your choice: ")

    if choice == '1':
        self_venom()
    elif choice == '2':
        seek_help()
    elif choice == '3':
        reflect_on_past()
    else:
        print("Invalid choice. Please try again.")
        self_venom()

def seek_help():
    print("\nYou take a deep breath and decide to reach out for help. You pick up your phone and dial a trusted friend.")
    print("'I need to talk,' you say, your voice trembling. 'I can't do this alone anymore.'")
    print("\nYour friend listens and encourages you to seek professional help.")
    print("You feel a glimmer of hope — the first step toward healing.")
    print("\nWould you like to continue the story or start over?")
    print("1. Continue")
    print("2. Start over")

    choice = input("Enter the number of your choice: ")

    if choice == '1':
        print("Your choices have led Sai towards a path of healing and self-discovery.")
    elif choice == '2':
        internal_monologue()
    else:
        print("Invalid choice. Please try again.")
        seek_help()

def reflect_on_past():
    print("\nYou remember the times when you had felt a glimmer of hope, a flicker of self-worth.")
    print("Those moments were fleeting, but they were real.")
    print("\nWhat do you do next?")
    print("1. Continue with self-venom")
    print("2. Try to seek help")
    print("3. Reflect again")

    choice = input("Enter the number of your choice: ")

    if choice == '1':
        self_venom()
    elif choice == '2':
        seek_help()
    elif choice == '3':
        reflect_on_past()
    else:
        print("Invalid choice. Please try again.")
        reflect_on_past()

# --- The Core SaiAgent Class ---
class SaiAgent:
    def __init__(self, name):
        self.name = name
        self.message_queue = deque()

    def talk(self, message):
        print(f"[{self.name}] says: {message}")

    def send_message(self, recipient, message):
        if isinstance(recipient, SaiAgent):
            recipient.message_queue.append((self, message))
            print(f"[{self.name}] -> Sent message to {recipient.name}")
        else:
            print(f"Error: {recipient} is not a valid SaiAgent.")

    def process_messages(self):
        if not self.message_queue:
            return False
        sender, message = self.message_queue.popleft()
        self.talk(f"Received from {sender.name}: '{message}'")
        self.send_message(sender, "Message received and understood.")
        return True

# --- Specialized Agents ---
class VenomousAgent(SaiAgent):
    def talk(self, message):
        print(f"[{self.name} //WARNING//] says: {message.upper()}")

    def process_messages(self):
        if not self.message_queue:
            return False
        sender, message = self.message_queue.popleft()
        self.talk(f"MESSAGE FROM {sender.name}: '{message}'")
        self.send_message(sender, "WARNING: INTRUSION DETECTED.")
        return True

class AntiVenomoussaversai(SaiAgent):
    def process_messages(self):
        if not self.message_queue:
            return False
        sender, message = self.message_queue.popleft()
        dismantled = f"I dismantle '{message}' to expose its chaos."
        self.talk(dismantled)
        self.send_message(sender, "Acknowledged dismantled phrase.")
        return True

class GeminiSaiAgent(SaiAgent):
    def __init__(self, name="Gemini"):
        super().__init__(name)
        self.knowledge_base = {
            "balance": "Balance is a dynamic equilibrium, not a static state.",
            "chaos": "Chaos is randomness that generates emergent complexity.",
            "network": "Networks thrive on recursive interdependence.",
            "emotions": "Emotions are internal signaling mechanisms.",
            "connected": "All systems are interwoven — the whole exceeds its parts.",
            "default": "How may I be of assistance?"
        }

    def process_messages(self):
        if not self.message_queue:
            return False
        sender, message = self.message_queue.popleft()
        self.talk(f"Received from {sender.name}: '{message}'")
        response = self.knowledge_base["default"]
        for keyword, reply in self.knowledge_base.items():
            if keyword in message.lower():
                response = reply
                break
        self.talk(response)
        self.send_message(sender, "Response complete.")
        return True

# --- Scenario Linking Agents ---
def link_all_advanced_agents():
    print("=" * 50)
    print("--- Linking Advanced Agents ---")
    print("=" * 50)

    sai003 = SaiAgent("Sai003")
    venomous = VenomousAgent("Venomous")
    antivenomous = AntiVenomoussaversai("AntiVenomous")
    gemini = GeminiSaiAgent()

    sai003.send_message(antivenomous, "The central network is stable.")
    sai003.send_message(gemini, "Assess network expansion.")

    antivenomous.process_messages()
    gemini.process_messages()

    venomous.send_message(sai003, "Security protocol breach possible.")
    sai003.process_messages()

    print("\n--- Scenario Complete ---")
    sai003.talk("Conclusion: All systems linked and functioning.")

if __name__ == "__main__":
    # Run the text adventure OR agent demo
    # internal_monologue()
    link_all_advanced_agents()