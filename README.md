# Power BI Report Factory

An AI-powered system for generating production-grade Power BI reports using a codified design system, MCP tooling, and Claude Code/Cursor orchestration.

## What This Is

A complete framework that takes a data source and a description, and produces a polished, on-brand Power BI report (.pbip) — using AI to handle the heavy lifting while maintaining design consistency through a codified design system.

This isn't a template. It's a **report factory**: design tokens as code, battle-tested DAX patterns, proven visual layouts, and an AI skill file that encodes years of BI best practices into a repeatable workflow.

## Why It Exists

Most Power BI development is manual, inconsistent, and slow. Every report starts from scratch. Every developer makes different design choices. Brand compliance is a manual check. This repo solves all of that by:

1. **Encoding the design system** — colors, fonts, layouts, and visual configs as version-controlled JSON
2. **Automating report generation** — AI builds the .pbip structure from natural language descriptions
3. **Standardizing DAX** — reusable, tested patterns for time intelligence, KPIs, and common calculations
4. **Providing real examples** — production-quality reports built with this system

## What's Inside

```
design-system/       → Design tokens extracted from production reports
ai-orchestration/    → AI skill file, prompts, and workflows
examples/            → Complete example reports (school analytics + data engineering)
scripts/             → Setup and validation utilities
docs/                → Design system reference, gotchas, and setup guide
```

## The Stack

- **[powerbi-report-mcp](https://github.com/jonathan-pap/powerbi-report-mcp)** — 56 tools for building .pbip reports programmatically (visuals, formatting, layout, themes)
- **[powerbi-modeling-mcp](https://github.com/microsoft/powerbi-modeling-mcp)** — Semantic model management
- **[fabric-cli](https://github.com/microsoft/fabric-cli)** — Cloud deployment and operations
- **Claude Code / Cursor** — AI orchestration layer

## Quick Start

```bash
# 1. Clone this repo
git clone <repo-url> && cd powerbi-report-factory

# 2. Set up MCP servers
bash scripts/setup-mcp.sh

# 3. Open in Claude Code or Cursor
# The skill file is auto-loaded from ai-orchestration/skills/

# 4. Describe your report
# "Build a student attendance dashboard with monthly trends,
#  campus breakdown, and YTD comparisons using the corporate theme"
```

## Example Reports

| Report | Domain | Highlights |
|--------|--------|------------|
| Student Performance Dashboard | Education/ADA | KPI cards, trend lines, campus drill-through, conditional formatting |
| Data Pipeline Observability | Engineering/DE | Job failure tracking, SLA monitoring, refresh history, alert thresholds |

## Design System

The design system is extracted from production reports and encoded as JSON theme files. Every report generated through this system inherits:

- Brand-compliant color palettes (primary, secondary, semantic)
- Typography standards (font family, sizes, weights)
- Layout grid definitions (margins, spacing, responsive breakpoints)
- Visual default configurations (chart styles, label positions, legend placement)

See [docs/DESIGN_SYSTEM.md](docs/DESIGN_SYSTEM.md) for the full spec.

## Roadmap

- [x] Design system extraction and documentation
- [x] AI skill file for Claude Code/Cursor
- [x] Example reports (school + data engineering)
- [ ] FUAM integration for tenant-wide analytics monitoring
- [ ] CI/CD pipeline for automated report deployment via fabric-cli
- [ ] Custom visual template library

## License

MIT — Use it, fork it, make it yours.
