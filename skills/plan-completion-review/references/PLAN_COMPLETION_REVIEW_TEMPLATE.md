# Plan Completion Review Report

## 1. Run tests, linters

### pytest

- Success/Failure: `[test file path]` `[test case name]`
  - Error:
  - Evidence:

### Playwright

- Success/Failure: `[test file path]` `[test case name]`
  - Error:
  - Evidence:

### Linters

- Success/Failure: `[command]`
  - Error:
  - Evidence:

### Type checks

- Success/Failure: `[command]`
  - Error:
  - Evidence:

### Build or runtime checks

- Success/Failure: `[command or manual check]`
  - Error:
  - Evidence:

## 2. Review code for unexpected side effects

- Finding: `[file path]:[line]` `[symbol or code path]`
  - Side effect category:
  - Impact:
  - Evidence:
  - Required change:
- None

## 3. Create a list of features and ensure they are all completed

| Feature or requirement     | Plan source              | Status                    |
| -------------------------- | ------------------------ | ------------------------- |
| `[feature or requirement]` | `[plan section or line]` | Completed/Partial/Missing |

## 4. Verify the plan is valid. Ensure the original goal has been met with the plan

| Goal description        | In Plan              | Short change description      | Has tests |
| ----------------------- | -------------------- | ----------------------------- | --------- |
| `[goal or requirement]` | Full/Partial/Missing | `[short description or None]` | Yes/No    |

## 5. Verify the code completes the original goal

| Goal description        | File name     | In Code              | Short change description      | Has tests |
| ----------------------- | ------------- | -------------------- | ----------------------------- | --------- |
| `[goal or requirement]` | `[file path]` | Full/Partial/Missing | `[short description or None]` | Yes/No    |

## 6. What are the unrequested modifications made

- `[description of modification]`
  - Reason for modification:
  - Impact rating: High/Medium/Low
- None

## 7. Is there anything that will fail to execute, or produce the expected outcome

### Runtime failures

- Runtime failure: `[file path]:[line]` `[code path]`
  - Error:
  - Evidence:

### Incorrect outputs

- Incorrect output: `[file path]:[line]` `[code path]`
  - Expected:
  - Actual:

### Blocking risks

- Risk: `[file path]:[line]` `[code path]`
  - Risk:
  - Evidence:

## 8. Questions: Is there any thing you are unsure about

- `[question]`
- None

## 9. Suggested improvements

- `[suggested improvement]`
- None

## 10. Migration

### Database

- `[database migration]`
- None

### Files

- `[file migration]`
- None

### Configuration

- `[configuration migration]`
- None

### Other

- `[other migration]`
- None

## 11. Assumptions

- `[assumption]`
- None

## 12. Changes required

- **Files needing changes:**
  - Add:
    - `[file path]:[line]`
      - Required change:
      - Reason:
  - Modify:
    - `[file path]:[line]`
      - Required change:
      - Reason:
  - Remove:
    - `[file path]:[line]`
      - Required change:
      - Reason:
- **Classes, properties, and types needing changes:**
  - Add:
    - `[file path]:[line]` `[ClassName | property_name | TypeName]`
      - Required change:
      - Reason:
  - Modify:
    - `[file path]:[line]` `[ClassName | property_name | TypeName]`
      - Required change:
      - Reason:
  - Remove:
    - `[file path]:[line]` `[ClassName | property_name | TypeName]`
      - Required change:
      - Reason:
- **Functions needing changes:**
  - Add:
    - `[file path]:[line]` `[function_name(signature)]`
      - Required change:
      - Reason:
  - Modify:
    - `[file path]:[line]` `[function_name(signature)]`
      - Required change:
      - Reason:
  - Remove:
    - `[file path]:[line]` `[function_name(signature)]`
      - Required change:
      - Reason:
- **Constants needing changes:**
  - Add:
    - `[file path]:[line]` `[CONSTANT_NAME]`
      - Required change:
      - Reason:
  - Modify:
    - `[file path]:[line]` `[CONSTANT_NAME]`
      - Required change:
      - Reason:
  - Remove:
    - `[file path]:[line]` `[CONSTANT_NAME]`
      - Required change:
      - Reason:
- **Tests needing changes:**
  - Add:
    - `[test file path]` `[test name]`
      - Required change:
      - Verification:
      - Coverage category:
  - Modify:
    - `[test file path]` `[test name]`
      - Required change:
      - Verification:
      - Coverage category:
  - Remove:
    - `[test file path]` `[test name]`
      - Required change:
      - Coverage category:
- **Resource files needing changes:**
  - Add:
    - `[resource file path]`
      - Resource type: Markdown/Text/JSON/XML/Data/Other
      - Required change:
      - Reason:
  - Modify:
    - `[resource file path]`
      - Resource type: Markdown/Text/JSON/XML/Data/Other
      - Required change:
      - Reason:
  - Remove:
    - `[resource file path]`
      - Resource type: Markdown/Text/JSON/XML/Data/Other
      - Required change:
      - Reason:
- **Notes of major removals:**
  - `[removal note]`
    - Impact:
    - Reason:
  - None

## 13. Summary

- Percent complete:
- Rationale:
