---
name: python-beanie-orm
description: Use Beanie ODM patterns for MongoDB async operations. Covers document models, queries, inserts, updates, deletions, indexing, and migrations with Pydantic integration.
---

# Python Beanie ORM

Use this skill when working with MongoDB in Python using the Beanie ODM (Object-Document Mapper).

## What is Beanie ODM?

[Beanie](https://github.com/roman-right/beanie) is an asynchronous Python ODM for MongoDB. Data models are based on [Pydantic](https://pydantic-docs.helpmanual.io/), allowing you to define schemas that validate data and serialize/deserialize automatically.

Each database collection has a corresponding `Document` class that is used to interact with that collection - retrieving, adding, updating, or deleting documents.

Beanie provides:
- Async operations via PyMongo's async client
- Pydantic-based schema validation
- Built-in schema migrations
- Query builder with Pythonic syntax
- Index management

## Installation

```shell
pip install beanie
# or
poetry add beanie
```

Optional dependencies:
- `beanie[srv]` - mongodb+srv:// URI support
- `beanie[aws]` - MONGODB-AWS authentication
- `beanie[gssapi]` - GSSAPI authentication
- `beanie[ocsp]` - OCSP support
- `beanie[snappy]` - Snappy compression
- `beanie[zstd]` - Zstandard compression
- `beanie[encryption]` - Client-Side Field Level Encryption

## Basic Usage

### Define a Document

```python
from typing import Optional
from pydantic import BaseModel
from beanie import Document, Indexed, init_beanie
from pymongo import AsyncMongoClient

class Category(BaseModel):
    name: str
    description: str

class Product(Document):
    name: str
    description: Optional[str] = None
    price: Indexed(float)  # Creates an index
    category: Category
```

### Initialize Beanie

```python
async def init_db():
    client = AsyncMongoClient("mongodb://user:pass@host:27017")
    await init_beanie(database=client.db_name, document_models=[Product])
```

### CRUD Operations

```python
# Insert
chocolate = Category(name="Chocolate", description="Cacao")
product = Product(name="Tony's", price=5.95, category=chocolate)
await product.insert()

# Find one
product = await Product.find_one(Product.price < 10)

# Find many
products = await Product.find(Product.category.name == "Chocolate").to_list()

# Update
await product.set({Product.name: "Gold bar"})
# Or update directly
product.name = "Gold bar"
await product.save()

# Delete
await product.delete()
```

## Documentation

Full documentation is available at: `skills/python-beanie-orm/resources/docs/`

Key docs:
- [index.md](resources/docs/index.md) - Overview and links
- [getting-started.md](resources/docs/getting-started.md) - Installation and initialization
- [development.md](resources/docs/development.md) - Contributing guidelines

Official docs: https://beanie-odm.dev/