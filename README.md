# ⚔️ Analytics Toolkit

A centralized collection of reusable analytics resources, code patterns, standards, and accelerators for developers.

The Analytics Toolkit is intended to reduce duplicate effort, promote consistency, and provide proven solutions that can be reused across projects.

## 🧰 Desktop Tools

Standalone Windows apps for Power BI projects (PBIP / TMDL). No install and no Python needed: download the `.exe` and run it. Everything runs locally and nothing is uploaded.

| Tool | What it does | Download |
|------|--------------|----------|
| [Model Documenter](./Model%20Documenter/) | Generates a standalone HTML document of a semantic model and its report pages: tables, measures, relationships, lineage and validation | [ModelDocumenter.exe](https://github.com/FosterBiServices/Power-BI-Portfolio/releases/latest/download/ModelDocumenter.exe) |
| [AI Model Context Generator](./AI%20Model%20Context%20Generator/) | Writes one AI-ready `.semantic-context.md` file describing a model, with privacy controls for DAX, hidden objects and source locations | [AIModelContextGenerator.exe](https://github.com/FosterBiServices/Power-BI-Portfolio/releases/latest/download/AIModelContextGenerator.exe) |
| [About This Report Generator](./About%20This%20Report%20Generator/) | Builds an AI prompt from a report, validates the AI's JSON response against the model and turns it into an "About This Report" HTML DAX measure | [AboutThisReportGenerator.exe](https://github.com/FosterBiServices/Power-BI-Portfolio/releases/latest/download/AboutThisReportGenerator.exe) |

All versions and release notes: [Releases](https://github.com/FosterBiServices/Power-BI-Portfolio/releases)

> **First run:** the apps are not code-signed, so Windows may show *"Windows protected your PC"*. Select **More info → Run anyway**.

---

## 🔥 Most Used Resources

| Resource | Description |
|-----------|-------------|
| [DAX](./DAX/) | DAX Measures and Formatting |
| [Power Query](./PowerQuery/) | Reusable functions and transformations|
| [Tabular Editor Scripts](./TabularEditor/) | Model automation and bulk updates |
| [Python Scripts for Balanced Scorecard](./Python/BalancedScorecard/Balanced%20Scorecard) | Generate DAX and model artifacts |
| Standards | Naming conventions and best practices |

---

## 🎯 Purpose

This repository contains:

- Reusable Power Query patterns
- DAX examples and calculation patterns
- Tabular Editor scripts
- Python automation utilities
- Power BI templates and themes
- Development standards and best practices
- Training and reference materials

This repository is **not** intended for active project development. Project-specific work should remain in their respective repositories.

---

## 📁 Repository Structure

```text
Analytics-Tookkit/
│
├── DAX/
│   ├── Calculation Groups/
│   ├── Formatting/
│   ├── KPIPatterns/
│   ├── Measures/
│   ├── SVG Measures/
│   └── TimeIntelligence/
│   ├── User Defined Functions/
│
├── PowerQuery/
│   ├── DataCleansing/
│   ├── DateLogic/
│   ├── Functions/
│   ├── Ingestion/
│   └── Transformations/
│
├── TabularEditor/
│   ├── Analysis/
│   ├── Documentation/
│   └── Measures/
│   ├── Model/
│
├── Python/
│   ├── Automation/
│   ├── DataQuality/

│
├── PowerBI/
│   ├── Templates/
│   ├── Themes/
│
├── Standards/
│
├── Training/
│
└── Accelerators/
```

---

## 🚀 Getting Started

Browse the folders above and reference the solution that best matches your use case.

Each object should include:

- Purpose
- Usage instructions
- Requirements
- Example inputs
- Example outputs
- Author and maintenance information

---

## 📚 Recommended Resources

### DAX

Common measure patterns, formatting logic, and dynamic calculation examples.

### Power Query

Reusable M code for transformations, cleansing, APIs, and data preparation.

### Tabular Editor

Scripts and automation tools for semantic model development.

### Python

Utilities for metadata generation, reporting automation, validation, and data quality.

### Standards

Development guidelines and naming conventions used by the analytics team.

---

## 🤝 Contributing

Before submitting content:

1. Verify the solution is reusable.
2. Add documentation.
3. Include examples.
4. Test the solution.
5. Follow established naming standards.

Pull Requests should include:

- Description
- Purpose
- Dependencies
- Testing completed

---

## 🏷️ Naming Conventions

Follow the standards located in:

```text
/Standards
```

Examples include:

- Power BI naming standards
- DAX standards
- Power Query formatting standards
- Documentation templates

---

## 🛠 Maintenance

Repository maintainers are responsible for:

- Reviewing contributions
- Removing duplicate patterns
- Updating deprecated approaches
- Maintaining documentation quality

---

## ⚡ Guiding Principle

Don't reinvent it.

Search the Toolkit before building it.
