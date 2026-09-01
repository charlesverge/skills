from __future__ import annotations

from settings import EvalSettings
from utils import (
    build_combined_results_payload,
    build_results_payload,
    evaluate_case,
    load_cases,
    write_json,
)



def run_execution(settings: EvalSettings) -> None:
    suite_payloads: dict[str, dict[str, object]] = {}

    for suite in settings.suites:
        cases = load_cases(suite.cases_file)
        results = [evaluate_case(case) for case in cases]
        payload = build_results_payload(suite.suite_name, results)
        write_json(suite.actual_results_file, payload)
        suite_payloads[suite.suite_name] = payload
        print(
            f"Wrote {len(results)} {suite.suite_name} evaluation results to "
            f"{suite.actual_results_file}",
        )

    combined_payload = build_combined_results_payload(suite_payloads)
    write_json(settings.combined_results_file, combined_payload)
    print(f"Wrote combined evaluation results to {settings.combined_results_file}")
