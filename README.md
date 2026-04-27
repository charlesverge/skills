# Skills by Charles Verge

These are my current coding agent skills that I am experimenting with to discover the boundaries coding agents work in. Consider them early work in progress. As they mature, I'll add example uses and evaluations.

[Skills list](skills.md)

## Skill Directory Structure

```
skills/
└── skill-name/
    ├── SKILL.md           # Required - skill documentation
    └── resources/        # Optional - supporting files
        ├── deploy/      # deployment scripts
        └── ...
```

## SKILL.md Format

Each skill must have a `SKILL.md` file with YAML front matter:

```yaml
---
name: skill-name
description: Brief description of what the skill does. Use when...
---

# Skill Title

Detailed skill documentation...
```

### Front Matter Fields

- `name`: Skill identifier (kebab-case)
- `description`: What the skill covers and when to use it

## Resources Directory

The `resources/` directory stores supporting files needed by the skill:

- `deploy/` - deployment configurations and scripts
- Example files and templates
- Any non-code documentation

Note: Only include resources if the skill actually uses them.

## Registration

After creating the skill, register it in two places:

### 1. skills_index.json

Add to the top of the array:

```json
{
  "id": "skill-name",
  "path": "skills/skill-name",
  "category": "engineering",
  "name": "skill-name",
  "description": "Description of skill.",
  "risk": "safe",
  "source": "personal",
  "date_added": "YYYY-MM-DD"
}
```

### 2. skills.md

Add to the top (after existing skills), using this format:

```markdown
## skill-name

* `id`: `skill-name`
* `path`: `skills/skill-name`
* `category`: `engineering`
* `name`: `skill-name`
* `risk`: `safe`
* `source`: `personal`
* `date_added`: `YYYY-MM-DD`

### Description

Description of skill.

### Skill File

* [skills/skill-name/SKILL.md](skills/skill-name/SKILL.md)
```

## Example: Creating "my-new-skill"

1. Create directory: `skills/my-new-skill/`
2. Create `SKILL.md` with front matter
3. Add to `skills_index.json` (top of array)
4. Add to `skills.md` (top of list)