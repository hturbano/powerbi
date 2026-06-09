# Example Report 2: Data Pipeline Observability Dashboard

**Domain**: Data Engineering / Operations
**Layout**: kpi-cards
**Theme**: dark-mode

## Overview

An engineering-facing dashboard monitoring data pipeline health across the organization. Tracks job failures, SLA compliance, refresh history, and data quality metrics.

## Pages

### Page 1: Pipeline Health Overview
- **KPI Cards** (top row):
  - Jobs Running (card)
  - Jobs Failed Today (card, red if > 0)
  - Jobs Succeeded Today (card, green)
  - Overall Success Rate % (card, conditional formatting)

- **Charts**:
  - Left: Success/Fail Trend (stacked bar, last 14 days)
  - Right: Failures by Pipeline (bar chart, sorted by count)
  - Bottom: Refresh Duration Trend (line chart, avg duration over time)

### Page 2: Job Detail
- Pipeline selector slicer
- Job run history table (start time, end time, duration, status)
- Failure details with error messages
- SLA compliance indicator per pipeline

### Page 3: Data Quality
- Data quality score by source (gauge visuals)
- Row count trends (expected vs actual)
- Schema change detection alerts
- Freshness indicators (time since last refresh)

## Data Sources
- Pipeline orchestration metadata (Airflow/Databricks/ADF)
- Job run logs
- Data quality monitoring tables
- SLA configuration reference

## Key DAX Measures
- `Success Rate = DIVIDE(COUNT(SuccessRuns), COUNT(AllRuns), 0)`
- `Avg Refresh Duration = AVERAGE(DurationMinutes)`
- `SLA Compliance = IF([AvgDuration] <= [SLATarget], "Met", "Breached")`
- `Days Since Last Refresh = DATEDIFF(MAX(RefreshDate), TODAY(), DAY)`

## Design Notes
- Uses dark mode theme (reduced eye strain for ops teams)
- Red/green status indicators throughout
- Auto-refresh friendly layout
- Job drill-through from summary to detail

## Files
To be populated after design system extraction from .pbip:
- `definition/report.json` — report layout and visuals
- `design-system/themes/dark-mode.json` — theme extracted to this location
