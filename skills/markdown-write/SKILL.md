# Markdown Writing Rules

This skill defines the rules for creating, writing, or editing Markdown files in this project to ensure they pass `remark` linting without errors.

## Auto-Fix with remark

Use remark's `--output` (or `-o`) flag to automatically fix linting errors:

```bash
# Process input.md and write fixed version to output.md
remark input.md -o output.md

# Overwrite the original file (use with caution)
remark input.md -o input.md

# Fix all markdown files in place
remark . -o .
```

**Note**: Auto-fix handles most formatting issues (table alignment, list markers, spacing, etc.) but cannot fix semantic issues like:
- Heading content/structure
- Missing link definitions
- Shortcut reference links (must manually convert to collapsed references `[text][]`)
- Definition placement (must move definitions after content)

## Core Rules

### List Formatting

**Ordered Lists**: Must use `1.` for all items (not `1.`, `2.`, `3.`)

```markdown
## Correct
1. First item
1. Second item
1. Third item

## Incorrect
1. First item
2. Second item
3. Third item
```

**Unordered Lists**: Use `-` (configured in settings.bullet)

```markdown
- Item one
- Item two
- Item three
```

### Headings

- Use ATX style: `# Heading`, `## Heading`, etc.
- Headings must increment properly (no skipping levels)
- Maximum heading length: 120 characters
- No punctuation restriction (disabled)

### Code Blocks

- Use fenced code blocks with backticks (```)
- Specify language after opening fence
- Empty language flag is allowed

```markdown
```python
def hello():
    print("world")
```
```

### Tables

- Use pipes for separation
- Align pipes properly
- Pad cells with spaces
- No indentation on tables

```markdown
| Header 1 | Header 2 |
| -------- | -------- |
| Cell 1   | Cell 2   |
```

### Links & References

- Link titles use double quotes: `[text](url "title")`
- No shortcut reference links or images
- Definitions must be properly spaced and cased

### Emphasis & Strong

- Use `*` for both emphasis and strong (not `_`)
- `*italic*` and `**bold**`

### Horizontal Rules

- Use `---` (three hyphens)

### General Formatting

- Maximum line length: 500 characters
- No consecutive blank lines
- No shell dollars (`$`) in code blocks
- No hard break spaces (trailing spaces for line breaks)
- Blockquotes indented with 2 spaces
- File names: only `.a-zA-Z0-9_-` characters, no consecutive/outer dashes

## Validation

Before committing markdown changes, run:

```bash
remark <file.md>
```

Or for all files:

```bash
remark .
```

## Files Ignored

Per `.remarkignore`:
- `AGENTS.md`
- `.venv/`
- `build/`
- `vendors/`

## Quick Reference Checklist

- [ ] Ordered lists use `1.` for every item
- [ ] Unordered lists use `-`
- [ ] Headings use `#` syntax and increment properly
- [ ] Code blocks use ``` with language
- [ ] Tables have aligned pipes and padded cells
- [ ] Links use `"title"` format
- [ ] Emphasis uses `*`
- [ ] No lines exceed 500 characters
- [ ] No consecutive blank lines
- [ ] Blockquotes indented 2 spaces
- [ ] File name follows conventions