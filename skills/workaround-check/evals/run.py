#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil

from execution import run_execution
from health import run_health_checks
from settings import load_settings
from setup import run_setup
from verify import run_verify



def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run workaround-check evals")
    parser.add_argument("--setup", action="store_true", help="Only perform setup")
    parser.add_argument("--execute", action="store_true", help="Only perform execution")
    parser.add_argument("--verify", action="store_true", help="Only perform verification")
    parser.add_argument("--cleanup", action="store_true", help="Remove generated artifacts")
    return parser.parse_args()



def _cleanup() -> None:
    settings = load_settings()
    if settings.artifacts_dir.exists():
        shutil.rmtree(settings.artifacts_dir)
    print(f"Removed artifacts under {settings.artifacts_dir}")



def main() -> int:
    args = _parse_args()

    if args.cleanup:
        _cleanup()
        return 0

    settings = load_settings()
    selected_stages = [args.setup, args.execute, args.verify]
    run_all_stages = not any(selected_stages)

    if run_all_stages or args.setup:
        run_setup(settings)
        run_health_checks(settings)

    if (args.execute or args.verify) and not run_all_stages:
        run_health_checks(settings)

    if run_all_stages or args.execute:
        run_execution(settings)

    if run_all_stages or args.verify:
        run_verify(settings)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
