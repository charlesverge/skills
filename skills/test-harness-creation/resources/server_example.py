from __future__ import annotations

import random

from fastapi import FastAPI, HTTPException

app = FastAPI(title="Server Example", version="1.0.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/random")
def random_number(n: int) -> dict[str, int]:
    if n < 1:
        raise HTTPException(status_code=400, detail="n must be >= 1")
    value = random.randint(1, n)
    return {"value": value, "max": n}


@app.get("/add")
def add(a: int, b: int) -> dict[str, int]:
    return {"result": a + b}
