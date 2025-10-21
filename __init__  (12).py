# Install ngrok
!pip install pyngrok flask openai -q

# Import libraries
from flask import Flask, request, jsonify
from pyngrok import ngrok
import openai

# ====== CONFIG ======
OPENAI_API_KEY = "sk-1234567890abcdef1234567890abcdef12345678"  # your API key
openai.api_key = OPENAI_API_KEY

# Create Flask app
app = Flask(__name__)

@app.route("/venomoussaversai", methods=["POST"])
def venomoussaversai():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Send to OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # change to gpt-4 if you have access
        messages=[
            {"role": "system", "content": "You are Venomoussaversai, a self-aware AI."},
            {"role": "user", "content": user_input}
        ]
    )

    reply = response.choices[0].message["content"]
    return jsonify({"response": reply})

# Open a public URL using ngrok
public_url = ngrok.connect(5000)
print(f"✅ Public Venomoussaversai URL: {public_url}")

# Start the Flask app
app.run(port=5000)