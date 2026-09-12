# Contributing

## Pull request requirements

- Keep placeholders unchanged unless the placeholder contract is intentionally revised.
- Preserve comments that explain purpose, replacements, assumptions, and output type.
- Use underscore-prefixed, singular DAX variable names with proper casing.
- Use `DIVIDE` for ratios.
- Add or update validation notes when calculation behavior changes.
- Do not mix fiscal and calendar behavior in the same template.

## Review checklist

- [ ] DAX parses successfully.
- [ ] Current-period result matches a manually verified result.
- [ ] Prior-period result is aligned to the intended comparison window.
- [ ] Totals and hierarchy levels behave as documented.
- [ ] Blank and zero comparison values do not produce errors.
- [ ] Date filters outside the target period do not leak into complete-period results.
