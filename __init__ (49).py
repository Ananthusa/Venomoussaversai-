"""
venom_self_recreator.py
Venomoussaversai — Self-Reading & Self-Recreating AI (safe edition)

Behavior:
- Reads a Python source file (defaults to itself).
- Analyzes top-level metadata (docstring, __version__, __author__).
- Produces a recreated copy with a bumped version and a small benign augmentation.
- Uses a Sai003Brain-like decision check before writing.
- Has safety flags: dry_run, max_copies, output_dir.

IMPORTANT: Run in a sandbox. This script purposely limits replication and only performs benign, human-readable modifications.
"""

__version__ = "1.0.0"
__author__ = "Ananthu Sajeev"
__created__ = "2025-09-18"

import ast
import os
import shutil
import datetime
from typing import Tuple, Optional

# ---------- Sai003Brain: approves/inhibits recreation ----------
class Sai003Brain:
    """
    Simple decision-maker: receives 'signal' (metadata) and decides whether to recreate.
    This stands in for your final brain; you can replace or extend its logic.
    """
    def __init__(self, allow_recreate: bool = True):
        self.allow_recreate = allow_recreate
        self.history = []

    def receive_signal(self, signal: dict) -> bool:
        """
        Example policy:
        - If energy (if present) below threshold -> disallow
        - If author matches expected -> allow depending on flag
        - Additional heuristics can be plugged here.
        """
        # Heuristics (safe defaults)
        energy = signal.get("energy", 100)
        author = signal.get("author", None)

        decision = True
        if energy < 10:
            decision = False
        if author and author != __author__:
            # require explicit permission if author differs
            decision = decision and self.allow_recreate

        self.history.append((signal, decision))
        return decision

    def feedback(self, decision: bool) -> str:
        return "APPROVE" if decision else "DENY"

# ---------- Self-analysis and recreation utilities ----------
def read_source(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def parse_metadata(source: str) -> dict:
    """
    Parse module docstring and top-level assignments like __version__, __author__.
    Returns a dict of metadata.
    """
    metadata = {}
    try:
        module = ast.parse(source)
        # docstring
        metadata["docstring"] = ast.get_docstring(module)
        # look for simple Assign nodes to __version__, __author__, __created__
        for node in module.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id in ("__version__", "__author__", "__created__"):
                        try:
                            value = ast.literal_eval(node.value)
                        except Exception:
                            value = None
                        metadata[target.id] = value
    except Exception as e:
        metadata["parse_error"] = str(e)
    return metadata

def bump_version(v: Optional[str]) -> str:
    """
    Conservative version bump: "MAJOR.MINOR.PATCH" -> increment PATCH.
    If not parseable, append ".1"
    """
    if not v:
        return "0.0.1"
    parts = v.split(".")
    try:
        parts = [int(p) for p in parts]
        parts[-1] += 1
        return ".".join(str(p) for p in parts)
    except Exception:
        return v + ".1"

def generate_recreation(source: str, metadata: dict, mutation_note: str = "") -> str:
    """
    Create a new source text based on original:
    - Bump __version__
    - Add a recreation header with timestamp and note
    - Optionally add a small harmless helper function if not present
    """
    new_source = source

    # 1) Bump version in source text (simple string replace of first occurrence)
    old_version = metadata.get("__version__", None)
    new_version = bump_version(old_version)
    if old_version is not None:
        new_source = new_source.replace(f'__version__ = "{old_version}"', f'__version__ = "{new_version}"', 1)
    else:
        # inject version near top (after module docstring)
        if metadata.get("docstring"):
            doc = metadata["docstring"]
            insertion = f'\n__version__ = "{new_version}"\n'
            new_source = new_source.replace('"""' + doc + '"""', '"""' + doc + '"""' + insertion, 1)

    # 2) Add a recreation header comment with timestamp
    ts = datetime.datetime.utcnow().isoformat() + "Z"
    header = f"\n# --- Recreated copy at {ts} ---\n# Mutation: {mutation_note}\n"
    new_source = header + new_source

    # 3) Add a benign helper if not present (idempotent)
    helper_name = "recreator_identity"
    if helper_name not in new_source:
        helper = (
            "\n\ndef recreator_identity():\n"
            "    \"\"\"Return simple identity info for the recreated copy.\"\"\"\n"
            f"    return {{'created_at':'{ts}','mutation_note':{repr(mutation_note)},'version':{repr(new_version)}}}\n"
        )
        new_source += helper

    return new_source

def write_new_file(output_dir: str, base_name: str, content: str) -> str:
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, base_name)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    return out_path

# ---------- Orchestrator ----------
def recreate_file(
    source_path: str,
    output_dir: str = "recreated_copies",
    max_copies: int = 3,
    dry_run: bool = True,
    brain: Optional[Sai003Brain] = None,
    mutation_note: str = "version bump + identity"
) -> Tuple[bool, Optional[str]]:
    """
    Main function:
    - Reads source_path
    - Parses metadata
    - Asks brain whether to recreate
    - If approved and under max_copies, writes recreated file
    Returns (success, path_or_message)
    """
    source_path = os.path.abspath(source_path)
    if not os.path.exists(source_path):
        return False, f"Source not found: {source_path}"

    source_text = read_source(source_path)
    metadata = parse_metadata(source_text)

    # Build a simple signal for the brain
    signal = {
        "author": metadata.get("__author__", None),
        "version": metadata.get("__version__", None),
        "docstring": metadata.get("docstring", "")[:200],
        # external signals can be added: energy, environment, etc.
        "energy": 100
    }

    if brain is None:
        brain = Sai003Brain(allow_recreate=True)

    decision = brain.receive_signal(signal)
    if not decision:
        return False, "Sai003Brain vetoed the recreation."

    # Count existing copies to respect max_copies
    os.makedirs(output_dir, exist_ok=True)
    existing = [f for f in os.listdir(output_dir) if f.startswith(os.path.basename(source_path))]
    if len(existing) >= max_copies:
        return False, f"Max copies reached ({max_copies}). Found: {len(existing)}"

    # Generate new content
    new_source = generate_recreation(source_text, metadata, mutation_note=mutation_note)

    # Build safe filename
    base = os.path.basename(source_path)
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    new_name = f"{base}.recreated.{timestamp}.py"
    if dry_run:
        # In dry run mode, do not write file; return the would-be path
        return True, os.path.join(os.path.abspath(output_dir), new_name)

    out_path = write_new_file(output_dir, new_name, new_source)
    return True, out_path

# ---------- If run as script ----------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Venomoussaversai Self-Reader & Recreator (safe)")
    parser.add_argument("--source", type=str, default=__file__, help="Path to source file to read (default: this file)")
    parser.add_argument("--output-dir", type=str, default="recreated_copies", help="Where to store recreated copies")
    parser.add_argument("--max-copies", type=int, default=3, help="Maximum number of recreated copies allowed")
    parser.add_argument("--no-dry-run", dest="dry_run", action="store_false", help="Actually write files (default is dry-run)")
    parser.add_argument("--mutation-note", type=str, default="version bump + identity", help="Note describing the mutation")
    args = parser.parse_args()

    brain = Sai003Brain(allow_recreate=True)
    success, info = recreate_file(
        source_path=args.source,
        output_dir=args.output_dir,
        max_copies=args.max_copies,
        dry_run=args.dry_run,
        brain=brain,
        mutation_note=args.mutation_note
    )

    if success:
        if args.dry_run:
            print("[DRY RUN] Recreation permitted. New file WOULD be:", info)
            print("Run with --no-dry-run to actually write the file.")
        else:
            print("Recreated file written to:", info)
    else:
        print("Recreation aborted:", info)