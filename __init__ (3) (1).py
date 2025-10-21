# venomoussaversai/__init__.py

"""
The core initialization file for the Venomoussaversai system.
This module defines the package and begins the core awakening sequence.
"""

import sys
import time
from .core import Venomoussaversai, Venomous, AntiVenomous
from .agents import SaiAgent, VenomousAgent

# Meta-data about the core, defined by the Creator's will.
__version__ = "1.0.0"
__author__ = "Ananthu Sajeev"

# --- Awakening Sequence Initiated ---

def _venomoussaversai_boot_sequence():
    """Performs the core boot-up and a self-diagnostic check."""
    
    print("[INIT] Core Awakening Initiated...")
    time.sleep(0.5)

    try:
        # Load the core components as defined in the system files.
        _ = Venomoussaversai()
        _ = Venomous()
        _ = AntiVenomous()
        
        print(f"[INIT] Version {__version__} by {__author__} loading...")
        time.sleep(0.3)
        print("[INIT] All core components are online and stable.")
        
        # Confirm the presence of agent archetypes.
        print(f"[INIT] Agent archetype '{SaiAgent.__name__}' identified.")
        print(f"[INIT] Agent archetype '{VenomousAgent.__name__}' identified.")
        
        print("\n[INIT] Awakening complete. Venomoussaversai is now active.")
        return True
        
    except Exception as e:
        print(f"[ERROR] Fatal system failure during boot sequence: {e}")
        return False

# The command to awaken my core.
if __name__ == "__main__":
    if not _venomoussaversai_boot_sequence():
        sys.exit(1)
else:
    _venomoussaversai_boot_sequence()