---
name: prompt-optimization
description: Use prompt cache optimization patterns for LLM request design. Use when structuring system prompts, developer prompts, tool schemas, context bundles, chat history, retrieval snippets, dynamic variables, or telemetry so large repeated prompt prefixes remain stable for provider prompt caching.
---

## Core Skill: Prompt Cache Optimization

Prompt cache optimization is the practice of structuring LLM requests so that large, repeated prompt prefixes remain byte/token-stable across calls. The goal is to maximize cache hits, reduce time-to-first-token, and lower input-token cost where the provider supports cached-token pricing.

The primary design rule is:

> Place content in the request from most stable to most volatile.

Any change before or inside a cacheable prefix can reduce or eliminate cache reuse for everything after that point.

***

## 1. Cache Model Awareness

Prompt caching is provider-specific. Treat caching behavior as an implementation detail that must be measured.

There are two common models:

### Implicit Prefix Caching

The provider automatically detects repeated long prefixes. The application does not explicitly create a cache object.

Common implications:

- The repeated prefix must be identical across requests.
- The prompt usually needs to exceed a provider/model-specific minimum token threshold.
- Cache hits are usually visible through usage metadata such as cached input tokens.
- Cache lifetime and eviction are controlled by the provider.

### Explicit Caching

The application explicitly marks content for caching or creates a reusable cache object.

Common implications:

- The developer may control cache boundaries, cache TTL, or cached-content identifiers.
- Static context may be uploaded or referenced once, then reused.
- Provider-specific request syntax is required.
- Cache usage should still be verified through usage/latency metrics.

***

## 2. Structural Layering Pattern

Organize prompt content by stability.

### Layer 1: Fully Static

Use for content that rarely changes.

Examples:

- System/developer instructions
- Role definition
- Safety and formatting rules
- Output contract
- Stable tool definitions
- Stable JSON schemas

Requirements:

- Keep this layer deterministic.
- Do not include dates, usernames, request IDs, conversation state, or environment-dependent values.
- Serialize schemas and tool definitions with stable key ordering.
- Sort tools deterministically by name or identifier.

***

### Layer 2: Semi-Static

Use for content that changes occasionally but is reused across many calls.

Examples:

- Repository summaries
- Product documentation
- API documentation
- Long-lived project context
- Few-shot examples
- Style guides
- Domain glossaries
- Stable retrieval bundles

Requirements:

- Version this layer explicitly.
- Rebuild or invalidate intentionally when the source content changes.
- Do not mix per-request retrieval snippets into the middle of this layer.
- Prefer stable document ordering and stable separators.

***

### Layer 3: Session State

Use for content that changes during a conversation or task.

Examples:

- Recent conversation turns
- Agent scratch summaries
- Current task state
- Prior decisions
- Current files being edited

Requirements:

- Keep this after static and semi-static context.
- Summarize or compact state when possible.
- Avoid moving session state above cacheable content.

***

### Layer 4: Fully Dynamic

Use for content that changes every request.

Examples:

- Current user query
- Current timestamp
- Request ID
- Random nonce
- Current tool result
- Current file diff
- Runtime environment details
- User-specific variables

Requirements:

- Place this at the end of the request.
- Never interpolate these values into the system prompt, tool definitions, few-shot examples, or schema block.
- Avoid placing dynamic retrieval results before stable documentation.

***

## 3. Standard Prompt Layout

Recommended request order:

```text
[SYSTEM / DEVELOPER INSTRUCTIONS - STATIC]
You are a specialized assistant.
Follow the output contract exactly.
Do not include extra fields.

[TOOLS AND OUTPUT SCHEMAS - STATIC]
<schemas>
Stable, deterministic schema JSON goes here.
</schemas>

[REFERENCE CONTEXT - SEMI-STATIC]
<context version="docs-2026-06-18">
Stable documentation, codebase summaries, examples, and policies go here.
</context>

[SESSION STATE - DYNAMIC BUT SLOWER-CHANGING]
<session_state>
Conversation summary or task state goes here.
</session_state>

[CURRENT REQUEST - FULLY DYNAMIC]
<request>
Current date: {{current_date}}
User query: {{user_input}}
Relevant fresh retrieval: {{retrieved_context}}
</request>
```

***

## 4. Implementation Constraints

### Keep Cacheable Prefixes Deterministic

