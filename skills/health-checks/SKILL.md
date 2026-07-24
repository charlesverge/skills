---
name: health-checks
description: Create or review health checks for services, containers, container-to-container dependencies, and external APIs. Use when verifying that a service is not only running but reachable from the right network boundary, returning expected data, and internally connected to required dependencies such as databases, Redis, queues, or downstream services.
---

# Health Checks

Use this skill when defining, implementing, or reviewing service health checks.

The goal is not "process exists" or "port is open." The goal is to prove the service is:

- Running.
- Reachable from the expected boundary.
- Returning the expected response shape or sentinel data.
- Internally healthy with all required dependencies connected.

## Core rules

- Separate liveness from readiness.
- Validate from every relevant boundary, not just one location.
- Prefer dedicated health endpoints over probing business endpoints.
- Verify expected payload content, not only HTTP status code.
- Fail with specific reasons so the broken dependency is obvious.
- Keep health checks cheap, deterministic, and safe to run frequently.

## Health check levels

Every service should be checked at multiple levels when applicable:

- Process/container level: the process is running and the container is alive.
- Local service level: the service responds correctly inside its own runtime environment.
- Network level: DNS, routing, and port reachability work from the caller boundary.
- Dependency level: required internal dependencies are connected and usable.
- Contract level: the returned response shape and sentinel values match expectations.

Do not treat one passing level as proof that the others are healthy.

## Ideal endpoint design

Prefer dedicated endpoints such as:

- `/health/live`: returns success when the process can serve requests.
- `/health/ready`: returns success only when the service can do useful work now.
- `/health`: optional aggregated endpoint for operators and diagnostics.

### What `/health/live` should test

- The app process is initialized.
- The request pipeline can return a response.

`/health/live` should not fail because a downstream dependency is temporarily unavailable unless the service is completely unable to function without it even for startup.

### What `/health/ready` should test

- Required database connection is active and a trivial query succeeds.
- Required Redis connection is active and a ping or simple get/set succeeds.
- Required queue, broker, cache, storage, or internal HTTP dependencies are reachable.
- Required migrations or startup initialization completed.
- The service can return a known-good response through its real runtime path.

If the service depends on another service to satisfy normal traffic, `/health/ready` must fail when that dependency is unavailable or returns invalid data.

### What `/health` should return

Return a machine-readable payload. Keep it stable and explicit.

Example shape:

```json
{
  "status": "ok",
  "service": "billing-api",
  "version": "1.2.3",
  "timestamp": "2026-04-22T12:00:00Z",
  "checks": {
    "database": {
      "status": "ok",
      "latency_ms": 4
    },
    "redis": {
      "status": "ok",
      "latency_ms": 2
    },
    "downstream_customer_api": {
      "status": "ok",
      "latency_ms": 18
    }
  }
}
```

Required characteristics:

- Top-level status is derived from required checks.
- Each dependency reports its own status.
- Include latency where practical.
- Include enough detail to identify the failing subsystem.
- Do not expose secrets or sensitive config values.

## Containerized service checks

For a service running in a container, checks must be done both inside and outside the container.
When a command is run in the container the execution command should be logged, preferring a logging.info or a print command to the console.

### Inside the container

Verify:

- The service process is running.
- The service listens on the expected interface and port.
- The dedicated health endpoint responds locally.
- The response payload contains expected values, not just `200 OK`.
- Internal dependencies required for readiness are healthy.

Typical examples:

- `curl http://127.0.0.1:<port>/live`
- `curl http://127.0.0.1:<port>/ready`
- Validate returned JSON fields such as `status=ok` and dependency statuses.

### Outside the container

Verify:

- Port mapping or ingress exposure works from the host.
- The host can resolve and reach the service through the intended path.
- The response time is within a reasonable threshold.
- The returned payload matches the expected contract.

Typical examples:

- `curl http://localhost:<published-port>/ready`
- If behind reverse proxy, call through the real proxy route as well.

### Required rule

A container is not healthy only because Docker marks it running. A passing result requires:

- Container is running.
- Health endpoint succeeds inside the container.
- Health endpoint succeeds from the host boundary.
- Returned data proves the service is actually functioning.

## Container-to-container checks

For services that talk from one container to another, check from both the host and the calling container.

### From the calling container

Verify:

- DNS resolution works for the target service name.
- Network connectivity to the target port works.
- TLS or auth handshake works if required.
- The target health or readiness endpoint returns expected data.
- Latency is acceptable for the dependency type.

This proves the actual caller path works, not just the host path.

### From the host

Verify:

- The target container is reachable from the host if it is expected to be exposed.
- The service can be inspected independently during debugging.
- Host-side route, published ports, or reverse proxy configuration is correct.

### Required rule

Do not rely only on host-to-container checks for container-to-container dependencies. Internal DNS, bridge networking, service aliases, or sidecar routing can fail while the host path still works.

## External API checks

External API health checks should be minimal, cheap, and non-destructive.

Preferred order:

- Vendor-provided status or health endpoint that does not consume credits.
- Lightweight authenticated endpoint with negligible cost and no state change.
- HEAD or metadata request if supported and contractually valid.

Avoid:

- Expensive inference or generation requests just to prove availability.
- Writes, mutations, or billable operations unless no safer option exists.
- Checks that consume rate limits aggressively.

A good external API health check should verify:

- DNS resolution works.
- TCP/TLS connection succeeds.
- Authentication is accepted if auth is required.
- A cheap endpoint returns expected response shape.
- Response time is within an acceptable threshold.

## Expected data verification

A health check must validate response content, not only reachability.

Examples of acceptable assertions:

- JSON field `status` equals `ok`.
- Dependency map contains required keys such as `database` and `redis`.
- Version field is present.
- Sentinel query returns expected constant or row count.
- Ping response matches expected text or value.

Examples of weak assertions:

- Status code is `200` with no payload validation.
- Socket opened successfully.
- HTML page loaded, but no service-specific signal was checked.

## Internal dependency checks

When a service exposes a readiness or health endpoint, it should directly test the dependencies required for normal operation.

Common checks:

- Database: open connection and run a trivial query.
- Redis: ping and optionally perform a trivial read/write if that reflects real usage.
- Queue or broker: connection/channel creation succeeds.
- Object storage: authenticated list/head call succeeds for expected bucket or container.
- Downstream service: call its readiness endpoint or cheap internal contract endpoint.
- Disk or temp directory: verify required writable path exists if the service depends on it.
- Migrations/config: verify required startup state is complete.

Keep these checks shallow but real. They should prove the dependency works now without causing side effects.

## Time and failure policy

- Use short, explicit timeouts.
- Return degraded or failed status quickly.
- Record dependency-specific latency.
- Distinguish timeout, DNS, auth, and invalid-response failures.
- Do not hide failing dependencies behind a single generic "unhealthy" message.

## Anti-patterns

- Using only container running state as health.
- Using only a TCP connect as health.
- Using business-critical or expensive endpoints for routine health checks.
- Returning success while required dependencies are disconnected.
- Making readiness depend on optional dependencies that do not block core traffic.
- Returning opaque strings instead of machine-readable details.

## Review checklist

- Is there a dedicated `/live` and `/ready` distinction where needed?
- Are checks performed from every relevant boundary?
- Does the check verify payload content, not just response code?
- Are required dependencies explicitly validated?
- Are checks cheap, frequent, and safe?
- Are timeout and latency expectations defined?
- Is the failure reason specific enough to act on?
