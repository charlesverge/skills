from dataclasses import dataclass


@dataclass(frozen=True)
class Row:
  id: int
  payload: str


def summarize_bad(rows: list[Row]) -> int:
  copied = [
    {
      "id": row.id,
      "tokens": [part.strip().lower() for part in row.payload.split(",")],
    }
    for row in rows
  ]
  flattened = [token for row in copied for token in row["tokens"]]
  filtered = [token for token in flattened if len(token) > 3]
  return len(filtered)


def summarize_good(rows: list[Row]) -> int:
  total = 0
  for row in rows:
    for part in row.payload.split(","):
      token = part.strip().lower()
      if len(token) > 3:
        total += 1
  return total
