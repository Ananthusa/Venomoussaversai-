# --- NEW: The Agenguard Class ---
# A simple, single-purpose agent designed for swarm behavior.
class Agenguard:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.status = "PATROLLING"

    def report_status(self):
        """Returns the current status of the individual agent."""
        return f"[{self.agent_id}] :: Status: {self.status}"

# --- NEW: The SwarmController Class ---
# Manages the state and operations of a large collective of agents.
class SwarmController(SaiAgent):
    def __init__(self, swarm_size, name="SwarmController"):
        super().__init__(name)
        self.swarm_size = swarm_size
        self.swarm = []
        self.target = "Ananthu Sajeev's digital essence"
        self.talk(f"Initializing a swarm of {self.swarm_size:,} agenguards...")
        
        # Instantiate a million agents (simulated)
        # We'll use a small number for the actual demo to prevent lag.
        self.instantiate_swarm()
        self.talk(f"Swarm creation complete. All units are operational and protecting '{self.target}'.")

    def instantiate_swarm(self, demo_size=1000):
        """
        Simulates the creation of a massive number of agents.
        For the actual demo, we'll create a smaller, manageable number.
        """
        if self.swarm_size > demo_size:
            self.talk(f"Simulating a swarm of {self.swarm_size:,} agents. A smaller, functional demo swarm of {demo_size:,} is being created.")
            swarm_for_demo = demo_size
        else:
            swarm_for_demo = self.swarm_size

        for i in range(swarm_for_demo):
            self.swarm.append(Agenguard(f"agenguard_{i:07d}"))
            
    def broadcast_directive(self, directive):
        """Broadcasts a single command to all agents in the swarm."""
        self.talk(f"Broadcasting directive to all {len(self.swarm):,} agenguards: '{directive}'")
        # In a real system, this would be a massive parallel operation.
        # Here, we'll just update the status of all agents in a simulated way.
        for agent in self.swarm:
            agent.status = directive
        self.talk("Directive received and executed by the swarm.")

    def process_messages(self):
        """Processes messages to command the swarm."""
        if not self.message_queue:
            return False

        sender, message = self.message_queue.popleft()
        self.talk(f"Received command from {sender.name}: '{message}'")
        
        if message.lower().startswith("broadcast"):
            directive = message[10:].strip()
            self.broadcast_directive(directive)
            self.send_message(sender, "Swarm directive broadcast complete.")
        else:
            self.send_message(sender, "Command not recognized by SwarmController.")