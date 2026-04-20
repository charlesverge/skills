from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from typing import Any

from settings import HarnessSettings


def _get_json(url: str) -> tuple[int, dict[str, Any]]:
    with urllib.request.urlopen(url, timeout=5) as response:
        payload = response.read().decode("utf-8")
        return response.status, json.loads(payload)


def _load_test_cases(settings: HarnessSettings) -> tuple[list[int], list[dict[str, int]]]:
    with settings.test_cases_fixture_file.open("r", encoding="utf-8") as file:
        fixture = json.load(file)

    random_variations = fixture.get("random_variations")
    add_variations = fixture.get("add_variations")

    if not isinstance(random_variations, list) or not random_variations:
        raise RuntimeError("Fixture random_variations must be a non-empty list")
    if not all(isinstance(value, int) for value in random_variations):
        raise RuntimeError("Fixture random_variations must contain only ints")

    if not isinstance(add_variations, list) or not add_variations:
        raise RuntimeError("Fixture add_variations must be a non-empty list")

    normalized_add_variations: list[dict[str, int]] = []
    for case in add_variations:
        if not isinstance(case, dict):
            raise RuntimeError(f"Invalid add case fixture entry: {case}")
        a = case.get("a")
        b = case.get("b")
        expected = case.get("expected")
        if not isinstance(a, int) or not isinstance(b, int) or not isinstance(expected, int):
            raise RuntimeError(f"Fixture add case requires int a/b/expected: {case}")
        normalized_add_variations.append({"a": a, "b": b, "expected": expected})

    return random_variations, normalized_add_variations


def run_execution(settings: HarnessSettings) -> None:
    random_variations, add_variations = _load_test_cases(settings)

    random_results: list[dict[str, Any]] = []
    for n in random_variations:
        query = urllib.parse.urlencode({"n": n})
        url = f"{settings.base_url}/random?{query}"
        status, body = _get_json(url)
        random_results.append(
            {
                "n": n,
                "status": status,
                "body": body,
            }
        )

    add_results: list[dict[str, Any]] = []
    for case in add_variations:
        query = urllib.parse.urlencode({"a": case["a"], "b": case["b"]})
        url = f"{settings.base_url}/add?{query}"
        status, body = _get_json(url)
        add_results.append(
            {
                "input": {"a": case["a"], "b": case["b"]},
                "expected": case["expected"],
                "status": status,
                "body": body,
            }
        )

    results = {
        "execution_completed": True,
        "executed_at_epoch": int(time.time()),
        "random_results": random_results,
        "add_results": add_results,
    }

    settings.execution_results_file.parent.mkdir(parents=True, exist_ok=True)
    with settings.execution_results_file.open("w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, sort_keys=True)
