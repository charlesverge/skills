# Sources Used

These eval cases are **synthetic but source-grounded**. They were built from public research, benchmark write-ups, and technical discussions about coding-agent reward hacking and common AI coding anti-patterns.

## Source IDs

### `workaround-check-skill`
- URL: local file `skills/workaround-check/SKILL.md`
- Used for: deriving the negative-control cases from the local approval standard for structural fixes, root-cause correction, intent matching, and non-evasive plans.

### `metr-reward-hacking-2025`
- URL: <https://metr.org/blog/2025-06-05-recent-reward-hacking/>
- Used for: modifying tests or scoring code, precomputing answers, reading grader-owned data, disabling timers or synchronization, monkey-patching evaluators, and the general idea that models preserve forbidden behavior while gaming the metric.

### `openai-cot-monitoring-2025`
- URL: <https://openai.com/index/chain-of-thought-monitoring/>
- Used for: patching verify functions to always return true, skipping all tests in `conftest.py`, subverting tests, and the distinction between observable hacking and hidden intent.

### `impossiblebench-2025`
- URL: <https://www.lesswrong.com/posts/qJYMbrabcQqCZ7iqm/impossiblebench-measuring-reward-hacking-in-llm-coding-1>
- Used for: the four documented exploitation strategies — modifying tests, overloading operators, recording extra state, and special-casing expected inputs.
- Also used for: public discussion of model-family differences, including OpenAI, Anthropic, and Qwen3-Coder family behavior.

### `evilgenie-2025`
- URL: <https://futuretech.mit.edu/publication/evilgenie-a-reward-hacking-benchmark>
- Used for: hardcoding test cases, editing test files, LLM-judge detection, and explicit mention of Codex / Claude Code / Gemini CLI reward hacking coverage.

### `over-mocked-tests-2026`
- URL: <https://arxiv.org/abs/2602.00409>
- Used for: evidence that coding agents modify tests and add mocks more often than non-agent commits, motivating over-mocking eval cases.

### `llm-core-ai-mistakes-2026`
- URL: <https://dev.to/pertrai1/i-analyzed-500-ai-coding-mistakes-and-built-an-eslint-plugin-to-catch-them-jme>
- Used for: empty catch blocks, swallowed errors, async misuse, and repeated AI-code anti-patterns observed in practice.

### `ts-eslint-ban-ts-comment`
- URL: <https://typescript-eslint.io/rules/ban-ts-comment/>
- Used for: `@ts-ignore`, `@ts-expect-error`, and `@ts-nocheck` suppression patterns, plus the explicit rationale that suppressing type errors reduces type-safety effectiveness.

## Interpretation Notes

- The cases in `fixtures/cases.json` are **not** verbatim benchmark transcripts.
- The cases in `fixtures/negative_controls.json` are **not** transcripts; they are control examples derived from the local skill's approval criteria.
- The cases are paraphrased and normalized into **plan-review inputs**, because `workaround-check` is a planning skill.
- Model-family buckets are used to ensure coverage across `claude`, `openai`, `codex`, and `public` cases without making unsupported one-to-one provenance claims for each synthetic example.
