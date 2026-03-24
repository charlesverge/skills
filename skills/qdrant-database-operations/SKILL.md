---
name: qdrant-database-operations
description: Use Qdrant Python client patterns for common collection operations including insert, upsert, delete, and retrieval with clear payload type expectations.
metadata:
  short-description: Qdrant CRUD operation patterns
---

# Qdrant Database Operations

Use this skill when implementing or reviewing Qdrant vector collection write/read logic with the Python client.

Official docs: https://python-client.qdrant.tech/

## Quick setup

```python
from datetime import datetime, timezone
from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333")
collection_name = "documents"
```

## 1) Insert

`insert` is commonly used for adding new points when you are not explicitly handling existing ids.

```python
points = [
    models.PointStruct(
        id=1,  # int | str | UUID
        vector=[0.12, 0.34, 0.56],  # list[float]
        payload={
            "source": "support_ticket",   # str
            "priority": 2,                # int
            "score": 0.98,                # float
            "is_open": True,              # bool
            "tags": ["billing", "vip"],   # list[str]
        },
    )
]

client.insert(collection_name=collection_name, points=points)
```

Types sent:
- `id`: `int | str | UUID`
- `vector`: `list[float]`
- `payload`: JSON-like values (`str`, `int`, `float`, `bool`, `list`, `dict`, `None`)

## 2) Upsert

`upsert` inserts a new point if `id` does not exist, or updates it if it does.

```python
created_at_dt = datetime.now(timezone.utc)

client.upsert(
    collection_name=collection_name,
    points=[
        models.PointStruct(
            id=1,
            vector=[0.10, 0.20, 0.30],
            payload={
                "title": "Reset password flow",
                "created_at": created_at_dt,  # Python datetime sent
            },
        )
    ],
)
```

Important payload typing note:
- Sending `datetime` in payload is accepted by the Python client.
- Retrieving that payload returns an RFC3339 timestamp `str`, not a Python `datetime`.
- Example returned value: `'2026-03-24T12:21:10.136767Z'`

## 3) Delete

Delete by point id:

```python
client.delete(
    collection_name=collection_name,
    points_selector=models.PointIdsList(
        points=[1, 2, 3],  # list[int | str | UUID]
    ),
)
```

Delete by filter:

```python
client.delete(
    collection_name=collection_name,
    points_selector=models.FilterSelector(
        filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="source",
                    match=models.MatchValue(value="support_ticket"),
                )
            ]
        )
    ),
)
```

## 4) Retrieval

Retrieve known ids:

```python
records = client.retrieve(
    collection_name=collection_name,
    ids=[1],
    with_payload=True,
    with_vectors=False,
)

point = records[0]
created_at_raw = point.payload.get("created_at")
print(type(created_at_raw), created_at_raw)
# <class 'str'> 2026-03-24T12:21:10.136767Z
```

Types retrieved:
- `records`: `list[models.Record]`
- `record.id`: `int | str | UUID`
- `record.vector`: `list[float] | dict[str, list[float]] | None` (depends on vector config and `with_vectors`)
- `record.payload`: `dict[str, Any] | None`
- Datetime payload values are returned as `str` (RFC3339), not `datetime`

## Conversion pattern for datetime fields

```python
from datetime import datetime

created_at_str = point.payload["created_at"]
created_at_dt = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
```

Use this conversion when your application expects a Python `datetime` after retrieval.
