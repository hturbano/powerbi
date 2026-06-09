# Theme Toggle Implementation

This document describes how to implement the light/dark theme toggle in Power BI reports.

## Concept

The theme toggle uses Power BI bookmarks to switch between light and dark visual configurations on the same page. A button triggers a bookmark that:
1. Updates all visual colors (background, foreground, accent)
2. Updates card colors and shadows
3. Updates chart axis and gridline colors
4. Switches the toggle button icon

## Implementation

### Step 1: Create Two Theme Bookmarks

**Light Theme Bookmark:**
1. Apply the light theme colors to all visuals
2. Create a bookmark named "Theme_Light"
3. In bookmark settings: check "Display" and uncheck "Data"

**Dark Theme Bookmark:**
1. Apply the dark theme colors to all visuals
2. Create a bookmark named "Theme_Dark"
3. In bookmark settings: check "Display" and uncheck "Data"

### Step 2: Create Toggle Button

1. Add an Action Button to the report canvas
2. Set action type to "Bookmark"
3. Create two button states (light icon / dark icon)
4. Use the button to toggle between bookmarks

### Step 3: Theme Colors Reference

See `design-system/themes/modern-fintech.json` (light) and `design-system/themes/modern-fintech-dark.json` (dark) for the full color palette.

Key colors to toggle:
- Background: #F8F9FC → #0A1628
- Surface: #FFFFFF → #111D30
- Text: #0D1B2A → #E8ECF1
- Text Secondary: #576574 → #7B8A9E
- Border: #E2E8F0 → #1E3048
- Accent: #00C9A7 → #00E4BA

### Step 4: Validation

After implementing the toggle:
1. Click the toggle button — all visuals should switch to dark theme
2. Click again — all visuals should switch back to light
3. Verify no visual retains the old theme colors
4. Check slicers, filters, and tooltips also toggle

## Notes

- Bookmarks only affect visuals on the current page. For multi-page reports, apply to each page.
- The toggle is a UX enhancement, not a data change. Always keep "Data" unchecked in bookmarks.
- The MCP server can generate both theme variants. Request both when generating a report with toggle enabled.

## Author

hturbano
