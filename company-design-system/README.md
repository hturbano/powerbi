# Company Design System — reskin kit

A reusable kit for taking **any** Power BI report and making it adopt the company
look: the **theme** (colors/fonts/chart defaults) plus a library of **recipes**
(scripted transformations a theme alone can't do).

Built and validated against real reports (an attendance dashboard and a 6-page
Zendesk report). See [the reskin workflow](#the-reskin-workflow) for the repeatable
process.

## What's here

```
company-design-system/
├── theme/
│   └── CompanyDesignSystem.theme.json   # import via View → Themes → Browse
├── templates/
│   └── nav_header.json                  # extracted nav band (for brand-nav-header)
└── recipes/
    ├── lib.py                           # shared PBIR helpers + safety checks
    └── recipes.py                       # the recipe toolkit + CLI
```

## Hard prerequisites

1. **Enhanced PBIR only.** The report's `.Report` folder must contain a `definition/`
   subfolder. Legacy `.pbip` (single root `report.json`) won't work — convert it in
   Power BI Desktop first (enable *Preview features → enhanced metadata format (PBIR)*,
   then Save As `.pbip`).
2. **Close Power BI Desktop** before running any recipe — it will clobber edits on its
   next save otherwise.
3. **Back up the `.Report` folder** before a batch. Recipes are file edits.

## The three bands (why a theme isn't enough)

| Band | Owner | Examples |
|---|---|---|
| **Chrome** | the **theme** | colors, fonts, chart/table/slicer defaults, gridlines, borders |
| **Structural** | **structural recipes** | colored page backgrounds, decorative panels, header/nav bars |
| **Semantic** | **additive recipes** | status colors, threshold lines, accent bars, conditional colors |

A theme only fills the Chrome band. The Structural and Semantic bands are baked into
the report as shapes / page settings / per-visual overrides — that's what the recipes
handle.

## The reskin workflow

```
1. Convert to enhanced PBIR (Power BI Desktop → Save As .pbip)
2. Close Power BI Desktop
3. Back up the .Report folder
4. Apply the theme:  View → Themes → Browse → theme/CompanyDesignSystem.theme.json  → Save
   (or it gets registered once and travels with the report)
5. Run recipes (see below), e.g.:
     cd company-design-system/recipes
     python recipes.py strip-datapoint-colors --report "<...>.Report" --page "Home"
     python recipes.py brand-title            --report "<...>.Report" --page "Home"
     python recipes.py clean-page-background   --report "<...>.Report" --page "Home"
6. Every recipe auto-runs a JSON-validity + dangling-reference check.
7. Open once in Power BI Desktop, Refresh data, eyeball vs the design, Save.
```

`python recipes.py list` prints all recipes. `--page` accepts a page **display name**
or its **id**. Recipe options use `--set key=value` (repeatable).

## Recipe library

### Reskin — remove overrides so the theme wins
| Recipe | What it does | Options |
|---|---|---|
| `strip-datapoint-colors` | Remove hard-coded chart series colors → theme palette | — |
| `strip-title-override` | Remove title bg/fontColor overrides (keeps text) | — |
| `brand-title` | Force every chart/card/table title to navy Segoe UI Semibold | `color`, `size` |
| `recolor-textbox` | Replace an old text color with a brand color in textboxes | `old`, `new` |
| `strip-axis-override` | Remove axis color/font overrides → theme | — |
| `strip-legend-override` | Remove legend color/font overrides → theme | — |

### Structural — the page chrome a theme can't reach
| Recipe | What it does | Options |
|---|---|---|
| `clean-page-background` | Set page canvas + wallpaper to the company tone (`#DDE6EE`) | `color` |
| `neutralize-panels` | Recolor decorative shape fills to a clean surface color | `old`, `new` |
| `brand-header` | Recolor a wide header-bar shape to white + white title text → navy | — |
| `wrap-in-panel` | Insert a white rounded panel behind a region for section grouping | `x`,`y`,`w`,`h`,`color`,`border` |
| `brand-nav-header` *(beta)* | Stamp the LOCUS nav band (title / Support / Feature Request / filter toggle), scaled to page width | — |

### Additive — semantic, data-driven polish
| Recipe | What it does | Options |
|---|---|---|
| `card-label-fix` | Put the card label above the value (Segoe UI Bold) so it doesn't clip | — |
| `kpi-status-color` | Color a card background by status bands (first match wins) | `visual`,`entity`,`measure`,`bands`,`default` |
| `threshold-line` | Add a y-axis reference line at a value to a line/column chart | `visual`,`value`,`label`,`color` |
| `accent-bar-status` *(beta)* | Turn on a left accent bar on a card in a fixed color | `visual`,`color` |
| `semantic-series-colors` *(beta)* | Assign explicit colors to chart series by category | `visual`,`entity`,`column`,`map` |

`(beta)` recipes work but need a manual finish/eyeball in Desktop (e.g. the nav
toggle's bookmark wiring, exact accent positioning).

## Gotchas learned (see also ../docs/GOTCHAS.md)

- **`pbir_duplicate_page` leaves dangling `visualInteractions`** → the report crashes on
  open (`serializeRelationship … reading 'name'`). Always remap or strip interactions
  after duplicating. `lib.scan_dangling()` catches this.
- **`cardVisual` value/label formatting is ignored without a `selector`** matching the
  measure's queryRef (e.g. `{"metadata": "_Measures.Total"}`). `card-label-fix` handles it.
- **Themes can't touch custom visuals** (e.g. `enlightenDataStory`), page backgrounds set
  to a `ThemeDataColor` index, or hard-coded shape fills — hence the structural recipes.
- **Force-killing Power BI mid-write** can disturb an import model's cache; close it
  gracefully.
