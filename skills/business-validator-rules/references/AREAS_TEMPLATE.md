# Business rule areas

Use one flat, human-focused taxonomy. Each area maps to exactly one direct child directory of `plans/rules/`, except `general`, which is reserved for rules that apply across the application.

| Area label | Directory | Human-focused boundary | Excludes |
| ---------- | --------- | ---------------------- | -------- |
| `general` | `plans/rules/general/` | Rules that apply globally across the application. | Rules owned by one specific area. |
| `[area-label]` | `plans/rules/[area-label]/` | [User flow, stakeholder activity, or business capability governed by this area.] | [Adjacent areas and their distinguishing boundary.] |

Do not add parent-child areas to this table. If more than one taxonomy level is required, split the domain into separate projects and document their relationship outside `plans/rules/`.
