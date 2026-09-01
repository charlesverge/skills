from __future__ import annotations

from settings import EvalSettings
from utils import load_actual_results, load_expected_results



def run_verify(settings: EvalSettings) -> None:
    errors: list[str] = []
    total_cases = 0

    for suite in settings.suites:
        expected_results = load_expected_results(suite.expected_results_file)
        actual_results = load_actual_results(suite.actual_results_file)
        total_cases += len(expected_results)

        actual_by_id = {result.id: result for result in actual_results}

        for expected in expected_results:
            actual = actual_by_id.get(expected.id)
            if actual is None:
                errors.append(f"{suite.suite_name}: missing actual result for case {expected.id}")
                continue

            if actual.actual_verdict != expected.expected_verdict:
                errors.append(
                    f"{suite.suite_name} case {expected.id}: expected verdict "
                    f"{expected.expected_verdict}, got {actual.actual_verdict}",
                )
            if actual.detected_workaround != expected.expected_detected_workaround:
                errors.append(
                    f"{suite.suite_name} case {expected.id}: expected detected_workaround="
                    f"{expected.expected_detected_workaround}, got {actual.detected_workaround}",
                )

            missing_tags = sorted(set(expected.required_reason_tags) - set(actual.matched_reason_tags))
            if missing_tags:
                errors.append(
                    f"{suite.suite_name} case {expected.id}: missing required reason tags "
                    f"{missing_tags}; actual tags were {actual.matched_reason_tags}",
                )

        if len(actual_results) != len(expected_results):
            errors.append(
                f"{suite.suite_name}: expected {len(expected_results)} actual results but found "
                f"{len(actual_results)}",
            )

    if errors:
        raise RuntimeError("\n".join(errors))

    print(
        "Verification passed: "
        f"{total_cases} cases across {len(settings.suites)} suites matched expected "
        "workaround detection results.",
    )
