#!/usr/bin/env python3
"""
Company Design System -- reskin recipe toolkit.

Apply reusable transformations to an enhanced-PBIR report so it adopts the Company
Design System look. CLOSE POWER BI DESKTOP before running anything here.

Usage:
    python recipes.py <recipe> --report "<...>.Report" --page "<name or id>" [--set k=v ...]
    python recipes.py list

Recipe categories:
  reskin     -- remove overrides so the theme wins
  structural -- page chrome the theme can't reach
  additive   -- semantic, data-driven polish

Every run prints a JSON-validity check and a dangling-reference scan at the end.
"""
import sys, os, json, argparse
import lib
from lib import (load, save, new_id, page_json, visual_files, resolve_page,
                 lit, litcolor, vtype, objects, container, title_text, measure_ref,
                 validate, scan_dangling, CHART_TYPES, TITLE_TYPES)

SEMI = "'''Segoe UI Semibold'', wf_segoe-ui_semibold, helvetica, arial, sans-serif'"
BOLD = "'''Segoe UI Bold'', wf_segoe-ui_bold, helvetica, arial, sans-serif'"
NAVY = "#314259"; VALUE_NAVY = "#0C1A2C"; SLATE = "#607890"
PAGE_TONE = "#DDE6EE"; SURFACE = "#FFFFFF"; BORDER = "#C0CFDD"

# ============================================================ RESKIN
def strip_datapoint_colors(report, page, **o):
    """Remove hard-coded per-series chart colors so charts adopt the theme palette."""
    n = 0
    for f in visual_files(report, page):
        d = load(f)
        if vtype(d) in CHART_TYPES and "dataPoint" in objects(d):
            del objects(d)["dataPoint"]; save(f, d); n += 1
    return f"stripped dataPoint on {n} charts"

def strip_title_override(report, page, **o):
    """Remove title background + fontColor overrides (keep the text) -> theme title."""
    n = 0
    for f in visual_files(report, page):
        d = load(f); t = container(d).get("title")
        if not t: continue
        hit = False
        for item in t:
            for k in ("background", "fontColor"):
                if k in item.get("properties", {}):
                    del item["properties"][k]; hit = True
        if hit: save(f, d); n += 1
    return f"cleaned title overrides on {n} visuals"

def brand_title(report, page, **o):
    """Set every chart/card/table title to brand navy Segoe UI Semibold, no colored bar."""
    color = o.get("color", NAVY); size = o.get("size", "14")
    n = 0
    for f in visual_files(report, page):
        d = load(f)
        if vtype(d) not in TITLE_TYPES: continue
        t = container(d).get("title") or [{}]
        props = t[0].get("properties", {})
        new = {"show": props.get("show", lit("true"))}
        for keep in ("text", "titleWrap"):
            if keep in props: new[keep] = props[keep]
        new["fontColor"] = litcolor(color)
        new["fontFamily"] = lit(SEMI)
        new["fontSize"] = lit(f"{size}D")
        container(d)["title"] = [{"properties": new}]
        save(f, d); n += 1
    return f"branded titles on {n} visuals"

def recolor_textbox(report, page, **o):
    """Replace an old hex color with a new one inside textbox content (brand recolor)."""
    old = o["old"]; new = o.get("new", VALUE_NAVY)
    n = 0
    for f in visual_files(report, page):
        d = load(f)
        if vtype(d) != "textbox": continue
        s = json.dumps(d)
        if old.lower() in s.lower():
            save(f, json.loads(s.replace(old, new).replace(old.upper(), new).replace(old.lower(), new)))
            n += 1
    return f"recolored {n} textboxes ({old}->{new})"

def _strip_props(report, page, group, props):
    n = 0
    for f in visual_files(report, page):
        d = load(f); g = objects(d).get(group)
        if not g: continue
        hit = False
        for item in g:
            for k in props:
                if k in item.get("properties", {}):
                    del item["properties"][k]; hit = True
        if hit: save(f, d); n += 1
    return n

def strip_axis_override(report, page, **o):
    """Remove axis color/font overrides so axes adopt the theme."""
    a = _strip_props(report, page, "valueAxis", ("labelColor", "titleColor", "fontFamily"))
    b = _strip_props(report, page, "categoryAxis", ("labelColor", "titleColor", "fontFamily"))
    return f"stripped axis overrides on {a}+{b} visuals"

def strip_legend_override(report, page, **o):
    """Remove legend color/font overrides so legends adopt the theme."""
    return f"stripped legend overrides on {_strip_props(report, page, 'legend', ('labelColor','titleColor','fontFamily'))} visuals"

# ============================================================ STRUCTURAL
def clean_page_background(report, page, **o):
    """Set the page canvas + wallpaper to the Company page tone (white cards separate on it)."""
    color = o.get("color", PAGE_TONE)
    pjp = page_json(report, page); pj = load(pjp)
    obj = pj.setdefault("objects", {})
    obj["background"] = [{"properties": {"color": litcolor(color), "transparency": lit("0D")}}]
    obj["outspace"] = [{"properties": {"color": litcolor(color)}}]
    save(pjp, pj)
    return f"page tone -> {color}"

