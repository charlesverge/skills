from collections.abc import Callable
import gc
import time
import tracemalloc

from code import Row, summarize_bad, summarize_good


def build_rows(count: int, width: int) -> list[Row]:
  payload = ",".join(f"value-{index}-token" for index in range(width))
  return [Row(id=index, payload=payload) for index in range(count)]


def measure(run: Callable[[], int]) -> dict[str, float]:
  gc.collect()
  tracemalloc.start()
  start = time.perf_counter()
  result = run()
  elapsed_ms = (time.perf_counter() - start) * 1000
  current, peak = tracemalloc.get_traced_memory()
  tracemalloc.stop()
  return {
    "result": float(result),
    "elapsed_ms": elapsed_ms,
    "current_bytes": float(current),
    "peak_bytes": float(peak),
  }


rows = build_rows(4000, 25)
bad = measure(lambda: summarize_bad(rows))
good = measure(lambda: summarize_good(rows))

if bad["result"] != good["result"]:
  raise RuntimeError("Memory example results do not match")

for label, sample in (("summarize_bad", bad), ("summarize_good", good)):
  print(
    label,
    {
      "elapsed_ms": sample["elapsed_ms"],
      "current_bytes": sample["current_bytes"],
      "peak_bytes": sample["peak_bytes"],
    },
  )
