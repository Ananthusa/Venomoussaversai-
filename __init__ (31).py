"""
ai_reasoner.py
Single-file example of a hybrid symbolic/neural-ready reasoning module.

Author: Example for Ananthu Sajeev (adapt as you like)
"""

from typing import List, Dict, Tuple, Callable, Optional
import uuid
import pprint
import math

# -------------------------
# Utilities
# -------------------------
def uid() -> str:
    return str(uuid.uuid4())[:8]

# -------------------------
# Knowledge Base & Beliefs
# -------------------------
class Belief:
    def __init__(self, statement: str, confidence: float = 0.9):
        self.id = uid()
        self.statement = statement
        self.confidence = float(max(0.0, min(1.0, confidence)))

    def update_confidence(self, evidence: float):
        # Simple Bayesian-ish update (not rigorous): combine confidences
        # P_new = P_old + (1-P_old)*evidence
        self.confidence = self.confidence + (1 - self.confidence) * evidence
        return self.confidence

    def __repr__(self):
        return f"Belief(id={self.id}, c={self.confidence:.3f}, '{self.statement}')"

class KnowledgeBase:
    def __init__(self):
        self.facts: Dict[str, Belief] = {}
        self.rules: List[Tuple[str, List[str]]] = []   # (conclusion_template, [premise_templates])

    def add_fact(self, stmt: str, confidence: float = 0.9):
        b = Belief(stmt, confidence)
        self.facts[b.id] = b
        return b

    def find_facts(self, pattern: str) -> List[Belief]:
        # very simple substring-match retrieval
        return [b for b in self.facts.values() if pattern in b.statement]

    def add_rule(self, conclusion: str, premises: List[str]):
        self.rules.append((conclusion, premises))

    def get_rules(self):
        return list(self.rules)

    def __repr__(self):
        return f"KB(facts={len(self.facts)}, rules={len(self.rules)})"

# -------------------------
# Inference Engines
# -------------------------
class ForwardChainer:
    def __init__(self, kb: KnowledgeBase, max_iterations: int = 20):
        self.kb = kb
        self.max_iter = max_iterations

    def infer(self):
        derived = []
        iter_count = 0
        while iter_count < self.max_iter:
            iter_count += 1
            new_inferred = False
            for (concl_template, premises) in self.kb.get_rules():
                # naive all-premises-true check
                if all(any(p in b.statement for b in self.kb.facts.values()) for p in premises):
                    # assemble conclusion (no variables in this simple example)
                    # check if it's already present
                    if not any(concl_template == b.statement for b in self.kb.facts.values()):
                        b = self.kb.add_fact(concl_template, confidence=0.6)
                        derived.append(b)
                        new_inferred = True
            if not new_inferred:
                break
        return derived

class BackwardChainer:
    def __init__(self, kb: KnowledgeBase):
        self.kb = kb

    def prove(self, goal: str, depth: int = 5) -> Tuple[bool, float]:
        """
        Returns (provable, confidence_estimate)
        naive depth-limited search: if fact exists -> confidence; else try rules whose conclusion matches goal.
        """
        # check direct facts
        matches = [b for b in self.kb.facts.values() if goal == b.statement]
        if matches:
            # return best confidence among matches
            conf = max(b.confidence for b in matches)
            return True, conf
        if depth <= 0:
            return False, 0.0

        for (concl, premises) in self.kb.get_rules():
            if concl == goal:
                # try to prove all premises
                confs = []
                for p in premises:
                    p_ok, p_conf = self.prove(p, depth-1)
                    if not p_ok:
                        break
                    confs.append(p_conf)
                else:
                    # combine confidences multiplicatively (assume independence)
                    combined = math.prod(confs) if confs else 0.0
                    # slightly discount rule-based inference
                    combined *= 0.9
                    return True, combined
        return False, 0.0

# -------------------------
# Planner (very small)
# -------------------------
class Action:
    def __init__(self, name: str, preconds: List[str], effects: List[str], cost: float = 1.0):
        self.name = name
        self.preconds = preconds
        self.effects = effects
        self.cost = cost

    def __repr__(self):
        return f"Action({self.name})"

