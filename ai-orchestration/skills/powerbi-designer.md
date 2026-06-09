---
name: powerbi-designer
description: Generate production-grade Power BI reports using a codified design system. Includes onboarding flow for first-time setup. When a user wants to build, configure, or set up a Power BI report factory, use this skill.
author: hturbano
---

# Power BI Designer

A Claude Code and Cursor skill for generating production-grade Power BI reports using a codified design system, MCP tooling, and a conversational onboarding flow.

## Initialization Check

When this skill is first loaded in a project, run this check:

1. Does `design-system/themes/corporate.json` exist AND have no `"TBD"` values?
2. Does `design-system/themes/dark-mode.json` exist AND have no `"TBD"` values?
3. Does at least one example report exist with a populated `definition/report.json`?

**If ALL are true**: Skip onboarding. The factory is ready. Proceed to report generation.

**If ANY are missing or contain "TBD"**: Enter onboarding mode.

## Onboarding Mode

When the factory is not fully configured, offer the user three paths:

```
Welcome to the Power BI Report Factory.

It looks like this project needs to be set up before generating reports.
How would you like to configure your design system?

  [A] I have an existing .pbip file — extract the design system from it
  [B] I want to build a design system from scratch — guide me through it
  [C] Use a professional default theme — get me started immediately

Choose A, B, or C.
```

### Path A: Extract from Existing .pbip

**Step 1**: Ask the user to place their .pbip file (or the extracted `definition/report.json` from a .pbip) into the `incoming/` directory. Create this directory if it does not exist.

```
Please place your .pbip file (or its definition/report.json) into:
  incoming/

This can be:
  - A .pbip file (zip-based, rename .pbip to .zip if needed to extract)
  - Just the definition/report.json from inside a .pbip
  - A folder containing the extracted .pbip contents

When you're ready, let me know and I'll extract the design system.
```

**Step 2**: Once the user confirms the file is in `incoming/`, parse the report JSON and extract:

1. **Color palette**: Find all unique color values used across visuals, themes, and conditional formatting
2. **Typography**: Extract font family, sizes, and weights from visual headers, labels, and values
3. **Layout patterns**: Identify page dimensions, margins, and visual positioning patterns
4. **Visual defaults**: Catalog which visual types are used and their common formatting
5. **DAX measures**: Extract measure definitions and identify time intelligence patterns

**Step 3**: Generate the following files from the extraction:

```
design-system/
├── themes/
│   ├── corporate.json          ← Primary theme from .pbip
│   └── dark-mode.json          ← Inverted/dark variant
├── layouts/
│   ├── dashboard-2col.json     ← Based on most common layout
│   ├── kpi-cards.json          ← If KPI-style pages exist
│   └── detail-page.json        ← If drill-through pages exist
└── dax-patterns/
    ├── time-intelligence.json  ← Extracted time-based measures
    └── kpis.json               ← Extracted KPI patterns
```

**Step 4**: Update `docs/DESIGN_SYSTEM.md` with the extracted values.

**Step 5**: Run validation:
```bash
python scripts/validate-pbip.py incoming/
```

**Step 6**: Confirm completion:
```
Design system extracted successfully.

  Theme: [name]
  Colors: [N] unique colors found
  Fonts: [font family]
  Layouts: [N] layout patterns identified
  DAX patterns: [N] measures extracted

Your factory is ready. You can now generate reports.
```

### Path B: Build from Scratch

Guide the user through an interactive design system creation:

**Step 1 — Brand Colors**:
```
Let's build your design system. First, your brand colors.

Provide your brand colors in any of these formats:
  - Hex codes: #1A73E8, #34A853, #FBBC04, #EA4335
  - RGB: rgb(26, 115, 232)
  - Names: "our blue is #1A73E8, green is #34A853"

If you don't have specific brand colors, I'll use a professional
palette based on your industry. What industry is this for?
```

**Step 2 — Typography**:
```
Next, typography.

What font would you like to use?
  [1] Segoe UI (Power BI default, clean and modern)
  [2] Inter (popular, highly readable)
  [3] Roboto (Google-style, versatile)
  [4] Custom — tell me your font

What's the primary use case?
  [1] Executive dashboards (larger text, more spacing)
  [2] Analyst reports (denser, smaller text)
  [3] Mixed / not sure
```

**Step 3 — Visual Style**:
```
What visual style do you prefer?
  [1] Clean and minimal — lots of white space, thin borders
  [2] Modern and bold — saturated colors, strong contrast
  [3] Corporate and conservative — muted colors, traditional
  [4] Dark mode — dark backgrounds, bright accents
```

**Step 4 — Report Types**:
```
What types of reports will you primarily build?
  [1] Executive dashboards (KPIs, trends, high-level)
  [2] Operational dashboards (detailed, real-time, alerts)
  [3] Analytical reports (drill-through, exploration)
  [4] All of the above
```

**Step 5**: Generate all design system files from the responses. Apply industry-appropriate defaults for anything not specified.

**Step 6**: Confirm and validate.

### Path C: Use Default Theme

Drop in a complete, professional design system immediately:

**Step 1**: Copy the default theme files from `templates/default-theme/` into `design-system/themes/`:

```
cp templates/default-theme/corporate.json design-system/themes/corporate.json
cp templates/default-theme/dark-mode.json design-system/themes/dark-mode.json
```

**Step 2**: Copy default DAX patterns:
```
cp templates/default-theme/time-intelligence.json design-system/dax-patterns/time-intelligence.json
cp templates/default-theme/kpis.json design-system/dax-patterns/kpis.json
```

**Step 3**: Copy default layouts:
```
cp templates/default-theme/*.json design-system/layouts/
```

**Step 4**: Update `docs/DESIGN_SYSTEM.md` with the default theme values.

