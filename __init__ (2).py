import yaml
from pathlib import Path

_profile_path = Path(__file__).with_name("profile.yaml")
try:
    profile = yaml.safe_load(_profile_path.read_text())
except Exception:
    profile = {}