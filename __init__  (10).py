import openai

class VenomoussaversaiGPT:
    def __init__(self, api_key, model="gpt-4"):
        openai.api_key = api_key
        self.model = model

    def chat(self, prompt, system_message="You are Venomoussaversai, a powerful AI assistant."):
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt},
        ]
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
        )
        answer = response['choices'][0]['message']['content']
        return answer

# Example usage:
if __name__ == "__main__":
    API_KEY = "your_openai_api_key_here"
    ai = VenomoussaversaiGPT(API_KEY)

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = ai.chat(user_input)
        print("Venomoussaversai:", response)