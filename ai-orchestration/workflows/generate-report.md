# Power BI Report Generation Workflow

## Overview

This workflow describes how to go from a data source and a description to a finished Power BI report using the design system and AI orchestration.

## Prerequisites

- Claude Code or Cursor installed
- powerbi-report-mcp configured in MCP settings
- powerbi-modeling-mcp configured in MCP settings (for semantic model work)
- This repo cloned locally

## Workflow

### Phase 1: Discovery

**Input**: User describes what they need

Ask clarifying questions:
1. What business question does this report answer?
2. Who is the audience?
3. What data source(s) will this use?
4. What time period/granularity?
5. What are the 3-5 most important metrics?

**Output**: A report specification document

### Phase 2: Design

**Input**: Report specification

1. Select the appropriate layout template from `design-system/layouts/`
2. Select the appropriate theme from `design-system/themes/`
3. Map metrics to visual types (see visual standards in skill)
4. Define the page structure (rows, columns, visual placement)
5. Identify required DAX measures and select patterns from `design-system/dax-patterns/`

**Output**: A design document with visual layout and measure definitions

### Phase 3: Generation

**Input**: Design document

Using powerbi-report-mcp:

```
1. Create .pbip project structure
2. Apply theme JSON to report definition
3. Create pages per layout template
4. Add visuals with correct types and positions
5. Configure visual formatting (titles, labels, legends, colors)
6. Set up slicers and filters
7. Configure cross-filtering and interactions
```

Using powerbi-modeling-mcp:

```
1. Define base measures from source columns
2. Add time intelligence measures (YTD, MoM, YoY)
3. Add KPI status measures
4. Validate all measures
```

**Output**: A complete .pbip file

### Phase 4: Validation

**Input**: Generated .pbip

1. Run `python scripts/validate-pbip.py <path-to-report>`
2. Check all visuals use theme colors (no hardcoded colors)
3. Verify no invalid visual types (especially stackedBarChart)
4. Confirm all actionButton visuals have howCreated field
5. Test filter configurations use DAX format
6. Review DAX measures for correctness

**Output**: Validation report with any issues to fix

### Phase 5: Iteration

**Input**: Validation report

Fix any issues found, then re-validate. Common fixes:
- Replace invalid visual types
- Add missing howCreated fields
- Update hardcoded colors to theme references
- Fix DAX syntax errors

**Output**: Clean, validated .pbip ready for deployment

### Phase 6: Deployment (Optional)

**Input**: Validated .pbip

Using fabric-cli:
```bash
# Export to Fabric workspace
fab report import --workspace <workspace-id> --file <path-to-pbip>

# Or deploy via CI/CD pipeline
# See fabric-cli docs for pipeline integration
```

**Output**: Report live in Fabric workspace

## Prompt Templates

### New Report Prompt

```
Build a Power BI report with the following specifications:

Business Question: [question]
Audience: [audience]
Data Source: [source]
Time Granularity: [granularity]
Key Metrics: [metric1], [metric2], [metric3]

Use the [corporate/dark] theme from design-system/themes/
Use the [dashboard-2col/kpi-cards/detail-page] layout from design-system/layouts/
Follow all visual standards from ai-orchestration/skills/powerbi-designer.md
```

### Theme Application Prompt

```
Apply the [theme-name] theme to the report at [path].
Update all visuals to use the theme color palette.
Update all typography to match the theme font specifications.
```

### DAX Generation Prompt

```
Generate DAX measures for the following metrics using patterns from design-system/dax-patterns/:

Base measures: [list of base measures]
Time intelligence needed: [YTD/MTD/YoY/MoM]
KPI targets: [list of targets for status calculations]
```
