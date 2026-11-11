# Model Linter review

The model and report were checked with the [Model Linter](https://fosterbiservices.github.io/Power-BI-Toolkit/model-linter.html) from the Foster BI Toolkit, reading the PBIP folder (semantic model and report pages together).

## Before and after

| Check | First run | Now | What was done |
|---|---:|---:|---|
| Measures without a display folder | 0 | 0 | Every measure sits in a numbered subject folder. |
| Measures without a format string | 81 | 0 | The 76 helper measures that return text (status labels, colors, SVG cards, chart helpers) are hidden. They still drive the visuals and conditional formatting, but they no longer clutter the field list. |
| Visible key columns | 6 | 1 | Fact-table dates and the account and project keys are hidden. `Scenario[Scenario]` stays visible on purpose: it is the Actual / Budget / Forecast label people slice by. |
| Bidirectional relationships | 0 | 0 | All single direction. |
| Implicit measures | 0 | 0 | *Discourage implicit measures* is on. |
| Unused measures | 49 | 0 | `build/tidy_model.py` keeps only measures a visual, filter or formatting rule uses, plus everything those depend on (387 measures remain). |
| Unused columns | 36 | 36 | Kept on purpose. They are descriptive attributes for ad hoc analysis (store city, format and square feet, customer segment and terms, product group and list price, the full calendar from the Date Table Generator). `Locations[Region]` and `Customers[Customer Type]` also drive the row-level security roles, which the linter does not count as use. |
| Visuals without alt text | 85 | 0 | Every visual gets alt text from its title and subtitle. |
| Charts and tables with the title turned off | 29 | 0 | The KPI cards are now image visuals (the KPI Visualizer SVG measure as the image source), which the check doesn't apply to; the header text cards have alt text. |
| Hidden visuals, unused bookmarks, empty or crowded pages | 0 | 0 | |

**Result:** 286 findings at the first run, 37 now: the 36 deliberate unused columns and the visible `Scenario[Scenario]` label, both explained above.

The full model and report documentation from the [Model Documenter](https://fosterbiservices.github.io/Power-BI-Toolkit/model-documenter.html) is in [`model-documentation.html`](./model-documentation.html) (developer edition: report pages and visual usage, DAX, hidden objects and model checks; Power Query left out because the queries hold the embedded data).
