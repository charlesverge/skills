---
name: needless-helper-decisions
description: Use this rubric and example set for future needless helper decisions. Use when creating, reviewing or refactoring helper methods to decide whether to keep phase-boundary logic helpers or inline thin pass-through wrappers while preserving behavior, side effects, exception semantics, and logging.
---

## Rules

1. Keep a helper when it represents a real phase with multiple steps, branching, or reusable domain logic.
2. Remove a helper when it is single-use, same-file, and only does a pass-through dependency call (optionally plus logging).
3. Remove or inline near-duplicate helpers that differ only by exception type or message text.
4. Keep behavior identical when inlining: same side effects, return values, error semantics, and log levels/messages.
5. Prefer readability at the call site for exception handling; inline thin exception-only wrappers.
6. If tests fail due to harness/setup (fixtures/env), stop reshaping and report blocker.

## Generic Example: Helper to Remove

```python
class Worker:
  async def process(self, task_id: str) -> None:
    try:
      await self._run(task_id)
    except TimeoutError as exc:
      await self._handle_timeout(task_id, exc)

  async def _handle_timeout(self, task_id: str, error: TimeoutError) -> None:
    await self.queue.requeue(task_id, delay_seconds=60, reason=str(error))
    logger.warning(f"task_id={task_id} timeout retry=60")
```

Why remove:
- Single call site.
- Pass-through queue call + log.
- No transformation or reusable phase logic.

Inline target:

```python
class Worker:
  async def process(self, task_id: str) -> None:
    try:
      await self._run(task_id)
    except TimeoutError as exc:
      await self.queue.requeue(task_id, delay_seconds=60, reason=str(exc))
      logger.warning(f"task_id={task_id} timeout retry=60")
```

## Generic Example: Helper to Keep

```python
class Worker:
  async def process(self, task_id: str, payload: dict[str, str]) -> None:
    should_stop = await self._pre_checks(task_id, payload)
    if should_stop:
      return
    await self._run(task_id, payload)

  async def _pre_checks(self, task_id: str, payload: dict[str, str]) -> bool:
    url = payload["url"]
    if not self.url_validator.is_allowed(url):
      await self.queue.fail(task_id, reason="url_denied", temporary=False)
      logger.error(f"task_id={task_id} denied_url=True")
      return True

    domain = self.extract_domain(url)
    if await self.domain_tracker.is_blocked(domain):
      await self.queue.block(task_id, reason="domain_blocked")
      logger.info(f"task_id={task_id} domain={domain} blocked=True")
      return True

    retry_on = await self.domain_tracker.temporary_until(domain)
    if retry_on is not None:
      await self.queue.requeue_at(task_id, retry_on=retry_on, reason="temporary_block")
      logger.info(f"task_id={task_id} domain={domain} retry_on={retry_on.isoformat()}")
      return True

    return False
```

Why keep:
- Multi-step phase boundary (`collect/validate/decision/side effects`).
- Contains branching and multiple outcomes.
- Improves readability and reuse potential, not a pass-through wrapper.
