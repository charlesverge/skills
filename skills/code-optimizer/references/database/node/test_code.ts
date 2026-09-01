import { FakeDb, totalsBad, totalsGood, type Order, type QueryStats } from "./code.ts";

type Sample = QueryStats & {
  label: string;
  result: Array<[string, number]>;
};

function buildOrders(
  userCount: number,
  ordersPerUser: number,
): { userIds: string[]; orders: Order[] } {
  const userIds: string[] = [];
  const orders: Order[] = [];
  for (let userIndex = 0; userIndex < userCount; userIndex += 1) {
    const userId = `user-${userIndex}`;
    userIds.push(userId);
    for (let orderIndex = 0; orderIndex < ordersPerUser; orderIndex += 1) {
      orders.push({
        userId,
        total: (orderIndex % 5) + 1,
      });
    }
  }
  return { userIds, orders };
}

function measure(
  label: string,
  work: (db: FakeDb, userIds: string[]) => Map<string, number>,
  db: FakeDb,
  userIds: string[],
): Sample {
  db.reset();
  const result = work(db, userIds);
  return {
    label,
    result: Array.from(result.entries()),
    ...db.snapshot(),
  };
}

const { userIds, orders } = buildOrders(200, 12);
const db = new FakeDb(orders);
const bad = measure("totalsBad", totalsBad, db, userIds);
const good = measure("totalsGood", totalsGood, db, userIds);

if (JSON.stringify(bad.result) !== JSON.stringify(good.result)) {
  throw new Error("Database example results do not match");
}

console.table([
  {
    label: bad.label,
    queryCount: bad.queryCount,
    rowsReturned: bad.rowsReturned,
    bytesReturned: bad.bytesReturned,
    elapsedMs: bad.elapsedMs,
  },
  {
    label: good.label,
    queryCount: good.queryCount,
    rowsReturned: good.rowsReturned,
    bytesReturned: good.bytesReturned,
    elapsedMs: good.elapsedMs,
  },
]);
