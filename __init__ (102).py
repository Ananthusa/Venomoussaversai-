import os
import contextlib
from collections import deque

# Define a base class for all agents
class SaiAgent:
    """A base class for all agents to enable communication."""
    def __init__(self, name="Sai"):
        self.name = name
        self.message_queue = deque()

    def send_message(self, recipient, message):
        """Sends a message to another agent."""
        recipient.message_queue.append((self, message))

# The new and improved SimplifierAgent
class SimplifierAgent(SaiAgent):
    """
    SimplifierAgent specializes in code simplification and project analysis.
    It can now scan a project for all __init__.py files.
    """
    def __init__(self, name="Simplifier"):
        super().__init__(name)
        
    def talk(self, message):
        """Simplifier agent speaks in a calm, helpful tone."""
        print(f"[{self.name} //HELPER//] says: {message}")

    def open_all_init_files(self, project_directory="."):
        """
        Finds and opens all __init__.py files within a project directory.
        It reads their contents and returns them as a single string.
        """
        self.talk(f"Scanning '{project_directory}' for all __init__.py files...")
        
        init_files = []
        for root, dirs, files in os.walk(project_directory):
            if "__init__.py" in files:
                init_files.append(os.path.join(root, "__init__.py"))
        
        if not init_files:
            self.talk("No __init__.py files found in the specified directory.")
            return None, "No files found."
        
        self.talk(f"Found {len(init_files)} __init__.py files. Opening simultaneously...")
        
        # Use ExitStack to safely open all files at once
        try:
            with contextlib.ExitStack() as stack:
                # Open each file and add its contents to a list
                file_contents = []
                for file_path in init_files:
                    try:
                        file = stack.enter_context(open(file_path, 'r'))
                        file_contents.append(f"\n\n--- Contents of {file_path} ---\n{file.read()}")
                    except IOError as e:
                        self.talk(f"Error reading file '{file_path}': {e}")
                
                # Combine all contents into a single string
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
        
        # Simple command parsing to trigger a function
        if message.lower().startswith("open init files"):
            # The directory is the part of the message after the command
            directory = message[len("open init files"):].strip()
            directory = directory if directory else "."
            
            contents, status = self.open_all_init_files(directory)
            if status == "Success":
                self.send_message(sender, f"All __init__.py files opened. Contents:\n{contents}")
            else:
                self.send_message(sender, f"Failed to open files. Reason: {status}")
        
        else:
            self.send_message(sender, "Request not understood. Please use 'open init files'.")
        
        return True

# --- Main execution block for demonstration ---
if __name__ == "__main__":
    # Create a simple project structure for testing
    os.makedirs("test_project/module1", exist_ok=True)
    os.makedirs("test_project/module2/sub_module", exist_ok=True)
    
    with open("test_project/__init__.py", "w") as f:
        f.write("# Top-level __init__.py")
    with open("test_project/module1/__init__.py", "w") as f:
        f.write("from . import file1")
    with open("test_project/module2/sub_module/__init__.py", "w") as f:
        f.write("from . import another_file")
    
    # Create an instance of the SimplifierAgent and another agent to send messages
    simplifier_agent = SimplifierAgent()
    user_agent = SaiAgent("User")

    # Simulate a conversation
    print("--- Simulating Agent Interaction ---")
    user_agent.send_message(simplifier_agent, "open init files test_project")
    
    # Process messages until the queue is empty
    while simplifier_agent.process_messages():
        # The user agent can process its reply here
        if user_agent.message_queue:
            sender, message = user_agent.message_queue.popleft()
            print(f"[{user_agent.name}]: Received reply from {sender.name}: '{message}'")

    print("\n--- Clean up test files ---")
    import shutil
    shutil.rmtree("test_project")