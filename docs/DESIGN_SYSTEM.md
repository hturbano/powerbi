# Design System

This document describes the Power BI design system encoded in this repository.

## Source

The design system can be:
- **Extracted from an existing .pbip file** via the onboarding flow (Path A)
- **Built from scratch** via the interactive onboarding flow (Path B)  
- **Installed from the default professional theme** (Path C)

All themes are maintained by hturbano.

## Themes

### Corporate Theme
- **File**: `design-system/themes/corporate.json`
- **Use for**: All business-facing reports, executive dashboards, school/education reports
- **Style**: Clean and professional with blue primary and semantic status colors

### Dark Mode Theme
- **File**: `design-system/themes/dark-mode.json`
- **Use for**: Engineering dashboards, data pipeline observability, operational reports
- **Style**: Dark backgrounds with bright accents, optimized for reduced eye strain

## Color Palette (Corporate)

| Token | Hex Value | Usage |
|-------|-----------|-------|
| primary | #1A73E8 | Headers, primary buttons, key metrics |
| primaryDark | #1557B0 | Hover states, emphasis |
| primaryLight | #E8F0FE | Backgrounds for primary elements |
| secondary | #5F6368 | Secondary elements, borders |
| accent | #F9AB00 | Highlights, call-to-action |
| success | #34A853 | Positive trends, passing KPIs |
| warning | #FBBC04 | At-risk items, approaching thresholds |
| danger | #EA4335 | Failing KPIs, critical alerts |
| neutral | #9AA0A6 | Secondary text, dividers |
| background | #FFFFFF | Report canvas |
| surface | #F8F9FA | Card backgrounds |
| text | #202124 | Primary text |
| textSecondary | #5F6368 | Secondary text |

## Typography

| Element | Font | Size (px) | Weight |
|---------|------|-----------|--------|
| Title | Segoe UI | 20 | Bold (700) |
| Subtitle | Segoe UI | 14 | Semibold (600) |
| Card Value | Segoe UI | 28 | Bold (700) |
| Card Label | Segoe UI | 12 | Regular (400) |
| Axis Labels | Segoe UI | 11 | Regular (400) |
| Legend | Segoe UI | 11 | Regular (400) |

## Layout Grid

```
Page Size:       1280 x 720
Margins:         20px all sides
Gutter:          16px between visual containers
Card Padding:    12px internal
Border Radius:   4px
```

## Layout Templates

### dashboard-2col
- **Best for**: Executive dashboards, summary reports
- **Structure**: KPI cards in top row (4 cards), two-column grid for charts below
- **Max visuals**: 8-10

### kpi-cards
- **Best for**: Scorecard views, status dashboards
- **Structure**: Grid of card visuals with conditional formatting
- **Max visuals**: 12-15 cards

### detail-page
- **Best for**: Drill-through pages, detailed analysis
- **Structure**: Left panel (40%) for detail table, right panel (60%) for supporting charts

## DAX Patterns

### Time Intelligence (`design-system/dax-patterns/time-intelligence.json`)
- YTD, MTD, QTD — Running totals
- YoY, MoM — Period-over-period comparisons
- Rolling 7-day, 30-day — Moving averages
- Running Total — Cumulative sum

### KPIs (`design-system/dax-patterns/kpis.json`)
- KPI Status — On Track / At Risk / Off Track
- KPI Status Color — Hex codes for conditional formatting
- KPI Trend — Up / Down / Flat
- SLA Compliance — Met / Breached
- Success Rate / Failure Rate — Pipeline metrics
- Rank — Category ranking by measure

## How to Customize

1. Edit the theme JSON files in `design-system/themes/`
2. Edit DAX patterns in `design-system/dax-patterns/`
3. Edit layout templates in `design-system/layouts/`
4. Update this documentation with new values
5. Run `python scripts/validate-pbip.py examples/<report>` to verify

## Author

hturbano
