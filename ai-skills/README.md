# AI Skills for PBIP Authoring

Agent skills (for Claude, Copilot and similar assistants) that add specific, hard-to-build visuals to a **PBIP project** (PBIR report + TMDL model) by editing the files directly. Each skill has a `skill.md` with the goal, placeholder tokens and steps, a `templates/` folder of TMDL and visual JSON, and a worked example against a sample model.

| Skill | What it builds |
|---|---|
| [clustered-chart-labels-above-bar](clustered-chart-labels-above-bar/) | Add a clustered column/bar chart whose data labels sit above (outside) the bar. |
| [column-line-combo-bubble-markers](column-line-combo-bubble-markers/) | Add a column+line combo chart where a line series floats fixed-height "bubble" markers above every column, each carrying a custom dynamic label (e.g. % of total), connected to its bar top by an error-bar stem. |
| [highlight-time-window-linechart](highlight-time-window-linechart/) | Add a "Between" date-range slicer that shades a highlighted time window on a Power BI line chart. |
| [stacked-bar-pagination](stacked-bar-pagination/) | Add a "top N per page" stacked bar chart with Next/page-number pagination. |
| [stacked-bar-percent-of-total](stacked-bar-percent-of-total/) | Add a stacked bar/column chart where each bar reads as a single solid-color segment carrying a "% of total" label in blended headroom. |
