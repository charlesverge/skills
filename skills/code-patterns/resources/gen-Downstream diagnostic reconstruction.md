# Coding Pattern Rule: Do Not Reconstruct Diagnostics Downstream

## Context

Downstream diagnostic reconstruction occurs when code catches an error, decides what the error means by comparing its human-readable message, and performs new work to rebuild diagnostic details that were available where the error originated.

This creates two coupled problems:

- **Stringly typed control flow:** changing the exception message can silently change program behavior.
- **Misplaced diagnostic ownership:** the catcher must know how the source detected the failure and repeat source-specific operations.

It can also produce inaccurate diagnostics because the downstream query observes state after the failure rather than the exact state that caused it.

## Pattern Not to Use

Do not identify an error by matching its message and then query mutable state again to reconstruct its details:

```python
except StopReached as exc:
  state.success = False
  self.stop_reason = str(exc)
  if self.stop_reason == "workspace_dir must be clean before agent execution":
    changes = git_status_porcelain(
      cwd=runtime_settings.workspace_dir,
      git_log_path=runtime_settings.orchestrator_dir / "logs" / "git.log",
    ).stdout.rstrip()
    self.stop_reason = (
      f"{runtime_settings.workspace_dir} has uncommited changes. "
      "Repository needs to be clean before work can start. "
      f"Address the following:\n{changes}"
    )
```

This is rejected because:

- the exception message is being used as an error type;
- the downstream layer is coupled to the source layer's Git implementation;
- Git is queried again after the failure, so the reported state may differ from the failure state;
- formatting and error classification are mixed into the catch path.

## Pattern to Use

Define a specific exception in the feature's dedicated exception module. The
exception captures the diagnostic context at the point where the failure is
detected:

```python
# coding_orchestrator/agents/exceptions.py
from pathlib import Path

from coding_orchestrator_types.builder_types import StopReached


class DirtyWorkspaceError(StopReached):
  def __init__(self, directory: Path, changes: str) -> None:
    self.directory = directory
    self.changes = changes
    super().__init__(
      f"{directory} has uncommitted changes. "
      "Repository needs to be clean before work can start. "
      f"Address the following:\n{changes}"
    )
```

Capture the failing state once and raise the typed exception from the source that owns the clean-workspace check:

```python
from .exceptions import DirtyWorkspaceError


def check_clean(self) -> None:
  builder = context_runtime_settings()
  status = git_status_porcelain(
    cwd=builder.workspace_dir,
    git_log_path=builder.orchestrator_dir / "logs" / "git.log",
  )
  status.check_returncode()
  changes = status.stdout.rstrip()
  if not changes:
    return
  raise DirtyWorkspaceError(builder.workspace_dir, changes)
```

The downstream catch path preserves the supplied diagnostic without classifying the exception by its message or repeating the source operation:

```python
except StopReached as exc:
  state.success = False
  self.stop_reason = str(exc)
```

## Rule

Capture failure-specific diagnostic data at the boundary that detects the failure. Represent distinct failure conditions with specific exception types and carry the observed context with the exception.

Downstream handlers may record, translate, or present that captured information. They must not determine exception identity from message text or re-query mutable state to reconstruct information the error source could provide.

## Exception Module Ownership

Exception definitions must live in a language-appropriate, dedicated exception
or error module rather than the operation, service, or handler that raises them.
For example, use `exceptions.py` in Python or `errors.ts` in TypeScript. Import
the concrete exception directly from its owning module; do not re-export it from
the operation module.

Keep every exception module at or below 400 lines. Before a module would exceed
400 lines, split its exceptions by stable domain or failure category, with each
category module also limited to 400 lines. Use names such as
`workspace_exceptions.py` and `model_exceptions.py`; do not use arbitrary
numbered files.
