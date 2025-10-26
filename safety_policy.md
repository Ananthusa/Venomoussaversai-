# Safety & Governance Policy (Venomoussaversai)

## Core Rules
1. No autonomous actions with real-world destructive potential without explicit multi-human signoff.
2. All capabilities that could be dual-use (offensive/defensive) are restricted to sandboxed labs.
3. Immutable logging: every decision, module spawn, and model update is recorded with cryptographic hashes.
4. Anti-Venomous acts as the mandatory verifier for any action flagged as 'high-risk'.
5. Human-in-the-loop: any change to production configurations requires 2 or more human approvers.

## Audit & Monitoring
- Log format includes: event_id, module, inputs, outputs, signer, timestamp, signature.
- Periodic audits: weekly model-change summaries and monthly red-team review (sandbox only).
