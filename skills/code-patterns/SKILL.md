---
name: code-patterns
description: Python coding patterns for preferred styles, use when making code changes or refactors to ensure code change is in line with preferred patterns.
metadata:
  short-description: Enforce preferred code patterns
---

# Code patterns

## When to use this skill

When making any code change, check that the change matches the preferred pattern. If not stop and ask for approval.

## Preferred patterns

# CODE PATTERNS

This document captures accepted Python coding patterns for this repository. It is intentionally concise and practical: use classes for stage/repository logic, prefer strongly typed function signatures, and keep control flow explicit and readable.

## `if / else`

* Use explicit condition checks.
* Prefer early return to avoid deep nesting.
* Keep each branch small and clear.

Example:

```python
if task is None:
    logger.debug("No pending task available")
    return None

if queue_name in ("page_fetch", "page_triage"):
    sort_fields = [
        ("next_retry_on", SortDirection.ASCENDING),
        ("payload.url_score", SortDirection.ASCENDING),
        ("created_on", SortDirection.ASCENDING),
    ]
else:
    sort_fields = ["created_on"]
```

* Use `elif` when a second condition is mutually exclusive.
* Use `else` only when there is a clear default.
* Avoid complex boolean expressions in one line; split them into named intermediate variables when helpful.

## `for` loops

* Use `for item in iterable:` for iteration.
* Prefer list comprehensions for simple transforms.
* Use explicit value checks inside loops when needed.

Example:

```python
results: list[str] = []
for url in candidate_urls:
    if not is_denied_url(url):
        results.append(url)
```

* Use `enumerate()` when the index is required.
* Avoid iterating over indexes manually unless you need numeric control.

## `while` loops

* Use `while` only when repeated execution depends on a changing condition rather than a fixed collection.
* Keep the loop condition simple.
* Update loop state clearly inside the body.
* Avoid unbounded `while True` loops.

Example:

```python
while len(frontier_task_ids) > 0:
    child_task_ids: list[PydanticObjectId] = []
    for task_id in frontier_task_ids:
        child_task_ids.extend(await self._find_child_task_ids(task_id))
    frontier_task_ids = child_task_ids
```

* Avoid infinite loops without an obvious break condition.
* Prefer queue deques or generator-based iteration when possible.

## `BaseModel` class usage

* Use `pydantic.BaseModel` for task payloads and structured inputs.
* Define payload classes in `src/worker/integrations/company_research/types.py` or suitable shared modules.
* When parsing agent output, accept both `BaseModel` values and raw data safely.

Example:

```python
class EnqueueTaskRequest(BaseModel):
    key: str
    stage: DiscoveryStage
    parent_trace_id: PydanticObjectId | None = None
    payload: DiscoveryTaskPayload
```

* Keep model fields explicit with types.
* Use `model_dump(mode="python")` to serialize models for storage or output.
* Use `isinstance(result, BaseModel)` when you need to support both model and plain data inputs.

## Strong typing for function parameters and return values

* Always annotate function parameters and return types.
* Use Python 3.10-style unions: `str | None`, `list[str]`, `dict[str, object]`.
* Prefer concrete, descriptive types over `Any`.

Example:

```python
async def claim_task(self, stage: DiscoveryStage) -> dict[str, object] | None:
    ...

async def get_keys(
    self,
    queue_name: DiscoveryStage,
    task_keys: list[str],
) -> set[str]:
    ...
```

* For `BaseModel` subclasses and domain objects, use the actual class name.
* Use `PydanticObjectId` for MongoDB object ids, and `datetime` for timestamps.

## Using classes

* Prefer classes for stage behavior, repository access, and reusable helpers.
* Use `__init__` to inject dependencies and configuration.
* Keep methods focused on a single responsibility.

Example:

```python
class DiscoveryQueueRepository:
    def __init__(
        self,
        now_provider: Callable[[], datetime] | None = None,
        max_attempts: int = 3,
    ) -> None:
        self.now_provider = now_provider
        self.max_attempts = max_attempts
```

* Use private helper methods for repeated logic, e.g. `_now()`, `_get_stage()`, `_apply_completed_fields()`.
* Keep public methods stable and testable; use private methods to reduce duplication.
* Prefer small, single-purpose classes over large procedural modules.

## Array handling

* Use extend to add multiple items to a list instead of append in a loop.

Prefer this pattern

```python
           candidate.locations.extend(new_locations)
```

This should not be done

```python
            for location_source in new_locations:
                candidate.locations.append(location_source)
```

## Practical style reminders

* Prefer clear variable names: `task`, `stage`, `task_id`, `candidate_urls`.
* Use `logger` for runtime events, not `print()`.
* Avoid deep nesting by returning early when invalid state is detected.
* Use explicit `None` checks instead of relying on truthy/falsy semantics for optional values.

Example:

```python
if task_document is not None:
    key_value = task_document.get("key")
    if isinstance(key_value, str):
        existing_keys.add(key_value)
```

## Patterns to avoid

### Don't use tuples unless absolutely necessary

Use a class with property names instead of a tuple. For example:

```python
class LocationSource(BaseModel):
    source_type: str
    source_id: str
    location: Location
```

### Don't use this pattern when class has a defined property.

This should not be done

```python
  url = self.random_class.property_name if self.random_class.property_name else ""
  if not random_class:
    return 0
```

Simplify to

```python
  if not random_class.property_name:
     return 0
```

### Don't inline imports

This should not be done