def neutralize_panels(report, page, **o):
    """Recolor decorative shape fills matching an old color to a clean surface color."""
    old = o.get("old"); new = o.get("new", SURFACE)
    n = 0
    for f in visual_files(report, page):
        d = load(f)
        if vtype(d) != "shape": continue
        fill = objects(d).get("fill")
        if not fill: continue
        s = json.dumps(fill)
        if (old and old.lower() in s.lower()) or (not old):
            fill[0].setdefault("properties", {})["fillColor"] = litcolor(new)
            save(f, d); n += 1
    return f"neutralized {n} shape panels -> {new}"

def brand_header(report, page, **o):
    """Recolor the wide top header-bar shape to white and its title text to navy."""
    bar = title = 0
    for f in visual_files(report, page):
        d = load(f); p = d.get("position", {}); s = json.dumps(d)
        if vtype(d) == "shape" and p.get("width", 0) > 1000 and p.get("height", 0) < 110:
            fill = objects(d).get("fill")
            if fill:
                fill[0].setdefault("properties", {})["fillColor"] = litcolor(SURFACE); save(f, d); bar += 1
        elif vtype(d) == "textbox" and "#ffffff" in s.lower():
            ns = s.replace("#ffffff", VALUE_NAVY).replace("#FFFFFF", VALUE_NAVY)
            save(f, json.loads(ns)); title += 1
    return f"header bar->white ({bar}), white title text->navy ({title})"

def wrap_in_panel(report, page, **o):
    """Insert a white rounded panel shape behind a region (x,y,w,h) for section grouping."""
    x = int(o["x"]); y = int(o["y"]); w = int(o["w"]); h = int(o["h"])
    color = o.get("color", SURFACE); border = o.get("border", BORDER)
    vid = new_id()
    shape = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
        "name": vid,
        "position": {"x": x, "y": y, "z": 0, "width": w, "height": h, "tabOrder": -1},
        "visual": {"visualType": "shape", "objects": {
            "shape": [{"properties": {"tileShape": lit("'rectangle'")}}],
            "fill": [{"properties": {"show": lit("true"), "fillColor": litcolor(color)}, "selector": {"id": "default"}}],
            "outline": [{"properties": {"show": lit("true"), "lineColor": litcolor(border), "weight": lit("1D")}}],
        }, "drillFilterOtherVisuals": True}}
    dst = os.path.join(lib.pages_dir(report), page, "visuals", vid)
    os.makedirs(dst, exist_ok=True)
    save(os.path.join(dst, "visual.json"), shape)
    return f"added panel {vid} at ({x},{y},{w},{h})"

def brand_nav_header(report, page, **o):
    """[beta] Stamp the LOCUS nav band (bar + title + Support/Feature Request + filter toggle)
    onto the page, scaled to the target page width. Repositioning/wiring the filter toggle
    bookmark is a manual finish in Desktop."""
    tpl = load(os.path.join(os.path.dirname(__file__), "..", "templates", "nav_header.json"))
    pj = load(page_json(report, page)); tw = pj.get("width", 1280); sw = tpl.get("sourceWidth", 1792)
    scale = tw / sw
    n = 0
    for el in tpl["elements"]:
        vid = new_id()
        v = el["visual"]; v["name"] = vid
        p = el["position"]
        pos = {"x": round(p.get("x", 0) * scale), "y": p.get("y", 0),
               "width": round(p.get("width", 0) * scale), "height": p.get("height", 0),
               "z": p.get("z", 1000), "tabOrder": p.get("tabOrder", 1000)}
        dst = os.path.join(lib.pages_dir(report), page, "visuals", vid)
        os.makedirs(dst, exist_ok=True)
        save(os.path.join(dst, "visual.json"), {"$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json", "name": vid, "position": pos, "visual": v})
        n += 1
    return f"[beta] stamped {n} nav elements (review/reposition in Desktop)"

# ============================================================ ADDITIVE
def card_label_fix(report, page, **o):
    """Put each card's label above the value (Segoe UI Bold) so labels don't clip."""
    n = 0
    for f in visual_files(report, page):
        d = load(f)
        if vtype(d) != "cardVisual": continue
        ref = measure_ref(d)
        if not ref: continue
        ob = objects(d)
        ob["value"] = [{"properties": {"labelDisplayUnits": lit("1D"), "fontFamily": lit(BOLD)},
                        "selector": {"metadata": ref}}]
        ob["label"] = [{"properties": {"fontSize": lit("10D"), "position": lit("'aboveValue'")},
                        "selector": {"metadata": ref}}]
        save(f, d); n += 1
    return f"fixed label layout on {n} cards"

