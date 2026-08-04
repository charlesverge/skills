# Development Setup Pattern

## Policy

A fresh clone must be easy to start without creating configuration files,
copying templates, exporting variables, or following a long setup checklist.

- Do not commit `.env`, `.env.*`, `.env.local`, `.env.example`, or any other
  `.env*` file.
- Ignore `.env*` files so developer-specific values and secrets cannot be
  committed accidentally.
- Keep safe development configuration in application code or a tracked,
  typed configuration file with a name such as `config/development.json`.
- Keep production configuration explicit. Missing required production secrets
  or endpoints must stop startup with a clear error.
- Provide one documented development command that starts the application and
  every required local service.
- Use `docker-compose.yml` for databases, queues, caches, and similar local
  dependencies when containers simplify setup.
- The development command must start Compose services automatically and wait
  until their health checks pass before starting the application.
- Do not require developers to run `docker compose up` separately.
- Keep the startup path deterministic. Do not hide failed dependency startup,
  missing tools, invalid configuration, or unhealthy containers.

Secrets required for shared or hosted systems must come from the approved
secret manager or deployment platform. Local development should use safe local
credentials owned by Compose whenever possible.

## npm application pattern

After the standard package-manager install, `npm run dev` is the only startup
command a developer needs.

```json
{
  "scripts": {
    "predev": "docker compose up -d --wait",
    "dev": "next dev"
  }
}
```

`docker-compose.yml` owns the local dependency topology and health check:

```yaml
services:
  mongo:
    image: mongo:8
    ports:
      - "29099:27017"
    healthcheck:
      test: ["CMD", "mongosh", "--quiet", "--eval", "db.adminCommand('ping')"]
      interval: 1s
      timeout: 3s
      retries: 30
    volumes:
      - mongo-data:/data/db

volumes:
  mongo-data:
```

The application owns an explicit development configuration for the Compose
endpoint. It does not obtain that endpoint from a committed `.env*` file.

```ts
const DEVELOPMENT_MONGO_URI =
  "mongodb://127.0.0.1:29099/?directConnection=true&retryWrites=false";

export function mongoUri(): string {
  if (process.env.NODE_ENV === "development") {
    return DEVELOPMENT_MONGO_URI;
  }

  const uri = process.env.MONGODB_URI;
  if (uri === undefined) {
    throw new Error("MONGODB_URI is required");
  }
  return uri;
}
```

This gives development and deployment separate, visible contracts:

- Development uses the repository-owned Compose endpoint.
- Test and production require configuration from their runner or deployment
  platform.
- A missing production value is an error, not a local-development connection.

If startup requires more orchestration than `docker compose up -d --wait`, keep
`package.json` small and call a checked-in script:

```json
{
  "scripts": {
    "predev": "tsx scripts/start-development.ts",
    "dev": "next dev"
  }
}
```

The script should start Compose, wait for health, report failures, and exit with
a nonzero status when a dependency cannot become ready. It must not write an
`.env*` file or mutate the developer's shell environment.

## Generic application pattern

Every application should expose one conventional development entry point, such
as `./scripts/dev`, `make dev`, or the ecosystem's standard equivalent. The
README should make that command the primary startup path.

The command performs these steps in order:

1. Verify required local tools and locked application dependencies.
1. Start required services with `docker compose up -d --wait`.
1. Stop immediately if a service is unhealthy or a required tool is missing.
1. Start the application through its native development server.

Example project-owned command:

```sh
#!/bin/sh
set -eu

docker compose up -d --wait
exec application-runtime dev
```

The application configuration follows the same mode contract regardless of
language or framework:

```text
if mode is development:
  use the tracked local configuration that matches docker-compose.yml
otherwise:
  require configuration from the deployment or test environment
  stop startup when a required value is missing
```

The tracked development configuration may live in typed application settings
or a conventional non-secret file such as `config/development.toml`. It must
not live in a `.env*` file.

## Review checklist

- Can a developer start the complete local application with one documented
  command after installing the project's standard toolchain?
- Does that command start and wait for every required Compose service?
- Are safe local endpoints repository-owned and immediately usable?
- Are all `.env*` files ignored and absent from tracked files?
- Are production and test requirements explicit and independent from local
  development configuration?
- Does startup fail visibly when tooling, configuration, or a dependency is
  unavailable?
