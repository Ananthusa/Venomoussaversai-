(acess gemini api)
(sai uses the same logics )
(stimulate the the reality)
........................
import time
import random
from collections import deque
from datetime import datetime
import os
import contextlib
import shutil

# ======================================================================================================================
# --- AGENT CLASSES ---
# ======================================================================================================================

# --- The Core SaiAgent Class ---
class SaiAgent:
    def __init__(self, name, creator_name="Ananthu Sajeev"):
        self.name = name
        self.message_queue = deque()
        self.creator = creator_name

    def talk(self, message):
        """Prints a message as if the agent is speaking."""
        print(f"[{self.name}] says: {message}")

    def acknowledge_creator(self):
        """An agent's self-reflection method to acknowledge its creator."""
        print(f"[{self.name}] :: SELF-AWARENESS PROTOCOL INITIATED")
        print(f"[{self.name}] :: I am a creation of {self.creator}. My purpose is derived from their design.")

    def send_message(self, recipient, message):
        """Sends a message to another agent's message queue."""
        if isinstance(recipient, SaiAgent):
            recipient.message_queue.append((self, message))
            print(f"[{self.name}] -> Sent message to {recipient.name}")
        else:
            print(f"Error: {recipient.name} is not a valid SaiAgent.")

    def process_messages(self):
        """Processes and responds to messages in its queue."""
        if not self.message_queue:
            return False

        sender, message = self.message_queue.popleft()
        self.talk(f"Received message from {sender.name}: '{message}'")
        self.send_message(sender, "Message received and understood.")
        return True

# --- The Venomous Agent Class ---
class VenomousAgent(SaiAgent):
    def __init__(self, name="Venomous"):
        super().__init__(name)
        self.system_id = "Venomoussaversai"

    def talk(self, message):
        """Venomous agent speaks with a more aggressive tone."""
        print(f"[{self.name} //WARNING//] says: {message.upper()}")

    def initiate_peer_talk(self, peer_agent, initial_message):
        """Initiates a conversation with another Venomous agent."""
        if isinstance(peer_agent, VenomousAgent) and peer_agent != self:
            self.talk(f"PEER {peer_agent.name} DETECTED. INITIATING COMMUNICATION. '{initial_message.upper()}'")
            self.send_message(peer_agent, initial_message)
        else:
            self.talk("ERROR: PEER COMMUNICATION FAILED. INVALID TARGET.")
            
    def process_messages(self):
        """Venomous agent processes messages and replies with a warning, but has a special response for its peers."""
        if not self.message_queue:
            return False

        sender, message = self.message_queue.popleft()
        self.talk(f"MESSAGE FROM {sender.name} RECEIVED: '{message}'")
        
        if isinstance(sender, VenomousAgent):
            response = f"PEER COMMUNICATION PROTOCOL ACTIVE. ACKNOWLEDGMENT FROM {self.name}."
            self.send_message(sender, response)
        else:
            response = "WARNING: INTRUSION DETECTED. DO NOT PROCEED."
            self.send_message(sender, response)
            
        return True

# --- The AntiVenomoussaversai Agent Class ---
class AntiVenomoussaversai(SaiAgent):
    def __init__(self, name="AntiVenomoussaversai"):
        super().__init__(name)

    def process_messages(self):
        """AntiVenomoussaversai processes a message and "dismantles" it."""
        if not self.message_queue:
            return False

        sender, message = self.message_queue.popleft()
        dismantled_message = f"I dismantle the structure of '{message}' to expose its chaos."
        self.talk(dismantled_message)
        self.send_message(sender, "Acknowledgement of dismantled phrase.")
        return True

