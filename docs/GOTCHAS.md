# Power BI MCP Gotchas

A comprehensive list of gotchas, quirks, and workarounds when using MCP tools to generate Power BI reports.

## Visual Type Gotchas

### stackedBarChart is Invalid

**Problem**: Using `stackedBarChart` as a visual type causes errors.
**Fix**: Use `barChart` and configure stacking in the format section:
```json
"visualType": "barChart",
"format": {
    "orientation": "stacked"
}
```

### actionButton Requires howCreated

**Problem**: Action buttons fail to render without the `howCreated` field.
**Fix**: Always include:
```json
{
    "visualType": "actionButton",
    "howCreated": "User"
}
```

### Visual Type Names Are Case-Sensitive

**Problem**: `barchart` fails but `barChart` works.
**Fix**: Always use exact casing. See the approved visual types list in the skill file.

## Filter Gotchas

### Filters Use DAX Format, Not REST API Format

**Problem**: Filters configured in REST API format don't work in PBIR.
**Fix**: Use DAX filter syntax:
```json
{
    "filter": {
        "from": "TableName",
        "where": [
            {
                "condition": {
                    "operator": "eq",
                    "value": "FilterValue"
                }
            }
        ]
    }
}
```

### Date Filters Need Special Handling

**Problem**: Relative date filters (last 30 days, this month) need dynamic DAX.
**Fix**: Use DAX date functions in filter expressions rather than hardcoded dates.

## Formatting Gotchas

### Property Names Vary Across Visual Types

**Problem**: What's `fontColor` in one visual is `color` in another. What's `titleText` in one is `visualTitle` in another.
**Fix**: Always check the visual-specific schema. When in doubt, inspect a working .pbip file for the correct property names.

### Color Format

**Problem**: Colors must be in specific format.
**Fix**: Use hex format with alpha channel: `"#FF605E5C"` (first two chars = alpha, remaining six = RGB).

### Font Sizes

**Problem**: Font sizes in points vs pixels.
**Fix**: Power BI uses points. The MCP expects points. Don't convert.

## PBIP Structure Gotchas

### PBIR vs TMSL

**Problem**: Mixing PBIR (report) and TMSL (model) formats causes corruption.
**Fix**: Keep them separate. PBIR for report layout, TMSL for semantic model. Don't edit TMSL sections when working on report visuals.

### [Content_Types].xml

**Problem**: Missing or incorrect Content_Types.xml breaks the .pbip package.
**Fix**: Always include this file. Use the template from `examples/report-1-sales-dashboard/`.

### Report.json Schema Version

**Problem**: Wrong schema version causes import failures.
**Fix**: Use the latest schema version. Check `examples/` for the current version being used.

## MCP Tool Gotchas

### powerbi-report-mcp Path Handling

**Problem**: Relative paths may resolve differently depending on working directory.
**Fix**: Always use absolute paths when specifying .pbip file locations.

### Batch Operations

**Problem**: Making too many MCP calls in rapid succession can cause timeouts.
**Fix**: Add small delays between batch visual creation calls. Group related operations.

### Visual Positioning

**Problem**: Visuals positioned outside page bounds or overlapping cause rendering issues.
**Fix**: Use the layout grid from the design system. Always specify x, y, width, height in pixels.

## DAX Gotchas

### DIVIDE vs / Operator

**Problem**: Using `/` for division causes errors on divide-by-zero.
**Fix**: Always use `DIVIDE(numerator, denominator, alternateResult)`:
```dax
DIVIDE([Numerator], [Denominator], 0)
```

### Date Table Requirements

**Problem**: Time intelligence functions require a proper date table marked as such.
**Fix**: Always mark your date table: `Mark as Date Table` in the model view, or use `CALENDARAUTO()` to generate one.

### Measure Dependencies

**Problem**: Measures that reference other measures can create circular dependencies.
**Fix**: Build base measures first, then layer calculated measures on top. Validate after each addition.

## Deployment Gotchas

### fabric-cli Authentication

**Problem**: fabric-cli needs Azure AD auth, not API keys.
**Fix**: Run `fab auth login` before any deployment commands. Use service principal for CI/CD.

### Report Rebinding

**Problem**: After deployment, reports may point to wrong semantic model.
**Fix**: Use `fab report rebind` to point to the correct model in the target workspace.

## Contributing Gotchas

If you find a new gotcha, add it to this file with:
1. Clear problem description
2. The fix or workaround
3. Example code if applicable
