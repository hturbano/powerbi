# Power BI Report Factory

An AI-powered system for generating production-grade Power BI reports using a fintech-grade design system, industry-specific KPI packs, and Claude Code/Cursor orchestration.

**Author**: hturbano

## What This Is

A complete framework that takes a data source and a description, and produces a polished, fintech-quality Power BI report (.pbip) — using AI to handle the heavy lifting while maintaining design consistency through a codified design system.

This isn't a template. It's a **report factory**: design tokens as code, industry-specific KPI packs, battle-tested DAX patterns, and an AI skill file that encodes BI best practices into a repeatable workflow.

## Design Philosophy

Inspired by the clean, data-dense aesthetics of fintech leaders like Credit Karma and TurboTax:

- **Bold KPI cards** with large values and clear hierarchy
- **Deep navy + teal** color palette with semantic status colors
- **Rounded corners, subtle shadows, generous whitespace**
- **Light/dark theme toggle** built into every report
- **Industry-specific KPI packs** with smart field mapping

## Quick Start

### 1. Clone and Open

```bash
git clone https://github.com/hturbano/powerbi.git
cd powerbi
```

Open in Claude Code or Cursor. The skill file is auto-loaded.

### 2. Onboarding

When you first open the project, the skill will offer three paths:

```
Welcome to the Power BI Report Factory.

How would you like to get started?

  [A] I have an existing .pbip file — extract the design system from it
  [B] I want to build a design system from scratch — guide me through it
  [C] Use the default fintech theme — get me started immediately

Or type "wizard" for a step-by-step guided setup.
```

### 3. Set Up MCP Servers

```bash
bash scripts/setup-mcp.sh
```

### 4. Generate Your First Report

```
Build an education dashboard using the Education KPI pack with:
- KPI cards for enrollment, ADA rate, and graduation rate
- Monthly attendance trend
- Campus breakdown
- Light/dark theme toggle
```

## What's Inside

```
powerbi-report-factory/
├── README.md
├── .gitignore
│
├── design-system/                         # Design tokens as code
│   ├── themes/
│   │   ├── modern-fintech.json            # Primary fintech theme (light)
│   │   ├── modern-fintech-dark.json       # Dark mode variant
│   │   ├── corporate.json                 # Classic corporate (legacy)
│   │   └── dark-mode.json                 # Classic dark (legacy)
│   ├── layouts/
│   │   └── dashboard-2col.json            # Layout templates
│   └── dax-patterns/
│       ├── time-intelligence.json         # 12 time intelligence patterns
│       └── kpis.json                      # 10 KPI status patterns
│
├── templates/default-theme/               # Default theme source files
│   ├── modern-fintech.json
│   ├── modern-fintech-dark.json
│   ├── time-intelligence.json
│   ├── kpis.json
│   └── layouts.json
│
├── kpi-packs/                             # Industry-specific KPI templates
│   ├── education/                         # Enrollment, ADA, graduation
│   ├── finance/                           # Revenue, margin, budget variance
│   ├── operations-sre/                    # Success rate, SLA, MTTR
│   ├── sales-marketing/                   # Pipeline, conversion, CAC
│   └── healthcare/                        # Patient volume, readmission
│
├── ai-orchestration/
│   ├── skills/
│   │   └── powerbi-designer.md           # Main skill (onboarding + generation)
│   ├── prompts/
│   │   └── system-prompt.md              # System prompt template
│   └── workflows/
│       └── generate-report.md            # Step-by-step workflow
│
├── incoming/                              # Drop .pbip files here for extraction
│
├── examples/
│   ├── report-1-sales-dashboard/          # Education/ADA dashboard
│   └── report-2-operational/              # Data engineering pipeline obs
│
├── scripts/
│   ├── setup-mcp.sh                      # One-command MCP setup
│   └── validate-pbip.py                  # PBIP validation utility
│
└── docs/
    ├── DESIGN_SYSTEM.md                   # Full design system reference
    ├── GOTCHAS.md                         # MCP gotchas and workarounds
    ├── SETUP.md                           # Detailed setup guide
    ├── THEME_TOGGLE.md                    # Light/dark toggle implementation
    └── FUAM_INTEGRATION.md               # Future: tenant-wide monitoring
```

## KPI Packs

| Pack | Key Metrics |
|------|-------------|
| Education | Enrollment, ADA Rate, Graduation Rate, Chronic Absenteeism, Suspension Rate, Teacher Retention |
| Finance | Revenue, Gross Margin, OpEx, Budget Variance, EBITDA, Cash Runway |
| Sales/Marketing | Pipeline, Conversion Rate, CAC, LTV, Win Rate, MQL→SQL |
| Healthcare | Patient Volume, Readmission Rate, Bed Occupency, Avg Length of Stay |
| Operations/SRE | Success Rate, SLA Compliance, Failed Runs, MTTR, Incidents |

Each pack includes:
- Pre-built DAX measures with field mapping
- Recommended layouts and visual configurations
- Conditional formatting rules with industry-appropriate thresholds

## The Stack

- **[powerbi-report-mcp](https://github.com/jonathan-pap/powerbi-report-mcp)** — 56 tools for building .pbip reports
- **[powerbi-modeling-mcp](https://github.com/microsoft/powerbi-modeling-mcp)** — Semantic model management
- **[fabric-cli](https://github.com/microsoft/fabric-cli)** — Cloud deployment
- **Claude Code / Cursor** — AI orchestration

## Roadmap

- [x] Fintech-grade design system (light + dark)
- [x] Light/dark theme toggle via bookmarks
- [x] 5 industry KPI packs with field mapping
- [x] Dual-mode onboarding (conversational + wizard)
- [x] Custom visual recommendations per report type
- [x] 12 time intelligence DAX patterns
- [x] 10 KPI status DAX patterns
- [ ] FUAM integration for tenant-wide monitoring
- [ ] CI/CD pipeline for automated deployment
- [ ] Mobile-optimized layout generation

## License

MIT — Use it, fork it, make it yours.
