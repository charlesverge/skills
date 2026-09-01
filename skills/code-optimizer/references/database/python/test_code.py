from collections.abc import Callable

from code import FakeDb, Order, QueryStats, totals_bad, totals_good


def build_orders(user_count: int, orders_per_user: int) -> tuple[list[str], list[Order]]:
  user_ids: list[str] = []
  orders: list[Order] = []
  for user_index in range(user_count):
    user_id = f"user-{user_index}"
    user_ids.append(user_id)
    for order_index in range(orders_per_user):
      orders.append(
        Order(
          user_id=user_id,
          total=(order_index % 5) + 1,
        )
      )
  return user_ids, orders


def measure(
  label: str,
  work: Callable[[FakeDb, list[str]], dict[str, int]],
  db: FakeDb,
  user_ids: list[str],
) -> tuple[dict[str, int], QueryStats, str]:
  db.reset()
  result = work(db, user_ids)
  return result, db.snapshot(), label


user_ids, orders = build_orders(200, 12)
db = FakeDb(orders)
bad_result, bad_stats, bad_label = measure("totals_bad", totals_bad, db, user_ids)
good_result, good_stats, good_label = measure("totals_good", totals_good, db, user_ids)

if bad_result != good_result:
  raise RuntimeError("Database example results do not match")

for label, stats in ((bad_label, bad_stats), (good_label, good_stats)):
  print(
    label,
    {
      "query_count": stats.query_count,
      "rows_returned": stats.rows_returned,
      "bytes_returned": stats.bytes_returned,
      "elapsed_ms": stats.elapsed_ms,
    },
  )
