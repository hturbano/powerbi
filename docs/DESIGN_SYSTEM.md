# Design System

This document describes the Power BI design system encoded in this repository.

## Source

The design system was extracted from a production .pbip report that contains multiple themes and visual configurations. All color values, typography settings, and layout specifications below are derived from that report's actual JSON definitions.

## Themes

### Corporate Theme
- **File**: `design-system/themes/corporate.json`
- **Use for**: All business-facing reports, executive dashboards, school/education reports
- **Source**: Extracted from production .pbip

### Dark Mode Theme
- **File**: `design-system/themes/dark-mode.json`
- **Use for**: Engineering dashboards, data pipeline observability, operational reports
- **Source**: Extracted from production .pbip

## Color Palette

*Values to be extracted from the provided .pbip file.*

| Token | Hex Value | Usage |
|-------|-----------|-------|
| primary | TBD | Headers, primary buttons, key metrics |
| secondary | TBD | Secondary elements, borders, subtle UI |
| accent | TBD | Highlights, call-to-action, selections |
| success | TBD | Positive trends, passing KPIs, on-track |
| warning | TBD | At-risk items, approaching thresholds |
| danger | TBD | Failing KPIs, critical alerts, off-track |
| neutral | TBD | Secondary text, dividers, disabled states |
| background | TBD | Report canvas background |
| surface | TBD | Card backgrounds, alternating rows |

## Typography

*Values to be extracted from the provided .pbip file.*

| Element | Font | Size (px) | Weight |
|---------|------|-----------|--------|
| Title | TBD | TBD | Bold |
| Subtitle | TBD | TBD | Semibold |
| Card Value | TBD | TBD | Bold |
| Card Label | TBD | TBD | Regular |
| Axis Labels | TBD | TBD | Regular |
| Legend | TBD | TBD | Regular |
| Tooltip | TBD | TBD | Regular |

## Layout Templates

### Dashboard 2-Column (`layouts/dashboard-2col.json`)
- **Best for**: Executive dashboards, summary reports
- **Structure**: KPI cards in top row (full width), two-column grid for charts below
- **Page size**: 1280 x 720
- **Max visuals**: 8-10

### KPI Cards (`layouts/kpi-cards.json`)
- **Best for**: Scorecard views, status dashboards
- **Structure**: Grid of card visuals with conditional formatting
- **Page size**: 1280 x 720
- **Max visuals**: 12-15 cards

### Detail Page (`layouts/detail-page.json`)
- **Best for**: Drill-through pages, detailed analysis
- **Structure**: Left panel for detail table, right panel for supporting charts
- **Page size**: 1280 x 720
- **Max visuals**: 4-6

## DAX Patterns

See `design-system/dax-patterns/` for reusable DAX measure definitions.

### Time Intelligence
- `time-intelligence.json` — YTD, MTD, QTD, YoY, MoM patterns

### KPIs
- `kpis.json` — Standard KPI definitions with status calculations

## How to Update

To update the design system:

1. Edit the .pbip file with your changes in Power BI Desktop
2. Extract the relevant JSON sections (theme, visual configs, layout)
3. Update the corresponding JSON files in `design-system/`
4. Update this documentation with new values
5. Run `python scripts/validate-pbip.py examples/<report>` to verify
