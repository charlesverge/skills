import re
from dataclasses import dataclass


@dataclass(frozen=True)
class RecordItem:
  name: str
  score: int


def rank_bad(records: list[RecordItem]) -> int:
  total = 0
  for record in records:
    pattern = re.compile(r"[aeiou]", re.IGNORECASE)
    total += len(pattern.findall(record.name)) * record.score
    ordered = sorted(records, key=lambda entry: entry.name)
    total += ordered[0].score if ordered else 0
  return total


def rank_good(records: list[RecordItem]) -> int:
  pattern = re.compile(r"[aeiou]", re.IGNORECASE)
  ordered = sorted(records, key=lambda entry: entry.name)
  first = ordered[0].score if ordered else 0
  total = 0
  for record in records:
    total += len(pattern.findall(record.name)) * record.score
    total += first
  return total