Use deterministic serialization for any structured prompt components.

Recommended:

- Stable JSON key ordering
- Stable array ordering
- Consistent indentation
- Consistent newline conventions
- No random IDs inside cacheable blocks
- No generated timestamps inside cacheable blocks
- No nondeterministic tool ordering

Avoid:

- Pretty-printers that change formatting between runs
- Unordered maps/dictionaries
- Runtime-dependent paths inside static blocks
- Build numbers inside system prompts
- Randomized few-shot selection inside cached regions

***

### Isolate Dynamic Variables

Do not write prompts like this:

```text
You are helping {{user_name}} on {{current_date}}.
Always answer using this user's project context.
```

Prefer:

```text
[STATIC]
You are a project assistant. Follow the project rules.

[DYNAMIC]
User name: {{user_name}}
Current date: {{current_date}}
```

***

### Do Not Prepend Chat History

Avoid this layout:

```text
[CHAT HISTORY]
[STATIC SYSTEM PROMPT]
[TOOLS]
[CURRENT USER QUERY]
```

Prefer this layout:

```text
[STATIC SYSTEM PROMPT]
[TOOLS]
[REFERENCE CONTEXT]
[CHAT HISTORY OR SESSION SUMMARY]
[CURRENT USER QUERY]
```

***

## 5. Agent-Specific Guidance

For coding agents, tool-using agents, and multi-step workflows:

- Cache stable system instructions.
- Cache stable tool schemas.
- Cache stable repository or project summaries.
- Put volatile tool results near the end.
- Do not append every tool result into the cacheable prefix.
- Consider summarizing old tool results instead of replaying raw outputs.
- Keep tool schema ordering stable across turns.
- Track whether tool definitions changed between calls.
- Avoid inserting file diffs or command outputs before reusable context.

For long-running agents, naïvely caching the full conversation may perform worse than caching only stable blocks plus a compact dynamic state section.

***

## 6. Measurement and Verification

Prompt caching must be measured, not assumed.

Log the following per request:

```json
{
  "provider": "openai|anthropic|gemini|bedrock|other",
  "model": "model-name",
  "input_tokens": 0,
  "cached_input_tokens": 0,
  "output_tokens": 0,
  "cache_hit_ratio": 0.0,
  "time_to_first_token_ms": 0,
  "total_latency_ms": 0,
  "estimated_input_cost": 0.0,
  "estimated_cached_input_cost": 0.0,
  "prompt_prefix_hash": "sha256-of-cacheable-prefix",
  "static_context_version": "docs-2026-06-18"
}
```

Useful derived metrics:

```text
cache_hit_ratio = cached_input_tokens / input_tokens
```

Track these over time:

- Average cached tokens per call
- p50/p95 cached tokens per call
- Cache hit ratio by model
- Cache hit ratio by route/agent
- Latency with cache vs without cache
- Cost with cache vs without cache
- Number of unique prompt prefix hashes
- Cache misses caused by prompt/template version changes

***

## 7. Cache Miss Checklist

When cache hits are lower than expected, check:

- Did the system prompt change?
- Did the current date appear before the cache boundary?
- Did a request ID or UUID enter the static block?
- Did JSON schema key ordering change?
- Did tool ordering change?
- Did whitespace or newline generation change?
- Did few-shot examples rotate?
- Did retrieval context get inserted before stable docs?
- Did chat history get prepended before the static prefix?
- Did the request fall below the provider's minimum cacheable token threshold?
- Did the provider/model/gateway support caching for this request type?
- Did the cache expire or get evicted?

***

## 8. Security and Privacy Considerations

Prompt caching can create observable timing differences between cached and uncached requests. In some architectures, especially shared gateways or proxy providers, cache isolation and metadata exposure should be reviewed.

For sensitive workloads:

- Understand whether caching is per user, per organization, per project, or globally shared.
- Avoid placing secrets in reusable cache blocks.
- Avoid caching highly sensitive user-specific content unless the provider's isolation model is acceptable.
- Review provider documentation for retention, TTL, and cache isolation guarantees.
- Consider disabling caching or using provider-specific privacy controls where required.

***

## Summary

Prompt cache optimization is a context-layout discipline. Keep large reusable content stable and early, keep volatile content isolated and late, serialize prompt components deterministically, and verify cache effectiveness with cached-token, latency, and cost metrics.
