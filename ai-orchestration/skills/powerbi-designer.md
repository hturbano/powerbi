---
name: powerbi-designer
description: Generate production-grade Power BI reports using a fintech-grade design system. Includes KPI packs for multiple industries, light/dark theme toggle, and conversational + wizard onboarding. When a user wants to build, configure, or set up a Power BI report factory, use this skill.
author: hturbano
---

# Power BI Designer

A Claude Code and Cursor skill for generating production-grade Power BI reports using a modern fintech-grade design system, industry-specific KPI packs, MCP tooling, and a dual-mode onboarding flow.

## Initialization Check

When this skill is first loaded in a project, run this check:

1. Does `design-system/themes/modern-fintech.json` exist AND have no `"TBD"` values?
2. Does `design-system/themes/modern-fintech-dark.json` exist AND have no `"TBD"` values?
3. Does at least one KPI pack exist in `kpi-packs/`?

**If ALL are true**: Skip onboarding. The factory is ready. Proceed to report generation.

**If ANY are missing or contain "TBD"**: Enter onboarding mode.

## Onboarding Mode

When the factory is not fully configured, offer the user:

```
Welcome to the Power BI Report Factory.

It looks like this project needs to be set up.
How would you like to get started?

  [A] I have an existing .pbip file — extract the design system from it
  [B] I want to build a design system from scratch — guide me through it
  [C] Use the default fintech theme — get me started immediately

Choose A, B, or C. Or type "wizard" for a step-by-step guided setup.
```

### Path A: Extract from Existing .pbip

Same as before — drop .pbip into `incoming/`, extract design system.

### Path B: Build from Scratch

Interactive Q&A to build a custom design system from brand specs.

### Path C: Use Default Fintech Theme

Installs the complete Modern Fintech theme (light + dark) with theme toggle:

```bash
cp templates/default-theme/modern-fintech.json design-system/themes/
cp templates/default-theme/modern-fintech-dark.json design-system/themes/
cp templates/default-theme/*.json design-system/dax-patterns/
```

### Wizard Mode

If the user types "wizard", enter a structured step-by-step flow:

```
Step 1/5: Choose Your Theme
  [1] Modern Fintech (default — clean, bold, data-dense)
  [2] Corporate Blue (traditional professional)
  [3] Custom (I'll provide my brand colors)

Step 2/5: Choose Your KPI Pack(s)
  Select one or more industry packs:
  [1] Education (enrollment, ADA, graduation rate)
  [2] Finance (revenue, margin, budget variance)
  [3] Sales/Marketing (pipeline, conversion, CAC, LTV)
  [4] Healthcare (patient volume, readmission, bed occupancy)
  [5] Operations/SRE (success rate, SLA, MTTR, incidents)
  [6] Generic (works with any data)

Step 3/5: Theme Toggle
  Enable light/dark theme toggle? [Y/n]
  This adds a bookmark-based toggle button to switch between themes.

Step 4/5: Report Domain
  What is the primary domain for this report?
  The skill will generate appropriate example visuals and layouts.

Step 5/5: Confirm
  Summary of choices:
    Theme: Modern Fintech
    KPI Pack(s): Education + Operations
    Toggle: Enabled
    Domain: Education

  Confirm? [Y/n]
```

After confirmation, scaffold all selected files and complete setup.

## Design System Reference

### Default Theme: Modern Fintech

A fintech-grade visual style inspired by Credit Karma and TurboTax. Key characteristics:

