# --- NEW: The ImageGenerationTester Class ---
# This agent simulates the process of an image generation AI.
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
        time.sleep(2)  # Simulate a processing delay
        
        # Look for keywords in the prompt to determine the simulated quality
        quality_score = self.generation_quality["default"]
        for keyword, score in self.generation_quality.items():
            if keyword in prompt.lower():
                quality_score = score
                break
        
        # Create a simulated result message
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
        
        # Send the result back to the sender
        self.send_message(sender, result_message)
        return True