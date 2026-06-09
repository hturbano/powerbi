# Power BI Report Generation Workflow

**Author**: hturbano | **Repo**: https://github.com/hturbano/powerbi

## Overview

This workflow describes how to go from a data source and a description to a finished Power BI report using the design system and AI orchestration.

## Prerequisites

- Claude Code or Cursor installed
- powerbi-report-mcp configured in MCP settings
- powerbi-modeling-mcp configured in MCP settings (for semantic model work)
- This repo cloned locally
- Design system set up (run onboarding: "Set up my Power BI report factory")

## Workflow

### Phase 1: Discovery

**Input**: User describes what they need

Ask clarifying questions:
1. What business question does this report answer?
2. Who is the audience?
3. What data source(s) will this use?
4. What time period/granularity?
5. What are the 3-5 most important metrics?
6. Which theme? (corporate or dark mode)

**Output**: A report specification

### Phase 2: Design

**Input**: Report specification

1. Select the appropriate layout template from `design-system/layouts/`
2. Select the appropriate theme from `design-system/themes/`
3. Map metrics to visual types (see visual standards in skill)
4. Define the page structure
5. Identify required DAX measures from `design-system/dax-patterns/`

**Output**: Design document with visual layout and measure definitions

### Phase 3: Generation

**Input**: Design document

Using powerbi-report-mcp:
1. Create .pbip project structure
2. Apply theme JSON to report definition
3. Create pages per layout template
4. Add visuals with correct types and positions
5. Configure visual formatting per visualDefaults in theme
6. Set up slicers and filters
7. Configure cross-filtering

Using powerbi-modeling-mcp:
1. Define base measures from source columns
2. Add time intelligence measures (YTD, MoM, YoY)
3. Add KPI status measures
4. Validate all measures

**Output**: Complete .pbip file

### Phase 4: Validation

**Input**: Generated .pbip

1. Run `python scripts/validate-pbip.py <path-to-report>`
2. Check all visuals use theme colors
3. Verify no invalid visual types
4. Confirm all actionButton visuals have howCreated field
5. Test filter configurations use DAX format

**Output**: Validation report with any issues to fix

### Phase 5: Iteration

Fix any issues found, then re-validate.

### Phase 6: Deployment (Optional)

Using fabric-cli:
```bash
fab report import --workspace <workspace-id> --file <path-to-pbip>
```

## Prompt Templates

### New Report

```
Build a Power BI report with:
Business Question: [question]
Audience: [audience]
Data Source: [source]
Time Granularity: [granularity]
Key Metrics: [metric1], [metric2], [metric3]
Theme: [corporate/dark]
```

### Quick Build

```
Build a [description] dashboard with:
- KPI cards for [metrics]
- [Chart type] for [metric] by [dimension]
- [Filter slicer]
- Use the [corporate/dark] theme
```
