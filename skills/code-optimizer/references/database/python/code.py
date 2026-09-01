import json
from dataclasses import asdict, dataclass
from time import perf_counter


@dataclass(frozen=True)
class Order:
  user_id: str
  total: int


@dataclass
class QueryStats:
  query_count: int = 0
  rows_returned: int = 0
  bytes_returned: int = 0
  elapsed_ms: float = 0.0


class FakeDb:
  def __init__(self, orders: list[Order]) -> None:
    self.orders = orders
    self.stats = QueryStats()

  def reset(self) -> None:
    self.stats = QueryStats()

  def snapshot(self) -> QueryStats:
    return QueryStats(
      query_count=self.stats.query_count,
      rows_returned=self.stats.rows_returned,
      bytes_returned=self.stats.bytes_returned,
      elapsed_ms=self.stats.elapsed_ms,
    )

  def read_orders_for_user(self, user_id: str) -> list[Order]:
    return self._record(
      [order for order in self.orders if order.user_id == user_id]
    )

  def read_orders_for_users(self, user_ids: list[str]) -> list[Order]:
    allowed = set(user_ids)
    return self._record(
      [order for order in self.orders if order.user_id in allowed]
    )

  def _record(self, rows: list[Order]) -> list[Order]:
    start = perf_counter()
    result = [Order(user_id=row.user_id, total=row.total) for row in rows]
    payload = json.dumps([asdict(row) for row in result])
    self.stats.query_count += 1
    self.stats.rows_returned += len(result)
    self.stats.bytes_returned += len(payload.encode("utf-8"))
    self.stats.elapsed_ms += (perf_counter() - start) * 1000
    return result


def totals_bad(db: FakeDb, user_ids: list[str]) -> dict[str, int]:
  totals: dict[str, int] = {}
  for user_id in user_ids:
    orders = db.read_orders_for_user(user_id)
    totals[user_id] = sum(order.total for order in orders)
  return totals


def totals_good(db: FakeDb, user_ids: list[str]) -> dict[str, int]:
  totals = {user_id: 0 for user_id in user_ids}
  for order in db.read_orders_for_users(user_ids):
    totals[order.user_id] += order.total
  return totals