- **Bold KPI cards** — large values (36px), uppercase labels, clean hierarchy
- **Deep navy primary** (#0D1B2A) with **vibrant teal accent** (#00C9A7)
- **Rounded corners** (12px) with subtle shadows
- **Generous whitespace** — 24px margins, 32px section gaps
- **Inter font family** with tight letter-spacing for titles
- **Data-dense but clean** — maximal insights per pixel without clutter

### Color Tokens

| Token | Light | Dark | Usage |
|-------|-------|------|-------|
| primary | #0D1B2A | #E8ECF1 | Headers, key text |
| accent | #00C9A7 | #00E4BA | Highlights, positive |
| success | #00C9A7 | #00E4BA | Passing metrics |
| warning | #FFB800 | #FFD042 | At-risk items |
| danger | #FF4757 | #FF6B7A | Failing metrics |
| background | #F8F9FC | #0A1628 | Canvas |
| surface | #FFFFFF | #111D30 | Cards |
| text | #0D1B2A | #E8ECF1 | Primary text |

### Typography

| Element | Size | Weight | Letter-Spacing |
|---------|------|--------|----------------|
| Hero | 48px | Extrabold (800) | -0.02em |
| Title | 22px | Semibold (600) | -0.02em |
| Card Value | 36px | Bold (700) | normal |
| Card Label | 11px | Semibold (600) | 0.05em |
| Body | 14px | Regular (400) | normal |

### Cards

```
KPI Card:
  - Background: #FFFFFF (light) / #111D30 (dark)
  - Border Radius: 12px
  - Padding: 20px
  - Shadow: 0 1px 3px rgba(0,0,0,0.04)
  - Value: 36px Bold, #0D1B2A
  - Label: 11px Semibold uppercase, #576574

Chart Card:
  - Same as KPI card with 20px internal padding
  - Title: 15px Semibold
```

### Approved Visual Types

| Visual | Use Case | Notes |
|--------|----------|-------|
| card | Single KPI | Large value + trend indicator |
| multiRowCard | KPI row | Max 4 cards per row |
| barChart | Comparisons | USE barChart, NEVER stackedBarChart |
| lineChart | Trends | Smooth lines, minimal markers |
| donutChart | Part-to-whole | Max 5 slices |
| stackedBarChart | Composition | NEVER use — use barChart + stacking |
| matrix | Cross-tab | Heat-map style, alternating rows |
| table | Detail data | Header uppercase, alternating rows |
| gauge | Progress | Min/max from data |
| slicer | Filters | Dropdown mode for >10 items |
| waterfallChart | Variance | P&L bridges, decomposition |

### Conditional Formatting

```
KPI Status:
  Green  (#00C9A7): >= target or >= 95% of target
  Amber  (#FFB800): Within 5-15% of target
  Red    (#FF4757): < 85% of target or critically low

Trend Arrows:
  Up   ▲ (#00C9A7)
  Flat ─ (#8395A7)
  Down ▼ (#FF4757)
```

### Theme Toggle

Reports should include a light/dark theme toggle by default:

1. Two bookmarks: `Theme_Light` and `Theme_Dark`
2. Toggle button that switches between bookmarks
3. Both themes defined in `design-system/themes/`
4. See `docs/THEME_TOGGLE.md` for implementation details

## KPI Packs

KPI packs provide industry-specific templates with field mapping. Located in `kpi-packs/`.

### Available Packs

| Pack | Directory | Key Metrics |
|------|-----------|-------------|
| Education | `kpi-packs/education/` | Enrollment, ADA, Graduation, Chronic Absenteeism, Suspension Rate, Teacher Retention |
| Finance | `kpi-packs/finance/` | Revenue, Gross Margin, OpEx, Budget Variance, EBITDA, Cash Runway |
| Sales/Marketing | `kpi-packs/sales-marketing/` | Pipeline, Conversion Rate, CAC, LTV, Win Rate, MQL→SQL |
| Healthcare | `kpi-packs/healthcare/` | Patient Volume, Readmission Rate, Bed Occupancy, Avg Length of Stay |
| Operations/SRE | `kpi-packs/operations-sre/` | Success Rate, SLA Compliance, Failed Runs, MTTR, Incidents |

### Using a KPI Pack

1. Select appropriate pack(s) during onboarding or report generation
2. The skill maps user's data columns to the pack's field requirements
3. Required fields must be mapped; optional fields enhance the report
4. Generated DAX measures follow the pack's base expressions with user's actual column names

### Field Mapping Flow

```
To use the Education KPI pack, I need to map your data:

Required:
  1. Date column → What column contains the date? [Date]
  2. Student ID column → What uniquely identifies students? [StudentID]

Optional (recommended):
  3. Campus column → Breakdown by campus? [CampusName]
  4. Grade column → Grade level breakdown? [GradeLevel]

Mapping complete. 6 KPIs will be generated with DAX measures tied to your columns.
```

## DAX Patterns

All DAX measures should use the patterns from `design-system/dax-patterns/`.

### Time Intelligence

```dax
YTD = TOTALYTD([Base], 'Date'[Date])
MTD = TOTALMTD([Base], 'Date'[Date])
YoY_Change = DIVIDE([Base] - [YoY], ABS([YoY]), 0)
MoM_Change = DIVIDE([Base] - [MoM], ABS([MoM]), 0)
Rolling_7d = AVERAGEX(DATESINPERIOD('Date'[Date], LASTDATE('Date'[Date]), -7, DAY), [Base])
Rolling_30d = AVERAGEX(DATESINPERIOD('Date'[Date], LASTDATE('Date'[Date]), -30, DAY), [Base])
```

### KPI Status

```dax
Status =
VAR Actual = [Base]
VAR Target = [Target]
VAR Pct = DIVIDE(Actual, Target, 0)
RETURN SWITCH(TRUE(),
    Pct >= 1, "On Track",
    Pct >= 0.9, "At Risk",
    "Off Track"
)

Status_Color =
VAR Pct = DIVIDE([Base], [Target], 0)
RETURN SWITCH(TRUE(),
    Pct >= 1, "#00C9A7",
    Pct >= 0.9, "#FFB800",
    "#FF4757"
)
```

### Pipeline / Operations

```dax
Success_Rate = DIVIDE(COUNTROWS(FILTER(Runs, [Status] IN {"Success","Succeeded"})), COUNTROWS(Runs), 0)
SLA_Compliance = DIVIDE(COUNTROWS(FILTER(Runs, [Duration] <= [SLATarget])), COUNTROWS(Runs), 0)
MTTR = AVERAGEX(FILTER(Incidents, [Resolved] = TRUE()), DATEDIFF([Detected], [Resolved], MINUTE))
```

## Report Generation Workflow

### Step 1: Understand Requirements

Before generating, confirm:
- What is the business question?
- Who is the audience? (executives, analysts, engineers)
- What is the data source?
- What time granularity?
- Which KPI pack applies? (or generic)

### Step 2: Select Layout

Choose from `design-system/layouts/`:
- `dashboard-2col` — Executive dashboard (KPIs top, charts below)
- `kpi-cards` — Scorecard view (grid of KPIs)
- `detail-page` — Drill-through detail
- `fintech-summary` — Fintech-style dense summary (NEW)

### Step 3: Map Data Fields

If using a KPI pack:
1. Identify the user's column names for each required field
2. Ask about optional fields to enhance the report
3. Substitute field names into DAX patterns

### Step 4: Generate Report

Using powerbi-report-mcp:
1. Connect to the target report with `pbir_set_report` (path to the `.pbip`/`.Report` folder). The report must already exist — if there is none, create a blank `.pbip` in Power BI Desktop first. `powerbi-report-mcp` edits an existing report; it does not scaffold one.
2. Apply Modern Fintech theme (light as default, dark as alternate)
3. Generate pages per layout template
4. Apply fintech card styling (rounded corners, shadows, bold values)
5. Configure conditional formatting per design system
6. Add theme toggle bookmarks and button

### Step 5: Add DAX Measures

Using powerbi-modeling-mcp:
1. Create base measures from mapped columns
2. Add time intelligence measures
3. Add KPI status measures with conditional formatting
4. Validate all measures

### Step 6: Configure Interactivity

1. Add slicers for key dimensions
2. Configure cross-filtering
3. Set up drill-through pages
4. Add theme toggle bookmark actions

### Step 7: Validate

```bash
python scripts/validate-pbip.py <report-path>
```

Check:
- All visuals use theme colors
- No stackedBarChart (use barChart)
- All actionButton visuals have howCreated
- Theme toggle bookmarks exist
- KPI card styling matches fintech specs

## Custom Visual Recommendations

For reports that need to go beyond built-in visuals, recommend these certified AppSource visuals based on report type:

| Report Type | Recommended Visual | Why |
|-------------|-------------------|-----|
| Funnels / Conversion | Funnel Chart by Powerviz | Native funnel support with drop-off calcs |
| Hierarchies | Chiclet Slicer by Microsoft | Better UX for hierarchical filtering |
| Infographics | Infographic Designer by Microsoft | Rich visual embellishments |
| Smart Narratives | Smart Narrative by Microsoft | Auto-generated text insights |
| Gantt / Timeline | Gantt by Microsoft | Project timeline views |
| KPIs with history | Bullet Chart by Microsoft | Compact KPI + trend + target |

To use: Ask the user if they want custom visuals. If yes, generate the visual configuration with the appropriate visualType for the custom visual. Document which custom visuals are needed in the report README.

## Gotchas

See `docs/GOTCHAS.md` for the full list. Key ones:

- **stackedBarChart is invalid** — use `barChart` with stacked orientation
- **actionButton needs howCreated** — every action button must include `"howCreated": "User"`
- **Filters use DAX format** — not REST API format
- **Formatting property names vary** across visual types
- **PBIR is now default** — aligns with this skill's approach
- **Theme toggle bookmarks** — keep "Data" unchecked, only "Display"

## Project Structure

```
report-name/
├── definition/
│   └── report.json       # Report layout and visuals (PBIR format)
├── model.tmdl            # Semantic model (if custom)
└── [Content_Types].xml   # Package definition
```

## Author

hturbano
