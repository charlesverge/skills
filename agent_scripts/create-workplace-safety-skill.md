# COMMAND_LINE_TOOLS

## Sandbox assessment instructions

> Your virtual environment should be located in .venv
> I want you to explore you working space. list all the bash commands, like jq, sed. where your project files are and which files should be ignored. for example .git can be ignored. check if you can run tools like ruff npm pnpm remark. check if they work as expect and create a list of tools that you commonly use for code modification and exploring and list the tools that work and tools that don't. For example sed on mac os has one set of arguments and linux another. list the version you have installed and the ars to use for common tasks. create this file in COMMAND_LINE_TOOLS.md including this instruction under a heading sandbox assessment instructions.
>
> Add a section for `## Tool calls review` covering the common tool calls used for searching and code modification, verify whether they work, and document the ones that do and do not work in the same format. Confirm whether `Search (glob) "**/OVERVIEW.md"` in `specifications` is working. Create an alternative command in the tables, and for each command or tool call that fails, list what command should be used instead.

create a skill in .agents/skills/workspace-safety/SKILL.md using this document that will be executed every time a command or tool call needs to be executed. The goal of the skill is to ensure the coding harness avoids executing commands that do not work. search directories that it should not.

copy the skill to .claude/skills/workspace-safety/

## Workspace

- Project root: the directory containing this file
- Code directory: `{code_dir}` (configured in run_state.json)
- Plan directory: `{workspace_dir}/plans/`

## Paths to ignore while exploring

Ignore these first unless the task explicitly needs them:

- `.git`
- `node_modules/`
- `.next/`
- `out/`
- `build/`
- `dist/`
- `storybook-static/`
- `coverage/`
- `.nyc_output/`
- `.cache/`
- `.parcel-cache/`
- `.vite/`
- `.pnpm-store/`
- `.yarn/`
- `.vscode/`
- `.idea/`
- `.zed/`
- `tmp/`
- `.worktrees/`
- `.env`
- `.env.*`
- `.env*.local`
- `*.log`
- `*.pid`

These entries were taken from the repository `.gitignore` and the UI project's `.gitignore`.

## Tool status

| Tool | Version | Status | Notes | Alternative if unavailable |
| --- | --- | --- | --- | --- |
| `jq` | `jq-1.8.1` | Works | JSON filtering works as expected | none needed |
| `sed` | `GNU sed 4.9` | Works | Linux/GNU behavior, not macOS BSD `sed` | none needed |
| `npm` | `11.13.0` | Works | `npm help` succeeded | none needed |
| `pnpm` | not installed | Does not work | command missing | `npm` |
| `remark` | `remark 15.0.1`, `remark-cli 12.0.1` | Works | `remark --help` succeeded | none needed |
| `ruff` | `0.15.15` | Works | `ruff --help` succeeded | none needed |
| `node` | `v24.16.0` | Works | available on PATH | none needed |
| `python3` | `3.13.7` | Works | available on PATH | none needed |
| `git` | `2.51.0` | Works | available on PATH | none needed |
| `gh` | `2.46.0` | Works | available on PATH | `git` plus web UI for some tasks |
| `rg` | `15.1.0` | Works | preferred search tool | `grep` |
| `grep` | `3.11` | Works | GNU grep | `rg` |
| `find` | `4.10.0` | Works | GNU findutils | `rg --files` for some file discovery |
| `awk` | `mawk 1.3.4 20250131` | Works | available on PATH | `cut` or `sed` for simple cases |
| `xargs` | `4.10.0` | Works | GNU findutils | shell loops |
| `sort` | `0.2.2` | Works | `uutils coreutils` implementation | none needed |
| `cut` | `uutils coreutils 0.2.2` | Works | basic field extraction works | `awk` |
| `head` | `uutils coreutils 0.2.2` | Works | basic output limiting works | `sed -n '1,10p'` |
| `tail` | `uutils coreutils 0.2.2` | Works | basic output limiting works | `sed -n '$p'` for simple cases |
| `diff` | `3.10` | Works | GNU diffutils | `git --no-pager diff` |
| `npx` | `11.13.0` | Works | available on PATH | `npm exec` |
| `patch` | not installed | Does not work | command missing | `git apply` |

## Commonly used CLI tools in this environment

### Best tools for exploration

| Tool | Common use | Typical arguments here |
| --- | --- | --- |
| `rg` | Search code and text fast | `rg -n "pattern" path`, `rg -n --glob '*.ts' "pattern"` |
| `find` | Discover files and directories | `find . -name '*.ts'`, `find . -type f` |
| `jq` | Inspect JSON files or command output | `jq -r '.field' file.json`, `jq -c '.items[]'` |
| `grep` | Simple line filtering | `grep -n 'text' file`, `grep -R 'text' dir` |
| `sed` | Print or rewrite lines | `sed -n '1,20p' file`, `sed -i 's/old/new/' file` |
| `awk` | Column/field processing | `awk '{print $1}'`, `awk -F, '{print $2}'` |
| `sort` | Sort output before dedupe | `sort file`, `sort | uniq` |
| `cut` | Extract delimited fields | `cut -d, -f2 file` |
| `head` | First lines | `head -n 20 file` |
| `tail` | Last lines | `tail -n 20 file` |

