# Power BI Designer Skill

A Claude Code / Cursor skill for generating production-grade Power BI reports using a codified design system and MCP tooling.

## When to Use This Skill

Use this skill when:
- Building a new Power BI report from scratch
- Modifying or enhancing an existing .pbip report
- Applying the design system theme to any report
- Generating DAX measures for common patterns (time intelligence, KPIs)
- Setting up report layouts and visual configurations

Do NOT use this skill for:
- Semantic model design (use powerbi-modeling-mcp directly)
- Cloud deployment operations (use fabric-cli)
- Data source configuration or gateway management

## Design System

All reports MUST follow the design system defined in `design-system/`. This ensures visual consistency across all reports generated through this factory.

### Theme Application

When building any report, start by applying the appropriate theme:

1. **Corporate theme** (`design-system/themes/corporate.json`) — Default for all business-facing reports
2. **Dark mode** (`design-system/themes/dark-mode.json`) — For operational/engineering dashboards

The theme JSON is applied to the report's `definition/report.json` section. See `design-system/themes/` for the full color palette and typography specs.

### Color Palette

```
Primary:    [EXTRACTED FROM .PBIP]
Secondary:  [EXTRACTED FROM .PBIP]
Accent:     [EXTRACTED FROM .PBIP]
Success:    #107C10  (green — positive trends, passing metrics)
Warning:    #FFB900  (amber — at-risk, approaching threshold)
Danger:     #D13438  (red — failing, critical, below threshold)
Neutral:    #605E5C  (gray — secondary text, borders)
Background: #FFFFFF  (white — report canvas)
Surface:    #F3F2F1  (light gray — card backgrounds)
```

### Typography

```
Font Family:    [EXTRACTED FROM .PBIP]
Title:          [SIZE]px, Bold
Subtitle:       [SIZE]px, Semibold
Card Value:     [SIZE]px, Bold
Card Label:     [SIZE]px, Regular
Axis Labels:    [SIZE]px, Regular
Legend:         [SIZE]px, Regular
```

### Layout Grid

```
Page Size:       1280 x 720 (standard dashboard)
Margins:         20px all sides
Gutter:          16px between visual containers
Card Padding:    12px internal
Border Radius:   4px (cards), 0px (charts)
```

## Visual Standards

### Approved Visual Types

| Visual | Use Case | Notes |
|--------|----------|-------|
| barChart | Comparisons across categories | NEVER use stackedBarChart (invalid type) |
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
2. **Data labels**: On for cards and KPIs. Off for dense charts (line, bar with >10 categories).
3. **Legends**: Position right for bar/line charts. Position bottom for pie charts.
4. **Colors**: Use theme palette only. Never hardcode colors in individual visuals.
5. **Tooltips**: Enable for all charts. Configure tooltip page for complex visuals.
6. **Action buttons**: Must include `howCreated` field in JSON definition.

### Conditional Formatting Rules

- **KPIs**: Green if >= target, Amber if within 10% of target, Red if < 90% of target
- **Trend arrows**: Up green, Down red, Flat neutral
- **Tables**: Alternating row colors from theme surface color
- **Heat maps**: Use sequential palette from theme

## DAX Patterns

All DAX measures MUST use the patterns from `design-system/dax-patterns/`. Key patterns:

### Time Intelligence

```dax
// Year-to-Date
YTD Measure = TOTALYTD([Base Measure], 'Date'[Date])

// Month-over-Month
MoM Change = 
VAR CurrentMonth = [Base Measure]
VAR PreviousMonth = CALCULATE([Base Measure], DATEADD('Date'[Date], -1, MONTH))
RETURN DIVIDE(CurrentMonth - PreviousMonth, PreviousMonth, 0)

// Year-over-Year
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

See [docs/GOTCHAS.md](docs/GOTCHAS.md) for the full list of MCP-specific gotchas. Key ones:

- **stackedBarChart is invalid** — use `barChart` with stacked orientation in the format section
- **actionButton needs howCreated** — every action button must include `"howCreated": "User"` in its JSON
- **Filters use DAX format** — not REST API format. Use `[Column] = "Value"` syntax
- **Formatting property names vary** — what's `fontColor` in one visual is `color` in another. Always check the visual-specific schema
- **PBIR vs TMSL** — this skill uses PBIR (Power BI Report) format, not TMSL. Don't mix them.

## File Structure

When generating a new report, create:

```
report-name/
├── report.json          # Main report definition (PBIR format)
├── definition/
│   └── report.json      # Report layout and visuals
├── model.tmdl           # Semantic model (if custom)
└── [Content_Types].xml  # Package definition
```

## Examples

See `examples/` for complete reports built with this system:
- `report-1-sales-dashboard/` — Education/ADA dashboard with KPI cards and trends
- `report-2-operational/` — Data engineering pipeline observability
