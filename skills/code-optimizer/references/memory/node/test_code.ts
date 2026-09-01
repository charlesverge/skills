import { summarizeBad, summarizeGood, type Row } from "./code.ts";

type MemoryUsage = {
  heapUsed: number;
  rss: number;
};

declare const process: {
  memoryUsage(): MemoryUsage;
};

type Sample = {
  elapsedMs: number;
  heapDeltaBytes: number;
  rssBytes: number;
  result: number;
};

function buildRows(count: number, width: number): Row[] {
  const rows: Row[] = [];
  const payload = Array.from(
    { length: width },
    (_, index) => `value-${index}-token`,
  ).join(",");
  for (let index = 0; index < count; index += 1) {
    rows.push({ id: index, payload });
  }
  return rows;
}

function collect(): void {
  const runtime = globalThis as { gc?: () => void };
  runtime.gc?.();
}

function measure(run: () => number): Sample {
  collect();
  const startHeap = process.memoryUsage().heapUsed;
  const start = performance.now();
  const result = run();
  const elapsedMs = performance.now() - start;
  const endMemory = process.memoryUsage();
  return {
    elapsedMs,
    heapDeltaBytes: endMemory.heapUsed - startHeap,
    rssBytes: endMemory.rss,
    result,
  };
}

const rows = buildRows(4000, 25);
const bad = measure(() => summarizeBad(rows));
const good = measure(() => summarizeGood(rows));

if (bad.result !== good.result) {
  throw new Error(`Result mismatch: ${bad.result} !== ${good.result}`);
}

console.table([
  {
    label: "summarizeBad",
    elapsedMs: bad.elapsedMs,
    heapDeltaBytes: bad.heapDeltaBytes,
    rssBytes: bad.rssBytes,
  },
  {
    label: "summarizeGood",
    elapsedMs: good.elapsedMs,
    heapDeltaBytes: good.heapDeltaBytes,
    rssBytes: good.rssBytes,
  },
]);