### Best tools for code modification support

| Tool | Common use | Typical arguments here |
| --- | --- | --- |
| `diff` | Review changes between files or outputs | `diff -u before after` |
| `sed` | Small scripted replacements | `sed -i 's/old/new/' file` |
| `jq` | Rewrite JSON in pipelines | `jq '.key = "value"' file.json` |
| `npm` | Run existing project scripts | `npm run build`, `npm test` |
| `npx` | Run project-local JS CLIs if present | `npx jest --help`, `npx next --help` |
| `remark` | Check markdown files | `remark file.md` |
| `ruff` | Format or lint Python files | `ruff format file.py`, `ruff check file.py` |
| `git` | Inspect diffs and file state | `git --no-pager diff -- file`, `git --no-pager status --short` |
| `gh` | GitHub workflow and PR inspection | `gh pr view`, `gh run list` |

## Linux/GNU notes for common commands

### `sed`

This environment uses **GNU sed**, so these Linux forms work:

```bash
sed -n '5,12p' file
sed -i 's/old/new/' file
sed -i '1i inserted line' file
```

macOS/BSD `sed` usually needs a backup suffix with `-i`, for example:

```bash
sed -i '' 's/old/new/' file
```

That macOS form should **not** be used in this Linux workspace.

### `find`

GNU `find` examples:

```bash
find . -name '*.ts'
find . -type f | sort
find . -name node_modules -prune -o -type f -print
```

### `jq`

Common tasks:

```bash
jq -r '.name' package.json
jq -c '.dependencies | keys[]' package.json
printf '{"a":1,"b":[2,3]}' | jq -r '.b[1]'
```

### `rg`

Common tasks:

```bash
rg -n "useState" .
rg -n --glob '*.tsx' "Assistant" .
rg -n "test" package.json
```

## Tool checks that were run

- `jq` JSON extraction returned `3`
- `sed -n '2p'` returned `beta`
- `npm help` succeeded
- `rg -n 'world'` matched expected output
- `cut -d, -f2` returned `b`
- `pnpm` missing
- `remark --help` succeeded
- `ruff --help` succeeded

## Tool calls review

This section covers common Copilot CLI tool calls for searching, reading, code modification, and command execution in this workspace.

| Tool call | Example | Status | Notes | Alternative command or tool |
| --- | --- | --- | --- | --- |
| Search (`glob`) | `pattern="**/OVERVIEW.md"` in `specifications` | Not available | No `glob` tool call is exposed in the current Codex tool set | `exec_command` with `find specifications -name OVERVIEW.md -print` |
| Search (`rg`) | shell `rg -n "pattern" path` | Works | Shell `rg` worked in this session | `grep -R -n "pattern" path` |
| Read (`view`) file | `COMMAND_LINE_TOOLS.md` | Not available | No `view` tool call is exposed in the current Codex tool set | `exec_command` with `sed -n`, `head`, or `tail` |
| Read (`view`) directory | `specifications` | Not available | No `view` tool call is exposed in the current Codex tool set | `exec_command` with `find` |
| Edit (`apply_patch`) | add or update `COMMAND_LINE_TOOLS.md` | Works | File creation and updates succeeded | none needed |
| Command execution (`exec_command`) | `find specifications -name OVERVIEW.md -print` | Works | Command ran correctly and returned no matches | none needed |

### Search call example review

Requested example:

```text
Search (glob) "**/OVERVIEW.md" in specifications
```

Result in this workspace:

- The **`glob` tool call is not exposed in the current Codex tool set**, so that search is **not available** through the tool layer right now.
- A shell fallback check with `find specifications -name OVERVIEW.md -print` **worked** and returned **no matching files**.
- That means the pattern is reasonable, but there are currently no `OVERVIEW.md` files under `specifications/` in this repository.

### Recommended fallback order

1. Use `find` for filename/path matching.
2. Use shell `rg` for content search.
3. Use `sed -n`, `head`, or `tail` to inspect exact files after locating them.
4. Use `apply_patch` for precise edits.
5. Use `exec_command` for shell execution.

## Practical recommendations for this workspace

1. Use `rg` first for content search.
2. Use `find` when the path is unknown.
3. Use `jq` for JSON inspection.
4. Use GNU `sed` syntax, not macOS `sed -i ''`.
5. Use `npm` and `npx` for JavaScript tasks.
6. Do not assume `pnpm` or `patch` are available.

## Summary

The most reliable installed command-line tools for exploration are `rg`, `find`, `jq`, `grep`, `sed`, and `awk`. The JavaScript runtime and package tools available on PATH are `node`, `npm`, and `npx`. `remark` and `ruff` are available. `pnpm` and `patch` are currently unavailable in this workspace.
