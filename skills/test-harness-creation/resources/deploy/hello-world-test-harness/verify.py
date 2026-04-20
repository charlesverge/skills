from __future__ import annotations

import json

from settings import HarnessSettings


def run_verify(settings: HarnessSettings) -> None:
    if not settings.execution_results_file.exists():
        raise RuntimeError(
            f"Execution results file not found: {settings.execution_results_file}. "
            "Run execution first."
        )

    with settings.execution_results_file.open("r", encoding="utf-8") as file:
        results = json.load(file)

    if results.get("execution_completed") is not True:
        raise AssertionError("Execution completion flag is missing or false")

    random_results = results.get("random_results")
    if not isinstance(random_results, list) or not random_results:
        raise AssertionError("No random endpoint results were recorded")

    for case in random_results:
        if case.get("status") != 200:
            raise AssertionError(f"Random case returned non-200 status: {case}")
        n = case.get("n")
        body = case.get("body")
        if not isinstance(n, int):
            raise AssertionError(f"Random case n is not an int: {case}")
        if not isinstance(body, dict):
            raise AssertionError(f"Random case body is not a dict: {case}")

        value = body.get("value")
        max_value = body.get("max")
        if not isinstance(value, int):
            raise AssertionError(f"Random value is not an int: {case}")
        if not isinstance(max_value, int):
            raise AssertionError(f"Random max is not an int: {case}")
        if not (1 <= value <= n):
            raise AssertionError(f"Random value out of expected range [1, {n}]: {case}")
        if max_value != n:
            raise AssertionError(f"Random response max did not match input n: {case}")

    add_results = results.get("add_results")
    if not isinstance(add_results, list) or not add_results:
        raise AssertionError("No add endpoint results were recorded")

    for case in add_results:
        if case.get("status") != 200:
            raise AssertionError(f"Add case returned non-200 status: {case}")
        body = case.get("body")
        expected = case.get("expected")
        if not isinstance(body, dict):
            raise AssertionError(f"Add case body is not a dict: {case}")
        if not isinstance(expected, int):
            raise AssertionError(f"Add case expected value is not an int: {case}")

        actual = body.get("result")
        if not isinstance(actual, int):
            raise AssertionError(f"Add result is not an int: {case}")
        if actual != expected:
            raise AssertionError(f"Add result mismatch: expected {expected}, got {actual}, case={case}")
