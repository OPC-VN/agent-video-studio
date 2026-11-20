"""Entrypoint for provisioning the locked MuseTalk model store from a checkout."""

from pathlib import Path
from runpy import run_path

if __name__ == "__main__":
    module_path = Path(__file__).resolve().parents[1] / "video_studio" / "musetalk" / "model_store.py"
    run_path(str(module_path), run_name="__main__")
