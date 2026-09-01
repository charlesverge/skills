export type RecordItem = {
  name: string;
  score: number;
};

function countVowels(text: string, pattern: RegExp): number {
  pattern.lastIndex = 0;
  return text.match(pattern)?.length ?? 0;
}

export function rankBad(records: RecordItem[]): number {
  let total = 0;
  for (const record of records) {
    const pattern = /[aeiou]/gi;
    total += countVowels(record.name, pattern) * record.score;
    const ordered = [...records].sort((left, right) =>
      left.name.localeCompare(right.name),
    );
    total += ordered[0]?.score ?? 0;
  }
  return total;
}

export function rankGood(records: RecordItem[]): number {
  const pattern = /[aeiou]/gi;
  const ordered = [...records].sort((left, right) =>
    left.name.localeCompare(right.name),
  );
  const first = ordered[0]?.score ?? 0;
  let total = 0;
  for (const record of records) {
    total += countVowels(record.name, pattern) * record.score;
    total += first;
  }
  return total;
}