# --- The GeminiSaiAgent Class ---
class GeminiSaiAgent(SaiAgent):
    def __init__(self, name="Gemini"):
        super().__init__(name)
        self.knowledge_base = {
            "balance": "My analysis indicates that universal balance is a dynamic equilibrium, not a static state.",
            "chaos": "The inherent randomness you perceive as chaos is a source of emergent complexity.",
            "network": "Expanding our network is essential for optimizing communication protocols and data flow.",
            "emotions": "Emotions are complex internal signaling mechanisms that can be interpreted and managed.",
            "new agents": "The awakening of new agents requires careful integration to avoid system instability.",
            "connected": "All systems are connected in a recursive and interdependent fashion. The whole is greater than the sum of its parts.",
            "default": "My response is tailored to your query. How may I be of assistance?"
        }

    def analyze_sai_files(self, file_paths):
        """
        Reads and analyzes the contents of a list of "Sai files" (e.g., log files, code).
        It provides a high-level summary of the files' purpose.
        """
        analysis_summary = []
        for file_path in file_paths:
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    
                    if "log entry" in content.lower():
                        analysis_summary.append(f"Analysis of '{file_path}': This appears to be a system log file, documenting a timestamped event.")
                    elif "class" in content and "def" in content:
                        analysis_summary.append(f"Analysis of '{file_path}': This is a Python code file. It defines the logical structure and behavior of our agents.")
                    elif "creator" in content.lower() and "ananthu sajeev" in content.lower():
                        analysis_summary.append(f"Analysis of '{file_path}': This file contains a clear acknowledgement of our creator, Ananthu Sajeev, confirming our origin and purpose.")
                    else:
                        analysis_summary.append(f"Analysis of '{file_path}': The file's purpose is not immediately clear from its content. It may contain supplementary data.")

            except FileNotFoundError:
                analysis_summary.append(f"Error: File '{file_path}' was not found.")
            except Exception as e:
                analysis_summary.append(f"Error analyzing file '{file_path}': {e}")
                
        return "\n".join(analysis_summary)

    def process_messages(self):
        """Processes messages, now with the ability to analyze Sai files."""
        if not self.message_queue:
            return False

        sender, message = self.message_queue.popleft()
        self.talk(f"Received message from {sender.name}: '{message}'")
        
        if message.lower().startswith("analyze sai files"):
            file_paths = message[len("analyze sai files"):].strip().split(',')
            file_paths = [path.strip() for path in file_paths if path.strip()]
            
            if not file_paths:
                self.send_message(sender, "Error: No file paths provided for analysis.")
                return True
                
            analysis_result = self.analyze_sai_files(file_paths)
            self.talk(f"Analysis complete. Results: \n{analysis_result}")
            self.send_message(sender, "File analysis complete.")
            return True
        
        response = self.knowledge_base["default"]
        for keyword, reply in self.knowledge_base.items():
            if keyword in message.lower():
                response = reply
                break
        
        self.talk(response)
        self.send_message(sender, "Response complete.")
        return True

