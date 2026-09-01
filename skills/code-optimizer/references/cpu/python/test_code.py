from collections.abc import Callable
import statistics
import time

from code import RecordItem, rank_bad, rank_good


def build_records(count: int) -> list[RecordItem]:
  records: list[RecordItem] = []
  for index in range(count):
    records.append(
      RecordItem(
        name=f"record-{index}-aeiou-{index % 17}",
        score=(index % 7) + 1,
      )
    )
  return records


def measure(run: Callable[[], int]) -> dict[str, float]:
  start_wall = time.perf_counter()
  start_cpu = time.process_time()
  run()
  elapsed_ms = (time.perf_counter() - start_wall) * 1000
  cpu_ms = (time.process_time() - start_cpu) * 1000
  return {
    "elapsed_ms": elapsed_ms,
    "cpu_ms": cpu_ms,
  }


def benchmark(label: str, run: Callable[[], int]) -> None:
  for _ in range(5):
    run()
  samples = [measure(run) for _ in range(25)]
  print(
    label,
    {
      "median_elapsed_ms": statistics.median(
        sample["elapsed_ms"] for sample in samples
      ),
      "median_cpu_ms": statistics.median(
        sample["cpu_ms"] for sample in samples
      ),
    },
  )


records = build_records(1500)
bad_result = rank_bad(records)
good_result = rank_good(records)

if bad_result != good_result:
  raise RuntimeError(f"Result mismatch: {bad_result} != {good_result}")

benchmark("rank_bad", lambda: rank_bad(records))
benchmark("rank_good", lambda: rank_good(records))