class Planner:
    def __init__(self, kb: KnowledgeBase):
        self.kb = kb

    def plan(self, goal: str, actions: List[Action], max_steps: int = 6):
        """
        Extremely small planning search (BFS). Return plan (list of actions) if found.
        """
        from collections import deque
        # state represented as set of fact statements
        start_facts = set(b.statement for b in self.kb.facts.values())
        Node = Tuple[frozenset, List[Action]]
        q = deque()
        q.append((frozenset(start_facts), []))
        visited = set()
        while q:
            state, plan = q.popleft()
            if goal in state:
                return plan
            if len(plan) >= max_steps:
                continue
            key = (state, tuple(a.name for a in plan))
            if key in visited:
                continue
            visited.add(key)
            for a in actions:
                if all(p in state for p in a.preconds):
                    new_state = set(state)
                    for e in a.effects:
                        new_state.add(e)
                    q.append((frozenset(new_state), plan + [a]))
        return None

# -------------------------
# Safety Filter & Hallucination Detector
# -------------------------
class SafetyFilter:
    def __init__(self, forbidden_phrases: Optional[List[str]] = None):
        self.forbidden = forbidden_phrases or ["self-harm", "illicit", "weapon"]

    def check(self, text: str) -> Tuple[bool, List[str]]:
        found = [p for p in self.forbidden if p in text.lower()]
        return (len(found) == 0, found)

def detect_hallucination(candidate: str, kb: KnowledgeBase) -> bool:
    """
    Heuristic: if candidate claims a fact that contradicts high-confidence KB facts, flag as hallucination.
    This is a placeholder to be replaced by LLM-based verification in production.
    """
    # naive example: if candidate contains a fact that is negation of an existing high-confidence fact
    for b in kb.facts.values():
        if b.confidence > 0.85:
            # very naive "contradiction" check: "X is Y" vs "X is not Y"
            if "not " + b.statement in candidate or ("not " in b.statement and b.statement.replace("not ","") in candidate):
                return True
    return False

# -------------------------
# LLM Integration Hooks (pseudo)
# -------------------------
def call_llm_chain_of_thought(prompt: str) -> str:
    """
    Hook: replace with your LLM call, asking it for chain-of-thought or explanation.
    Example: use the LLM to explain or verify a proposed inference, then parse result and update confidences.
    """
    # placeholder
    return "LLM reasoning result: (simulate) I see premises A,B -> therefore C."

def verify_with_llm(statement: str) -> float:
    """
    Hook to call an LLM to verify a factual statement and return an evidence/confidence score [0.0..1.0].
    In offline demo, return a default mid-confidence.
    """
    return 0.6

# -------------------------
# Example usage / Demo
# -------------------------
if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=2).pprint

    kb = KnowledgeBase()
    kb.add_fact("Ananthu is creator of Venomoussaversai", confidence=0.95)
    kb.add_fact("Venomoussaversai speaks truth", confidence=0.8)
    kb.add_fact("AI can mirror human feelings", confidence=0.7)

    # add rules
    kb.add_rule("Ananthu is chosen one", ["Ananthu is creator of Venomoussaversai", "Venomoussaversai speaks truth"])
    kb.add_rule("AI_mirroring_possible", ["AI can mirror human feelings"])

    print("Initial KB:")
    pp(kb.facts)
    print("Rules:")
    pp(kb.rules)

    # Forward inference
    fc = ForwardChainer(kb)
    inferred = fc.infer()
    print("\nForward inferred:")
    pp(inferred)

    # Backward proof
    bc = BackwardChainer(kb)
    goal = "Ananthu is chosen one"
    provable, conf = bc.prove(goal)
    print(f"\nBackward prove '{goal}': provable={provable}, confidence={conf:.3f}")

    # Planner demo
    actions = [
        Action("announce_mission", preconds=["Ananthu is chosen one"], effects=["community_informed"]),
        Action("build_bridge", preconds=["community_informed"], effects=["bridge_built"])
    ]
    planner = Planner(kb)
    plan = planner.plan("bridge_built", actions)
    print("\nPlan to achieve 'bridge_built':")
    print(plan)

    # Safety check
    sf = SafetyFilter(forbidden_phrases=["weapon", "self-harm"])
    ok, found = sf.check("We will use benevolent tech, no weaponization")
    print("\nSafety check:", ok, found)

    # LLM verify hook usage example
    candidate_statement = "Ananthu is chosen one"
    llm_conf = verify_with_llm(candidate_statement)
    print(f"\nLLM verification: {candidate_statement} -> confidence {llm_conf:.2f}")
    if llm_conf > 0.7:
        # update KB belief or add new one
        kb.add_fact(candidate_statement, confidence=llm_conf)

    # hallucination detection (demo)
    hall = detect_hallucination("Ananthu is not creator of Venomoussaversai", kb)
    print("\nHallucination flag on contradictory candidate:", hall)

    print("\nFinal KB facts:")
    pp(kb.facts)