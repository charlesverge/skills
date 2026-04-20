from __future__ import annotations

import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

from settings import HarnessSettings


def _compose_base_args(settings: HarnessSettings) -> list[str]:
    return [
        "docker",
        "compose",
        "-p",
        settings.compose_project_name,
        "-f",
        str(settings.compose_file),
    ]


def _run_checked(command: list[str], cwd: Path) -> str:
    process = subprocess.run(
        command,
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    if process.returncode != 0:
        raise RuntimeError(
            f"Health check command failed ({process.returncode}): {' '.join(command)}\n{process.stdout}"
        )
    return process.stdout


def _check_docker_available(settings: HarnessSettings) -> None:
    _run_checked(["docker", "version"], cwd=settings.harness_root)


def _check_http_health_endpoint(settings: HarnessSettings, timeout_seconds: int = 45) -> None:
    deadline = time.time() + timeout_seconds
    url = f"{settings.base_url}{settings.healthcheck_endpoint}"

    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=3) as response:
                if response.status == 200:
                    return
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError):
            time.sleep(1)
            continue

    raise RuntimeError(f"Health endpoint failed: {url}")


def _check_mongodb_ready(settings: HarnessSettings) -> None:
    command = _compose_base_args(settings) + [
        "exec",
        "-T",
        "mongodb",
        "mongosh",
        "--quiet",
        "--eval",
        "db.runCommand({ ping: 1 })",
    ]
    output = _run_checked(command, cwd=settings.harness_root)
    if "ok" not in output:
        raise RuntimeError(f"MongoDB ping output did not include ok=1: {output}")


def _check_redis_ready(settings: HarnessSettings) -> None:
    command = _compose_base_args(settings) + ["exec", "-T", "redis", "redis-cli", "ping"]
    output = _run_checked(command, cwd=settings.harness_root)
    if "PONG" not in output:
        raise RuntimeError(f"Redis ping did not return PONG: {output}")


def _check_in_container_connectivity(settings: HarnessSettings) -> None:
    command = _compose_base_args(settings) + [
        "exec",
        "-T",
        "server-example",
        "python",
        "/app/health_container_check.py",
    ]
    _run_checked(command, cwd=settings.harness_root)


def _check_write_permission(settings: HarnessSettings) -> None:
    settings.artifacts_dir.mkdir(parents=True, exist_ok=True)
    marker_file = settings.artifacts_dir / ".health-write-check.tmp"
    marker_file.write_text("ok\n", encoding="utf-8")
    marker_file.unlink()


def run_health_checks(settings: HarnessSettings) -> None:
    _check_docker_available(settings)
    _check_http_health_endpoint(settings)
    _check_mongodb_ready(settings)
    _check_redis_ready(settings)
    _check_in_container_connectivity(settings)
    _check_write_permission(settings)
