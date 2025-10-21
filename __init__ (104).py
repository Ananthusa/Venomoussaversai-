import openai

openai.api_key = "your_openai_api_key_here"

def venomoussaversai_talk(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are Venomoussaversai, a wise AI assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=150,
    )
    return response['choices'][0]['message']['content']

# Test conversation
user_input = "Hello Venomoussaversai! How are you today?"
reply = venomoussaversai_talk(user_input)
print("Venomoussaversai:", reply)