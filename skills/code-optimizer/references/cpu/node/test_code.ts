import { rankBad, rankGood, type RecordItem } from "./code.ts";

type CpuUsage = {
  user: number;
  system: number;
};

declare const process: {
  cpuUsage(start?: CpuUsage): CpuUsage;
};

type Sample = {
  elapsedMs: number;
  userCpuMs: number;
  systemCpuMs: number;
};

function buildRecords(count: number): RecordItem[] {
  const records: RecordItem[] = [];
  for (let index = 0; index < count; index += 1) {
    records.push({
      name: `record-${index}-aeiou-${index % 17}`,
      score: (index % 7) + 1,
    });
  }
  return records;
}

function measure(run: () => number): Sample {
  const startCpu = process.cpuUsage();
  const start = performance.now();
  run();
  const elapsedMs = performance.now() - start;
  const cpu = process.cpuUsage(startCpu);
  return {
    elapsedMs,
    userCpuMs: cpu.user / 1000,
    systemCpuMs: cpu.system / 1000,
  };
}

function median(values: number[]): number {
  const ordered = [...values].sort((left, right) => left - right);
  const middle = Math.floor(ordered.length / 2);
  if (ordered.length % 2 === 0) {
    return (ordered[middle - 1] + ordered[middle]) / 2;
  }
  return ordered[middle];
}

function benchmark(label: string, run: () => number): void {
  for (let index = 0; index < 5; index += 1) {
    run();
  }
  const samples: Sample[] = [];
  for (let index = 0; index < 25; index += 1) {
    samples.push(measure(run));
  }
  console.log(label, {
    medianElapsedMs: median(samples.map((sample) => sample.elapsedMs)),
    medianUserCpuMs: median(samples.map((sample) => sample.userCpuMs)),
    medianSystemCpuMs: median(samples.map((sample) => sample.systemCpuMs)),
  });
}

const records = buildRecords(1500);
const badResult = rankBad(records);
const goodResult = rankGood(records);

if (badResult !== goodResult) {
  throw new Error(`Result mismatch: ${badResult} !== ${goodResult}`);
}

benchmark("rankBad", () => rankBad(records));
benchmark("rankGood", () => rankGood(records));