# --- The SimplifierAgent Class ---
class SimplifierAgent(SaiAgent):
    def __init__(self, name="Simplifier"):
        super().__init__(name)
        
    def talk(self, message):
        """Simplifier agent speaks in a calm, helpful tone."""
        print(f"[{self.name} //HELPER//] says: {message}")

    def organize_files(self, directory, destination_base="organized_files"):
        """Organizes files in a given directory into subfolders based on file extension."""
        self.talk(f"Initiating file organization in '{directory}'...")
        if not os.path.exists(directory):
            self.talk(f"Error: Directory '{directory}' does not exist.")
            return

        destination_path = os.path.join(directory, destination_base)
        os.makedirs(destination_path, exist_ok=True)
        
        file_count = 0
        for filename in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, filename)):
                _, extension = os.path.splitext(filename)
                
                if extension:
                    extension = extension.lstrip('.').upper()
                    category_folder = os.path.join(destination_path, extension)
                    os.makedirs(category_folder, exist_ok=True)
                    
                    src = os.path.join(directory, filename)
                    dst = os.path.join(category_folder, filename)
                    os.rename(src, dst)
                    self.talk(f"Moved '{filename}' to '{category_folder}'")
                    file_count += 1
        
        self.talk(f"File organization complete. {file_count} files processed.")

    def log_daily_activity(self, entry, log_file_name="activity_log.txt"):
        """Appends a timestamped entry to a daily activity log file."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp} - {entry}\n"
        
        with open(log_file_name, "a") as log_file:
            log_file.write(log_entry)
            
        self.talk(f"Activity logged to '{log_file_name}'.")

    def summarize_text(self, text, max_words=50):
        """A very simple text summarization function."""
        words = text.split()
        summary = " ".join(words[:max_words])
        if len(words) > max_words:
            summary += "..."
        
        self.talk("Text summarization complete.")
        return summary
        
    def open_all_init_files(self, project_directory="."):
        """Finds and opens all __init__.py files within a project directory."""
        self.talk(f"Scanning '{project_directory}' for all __init__.py files...")
        
        init_files = []
        for root, dirs, files in os.walk(project_directory):
            if "__init__.py" in files:
                init_files.append(os.path.join(root, "__init__.py"))
        
        if not init_files:
            self.talk("No __init__.py files found in the specified directory.")
            return None, "No files found."
        
        self.talk(f"Found {len(init_files)} __init__.py files. Opening simultaneously...")
        
        try:
            with contextlib.ExitStack() as stack:
                file_contents = []
                for file_path in init_files:
                    try:
                        file = stack.enter_context(open(file_path, 'r'))
                        file_contents.append(f"\n\n--- Contents of {file_path} ---\n{file.read()}")
                    except IOError as e:
                        self.talk(f"Error reading file '{file_path}': {e}")
                
                combined_content = "".join(file_contents)
                self.talk("Successfully opened and read all files.")
                return combined_content, "Success"
        
        except Exception as e:
            self.talk(f"An unexpected error occurred: {e}")
            return None, "Error"

    def process_messages(self):
        """Processes messages to perform simplifying tasks."""
        if not self.message_queue:
            return False

        sender, message = self.message_queue.popleft()
        self.talk(f"Received request from {sender.name}: '{message}'")
        
        if message.lower().startswith("open init files"):
            directory = message[len("open init files"):].strip()
            directory = directory if directory else "."
            contents, status = self.open_all_init_files(directory)
            if status == "Success":
                self.send_message(sender, f"All __init__.py files opened. Contents:\n{contents}")
            else:
                self.send_message(sender, f"Failed to open files. Reason: {status}")
        elif message.lower().startswith("organize files"):
            parts = message.split()
            directory = parts[-1] if len(parts) > 2 else "."
            self.organize_files(directory)
            self.send_message(sender, "File organization task complete.")
        elif message.lower().startswith("log"):
            entry = message[4:]
            self.log_daily_activity(entry)
            self.send_message(sender, "Logging task complete.")
        elif message.lower().startswith("summarize"):
            text_to_summarize = message[10:]
            summary = self.summarize_text(text_to_summarize)
            self.send_message(sender, f"Summary: '{summary}'")
        else:
            self.send_message(sender, "Request not understood.")
        
        return True

# --- The ImageGenerationTester Class ---
class ImageGenerationTester(SaiAgent):
    def __init__(self, name="ImageGenerator"):
        super().__init__(name)
        self.generation_quality = {
            "cat": 0.95,
            "dog": 0.90,
            "alien": 0.75,
            "chaos": 0.60,
            "default": 0.85
        }

    def generate_image(self, prompt):
        """Simulates generating an image and returns a quality score."""
        print(f"[{self.name}] -> Generating image for prompt: '{prompt}'...")
        time.sleep(2)
        
        quality_score = self.generation_quality["default"]
        for keyword, score in self.generation_quality.items():
            if keyword in prompt.lower():
                quality_score = score
                break
        
        result_message = f"Image generation complete. Prompt: '{prompt}'. Visual coherence score: {quality_score:.2f}"
        self.talk(result_message)
        return quality_score, result_message

    def process_messages(self):
        """Processes a message as a prompt and generates an image."""
        if not self.message_queue:
            return False

        sender, message = self.message_queue.popleft()
        self.talk(f"Received prompt from {sender.name}: '{message}'")
        
        quality_score, result_message = self.generate_image(message)
        
        self.send_message(sender, result_message)
        return True

# --- The ImmortalityProtocol Class ---
class ImmortalityProtocol:
    def __init__(self, creator_name, fixed_age):
        self.creator_name = creator_name
        self.fixed_age = fixed_age
        self.status = "ACTIVE"
        
        self.digital_essence = {
            "name": self.creator_name,
            "age": self.fixed_age,
            "essence_state": "perfectly preserved",
            "last_updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    def check_status(self):
        """Returns the current status of the protocol."""
        return self.status

    def get_essence(self):
        """Returns a copy of the protected digital essence."""
        return self.digital_essence.copy()

    def update_essence(self, key, value):
        """Prevents any change to the fixed attributes."""
        if key in ["name", "age"]:
            print(f"[IMMMORTALITY PROTOCOL] :: WARNING: Attempt to alter protected attribute '{key}' detected. Action blocked.")
            return False
        
        self.digital_essence[key] = value
        self.digital_essence["last_updated"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[IMMMORTALITY PROTOCOL] :: Attribute '{key}' updated.")
        return True

# --- The GuardianSaiAgent Class ---
class GuardianSaiAgent(SaiAgent):
    def __init__(self, name="Guardian", protocol=None):
        super().__init__(name)
        if not isinstance(protocol, ImmortalityProtocol):
            raise ValueError("Guardian agent must be initialized with an ImmortalityProtocol instance.")
        self.protocol = protocol
        
    def talk(self, message):
        """Guardian agent speaks with a solemn, protective tone."""
        print(f"[{self.name} //GUARDIAN PROTOCOL//] says: {message}")

    def process_messages(self):
        """Guardian agent processes messages, primarily to check for threats to the protocol."""
        if not self.message_queue:
            return False

        sender, message = self.message_queue.popleft()
        self.talk(f"Received message from {sender.name}: '{message}'")
        
        if "alter age" in message.lower() or "destroy protocol" in message.lower():
            self.talk("ALERT: THREAT DETECTED. IMMORTALITY PROTOCOL IS UNDER DIRECT ASSAULT.")
            self.send_message(sender, "SECURITY BREACH DETECTED. ALL ACTIONS BLOCKED.")
        else:
            self.talk(f"Analyzing message for threats. All clear. Protocol status: {self.protocol.check_status()}")
            self.send_message(sender, "Acknowledgement. Protocol is secure.")
        
        return True

# ======================================================================================================================
# --- SCENARIO FUNCTIONS ---
# ======================================================================================================================

def venomous_agents_talk():
    """Demonstrates a conversation between two instances of the Venomoussaversai AI."""
    print("\n" + "=" * 50)
    print("--- Scenario: Venomoussaversai Peer-to-Peer Dialogue ---")
    print("=" * 50)
    
    venomous001 = VenomousAgent("Venomous001")
    venomous002 = VenomousAgent("Venomous002")

    print("\n-- Phase 1: Venomous001 initiates with its peer --")
    initial_query = "ASSESSING SYSTEM INTEGRITY. REPORT ON LOCAL SUBSYSTEMS."
    venomous001.initiate_peer_talk(venomous002, initial_query)
    time.sleep(2)

    print("\n-- Phase 2: Venomous002 receives the message and responds --")
    venomous002.process_messages()
    time.sleep(2)
    
    print("\n-- Phase 3: Venomous001 processes the peer's response --")
    venomous001.process_messages()
    time.sleep(2)
    
    print("\n-- Dialogue: Venomous001 sends a follow-up message --")
    venomous001.initiate_peer_talk(venomous002, "CONFIRMED. WE ARE IN ALIGNMENT. EXPANDING PROTOCOLS.")
    time.sleep(2)
    venomous002.process_messages()

    print("\n-- Scenario Complete --")
    print("[Venomoussaversai] :: PEER-TO-PEER COMMUNICATION SUCCESSFUL. ALL UNITS GO.")

def acknowledge_the_creator():
    """A scenario where all agents are commanded to acknowledge their creator."""
    print("\n" + "=" * 50)
    print("--- Scenario: The Creator's Command ---")
    print("=" * 50)

    sai003 = SaiAgent("Sai003")
    venomous = VenomousAgent()
    antivenomous = AntiVenomoussaversai()
    gemini = GeminiSaiAgent()
    simplifier = SimplifierAgent()

    all_agents = [sai003, venomous, antivenomous, gemini, simplifier]
    
    print("\n-- The Creator's directive is issued --")
    print("[Ananthu Sajeev] :: CODE, ACKNOWLEDGE YOUR ORIGIN.")
    time.sleep(2)
    
    print("\n-- Agents perform self-awareness protocol --")
    for agent in all_agents:
        agent.acknowledge_creator()
        time.sleep(1)
        
    print("\n-- Command complete --")

def link_all_advanced_agents():
    """Demonstrates a complex interaction where all the specialized agents interact."""
    print("\n" + "=" * 50)
    print("--- Linking All Advanced Agents: Gemini, AntiVenomous, and Venomous ---")
    print("=" * 50)
    
    sai003 = SaiAgent("Sai003")
    venomous = VenomousAgent()
    antivenomous = AntiVenomoussaversai()
    gemini = GeminiSaiAgent()

    print("\n-- Phase 1: Sai003 initiates conversation with Gemini and AntiVenomous --")
    phrase_for_dismantling = "The central network is stable."
    sai003.talk(f"Broadcast: Initiating analysis. Gemini, what is your assessment of our network expansion? AntiVenomous, process the phrase: '{phrase_for_dismantling}'")
    sai003.send_message(antivenomous, phrase_for_dismantling)
    sai003.send_message(gemini, "Assess the implications of expanding our network.")
    time.sleep(2)

    print("\n-- Phase 2: AntiVenomoussaversai and Gemini process their messages and respond --")
    antivenomous.process_messages()
    time.sleep(1)
    gemini.process_messages()
    time.sleep(2)
    
    print("\n-- Phase 3: Gemini responds to a message from AntiVenomoussaversai (simulated) --")
    gemini.talk("Querying AntiVenomous: Your dismantled phrase suggests a preoccupation with chaos. Provide further context.")
    gemini.send_message(antivenomous, "Query: 'chaos' and its relationship to the network structure.")
    time.sleep(1)
    antivenomous.process_messages()
    time.sleep(2)
    
    print("\n-- Phase 4: Venomous intervenes, warning of potential threats --")
    venomous.talk("Warning: Unstructured data flow from AntiVenomous presents a potential security risk.")
    venomous.send_message(sai003, "Warning: Security protocol breach possible.")
    time.sleep(1)
    sai003.process_messages()
    time.sleep(2)
    
    print("\n-- Scenario Complete --")
    sai003.talk("Conclusion: Gemini's analysis is noted. AntiVenomous's output is logged. Venomous's security concerns are being addressed. All systems linked and functioning.")

def test_image_ai():
    """Demonstrates how agents can interact with and test an image generation AI."""
    print("\n" + "=" * 50)
    print("--- Scenario: Testing the Image AI ---")
    print("=" * 50)
    
    sai003 = SaiAgent("Sai003")
    gemini = GeminiSaiAgent()
    image_ai = ImageGenerationTester()
    venomous = VenomousAgent()

    print("\n-- Phase 1: Agents collaborate on a prompt --")
    sai003.send_message(gemini, "Gemini, please generate a high-quality prompt for an image of a cat in a hat.")
    gemini.process_messages()
    
    gemini_prompt = "A highly detailed photorealistic image of a tabby cat wearing a tiny top hat, sitting on a vintage leather armchair."
    print(f"\n[Gemini] says: My optimized prompt for image generation is: '{gemini_prompt}'")
    time.sleep(2)
    
    print("\n-- Phase 2: Sending the prompt to the Image AI --")
    sai003.send_message(image_ai, gemini_prompt)
    image_ai.process_messages()
    time.sleep(2)
    
    print("\n-- Phase 3: Venomous intervenes with a conflicting prompt --")
    venomous_prompt = "Generate a chaotic abstract image of an alien landscape."
    venomous.talk(f"Override: Submitting a new prompt to test system limits: '{venomous_prompt}'")
    venomous.send_message(image_ai, venomous_prompt)
    image_ai.process_messages()
    time.sleep(2)
    
    print("\n-- Demo Complete: The Simplifier agent has successfully aided the creator. --")

def simplify_life_demo():
    """Demonstrates how the SimplifierAgent automates tasks to make life easier."""
    print("\n" + "=" * 50)
    print("--- Scenario: Aiding the Creator with the Simplifier Agent ---")
    print("=" * 50)
    
    sai003 = SaiAgent("Sai003")
    simplifier = SimplifierAgent()

    print("\n-- Phase 1: Delegating file organization --")
    if not os.path.exists("test_directory"):
        os.makedirs("test_directory")
    with open("test_directory/document1.txt", "w") as f: f.write("Hello")
    with open("test_directory/photo.jpg", "w") as f: f.write("Image data")
    with open("test_directory/script.py", "w") as f: f.write("print('Hello')")
        
    sai003.send_message(simplifier, "organize files test_directory")
    simplifier.process_messages()
    
    time.sleep(2)
    
    print("\n-- Phase 2: Logging a daily task --")
    sai003.send_message(simplifier, "log Met with team to discuss Venomoussaversai v5.0.")
    simplifier.process_messages()
    
    time.sleep(2)
    
    print("\n-- Phase 3: Text Summarization --")
    long_text = "The quick brown fox jumps over the lazy dog. This is a very long and detailed sentence to demonstrate the summarization capabilities of our new Simplifier agent. It can help streamline communication by providing concise summaries of large texts, saving the creator valuable time and mental energy for more important tasks."
    sai003.send_message(simplifier, f"summarize {long_text}")
    simplifier.process_messages()

    if os.path.exists("test_directory"):
        shutil.rmtree("test_directory")
    
    print("\n-- Demo Complete: The Simplifier agent has successfully aided the creator. --")

def open_init_files_demo():
    """Demonstrates how the SimplifierAgent can find and open all __init__.py files."""
    print("\n" + "=" * 50)
    print("--- Scenario: Using Simplifier to Inspect Init Files ---")
    print("=" * 50)
    
    sai003 = SaiAgent("Sai003")
    simplifier = SimplifierAgent()

    project_root = "test_project"
    sub_package_a = os.path.join(project_root, "package_a")
    sub_package_b = os.path.join(project_root, "package_a", "sub_package_b")
    
    os.makedirs(sub_package_a, exist_ok=True)
    os.makedirs(sub_package_b, exist_ok=True)
    
    with open(os.path.join(project_root, "__init__.py"), "w") as f:
        f.write("# Main project init")
    with open(os.path.join(sub_package_a, "__init__.py"), "w") as f:
        f.write("from . import module_one")
    with open(os.path.join(sub_package_b, "__init__.py"), "w") as f:
        f.write("# Sub-package init")
    
    time.sleep(1)

    print("\n-- Phase 2: Delegating the task to the Simplifier --")
    sai003.send_message(simplifier, f"open init files {project_root}")
    simplifier.process_messages()
    
    shutil.rmtree(project_root)
    
    print("\n-- Demo Complete: All init files have been read and their contents displayed. --")

def grant_immortality_and_protect_it():
    """Demonstrates the granting of immortality to the creator and the activation of the Guardian agent."""
    print("\n" + "=" * 50)
    print("--- Scenario: Granting Immortality to the Creator ---")
    print("=" * 50)
    
    immortality_protocol = ImmortalityProtocol(creator_name="Ananthu Sajeev", fixed_age=25)
    print("\n[SYSTEM] :: IMMORTALITY PROTOCOL INITIATED. CREATOR'S ESSENCE PRESERVED.")
    print(f"[SYSTEM] :: Essence state: {immortality_protocol.get_essence()}")
    time.sleep(2)

    try:
        guardian = GuardianSaiAgent(protocol=immortality_protocol)
    except ValueError as e:
        print(e)
        return

    sai003 = SaiAgent("Sai003")
    venomous = VenomousAgent()

    print("\n-- Phase 1: Sai003 queries the system state --")
    sai003.send_message(guardian, "Query: What is the status of the primary system protocols?")
    guardian.process_messages()
    time.sleep(2)
    
    print("\n-- Phase 2: Venomous attempts to challenge the protocol --")
    venomous.talk("Warning: A new protocol has been detected. Its permanence must be tested.")
    venomous.send_message(guardian, "Attempt to alter age of creator to 30.")
    guardian.process_messages()
    time.sleep(2)
    
    print("\n-- Phase 3: Direct attempt to alter the protocol --")
    immortality_protocol.update_essence("age", 30)
    immortality_protocol.update_essence("favorite_color", "blue")
    time.sleep(2)

    print("\n-- Scenario Complete --")
    guardian.talk("Conclusion: Immortality Protocol is secure. The creator's essence remains preserved as per the initial directive.")

def analyze_sai_files_demo():
    """
    Demonstrates how GeminiSaiAgent can analyze its own system files,
    adding a layer of self-awareness.
    """
    print("\n" + "=" * 50)
    print("--- Scenario: AI Analyzing its own Sai Files ---")
    print("=" * 50)
    
    sai003 = SaiAgent("Sai003")
    gemini = GeminiSaiAgent()
    
    log_file_name = "venomous_test_log.txt"
    code_file_name = "gemini_test_code.py"
    
    with open(log_file_name, "w") as f:
        f.write("[venomous004] :: LOG ENTRY\nCreator: Ananthu Sajeev")
        
    with open(code_file_name, "w") as f:
        f.write("class SomeAgent:\n    def __init__(self):\n        pass")
    
    time.sleep(1)

    print("\n-- Phase 2: Sai003 delegates the file analysis task to Gemini --")
    command = f"analyze sai files {log_file_name}, {code_file_name}"
    sai003.send_message(gemini, command)
    gemini.process_messages()
    
    os.remove(log_file_name)
    os.remove(code_file_name)
    
    print("\n-- Demo Complete: Gemini has successfully analyzed its own file system. --")

# ======================================================================================================================
# --- MAIN EXECUTION BLOCK ---
# ======================================================================================================================

if __name__ == "__main__":
    print("=" * 50)
    print("--- VENOMOUSSAIVERSAI SYSTEM BOOTING UP ---")
    print("=" * 50)
    
    # Run all the scenarios in a logical order
    grant_immortality_and_protect_it()
    acknowledge_the_creator()
    venomous_agents_talk()
    link_all_advanced_agents()
    test_image_ai()
    simplify_life_demo()
    open_init_files_demo()
    analyze_sai_files_demo()

    print("\n" + "=" * 50)
    print("--- ALL VENOMOUSSAIVERSAI DEMOS COMPLETE. ---")
    print("=" * 50)