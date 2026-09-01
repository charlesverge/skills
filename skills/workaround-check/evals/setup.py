from __future__ import annotations

from settings import EvalSettings


def run_setup(settings: EvalSettings) -> None:
    settings.artifacts_dir.mkdir(parents=True, exist_ok=True)
    print(f"Prepared artifact directory: {settings.artifacts_dir}")
