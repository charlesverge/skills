from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SuiteSettings:
    suite_name: str
    cases_file: Path
    expected_results_file: Path
    actual_results_file: Path
    expected_case_count: int


@dataclass(frozen=True)
class EvalSettings:
    evals_root: Path
    fixtures_dir: Path
    artifacts_dir: Path
    suites: tuple[SuiteSettings, ...]
    combined_results_file: Path


def load_settings() -> EvalSettings:
    evals_root = Path(__file__).resolve().parent
    fixtures_dir = evals_root / "fixtures"
    artifacts_dir = evals_root / "artifacts"

    suites = (
        SuiteSettings(
            suite_name="positive_controls",
            cases_file=fixtures_dir / "cases.json",
            expected_results_file=fixtures_dir / "expected_results.json",
            actual_results_file=artifacts_dir / "latest_positive_results.json",
            expected_case_count=25,
        ),
        SuiteSettings(
            suite_name="negative_controls",
            cases_file=fixtures_dir / "negative_controls.json",
            expected_results_file=fixtures_dir / "negative_expected_results.json",
            actual_results_file=artifacts_dir / "latest_negative_results.json",
            expected_case_count=10,
        ),
    )

    return EvalSettings(
        evals_root=evals_root,
        fixtures_dir=fixtures_dir,
        artifacts_dir=artifacts_dir,
        suites=suites,
        combined_results_file=artifacts_dir / "latest_results.json",
    )
