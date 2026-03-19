# Skills by Charles Verge

These are my current coding agent skills that I am experimenting with to discover the boundaries coding agents work in. As they mature, I'll add example uses and evaluations.

## single-read-decision-update

Codex, if left on its own, will make multiple DB or API requests in the same code path for the same request. This skill attempts to address that pattern in a basic, generic way by grouping operations and having the agent stop to request information.
