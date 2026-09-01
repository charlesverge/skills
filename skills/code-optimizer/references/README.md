# Code Optimizer Resources

This directory contains executable resource examples for CPU, database, and memory testing in Node and TypeScript and in Python.

## How to use

Run the sample command for the resource you want to inspect from the repository root.

## CPU

### Node and TypeScript

- Reference: [Node CPU example](cpu/node/README.md)

```bash
cd skills/code-optimizer/resources/cpu/node && node --experimental-strip-types test_code.ts
```

### Python

- Reference: [Python CPU example](cpu/python/README.md)

```bash
cd skills/code-optimizer/resources/cpu/python && python3 test_code.py
```

## Database

### Node and TypeScript

- Reference: [Node database example](database/node/README.md)

```bash
cd skills/code-optimizer/resources/database/node && node --experimental-strip-types test_code.ts
```

### Python

- Reference: [Python database example](database/python/README.md)

```bash
cd skills/code-optimizer/resources/database/python && python3 test_code.py
```

## Memory

### Node and TypeScript

- Reference: [Node memory example](memory/node/README.md)

```bash
cd skills/code-optimizer/resources/memory/node && node --experimental-strip-types --expose-gc test_code.ts
```

### Python

- Reference: [Python memory example](memory/python/README.md)

```bash
cd skills/code-optimizer/resources/memory/python && python3 test_code.py
```

## Directory layout

- `cpu/node/` - CPU example for Node and TypeScript
- `cpu/python/` - CPU example for Python
- `database/node/` - Database example for Node and TypeScript
- `database/python/` - Database example for Python
- `memory/node/` - Memory example for Node and TypeScript
- `memory/python/` - Memory example for Python
