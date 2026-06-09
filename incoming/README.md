# Incoming .pbip Files

Place your existing Power BI .pbip files (or extracted `definition/report.json` files) in this directory.

The onboarding flow will extract your design system from these files:
- Color palette
- Typography settings
- Layout patterns
- Visual configurations
- DAX measure patterns

## How to Get Your .pbip

1. Open your report in Power BI Desktop
2. Save as `.pbip` format (Power BI Project)
3. The .pbip is a folder containing `definition/report.json` and other files
4. Copy the entire folder or just the `definition/report.json` into this directory

## Supported Formats

- Full .pbip folder (with `definition/report.json`)
- Just the `definition/report.json` file
- A .pbip file renamed to .zip (will be extracted automatically)

## After Extraction

Once the onboarding flow completes:
- Your theme will be saved to `design-system/themes/`
- Your DAX patterns will be saved to `design-system/dax-patterns/`
- This folder will be cleaned up

## Author

hturbano
