#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from execution import run_execution
from health import run_health_checks
from settings import HarnessSettings, load_settings
from setup import run_setup
from verify import run_verify


def _compose_base_args(settings: HarnessSettings) -> list[str]:
    return [
        "docker",
        "compose",
        "-p",
        settings.compose_project_name,
        "-f",
        str(settings.compose_file),
    ]


def _run_streaming_command(
    command: Iterable[str],
    *,
    cwd: Path,
    log_file: Path | None = None,
    check: bool = True,
) -> int:
    command_list = list(command)
    print(f"$ {' '.join(command_list)}")

    log_handle = None
    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        log_handle = log_file.open("a", encoding="utf-8")

    process = subprocess.Popen(
        command_list,
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    assert process.stdout is not None
    for line in process.stdout:
        sys.stdout.write(line)
        if log_handle is not None:
            log_handle.write(line)

    return_code = process.wait()
    if log_handle is not None:
        log_handle.flush()
        log_handle.close()

    if check and return_code != 0:
        raise RuntimeError(f"Command failed with code {return_code}: {' '.join(command_list)}")

    return return_code


def _timestamped_log_file(settings: HarnessSettings, prefix: str) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return settings.logs_dir / f"{prefix}-{stamp}.log"


def _docker_compose_up(settings: HarnessSettings) -> None:
    command = _compose_base_args(settings) + ["up", "-d", "--build"]
    _run_streaming_command(
        command,
        cwd=settings.harness_root,
        log_file=_timestamped_log_file(settings, "compose-up"),
        check=True,
    )


def _docker_compose_down(settings: HarnessSettings) -> None:
    command = _compose_base_args(settings) + ["down", "--remove-orphans"]
    _run_streaming_command(
        command,
        cwd=settings.harness_root,
        log_file=_timestamped_log_file(settings, "compose-down"),
        check=True,
    )


def _collect_compose_logs(settings: HarnessSettings) -> None:
    command = _compose_base_args(settings) + ["logs", "--no-color"]
    _run_streaming_command(
        command,
        cwd=settings.harness_root,
        log_file=_timestamped_log_file(settings, "compose-logs"),
        check=False,
    )


def _cleanup(settings: HarnessSettings) -> None:
    _collect_compose_logs(settings)
    _docker_compose_down(settings)

    for directory in [settings.logs_dir, settings.artifacts_dir, settings.tmp_dir]:
        if directory.exists():
            shutil.rmtree(directory)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Hello world test harness runner")
    parser.add_argument("--setup", action="store_true", help="Only perform setup")
    parser.add_argument("--execute", action="store_true", help="Only perform execution")
    parser.add_argument("--verify", action="store_true", help="Only perform verification")
    parser.add_argument(
        "--no-tear-down",
        action="store_true",
        help="Leave Docker containers running after stage execution",
    )
    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="Remove Docker containers, logs, and temporary artifacts",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    settings = load_settings()

    if args.cleanup:
        _cleanup(settings)
        return 0

    selected_stages = [args.setup, args.execute, args.verify]
    run_all_stages = not any(selected_stages)

    try:
        if run_all_stages or args.setup:
            run_setup(settings)
            _docker_compose_up(settings)
            run_health_checks(settings)

        if run_all_stages or args.execute:
            run_execution(settings)

        if run_all_stages or args.verify:
            run_verify(settings)

        return 0
    finally:
        _collect_compose_logs(settings)
        if not args.no_tear_down:
            _docker_compose_down(settings)


if __name__ == "__main__":
    raise SystemExit(main())
