# Power BI Report Factory

An AI-powered system for generating production-grade Power BI reports using a codified design system, MCP tooling, and Claude Code/Cursor orchestration.

**Author**: hturbano

## What This Is

A complete framework that takes a data source and a description, and produces a polished, on-brand Power BI report (.pbip) — using AI to handle the heavy lifting while maintaining design consistency through a codified design system.

This isn't a template. It's a **report factory**: design tokens as code, battle-tested DAX patterns, proven visual layouts, and an AI skill file that encodes BI best practices into a repeatable workflow.

## Quick Start

### 1. Clone and Open

```bash
git clone https://github.com/hturbano/powerbi.git
cd powerbi
```

Open in Claude Code or Cursor. The skill file is auto-loaded.

### 2. Onboarding

When you first open the project, the skill will detect it needs setup and offer three paths:

```
Welcome to the Power BI Report Factory.

How would you like to configure your design system?

  [A] I have an existing .pbip file — extract the design system from it
  [B] I want to build a design system from scratch — guide me through it
  [C] Use a professional default theme — get me started immediately
```

- **Path A**: Drop your .pbip into `incoming/`, the skill extracts colors, fonts, layouts, and DAX patterns
- **Path B**: Interactive Q&A builds a custom design system from your brand specs
- **Path C**: Instant setup with a professional blue-themed corporate theme + dark mode

### 3. Set Up MCP Servers

```bash
bash scripts/setup-mcp.sh
```

This installs and configures both MCP servers (powerbi-report-mcp and powerbi-modeling-mcp) and generates the settings files for Claude Code and Cursor.

### 4. Generate Your First Report

In Claude Code or Cursor:

```
Build a student attendance dashboard with:
- KPI cards for total enrollment, attendance rate, and ADA percentage
- Monthly trend line for attendance
- Campus breakdown bar chart
- Date slicer for school year filtering
- Use the corporate theme
```

## What's Inside

```
powerbi-report-factory/
├── README.md                              # This file
├── .gitignore
│
├── design-system/                         # Design tokens as code
│   ├── themes/
│   │   ├── corporate.json                 # Primary business theme
│   │   └── dark-mode.json                 # Dark operational theme
│   ├── layouts/
│   │   └── dashboard-2col.json            # 3 layout templates
│   └── dax-patterns/
│       ├── time-intelligence.json         # YTD, MoM, YoY, rolling averages
│       └── kpis.json                      # Status, trend, SLA, success rate
│
├── templates/default-theme/               # Default theme for Path C onboarding
│   ├── corporate.json
│   ├── dark-mode.json
│   ├── time-intelligence.json
│   ├── kpis.json
│   └── layouts.json
│
├── ai-orchestration/                      # AI skill and workflows
│   ├── skills/
│   │   └── powerbi-designer.md           # Claude Code/Cursor skill (onboarding + generation)
│   ├── prompts/
│   │   └── system-prompt.md              # System prompt template
│   └── workflows/
│       └── generate-report.md            # Step-by-step workflow
│
├── incoming/                              # Drop .pbip files here for extraction
│   └── README.md
│
├── examples/
│   ├── report-1-sales-dashboard/          # Education/ADA dashboard scaffold
│   └── report-2-operational/              # Data engineering pipeline observability
│
├── scripts/
│   ├── setup-mcp.sh                      # One-command MCP setup
│   └── validate-pbip.py                  # PBIP validation utility
│
└── docs/
    ├── DESIGN_SYSTEM.md                   # Full design system reference
    ├── GOTCHAS.md                         # MCP gotchas and workarounds
    ├── SETUP.md                           # Detailed setup guide
    └── FUAM_INTEGRATION.md               # Future: tenant-wide monitoring
```

## The Stack

- **[powerbi-report-mcp](https://github.com/jonathan-pap/powerbi-report-mcp)** — 56 tools for building .pbip reports programmatically
- **[powerbi-modeling-mcp](https://github.com/microsoft/powerbi-modeling-mcp)** — Semantic model management
- **[fabric-cli](https://github.com/microsoft/fabric-cli)** — Cloud deployment and operations
- **Claude Code / Cursor** — AI orchestration layer

## Design System

Every report generated through this system inherits:

- **Brand-compliant color palettes** — primary, secondary, semantic (success/warning/danger)
- **Typography standards** — font family, sizes, weights
- **Layout grid definitions** — margins, spacing, page dimensions
- **Visual default configurations** — chart styles, label positions, legend placement
- **Reusable DAX patterns** — time intelligence, KPIs, SLA tracking

See [docs/DESIGN_SYSTEM.md](docs/DESIGN_SYSTEM.md) for the full spec.

## Example Reports

| Report | Domain | Highlights |
|--------|--------|------------|
| Student Performance Dashboard | Education/ADA | KPI cards, trend lines, campus drill-through, conditional formatting |
| Data Pipeline Observability | Engineering/DE | Job failure tracking, SLA monitoring, refresh history, alert thresholds |

## Roadmap

- [x] Design system as code (themes, layouts, DAX patterns)
- [x] Three-path onboarding flow (extract / build / default)
- [x] AI skill file for Claude Code/Cursor
- [x] Example report scaffolds
- [x] Setup scripts and validation utility
- [ ] FUAM integration for tenant-wide analytics monitoring
- [ ] CI/CD pipeline for automated report deployment via fabric-cli
- [ ] Custom visual template library

## License

MIT — Use it, fork it, make it yours.
