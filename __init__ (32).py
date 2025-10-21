"""
kb_error_correction.py
Error detection / correction and consistency management for an AI reasoning KB.

Author: Example for Ananthu Sajeev
"""

import uuid
import time
import hashlib
import copy
import pprint
from typing import Dict, List, Any, Optional, Tuple

# -------------------------
# Utilities
# -------------------------
def uid() -> str:
    return str(uuid.uuid4())[:8]

def now_ts() -> float:
    return time.time()

def checksum_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:12]

# -------------------------
# Data structures
# -------------------------
class Provenance:
    def __init__(self, source: str = "unknown", note: str = "", ts: Optional[float] = None):
        self.source = source
        self.note = note
        self.ts = ts or now_ts()

    def to_dict(self):
        return {"source": self.source, "note": self.note, "ts": self.ts}

    def __repr__(self):
        return f"Prov(source={self.source}, note={self.note}, ts={int(self.ts)})"

class Belief:
    def __init__(self, statement: str, confidence: float = 0.9, prov: Optional[Provenance] = None):
        self.id = uid()
        self.statement = statement.strip()
        self.confidence = float(max(0.0, min(1.0, confidence)))
        self.prov = prov or Provenance()
        self.checksum = checksum_text(self.statement + str(self.confidence) + str(self.prov.ts))

    def update_confidence(self, new_confidence: float):
        self.confidence = float(max(0.0, min(1.0, new_confidence)))
        self.checksum = checksum_text(self.statement + str(self.confidence) + str(self.prov.ts))

    def refresh_checksum(self):
        self.checksum = checksum_text(self.statement + str(self.confidence) + str(self.prov.ts))

    def to_dict(self):
        return {
            "id": self.id,
            "statement": self.statement,
            "confidence": self.confidence,
            "prov": self.prov.to_dict(),
            "checksum": self.checksum,
        }

    def __repr__(self):
        return f"Belief(id={self.id}, c={self.confidence:.3f}, '{self.statement}', {self.prov})"

# -------------------------
# Error / Event Logging
# -------------------------
class EventLog:
    def __init__(self):
        self.events: List[Dict[str, Any]] = []

    def log(self, level: str, msg: str, details: Optional[Dict[str, Any]] = None):
        entry = {
            "ts": now_ts(),
            "level": level,
            "msg": msg,
            "details": details or {},
        }
        self.events.append(entry)
        # lightweight console feedback for development
        print(f"[{level}] {msg}")

    def last(self, n=5):
        return self.events[-n:]

# -------------------------
# KnowledgeBase with transactions & correction
# -------------------------
class KBError(Exception):
    pass

