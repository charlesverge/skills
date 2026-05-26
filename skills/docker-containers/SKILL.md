---
name: docker-containers
description: Manage Docker container workflows and Docker Compose configuration. Use when creating or modifying Dockerfiles, `docker-compose.yml` files, Compose profiles, container services, build settings, volume mounts, or translating `docker run` usage into Docker Compose-based workflows. Enforce single-build reuse, Compose-first operations, Python setup with uv and `pyproject.toml`, Node setup with pnpm, reusable development caches, and separate production compose files that share the same Dockerfile.
---

# Docker Containers

Use this skill when defining, reviewing, or modifying Docker-based local development or production deployment workflows.

The goal is to keep container operations reproducible, Compose-first, cache-aware for development, and consistent across Python and Node services.

## Core rules

* Use `docker-compose.yml` as the primary orchestration file for all routine operations.
* Prefer `docker compose` workflows over ad hoc `docker run` commands.
* If a `docker run` example is necessary, it must run within the Docker Compose-defined environment and not bypass Compose-managed networking, volumes, or configuration.
* Docker image builds should be structured so development workflows normally build once and reuse that image unless dependencies or Docker build inputs change.
* For Python projects, use `uv` with `pyproject.toml`.
* For Node projects, use `pnpm`.
* Mount and reuse Python and Node package caches during development.
* For production, use a separate Compose file with production-only services while reusing the same shared Dockerfile.

## Compose-first workflow

When adding or changing containerized workflows:

* Start with `docker-compose.yml`.
* Put service definitions, networks, named volumes, bind mounts, and shared environment wiring in Compose.
* Prefer Compose service names for service-to-service communication.
* Keep commands, entrypoints, ports, and health checks aligned with Compose services rather than separate shell instructions.

Do not introduce a workflow where the main path depends on handwritten `docker run` commands that duplicate Compose configuration.

## Build strategy

Builds should be arranged so they do not need to happen repeatedly during normal development.

Preferred approach:

* Use one shared Dockerfile per service or app family.
* Separate dependency installation from frequently changing source code where practical.
* Copy lockfiles and manifest files before application source when that improves cache reuse.
* Keep build layers stable so source edits do not invalidate dependency layers unnecessarily.
* Let Compose reference the same image/build definition across services or profiles when appropriate.

Examples of stable dependency inputs:

* Python: `pyproject.toml`, `uv.lock`
* Node: `package.json`, `pnpm-lock.yaml`

## Python container rules

For Python services:

* Use `pyproject.toml` as the package definition.
* Use `uv` for dependency installation and environment management inside the container workflow.
* Prefer dependency installation patterns that respect lockfiles and maximize Docker layer reuse.
* Mount reusable development caches for `uv` or pip-compatible download caches when applicable.

Avoid older setup flows such as:

* `requirements.txt` as the primary package definition for new setups.
* `pip install` ad hoc bootstrap steps when `uv` should be the source of truth.

## Node container rules

For Node services:

* Use `pnpm`.
* Prefer `pnpm-lock.yaml` as the lockfile source for dependency installation.
* Structure Docker layers to preserve dependency cache reuse.
* Mount and reuse the pnpm store or other package caches during development.

Avoid using npm or yarn for new container setup unless the user explicitly requires an exception.

## Development cache rules

For development workflows:

* Reuse caches across rebuilds and container restarts.
* Mount Python cache locations and Node package store/cache locations as volumes.
* Prefer named volumes for persistent reusable caches.
* Keep cache mounts explicit in Compose so they are easy to inspect and reset.

Examples of cache categories to preserve in development:

* `uv` or Python package download caches
* pnpm store/cache
* Framework-specific build caches when they materially improve local iteration speed

The purpose is faster iteration without re-downloading or re-resolving dependencies on every rebuild.

## Production cache rules

For production workflows:

* Do not depend on warm development caches.
* Use clean cache state or empty caches during production builds.
* Optimize for deterministic, reproducible builds rather than local iteration speed.
* Keep production services minimal and production-only.

## Profiles for development variants

If development needs multiple optional configurations, use Compose profiles.

Examples:

* Optional worker services
* Debug tooling
* Admin tools
* Local-only supporting services
* Alternate dev entrypoints

Use profiles instead of duplicating entire Compose files for minor development variations.

## Separate production Compose file

For production:

* Use a separate Compose file for production-only services and production overrides.
* Reuse the same shared Dockerfile rather than creating an unrelated production Dockerfile unless there is a strong, explicit reason.
* Keep production service definitions focused on runtime concerns such as replicas, stricter environment settings, and production-only dependencies.

A good pattern is:

* `docker-compose.yml` for base and development-oriented configuration
* `docker-compose.prod.yml` for production-only services or overrides

## Translating `docker run` requests

If a task asks for `docker run`:

* First determine whether the same outcome should be expressed as a Compose service, override, or profile.
* Prefer documenting the Compose-based equivalent.
* If a one-off container command is still necessary, make sure it runs with the Compose network, volumes, and environment assumptions rather than inventing a parallel setup.

## Review checklist

* Does the workflow use `docker-compose.yml` as the primary source of truth?
* Is the image build structured for reuse instead of frequent rebuilds?
* Are Python services using `uv` with `pyproject.toml`?
* Are Node services using `pnpm`?
* Are development caches mounted and reusable?
* Are multiple development variants handled with profiles?
* Is production split into a separate Compose file while sharing the same Dockerfile?
* Does the change avoid introducing a parallel non-Compose runtime path?

## Anti-patterns

* Requiring repeated rebuilds for ordinary source-only changes when the image structure could avoid that.
* Introducing `docker run` as the primary workflow next to an existing Compose setup.
* Using separate unrelated Dockerfiles for development and production without a clear need.
* Using npm for new Node container setup when pnpm is required.
* Using `requirements.txt`-first setup for new Python container flows when `pyproject.toml` and `uv` should define the environment.
* Leaving development cache mounts undefined so dependencies are re-fetched on every cycle.
* Creating multiple near-duplicate dev Compose files when profiles would handle the variation cleanly.