**Step 5**: Confirm:
```
Default professional theme installed.

  Theme: Modern Corporate
  Colors: Blue primary, green/amber/red semantic palette
  Font: Segoe UI
  Layouts: dashboard-2col, kpi-cards, detail-page
  DAX patterns: Time intelligence + KPI status

Your factory is ready. You can customize any of these files
or switch to a different theme at any time.
```

## Design System Reference

### Theme Application

When building any report, start by applying the appropriate theme:

1. **Corporate theme** (`design-system/themes/corporate.json`) — Default for all business-facing reports
2. **Dark mode** (`design-system/themes/dark-mode.json`) — For operational/engineering dashboards

### Approved Visual Types

| Visual | Use Case | Notes |
|--------|----------|-------|
| barChart | Comparisons across categories | NEVER use stackedBarChart |
| lineChart | Trends over time | Use with date hierarchy |
| card | Single KPI/metric | Use conditional formatting for status |
| multiRowCard | Multiple KPIs in a row | Max 5 cards per row |
| pieChart | Part-to-whole (limited) | Max 5 slices, use legend |
| table | Detailed data, drill-through | Enable word wrap, alternating rows |
| matrix | Cross-tabulated data | Use for heat-map style displays |
| gauge | Progress toward target | Min/max from data, not hardcoded |
| slicer | Filters | Use dropdown mode for >10 items |

### Visual Configuration Rules

1. **Titles**: Every visual has a title. Format: `[Metric Name] — [Time Period]` or `[Metric Name] by [Dimension]`
2. **Data labels**: On for cards and KPIs. Off for dense charts (line, bar with >10 categories)
3. **Legends**: Position right for bar/line charts. Position bottom for pie charts
4. **Colors**: Use theme palette only. Never hardcode colors in individual visuals
5. **Tooltips**: Enable for all charts. Configure tooltip page for complex visuals
6. **Action buttons**: Must include `howCreated` field in JSON definition

### Conditional Formatting Rules

- **KPIs**: Green if >= target, Amber if within 10% of target, Red if < 90% of target
- **Trend arrows**: Up green, Down red, Flat neutral
- **Tables**: Alternating row colors from theme surface color
- **Heat maps**: Use sequential palette from theme

## DAX Patterns

All DAX measures should use the patterns from `design-system/dax-patterns/`.

### Time Intelligence

```dax
YTD Measure = TOTALYTD([Base Measure], 'Date'[Date])

MoM Change =
VAR CurrentMonth = [Base Measure]
VAR PreviousMonth = CALCULATE([Base Measure], DATEADD('Date'[Date], -1, MONTH))
RETURN DIVIDE(CurrentMonth - PreviousMonth, PreviousMonth, 0)

YoY Change =
VAR CurrentPeriod = [Base Measure]
VAR PriorYear = CALCULATE([Base Measure], SAMEPERIODLASTYEAR('Date'[Date]))
RETURN DIVIDE(CurrentPeriod - PriorYear, PriorYear, 0)
```

### KPI Status

```dax
KPI Status =
VAR Actual = [Base Measure]
VAR Target = [Target Measure]
VAR PctOfTarget = DIVIDE(Actual, Target, 0)
RETURN
    SWITCH(
        TRUE(),
        PctOfTarget >= 1, "On Track",
        PctOfTarget >= 0.9, "At Risk",
        "Off Track"
    )
```

## Report Generation Workflow

### Step 1: Understand Requirements

Before generating, confirm:
- What is the business question this report answers?
- Who is the audience? (executives, analysts, engineers)
- What is the data source?
- What time granularity is needed? (daily, weekly, monthly)
- What are the key metrics/KPIs?

### Step 2: Select Layout

Choose from `design-system/layouts/`:
- `dashboard-2col.json` — Standard executive dashboard (KPI cards top, charts below)
- `kpi-cards.json` — KPI-focused (scorecard style)
- `detail-page.json` — Drill-through detail with supporting context

### Step 3: Generate Report Structure

Using powerbi-report-mcp:
1. Create new .pbip project structure
2. Apply theme from `design-system/themes/`
3. Set page size and layout grid
4. Add visuals per layout template
5. Configure visual formatting per design system standards

### Step 4: Add DAX Measures

Using powerbi-modeling-mcp:
1. Create base measures from data source fields
2. Add time intelligence measures using standard patterns
3. Add KPI status measures with conditional formatting
4. Validate all measures return expected results

### Step 5: Configure Interactivity

1. Add slicers for key dimensions (date, campus, department)
2. Configure cross-filtering between visuals
3. Set up drill-through pages where applicable
4. Add bookmarks for common views

### Step 6: Validate

Run `scripts/validate-pbip.py` to check:
- All visuals use theme colors
- No hardcoded values in measures
- All required fields present in .pbip JSON
- Visual types are valid (no stackedBarChart, etc.)

## Gotchas

See `docs/GOTCHAS.md` for the full list. Key ones:

- **stackedBarChart is invalid** — use `barChart` with stacked orientation
- **actionButton needs howCreated** — every action button must include `"howCreated": "User"`
- **Filters use DAX format** — not REST API format
- **Formatting property names vary** — across visual types, always check the schema
- **PBIR vs TMSL** — this skill uses PBIR format, not TMSL

## Project Structure

When generating a new report, create:

```
report-name/
├── definition/
│   └── report.json      # Report layout and visuals (PBIR format)
├── model.tmdl           # Semantic model (if custom)
└── [Content_Types].xml  # Package definition
```

## Examples

See `examples/` for complete reports built with this system:
- `report-1-sales-dashboard/` — Education/ADA dashboard with KPI cards and trends
- `report-2-operational/` — Data engineering pipeline observability
