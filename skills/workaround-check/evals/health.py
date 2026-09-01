from __future__ import annotations

from settings import EvalSettings, SuiteSettings
from utils import load_cases, load_expected_results


def _run_suite_health_check(suite: SuiteSettings) -> None:
    if not suite.cases_file.exists():
        raise RuntimeError(f"Missing cases file: {suite.cases_file}")
    if not suite.expected_results_file.exists():
        raise RuntimeError(f"Missing expected-results file: {suite.expected_results_file}")

    cases = load_cases(suite.cases_file)
    expected_results = load_expected_results(suite.expected_results_file)

    if len(cases) != suite.expected_case_count:
        raise RuntimeError(
            f"Expected {suite.expected_case_count} cases but found {len(cases)} in {suite.cases_file}",
        )
    if len(expected_results) != suite.expected_case_count:
        raise RuntimeError(
            "Expected "
            f"{suite.expected_case_count} expected results but found {len(expected_results)} "
            f"in {suite.expected_results_file}",
        )

    case_ids = {case.id for case in cases}
    expected_ids = {result.id for result in expected_results}
    if case_ids != expected_ids:
        missing_expected = sorted(case_ids - expected_ids)
        missing_case = sorted(expected_ids - case_ids)
        raise RuntimeError(
            "Case IDs and expected-result IDs do not match. "
            f"Missing from expected: {missing_expected}; missing from cases: {missing_case}",
        )

    print(f"Health checks passed for {suite.suite_name}: {len(cases)} cases.")


def run_health_checks(settings: EvalSettings) -> None:
    for suite in settings.suites:
        _run_suite_health_check(suite)
