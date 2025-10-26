# Thought-Cycle and Packet Formats

## Thought-Cycle (step-by-step)
1. **Input**: External stimulus is received and duplicated to both hemispheres.
2. **Parallel Processing**:
   - Venomous: creates emotive/associative representations.
   - Anti-Venomous: produces symbolic/logical representations.
3. **Transmission**: both produce "neural packets" sent to SAI Bridge.
4. **Integration (SAI)**:
   - Align timestamps and confidences.
   - Fuse overlapping concepts and resolve conflicts via dynamic weighting.
   - Produce executive decision.
5. **Output**: Decision is executed via sai001 (simulated) and stored in memory.
6. **Learning**: sai006 updates models in sandbox; human review required for deployment.

## Packet Formats (JSON example)
- Sensory Packet (from sai002):
  {
    "id": "uuid",
    "type": "sensory",
    "modalities": ["text", "image"],
    "features": { "text_emb": [...], "img_emb": [...] },
    "ts": 1690000000.0
  }

- Hemispheric Packet (Venomous / Anti-Venomous):
  {
    "id": "uuid",
    "source": "venomous",
    "representation": "emotive-conceptual",
    "concepts": [{"c":"dream", "weight":0.8}, ...],
    "confidence": 0.72,
    "ts": 1690000000.1
  }

- SAI Decision Packet:
  {
    "id": "uuid",
    "decision": "reply_text or action_id",
    "confidence": 0.85,
    "explanation": "human-readable rationale",
    "updates": {"weights": {...}},
    "ts": 1690000000.2
  }
