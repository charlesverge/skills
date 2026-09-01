export type Row = {
  id: number;
  payload: string;
};

export function summarizeBad(rows: Row[]): number {
  const copied = rows.map((row) => ({
    id: row.id,
    tokens: row.payload.split(",").map((part) => part.trim().toLowerCase()),
  }));
  const flattened = copied.flatMap((row) => row.tokens);
  const filtered = flattened.filter((token) => token.length > 3);
  return filtered.length;
}

export function summarizeGood(rows: Row[]): number {
  let total = 0;
  for (const row of rows) {
    for (const part of row.payload.split(",")) {
      const token = part.trim().toLowerCase();
      if (token.length > 3) {
        total += 1;
      }
    }
  }
  return total;
}
