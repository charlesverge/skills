---
name: test-harness-creation
description: Create strict, production-like Python test harnesses with explicit setup, execution, and verification stages, a standard run.py interface, and containerized dependencies for complex or external flows.
---

# Test Harness Creation

Use this skill when building execution scripts that validate a partial flow or full end-to-end behavior in a production-like environment.

## What a test harness is

A test harness is an executable test script (or script set) that:

* Recreates an environment as close to production as practical.
* Runs a defined execution flow (partial or end to end).
* Verifies completion and expected outcomes with strict assertions.

## Required structure

Every test harness must have three explicit stages:

* Setup: Prepare dependencies, seed data, configure services, and ensure environment readiness.
* Execution: Run the target flow being validated.
* Verification: Assert completion and validate resulting state/output against expected values.

Keep these stages separated and readable. Do not blend verification into setup or setup into execution.

After setup completes, run a health check pass for all required dependencies and capabilities before entering execution.
The health check must fail fast if any requirement is unavailable.
Example required checks include Docker availability, MongoDB connectivity from inside Docker, Redis connectivity, and write permissions to required directories.

## Configuration model

* Use a shared/common settings configuration instead of passing many arguments or parameters through scripts.
* Keep runtime configuration centralized (for example: one settings module/file loaded by setup, execute, and verify).
* Command-line flags should select stages or lifecycle behavior, not carry large volumes of business configuration.
* Store parameterized test inputs and expected values in JSON fixture files (for example under a `fixtures/` directory) instead of hardcoding variation lists in `execution.py` or `verify.py`.

## Harness location

* Create each test harness at:
  * `{workspace}/deploy/{test shortname}-test-harness`
* Keep all harness-specific scripts, Docker assets, logs, and temporary outputs scoped under that directory unless explicitly directed otherwise.

## Strictness policy

* Default to strict verification; fail fast on mismatches.
* Do not write weak tests that only check that code "ran."
* Verify both:
  * Completion has been reached.
  * Results match expected outputs, state changes, side effects, and contracts.
* Prefer exact or strongly bounded assertions over loose contains/truthy checks unless a looser check is explicitly required.

## Environment policy

* Build harness environments to be production-like by default.
* For complex tasks, use Docker containers to isolate and reproduce runtime conditions.
* If the flow depends on external websites or downloadable remote resources, create a Dockerized impersonation/mocked service for those dependencies unless explicitly told otherwise.

## Script authoring constraints

* Prefer Python for harness implementation (setup, execution, verification, and orchestration).
* The primary entrypoint must be `run.py`.
* Use `utils.py` for shared utility functions used across stages (for example: loading settings, reading/writing common test artifact file formats, and other reusable harness helpers).
* No inline scripts embedded in other scripts.
* Do not embed Python blocks inside Bash scripts.
* Do not generate Bash scripts from Bash at runtime.
* Create each script as a real file and execute it directly (or copy it into a container and execute there).

## Required `run.py` contract

* Running `python run.py` with no arguments must perform: setup, execute, verify.
* `run.py` must be executable from the command line (for example `./run.py`) using a shebang and executable file permissions.
* Alongside `run.py`, stage modules must exist as separate files:
  * `setup.py` for setup logic.
  * `health.py` for post-setup requirement checks.
  * `execution.py` for execution logic.
  * `verify.py` for verification logic.
* `run.py` must support stage-selective flags:
  * `--setup`: only perform setup.
  * `--execute`: only perform execution.
  * `--verify`: only perform verification.
* `run.py` must support lifecycle/log flags:
  * `--no-tear-down`: do not stop/remove Docker containers after run stages complete.
  * `--cleanup`: remove Docker containers, log files, and temporary artifacts.
* When Docker Compose is used, `run.py` must stream Docker Compose output to stdout/stderr in real time.
* Docker execution logs must be retained on disk for post-run inspection (including failure runs).

## Operational checklist

* Define exact success criteria before writing assertions.
* Make setup deterministic and repeatable.
* Run post-setup health checks for all declared requirements before execution begins.
* Keep execution steps minimal and focused on the target flow.
* Ensure verification checks both completion and correctness.
* Ensure `run.py` default flow executes setup, execute, and verify in order.
* Ensure Docker logs are streamed during run and preserved after run.
* Return non-zero exit codes for failures.
* Print concise failure diagnostics that identify the violated expectation.
* Do not create scripts which run inline in bash, or python that will be executed locally or remotely. These scripts should be created in their own file and executed directly or copied into a container and executed there.
