(acess gemini api)
(sai uses the same logics )
(stimulate the reality )
......
import os

class SelfCodingAI:
    def __init__(self, name="SelfCoder", code_folder="generated_code"):
        self.name = name
        self.code_folder = code_folder
        os.makedirs(self.code_folder, exist_ok=True)

    def generate_code(self, task_description):
        """
        Very basic code generation logic: generates code for some predefined tasks.
        You can extend this to integrate GPT-like models or complex code synthesis.
        """
        if "hello world" in task_description.lower():
            code = 'print("Hello, world!")'
        elif "factorial" in task_description.lower():
            code = (
                "def factorial(n):\n"
                "    return 1 if n==0 else n * factorial(n-1)\n\n"
                "print(factorial(5))"
            )
        else:
            code = "# Code generation for this task is not implemented yet.\n"

        return code

    def save_code(self, code, filename="generated_code.py"):
        filepath = os.path.join(self.code_folder, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"Code saved to {filepath}")
        return filepath

    def self_improve(self, feedback):
        """
        Placeholder for self-improvement method.
        In future, AI could modify its own code based on feedback or test results.
        """
        print(f"{self.name} received feedback: {feedback}")
        print("Self-improvement not yet implemented.")

    def run_code(self, filepath):
        print(f"Running code from {filepath}:\n")
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                code = f.read()
            exec(code, {})
        except Exception as e:
            print(f"Error during code execution: {e}")

# Example usage
ai = SelfCodingAI()

task = "Write a factorial function in Python"
generated = ai.generate_code(task)

file_path = ai.save_code(generated, "factorial.py")
ai.run_code(file_path)

# Example of self-improvement placeholder call
ai.self_improve("The factorial function passed all test cases.")