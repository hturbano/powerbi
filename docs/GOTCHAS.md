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

### Report Must Be in Enhanced PBIR Format (definition/ folder)

**Problem**: `powerbi-report-mcp` only operates on the **enhanced PBIR** format — a
`.Report` folder that contains a `definition/` subfolder (`definition/report.json`,
`definition/pages/`, `definition/version.json`). Many existing `.pbip` files use the
**legacy** format instead: a single `report.json` at the `.Report` root (with a
`sections` array) plus a `definition.pbir` pointer and **no** `definition/` folder.
Connecting to a legacy report fails with:

```
{"success": false, "error": "No .Report folder found at: ...DesignSystemsTemplate.Report"}
```

even though the folder clearly exists. The check is literally
`endsWith(".Report") && existsSync(.Report/definition)`.

**Fix**: Convert the report to enhanced PBIR in Power BI Desktop (one-time, per file):

1. Open the `.pbip` in Power BI Desktop.
2. **File → Options and settings → Options → Preview features →** enable
   **"Store reports using enhanced metadata format (PBIR)"** → OK.
3. Restart Power BI Desktop if prompted, reopen the `.pbip`.
4. **Save** (`Ctrl+S`). Desktop rewrites the `.Report` into a `definition/` folder.

You'll know it worked when a `definition/` folder appears inside `.Report` (with
`pages/`, `report.json`, `version.json`) and the single root `report.json` is gone.

> The conversion is one-way for that file. Back up the `.Report` folder first if you
> may need the legacy layout later.

### Close Power BI Desktop Before Editing on Disk

**Problem**: If Power BI Desktop has the `.pbip` open while MCP tools write to disk,
a subsequent Desktop save clobbers the MCP changes, and Desktop won't show the MCP
changes until reloaded.
**Fix**: Close Power BI Desktop before a batch of MCP edits, then reopen (or use
`pbir_reload_report`) to view the result.

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
**Fix**: Use the layout grid from the design system. New visuals must clear the page
banner zone — content starts at roughly `y >= 57` on a standard canvas, or
`pbir_add_visual` rejects the placement with `layout_validation_failed` (pass
`strictLayout: false` to proceed with warnings).

### Data Bindings Require a `type`

**Problem**: `pbir_add_visual` bindings fail validation with
`expected: 'column' | 'measure' | 'aggregation'` when a field omits its kind.
**Fix**: Every binding field needs `type`, e.g.
`{ "entity": "EnrollmentMetrics", "property": "EnrolledTotal", "type": "measure" }`.

## Known Tool Issues (observed)

These are bugs in the underlying tools, not user error — listed so you can recognize
them. Tracked for upstream fixes.

### pbir_list_bookmarks can crash on some reports

**Symptom**: `Cannot read properties of undefined (reading 'map')` when listing
bookmarks on a report whose bookmark structure differs from what the tool expects.
**Workaround**: Manage bookmarks in Power BI Desktop until fixed.

### validate-pbip.py is noisy on real-world reports

**Symptom**: Hundreds of warnings/errors on a mature report — every authored textbox
color is flagged as a "hardcoded color," and `actionButton` visuals are flagged for a
missing `howCreated` even when valid (the field nests differently in enhanced PBIR).
**Workaround**: Treat these as informational on existing reports; focus the validator
on newly generated pages. A structure-aware rewrite is needed for full accuracy.

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
