# Sai Modules (Core Horsemen and Extension Rules)

## Core Modules
- sai001 — Motor / Executor
  - Role: Transform SAI decisions into outputs (text, simulated actions).
  - Permissions: simulated outputs only by default; requires human approval for real actuators.

- sai002 — Sensory Processing
  - Role: Ingest and normalize inputs (text, images, audio). Provides feature vectors to hemispheres.

- sai003 — Frontal Executive (SAI)
  - Role: Integrate Venomous and Anti-Venomous outputs, make executive decisions, spawn new sai modules.

- sai004 — Memory
  - Role: Episodic (recent events) and semantic (long-term facts) storage. Supports retrieval by context.

- sai005 — Emotion Regulation
  - Role: Modulate emotional intensity produced by Venomous before it reaches SAI.

- sai006 — Learning / Adaptation
  - Role: Apply training signals inside sandbox; propose parameter updates that require signoff.

- sai007 — Intuition / Imagination
  - Role: Produce creative symbolic outputs and hypothetical scenarios.

## Extension Rules for new sai00x
1. Every new `sai00x` must include metadata (id, purpose, owner, permissions, creation timestamp).
2. New modules default to **sandbox** permission: no external network access, read-only for critical resources.
3. Creation of modules is logged and signed. Deletion requires multi-party approval.
4. Modules expose the interface: `process(input_packet, context) -> output_packet, updates`.
