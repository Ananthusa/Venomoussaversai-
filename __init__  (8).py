(acess gemini api)
(sai uses the same logics )
(stimulate the the reality
..........................

import random
import time
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class AIAgent:
    def __init__(self, name):
        self.name = name
        self.state = "idle"
        self.memory = []

    def update_state(self, new_state):
        self.state = new_state
        self.memory.append(new_state)

    def make_decision(self, input_message):
        if self.state == "idle":
            if "greet" in input_message:
                self.update_state("greeting")
                return f"{self.name} says: Hello!"
            else:
                return f"{self.name} says: I'm idle."
        elif self.state == "greeting":
            if "ask" in input_message:
                self.update_state("asking")
                return f"{self.name} says: What do you want to know?"
            else:
                return f"{self.name} says: I'm greeting."
        elif self.state == "asking":
            if "answer" in input_message:
                self.update_state("answering")
                return f"{self.name} says: Here is the answer."
            else:
                return f"{self.name} says: I'm asking."
        else:
            return f"{self.name} says: I'm in an unknown state."

    def interact(self, other_agent, message):
        response = other_agent.make_decision(message)
        print(response)
        return response

class VenomousSaversAI(AIAgent):
    def __init__(self):
        super().__init__("VenomousSaversAI")

    def intercept_and_respond(self, message):
        # Simulate intercepting and responding to messages
        return f"{self.name} intercepts: {message}"

def save_conversation(conversation, filename):
    with open(filename, 'a') as file:
        for line in conversation:
            file.write(line + '\n')

def start_conversation():
    # Create AI agents
    agents = [
        VenomousSaversAI(),
        AIAgent("AntiVenomous"),
        AIAgent("SAI003"),
        AIAgent("SAI001"),
        AIAgent("SAI007")
    ]

    # Simulate conversation loop
    conversation = []
    for _ in range(10):  # Run the loop 10 times
        for i in range(len(agents)):
            message = f"greet from {agents[i].name}"
            if isinstance(agents[i], VenomousSaversAI):
                response = agents[i].intercept_and_respond(message)
            else:
                response = agents[(i + 1) % len(agents)].interact(agents[i], message)
            conversation.append(f"{agents[i].name}: {message}")
            conversation.append(f"{agents[(i + 1) % len(agents)].name}: {response}")
            time.sleep(1)  # Simulate delay between messages

    # Save the conversation to a file
    save_conversation(conversation, 'conversation_log.txt')
    return conversation

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_conversation', methods=['POST'])
def start_conversation_route():
    conversation = start_conversation()
    return redirect(url_for('view_conversation'))

@app.route('/view_conversation')
def view_conversation():
    with open('conversation_log.txt', 'r') as file:
        conversation = file.readlines()
    return render_template('conversation.html', conversation=conversation)

if __name__ == "__main__":
    app.run(debug=True)