```python
  async def function_name(self) -> int:
    from app.module_name import another_function
```

Instead place the import at the top of the file. If this causes a circular reference raise to the user architect a better solution. If it is a function you have created place it in a helper file if it is a simple helper.

### Don't add comments unless specifically asked for

This should not be done

```python
    # `Job.url` is required on the model; access it directly.
    url = self.job.property_name_1
```

Should be without the comment.

```python
    url = self.job.property_name_1
```

### For beanie classes use the insert, save for insert and updates

This should not be done.

```python
  await BeanieClass.get_pymongo_collection().update_one({"_id": data_object.id}, {"$set": {"property_name": value}})
```

Should be

```python
  data_object.property_name = value
  await data_object.save()
```

### Use cursors properly and stream records

This should not be done.

```python
cursor = BeanieClass.find(query)
if limit is not None and limit > 0:
  jobs = await cursor.limit(limit).to_list()
else:
  jobs = await cursor.to_list()
```

This pattern loads all records into memory which can cause performance issues and crashes. Instead use a cursor and stream records.

```python
      cursor = await collection.aggregate(pipeline)
      items = [doc async for doc in cursor]
    except Exception as e:
      logger.error(f"{prefix}: company_id={company_id} > Failed to run aggregation: {e}")
      return 0

    total_indexed = 0
    try:
      for item in items:
```

Should be

```python
cursor = BeanieClass.find(query).limit(limit)
async for result in cursor:
  # do something with result.
```

## Function creation

* Don't create a fall back unless explicitly asked for
* Avoid the use of built in functions like attrib, hasattr for classes which can accessed like ClassName.property\_name
* If a reference is already a str don't add str() to it.

## Beanie classes

### No unneeded checks for .id after a find

Checking if .id exists or not after a find is not needed. A find will always return an id

```ptyhon
cursor = Company.find_all()
async for company in cursor:
  company_id = company.id
  if not company_id:
    logger.warning(f"{prefix}: skipping company without id: {company.company_name}")
    continue
```

No check is needed, no assert.

```python
cursor = Company.find_all()
async for company in cursor:
  company_id = company.id
```

## Avoid needless if statements

If a parameter can accept a None value, then don't create an if statement to check if the parameter is None before using it. Instead, use the parameter directly and let it raise an error if it is None when it shouldn't be. Unless, the if condition is needed to handle a specific case or additional logic. For example, invalid combinations of parameters or additional actions are needed to be completed.

```python
def do_foo_function(
    param1: int,
    param2: NamedClass | None = None,
    param3: OtherClass | None = None,
) -> int:
   pass

  if param2 is None:
      result = do_foo_function(
          param1=param1, param3=param3
      )
  else:
      self.model = do_foo_function(
          param1=param1, param2=param2, param3=param3
      )
```

Simplify to

```python
    self.model = do_foo_function(
        param1=param1, param2=param2, param3=param3
    )
```

## Prefer model\_validate over manual model creation

Instead of listing every field when creating a beanie model from a dict, use model\_validate

## Assert usage

assert usage should be kept for unit tests

### Prefer guard clauses to end code paths early

This should not be done.

```python
async def process_record(self, record_id: str, key: str) -> None:
  await self.repo.update_flag(record_id, "needs_follow_up", True)
  if key:
    await self.tracker.record_result(key, success=False)
```

Should be.

```python
async def process_record(self, record_id: str, key: str) -> None:
  await self.repo.update_flag(record_id, "needs_follow_up", True)
  if not key:
    return
  await self.tracker.record_result(key, success=False)
```

## Beanie classes

### No unneeded checks for .id after a find

Checking if .id exists or not after a find is not needed. A find will always return an id

```ptyhon
cursor = Company.find_all()
async for company in cursor:
  company_id = company.id
  if not company_id:
    logger.warning(f"{prefix}: skipping company without id: {company.company_name}")
    continue
```

No check is needed, no assert.

```python
cursor = Company.find_all()
async for company in cursor:
  company_id = company.id
```

## Prefer model\_validate over manual model creation

Instead of listing every field when creating a beanie model from a dict, use model\_validate

## Assert usage

assert usage should be kept for unit tests

## Batch key-indexed ID cache pattern.

### Use it when:

* ID is discovered in one phase but applied in a later, separate phase.
* Re-querying is expensive, flaky, or unavailable later.
* There is no direct per-record channel to carry the ID forward.
* The correlation key is stable and unique for that pipeline step.

### Do not use it when:

* ID is already available at the point of write/process.
* ID can be passed directly in function args/event payload/result object.
* A cache introduces avoidable state, staleness, or key-mismatch risk.
* The phase boundary is weak (same call path, same scope) and no decoupling benefit exists.

### Rule of thumb:

* Prefer direct propagation first.
* Use key-indexed ID cache only to bridge a real phase boundary where direct propagation is not practical.

### Generic description:

* Build an in-memory dictionary keyed by batch artifact (file/job/message id), with value = all related IDs needed later.
* Reuse that dictionary during downstream processing to avoid re-querying or recomputing IDs.

\###Generic example:

```python
ids_by_file = {
  "batch_a.jsonl": {"worker_id": "...", "org_id": "...", "run_id": "..."},
  "batch_b.jsonl": {"worker_id": "...", "org_id": "...", "run_id": "..."},
}
ctx = ids_by_file.get(file_name)
```

### Future phrasing:

* “Use a key-indexed ID cache: store all IDs per file in a dict, then look them up during import/persist.”
