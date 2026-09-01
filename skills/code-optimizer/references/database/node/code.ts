const encoder = new TextEncoder();

export type Order = {
  userId: string;
  total: number;
};

export type QueryStats = {
  queryCount: number;
  rowsReturned: number;
  bytesReturned: number;
  elapsedMs: number;
};

export class FakeDb {
  private readonly orders: Order[];
  private stats: QueryStats;

  constructor(orders: Order[]) {
    this.orders = orders;
    this.stats = {
      queryCount: 0,
      rowsReturned: 0,
      bytesReturned: 0,
      elapsedMs: 0,
    };
  }

  reset(): void {
    this.stats = {
      queryCount: 0,
      rowsReturned: 0,
      bytesReturned: 0,
      elapsedMs: 0,
    };
  }

  snapshot(): QueryStats {
    return { ...this.stats };
  }

  readOrdersForUser(userId: string): Order[] {
    return this.record(
      this.orders.filter((order) => order.userId === userId),
    );
  }

  readOrdersForUsers(userIds: string[]): Order[] {
    const allowed = new Set(userIds);
    return this.record(
      this.orders.filter((order) => allowed.has(order.userId)),
    );
  }

  private record(rows: Order[]): Order[] {
    const start = performance.now();
    const result = rows.map((row) => ({ ...row }));
    const payload = JSON.stringify(result);
    this.stats.queryCount += 1;
    this.stats.rowsReturned += result.length;
    this.stats.bytesReturned += encoder.encode(payload).length;
    this.stats.elapsedMs += performance.now() - start;
    return result;
  }
}

export function totalsBad(db: FakeDb, userIds: string[]): Map<string, number> {
  const totals = new Map<string, number>();
  for (const userId of userIds) {
    const orders = db.readOrdersForUser(userId);
    totals.set(
      userId,
      orders.reduce((total, order) => total + order.total, 0),
    );
  }
  return totals;
}

export function totalsGood(db: FakeDb, userIds: string[]): Map<string, number> {
  const totals = new Map<string, number>();
  for (const userId of userIds) {
    totals.set(userId, 0);
  }
  for (const order of db.readOrdersForUsers(userIds)) {
    totals.set(order.userId, (totals.get(order.userId) ?? 0) + order.total);
  }
  return totals;
}
