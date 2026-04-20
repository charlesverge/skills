from __future__ import annotations

from settings import HarnessSettings


def run_setup(settings: HarnessSettings) -> None:
    settings.logs_dir.mkdir(parents=True, exist_ok=True)
    settings.artifacts_dir.mkdir(parents=True, exist_ok=True)
    settings.tmp_dir.mkdir(parents=True, exist_ok=True)
