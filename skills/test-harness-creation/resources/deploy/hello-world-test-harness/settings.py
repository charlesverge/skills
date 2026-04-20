from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class HarnessSettings:
    harness_root: Path
    workspace_root: Path
    compose_file: Path
    compose_project_name: str
    base_url: str
    healthcheck_endpoint: str
    execution_results_file: Path
    test_cases_fixture_file: Path
    logs_dir: Path
    artifacts_dir: Path
    tmp_dir: Path


def load_settings() -> HarnessSettings:
    harness_root = Path(__file__).resolve().parent
    workspace_root = harness_root.parents[4]
    compose_file = harness_root / "docker-compose.yml"
    logs_dir = harness_root / "logs"
    artifacts_dir = harness_root / "artifacts"
    tmp_dir = harness_root / "tmp"
    test_cases_fixture_file = harness_root / "fixtures" / "test_cases.json"

    return HarnessSettings(
        harness_root=harness_root,
        workspace_root=workspace_root,
        compose_file=compose_file,
        compose_project_name="hello-world-test-harness",
        base_url="http://127.0.0.1:18080",
        healthcheck_endpoint="/health",
        execution_results_file=artifacts_dir / "execution_results.json",
        test_cases_fixture_file=test_cases_fixture_file,
        logs_dir=logs_dir,
        artifacts_dir=artifacts_dir,
        tmp_dir=tmp_dir,
    )