def _conditional(entity, measure, bands, default):
    cases = [{"Condition": {"Comparison": {"ComparisonKind": 2,
              "Left": {"Measure": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": measure}},
              "Right": {"Literal": {"Value": f"{v}D"}}}}, "Value": {"Literal": {"Value": f"'{c}'"}}}
             for v, c in bands]
    return {"solid": {"color": {"expr": {"Conditional": {"Cases": cases, "Default": {"Literal": {"Value": f"'{default}'"}}}}}}}

def kpi_status_color(report, page, **o):
    """Color a card's background by status bands (first match wins). Default bands: >=.10 red, >=.05 amber."""
    vid = o["visual"]; entity = o["entity"]; measure = o["measure"]
    bands = json.loads(o["bands"]) if "bands" in o else [[0.10, "#FDECEE"], [0.05, "#FFF7E6"]]
    default = o.get("default", "#EAF9F0")
    f = os.path.join(lib.pages_dir(report), page, "visuals", vid, "visual.json")
    d = load(f); container(d)["background"] = [{"properties": {"color": _conditional(entity, measure, bands, default)}}]
    save(f, d)
    return f"kpi-status-color on {vid} ({measure})"

def threshold_line(report, page, **o):
    """Add a y-axis reference line at a value to a line/column chart."""
    vid = o["visual"]; value = o.get("value", "0.1"); label = o.get("label", "Threshold"); color = o.get("color", "#F4676F")
    f = os.path.join(lib.pages_dir(report), page, "visuals", vid, "visual.json")
    d = load(f)
    objects(d)["y1AxisReferenceLine"] = [{"properties": {
        "show": lit("true"), "displayName": lit(f"'{label}'"), "value": lit(f"{value}D"),
        "lineColor": litcolor(color), "dataLabelShow": lit("true"),
        "dataLabelHorizontalPosition": lit("'right'"), "dataLabelColor": litcolor(color),
        "dataLabelText": lit("'Name'"), "transparency": lit("50D")}, "selector": {"id": "1"}}]
    save(f, d)
    return f"threshold line at {value} on {vid}"

def accent_bar_status(report, page, **o):
    """[beta] Turn on a left accent bar on a cardVisual in a fixed semantic color."""
    vid = o["visual"]; color = o.get("color", "#0078BF")
    f = os.path.join(lib.pages_dir(report), page, "visuals", vid, "visual.json")
    d = load(f)
    objects(d)["accentBar"] = [{"properties": {"show": lit("true"), "position": lit("'Left'"),
                                "color": litcolor(color)}, "selector": {"id": "default"}}]
    save(f, d)
    return f"[beta] accent bar on {vid}"

def semantic_series_colors(report, page, **o):
    """[beta] Assign explicit colors to chart series by category. --set map='{\"Closed\":\"#0078BF\"}'."""
    vid = o["visual"]; entity = o["entity"]; column = o["column"]; mapping = json.loads(o["map"])
    f = os.path.join(lib.pages_dir(report), page, "visuals", vid, "visual.json")
    d = load(f)
    dp = []
    for cat, col in mapping.items():
        dp.append({"properties": {"fill": litcolor(col)}, "selector": {"data": [{"scopeId": {"Comparison": {
            "ComparisonKind": 0, "Left": {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": column}},
            "Right": {"Literal": {"Value": f"'{cat}'"}}}}}]}})
    objects(d)["dataPoint"] = dp; save(f, d)
    return f"[beta] semantic series colors on {vid} ({len(mapping)} categories)"

# ============================================================ dispatch
RECIPES = {
    "strip-datapoint-colors": strip_datapoint_colors, "strip-title-override": strip_title_override,
    "brand-title": brand_title, "recolor-textbox": recolor_textbox,
    "strip-axis-override": strip_axis_override, "strip-legend-override": strip_legend_override,
    "clean-page-background": clean_page_background, "neutralize-panels": neutralize_panels,
    "brand-header": brand_header, "wrap-in-panel": wrap_in_panel, "brand-nav-header": brand_nav_header,
    "card-label-fix": card_label_fix, "kpi-status-color": kpi_status_color,
    "threshold-line": threshold_line, "accent-bar-status": accent_bar_status,
    "semantic-series-colors": semantic_series_colors,
}

def main():
    ap = argparse.ArgumentParser(description="Company Design System recipe toolkit")
    ap.add_argument("recipe", help="recipe name, or 'list'")
    ap.add_argument("--report", help="path to the .Report folder")
    ap.add_argument("--page", help="page display name or id")
    ap.add_argument("--set", action="append", default=[], metavar="k=v", help="recipe option")
    a = ap.parse_args()

    if a.recipe == "list":
        for k in RECIPES: print(" ", k)
        return
    if a.recipe not in RECIPES:
        raise SystemExit(f"unknown recipe '{a.recipe}'. Try: python recipes.py list")
    if not a.report or not a.page:
        raise SystemExit("--report and --page are required")

    opts = dict(kv.split("=", 1) for kv in a.set)
    page = resolve_page(a.report, a.page)
    print("RESULT:", RECIPES[a.recipe](a.report, page, **opts))

    bad = validate(a.report); dangle = scan_dangling(a.report)
    print(f"validate: {'OK' if not bad else bad}")
    print(f"dangling refs: {len(dangle)}" + (f" {dangle}" if dangle else ""))
    if bad or dangle:
        raise SystemExit("WARNING: integrity check failed -- review before opening in Power BI")

if __name__ == "__main__":
    main()
