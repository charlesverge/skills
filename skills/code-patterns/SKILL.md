---
name: code-patterns
description: Enforce Python and Beanie code patterns that avoid unsafe defaults, inline imports, unnecessary comments/checks, manual model wiring, and non-streaming cursor usage. Use when writing or reviewing repository/service code for consistency and performance.
metadata:
  short-description: Enforce preferred code patterns
---

# Code patterns

## Patterns to avoid

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

- Don't create a fall back unless explicitly asked for
- Avoid the use of built in functions like attrib, hasattr for classes which can accessed like ClassName.property_name
- If a reference is already a str don't add str() to it.

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

## Prefer model_validate over manual model creation

Instead of listing every field when creating a beanie model from a dict, use model_validate

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

## Prefer model_validate over manual model creation

Instead of listing every field when creating a beanie model from a dict, use model_validate

## Assert usage

assert usage should be kept for unit tests