class KnowledgeBase:
    def __init__(self, enable_integrity: bool = True):
        self.facts: Dict[str, Belief] = {}
        self.rules: List[Tuple[str, List[str]]] = []
        self.log = EventLog()
        self.enable_integrity = enable_integrity
        # transaction buffer
        self._tx_stack: List[Dict[str, Any]] = []

    # -------------------------
    # Transactional operations
    # -------------------------
    def begin_tx(self):
        snapshot = {
            "facts": copy.deepcopy(self.facts),
            "rules": copy.deepcopy(self.rules)
        }
        self._tx_stack.append(snapshot)
        self.log.log("DEBUG", "Transaction begun", {"depth": len(self._tx_stack)})

    def commit_tx(self):
        if not self._tx_stack:
            self.log.log("WARN", "commit_tx called with no active transaction")
            return
        self._tx_stack.pop()
        self.log.log("DEBUG", "Transaction committed", {"depth": len(self._tx_stack)})

    def rollback_tx(self):
        if not self._tx_stack:
            self.log.log("WARN", "rollback_tx called with no active transaction")
            return
        snapshot = self._tx_stack.pop()
        self.facts = snapshot["facts"]
        self.rules = snapshot["rules"]
        self.log.log("WARN", "Transaction rolled back", {"depth": len(self._tx_stack)})

    # -------------------------
    # Fact management (with provenance/integrity)
    # -------------------------
    def add_fact(self, stmt: str, confidence: float = 0.9, source: str = "user", note: str = "") -> Belief:
        stmt = stmt.strip()
        # quick safety & normalization
        if not stmt:
            self.log.log("ERROR", "Attempt to add empty statement")
            raise KBError("Empty statement")
        b = Belief(stmt, confidence, Provenance(source=source, note=note))
        # collision detection: identical statement exists?
        existing = self.find_exact(stmt)
        if existing:
            # merge confidences instead of duplicate
            self.log.log("DEBUG", "Merging existing fact", {"stmt": stmt, "existing_id": existing.id})
            merged_conf = self._merge_confidences(existing.confidence, b.confidence, existing.prov, b.prov)
            existing.update_confidence(merged_conf)
            # update provenance to more recent/more trusted
            existing.prov = self._choose_provenance(existing.prov, b.prov)
            existing.refresh_checksum()
            return existing
        # otherwise insert
        self.facts[b.id] = b
        self.log.log("INFO", "Added fact", {"id": b.id, "stmt": stmt, "c": b.confidence})
        # optional integrity check
        if self.enable_integrity and not self._integrity_check(b):
            self.log.log("ERROR", "Integrity check failed after add_fact", {"id": b.id})
            raise KBError("Integrity check failed")
        return b

    def remove_fact(self, fact_id: str) -> bool:
        if fact_id in self.facts:
            del self.facts[fact_id]
            self.log.log("INFO", "Removed fact", {"id": fact_id})
            return True
        self.log.log("WARN", "Tried to remove non-existent fact", {"id": fact_id})
        return False

    def find_exact(self, stmt: str) -> Optional[Belief]:
        for b in self.facts.values():
            if b.statement == stmt:
                return b
        return None

    def find_facts(self, pattern: str) -> List[Belief]:
        # substring match (quick) - replace with FOL matcher if needed
        return [b for b in self.facts.values() if pattern in b.statement]

    def add_rule(self, conclusion: str, premises: List[str]):
        self.rules.append((conclusion.strip(), [p.strip() for p in premises]))
        self.log.log("INFO", "Rule added", {"concl": conclusion, "premises": premises})

    # -------------------------
    # Integrity & Consistency checks
    # -------------------------
    def _integrity_check(self, belief: Belief) -> bool:
        # check that checksum matches computed value and confidence in range
        recomputed = checksum_text(belief.statement + str(belief.confidence) + str(belief.prov.ts))
        ok = recomputed == belief.checksum and 0.0 <= belief.confidence <= 1.0
        if not ok:
            self.log.log("ERROR", "Integrity mismatch", {"id": belief.id, "recomputed": recomputed, "stored": belief.checksum})
        return ok

    def full_integrity_scan(self) -> List[str]:
        failed = []
        for b in list(self.facts.values()):
            if not self._integrity_check(b):
                failed.append(b.id)
        self.log.log("DEBUG", "Integrity scan completed", {"failed_count": len(failed)})
        return failed

    # -------------------------
    # Contradiction detection & resolution
    # -------------------------
    def detect_contradictions(self) -> List[Tuple[Belief, Belief]]:
        """
        Very naive contradiction detection:
         - detects pairs 'X is Y' vs 'X is not Y'
         - detects explicit negation phrases
        """
        contradictions = []
        items = list(self.facts.values())
        for i in range(len(items)):
            for j in range(i+1, len(items)):
                a = items[i]; b = items[j]
                if self._is_negation_pair(a.statement, b.statement):
                    contradictions.append((a, b))
        self.log.log("DEBUG", "Contradiction detection run", {"count": len(contradictions)})
        return contradictions

    @staticmethod
    def _is_negation_pair(s1: str, s2: str) -> bool:
        # normalized check
        s1n = s1.lower().strip()
        s2n = s2.lower().strip()
        # examples: "X is Y" vs "X is not Y"
        if (" not " in s1n and s1n.replace(" not ", " ") == s2n) or (" not " in s2n and s2n.replace(" not ", " ") == s1n):
            return True
        # check for explicit contradictory tokens: "is dead" vs "is alive" (configurable)
        CONTRA_PAIRS = [("alive", "dead"), ("true", "false"), ("working", "broken")]
        for x, y in CONTRA_PAIRS:
            if x in s1n and y in s2n or x in s2n and y in s1n:
                return True
        return False

    def resolve_contradictions(self, prefer_source_order: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        For every contradiction pair, choose which belief to keep/adjust:
         - keep the higher-confidence belief
         - if confidences equal, use provenance priority if provided
         - optional: perform belief revision instead of full removal
        Returns list of resolution actions taken
        """
        resolves = []
        contradictions = self.detect_contradictions()
        for a, b in contradictions:
            # choose winner
            winner, loser = self._choose_winner(a, b, prefer_source_order)
            # if confidences close, attempt revision instead of deletion
            conf_diff = abs(winner.confidence - loser.confidence)
            if conf_diff < 0.15:
                # revision: move winner confidence towards combined evidence and record provenance
                new_conf = self._merge_confidences(winner.confidence, loser.confidence, winner.prov, loser.prov)
                old_conf = winner.confidence
                winner.update_confidence(new_conf)
                winner.prov = self._choose_provenance(winner.prov, loser.prov)
                self.remove_fact(loser.id)
                action = {"action": "revised_and_removed", "kept": winner.id, "old_conf": old_conf, "new_conf": new_conf, "removed": loser.id}
                self.log.log("INFO", "Contradiction resolved by revision", action)
                resolves.append(action)
            else:
                # remove loser
                removed = self.remove_fact(loser.id)
                action = {"action": "removed_lower_conf", "kept": winner.id, "removed": loser.id, "kept_conf": winner.confidence}
                self.log.log("INFO", "Contradiction resolved by removal", action)
                resolves.append(action)
        return resolves

    def _choose_winner(self, a: Belief, b: Belief, prefer_source_order: Optional[List[str]] = None) -> Tuple[Belief, Belief]:
        # highest confidence wins
        if a.confidence > b.confidence:
            return a, b
        elif b.confidence > a.confidence:
            return b, a
        # tie-breaker: source preference
        if prefer_source_order:
            for s in prefer_source_order:
                if s == a.prov.source:
                    return a, b
                if s == b.prov.source:
                    return b, a
        # last resort: most recent prov timestamp wins
        if a.prov.ts >= b.prov.ts:
            return a, b
        else:
            return b, a

    # -------------------------
    # Belief revision & confidence merging
    # -------------------------
    @staticmethod
    def _merge_confidences(c1: float, c2: float, p1: Provenance, p2: Provenance) -> float:
        """
        Weighted merge heuristic:
         - weight by recency and by source trust (simple mapping)
         - default: recency gives slight priority
        """
        def source_trust(src: str) -> float:
            # domain specific mapping - extend as needed
            trust_map = {"user": 0.5, "sensor": 0.8, "llm": 0.6, "system": 0.9, "trusted": 0.95}
            return trust_map.get(src, 0.5)
        w1 = 0.5 + 0.3 * (1.0 if p1.ts >= p2.ts else 0.0) + 0.2 * source_trust(p1.source)
        w2 = 0.5 + 0.3 * (1.0 if p2.ts >= p1.ts else 0.0) + 0.2 * source_trust(p2.source)
        # normalize
        s = w1 + w2
        if s == 0:
            return max(c1, c2)
        merged = (c1 * w1 + c2 * w2) / s
        # small discount for automated merges
        return max(0.0, min(1.0, merged * 0.98))

    @staticmethod
    def _choose_provenance(p1: Provenance, p2: Provenance) -> Provenance:
        # prefer newer and more "trusted" source. Simple heuristic.
        trust_map = {"user": 0.5, "sensor": 0.8, "llm": 0.6, "system": 0.9, "trusted": 0.95}
        t1 = trust_map.get(p1.source, 0.5)
        t2 = trust_map.get(p2.source, 0.5)
        # weight by timestamp and trust
        score1 = t1 + (p1.ts / (p1.ts + p2.ts + 1e-9))
        score2 = t2 + (p2.ts / (p1.ts + p2.ts + 1e-9))
        return p1 if score1 >= score2 else p2

    # -------------------------
    # Repair suggestions (for humans or LLM assistants)
    # -------------------------
    def suggest_repairs(self, max_suggestions: int = 10) -> List[Dict[str, Any]]:
        suggestions = []
        # Suggest re-verification for low-confidence facts
        lows = [b for b in self.facts.values() if b.confidence < 0.5]
        for b in sorted(lows, key=lambda x: x.confidence)[:max_suggestions]:
            suggestions.append({"type": "re-verify", "id": b.id, "stmt": b.statement, "confidence": b.confidence, "prov": b.prov.to_dict()})
        # Suggest resolution for contradictions
        contradictions = self.detect_contradictions()
        for a, c in contradictions[:max_suggestions]:
            suggestions.append({"type": "contradiction", "a": a.to_dict(), "b": c.to_dict()})
        # Suggest integrity fixes
        bad_checks = self.full_integrity_scan()
        for fid in bad_checks[:max_suggestions]:
            suggestions.append({"type": "integrity_failed", "id": fid})
        self.log.log("DEBUG", "Generated repair suggestions", {"count": len(suggestions)})
        return suggestions

    # -------------------------
    # Persistence / export hooks (simple)
    # -------------------------
    def export_state(self) -> Dict[str, Any]:
        return {
            "facts": {fid: b.to_dict() for fid, b in self.facts.items()},
            "rules": copy.deepcopy(self.rules),
            "ts": now_ts()
        }

    def import_state(self, state: Dict[str, Any], strict: bool = False):
        # light import: recreate Belief objects with provenance data; if strict, check checksums
        imported = {}
        for fid, obj in state.get("facts", {}).items():
            p = Provenance(source=obj["prov"].get("source", "import"), note=obj["prov"].get("note", ""), ts=obj["prov"].get("ts"))
            b = Belief(obj["statement"], obj["confidence"], prov=p)
            b.id = fid
            b.checksum = obj.get("checksum", checksum_text(b.statement + str(b.confidence) + str(b.prov.ts)))
            if strict and not self._integrity_check(b):
                self.log.log("ERROR", "Imported belief failed integrity", {"id": fid})
                raise KBError("Imported belief failed integrity")
            imported[fid] = b
        self.facts = imported
        self.rules = copy.deepcopy(state.get("rules", []))
        self.log.log("INFO", "State imported", {"facts": len(self.facts), "rules": len(self.rules)})

# -------------------------
# Demo & basic tests
# -------------------------
if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=2).pprint
    kb = KnowledgeBase(enable_integrity=True)

    # start a transaction and add facts
    kb.begin_tx()
    b1 = kb.add_fact("Ananthu is creator of Venomoussaversai", 0.95, source="user", note="declared by user")
    b2 = kb.add_fact("Ananthu is not creator of Venomoussaversai", 0.6, source="llm", note="llm assertion")
    b3 = kb.add_fact("Venomoussaversai speaks truth", 0.8, source="system")
    kb.commit_tx()

    print("\nKB Facts before resolution:")
    pp({fid: b.to_dict() for fid, b in kb.facts.items()})

    # detect contradictions
    contr = kb.detect_contradictions()
    print("\nDetected contradictions (pairs):", [(a.id, b.id, a.statement, b.statement) for a, b in contr])

    # resolve contradictions preferring system sources
    resolves = kb.resolve_contradictions(prefer_source_order=["system", "user", "llm"])
    print("\nResolutions applied:")
    pp(resolves)

    print("\nKB Facts after resolution:")
    pp({fid: b.to_dict() for fid, b in kb.facts.items()})

    # introduce a low-confidence fact to trigger suggestion
    kb.add_fact("Bridge will be built tomorrow", 0.2, source="user")
    suggestions = kb.suggest_repairs()
    print("\nRepair suggestions:")
    pp(suggestions)

    # demonstrate rollback in failing transaction
    kb.begin_tx()
    try:
        kb.add_fact("", 0.7, source="user")  # deliberate error: empty statement
        kb.commit_tx()
    except Exception as e:
        print("\nException during tx:", e)
        kb.rollback_tx()

    print("\nFinal KB Facts:")
    pp({fid: b.to_dict() for fid, b in kb.facts.items()})