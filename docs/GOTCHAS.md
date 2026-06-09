# Power BI MCP Gotchas

**Author**: hturbano | **Repo**: https://github.com/hturbano/powerbi

A comprehensive list of gotchas, quirks, and workarounds when using MCP tools to generate Power BI reports.

## Visual Type Gotchas

### stackedBarChart is Invalid

**Problem**: Using `stackedBarChart` as a visual type causes errors.
**Fix**: Use `barChart` with stacked orientation in the format section:
```json
"visualType": "barChart",
"format": { "orientation": "stacked" }
```

### actionButton Requires howCreated

**Problem**: Action buttons fail to render without the `howCreated` field.
**Fix**: Always include:
```json
{ "visualType": "actionButton", "howCreated": "User" }
```

### Visual Type Names Are Case-Sensitive

**Problem**: `barchart` fails but `barChart` works.
**Fix**: Always use exact casing: barChart, lineChart, pieChart, etc.

## Filter Gotchas

### Filters Use DAX Format, Not REST API Format

**Problem**: REST API filter format doesn't work in PBIR.
**Fix**: Use DAX filter syntax with from/where/condition structure.

### Date Filters Need Special Handling

**Problem**: Relative date filters need dynamic DAX.
**Fix**: Use DAX date functions rather than hardcoded dates.

## Formatting Gotchas

### Property Names Vary Across Visual Types

**Problem**: `fontColor` in one visual is `color` in another.
**Fix**: Always check the visual-specific schema or inspect a working .pbip.

### Color Format

**Problem**: Wrong color format causes errors.
**Fix**: Use hex with alpha channel: `#AARRGGBB` or `#RRGGBB`.

## PBIP Structure Gotchas

### PBIR vs TMSL

**Problem**: Mixing report (PBIR) and model (TMSL) formats causes corruption.
**Fix**: Keep them separate. PBIR for report layout, TMSL for semantic model.

### [Content_Types].xml

**Problem**: Missing Content_Types.xml breaks the .pbip package.
**Fix**: Always include this file. Use the template from examples/.

## MCP Tool Gotchas

### Path Handling

**Problem**: Relative paths may resolve differently.
**Fix**: Always use absolute paths for .pbip file locations.

### Batch Operations

**Problem**: Too many rapid MCP calls cause timeouts.
**Fix**: Add small delays between batch visual creation calls.

### Visual Positioning

**Problem**: Visuals outside page bounds or overlapping cause issues.
**Fix**: Use the layout grid from the design system.

## DAX Gotchas

### DIVIDE vs / Operator

**Fix**: Always use `DIVIDE(numerator, denominator, alternateResult)`.

### Date Table Requirements

**Fix**: Mark your date table or use `CALENDARAUTO()`.

### Measure Dependencies

**Fix**: Build base measures first, then layer calculated measures on top.

## Deployment Gotchas

### fabric-cli Authentication

**Fix**: Run `fab auth login` before any deployment commands.

### Report Rebinding

**Fix**: Use `fab report rebind` after deployment to point to the correct model.
