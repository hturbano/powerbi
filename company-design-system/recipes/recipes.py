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
import os, json, argparse
import lib
from lib import (load, save, new_id, page_json, visual_files, resolve_page,
                 lit, litcolor, vtype, objects, container, measure_ref,
                 validate, scan_dangling, check_visual_schema, CHART_TYPES, TITLE_TYPES)

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

VC_SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json"

def _write_visual(report, page, vid, pos, visual):
    dst = os.path.join(lib.pages_dir(report), page, "visuals", vid)
    os.makedirs(dst, exist_ok=True)
    save(os.path.join(dst, "visual.json"), {"$schema": VC_SCHEMA, "name": vid, "position": pos, "visual": visual})

def _pos(x, y, w, h, z):
    return {"x": x, "y": y, "z": z, "width": w, "height": h, "tabOrder": z}

def _shape(report, page, x, y, w, h, fill, border, z):
    _write_visual(report, page, new_id(), _pos(x, y, w, h, z), {"visualType": "shape", "objects": {
        "shape": [{"properties": {"tileShape": lit("'rectangle'")}}],
        "fill": [{"properties": {"show": lit("true"), "fillColor": litcolor(fill)}, "selector": {"id": "default"}}],
        "outline": [{"properties": {"show": lit("true"), "lineColor": litcolor(border), "weight": lit("1D")}}],
    }, "drillFilterOtherVisuals": True})

def _textbox_multi(report, page, x, y, w, h, paragraphs, z, align="left", bg=None, border=None):
    """paragraphs: list of (text, color, size_pt, bold) -> one textbox, one paragraph each."""
    paras = []
    for (text, color, size, bold) in paragraphs:
        style = {"fontWeight": "bold" if bold else "normal", "fontSize": f"{size}pt",
                 "color": color, "fontFamily": "Segoe UI"}
        paras.append({"textRuns": [{"value": text, "textStyle": style}], "horizontalTextAlignment": align})
    visual = {"visualType": "textbox", "objects": {"general": [{"properties": {"paragraphs": paras}}]}}
    vco = {}
    if bg: vco["background"] = [{"properties": {"show": lit("true"), "color": litcolor(bg)}}]
    if border: vco["border"] = [{"properties": {"show": lit("true"), "color": litcolor(border), "radius": lit("6D")}}]
    else: vco["border"] = [{"properties": {"show": lit("false")}}]  # no default Power BI border
    visual["visualContainerObjects"] = vco
    _write_visual(report, page, new_id(), _pos(x, y, w, h, z), visual)

def _textbox(report, page, x, y, w, h, text, color, size, bold, align, z, bg=None, border=None):
    style = {"fontWeight": "bold" if bold else "normal", "fontSize": f"{size}pt",
             "color": color, "fontFamily": "Segoe UI"}
    visual = {"visualType": "textbox", "objects": {"general": [{"properties": {"paragraphs": [
        {"textRuns": [{"value": text, "textStyle": style}], "horizontalTextAlignment": align}]}}]}}
    vco = {}
    if bg: vco["background"] = [{"properties": {"show": lit("true"), "color": litcolor(bg)}}]
    if border: vco["border"] = [{"properties": {"show": lit("true"), "color": litcolor(border), "radius": lit("6D")}}]
    else: vco["border"] = [{"properties": {"show": lit("false")}}]  # no default Power BI border
    visual["visualContainerObjects"] = vco
    _write_visual(report, page, new_id(), _pos(x, y, w, h, z), visual)

def _refresh_line(report, page, x, y, w, imported, refreshes, z):
    """Top-right 'Last Data import / Dashboard Refreshes' line (LOCUS style: #334A67,
    labels normal + values bold), one right-aligned paragraph."""
    mk = lambda v, b: {"value": v, "textStyle": {"fontWeight": "bold" if b else "normal",
                       "fontSize": "9pt", "color": "#334A67", "fontFamily": "Segoe UI"}}
    runs = [mk("Last Data import: ", False), mk(imported + "    ", True),
            mk("Dashboard Refreshes: ", False), mk(refreshes, True)]
    visual = {"visualType": "textbox", "objects": {"general": [{"properties": {"paragraphs":
              [{"textRuns": runs, "horizontalTextAlignment": "right"}]}}]},
              "visualContainerObjects": {"border": [{"properties": {"show": lit("false")}}]}}
    _write_visual(report, page, new_id(), _pos(x, y, w, 16, z), visual)

def _action_button(report, page, x, y, w, h, text, accent, z, surface=SURFACE):
    """A real LOCUS actionButton: white fill, accent outline + Segoe UI Semibold 12pt accent
    text, 4px rounded edges, hover inverts to accent fill + white text. (Matches the
    DesignSystemsTemplate Support / Feature Request buttons.)"""
    visual = {"visualType": "actionButton", "objects": {
        "icon": [{"properties": {"shapeType": lit("'blank'")}, "selector": {"id": "default"}},
                 {"properties": {"show": lit("false")}}],
        "text": [{"properties": {"show": lit("true")}},
                 {"properties": {"text": lit(f"'{text}'"), "fontColor": litcolor(accent),
                                 "fontFamily": lit(SEMI), "fontSize": lit("12D")}, "selector": {"id": "default"}},
                 {"properties": {"fontColor": litcolor(surface)}, "selector": {"id": "hover"}}],
        "outline": [{"properties": {"show": lit("true")}},
                    {"properties": {"lineColor": litcolor(accent), "weight": lit("1D")}, "selector": {"id": "default"}}],
        "shape": [{"properties": {"roundEdge": lit("4L")}, "selector": {"id": "default"}}],
        "fill": [{"properties": {"show": lit("true")}},
                 {"properties": {"fillColor": litcolor(surface), "transparency": lit("0D")}, "selector": {"id": "default"}},
                 {"properties": {"fillColor": litcolor(accent)}, "selector": {"id": "hover"}}],
    }, "drillFilterOtherVisuals": True}
    _write_visual(report, page, new_id(), _pos(x, y, w, h, z), visual)

def brand_nav_header(report, page, **o):
    """Build the LOCUS nav header (sized to page width): white bar + two-line title (blue
    Segoe UI Bold 14pt name over a slate 11pt subtitle, matching DesignSystemsTemplate) +
    a top-right 'Last Data import / Dashboard Refreshes' line + Support / Feature Request
    buttons + a Filters (funnel) pill. --set title= subtitle= [titlex=20 clears a left logo]
    [imported='1/8/2026 1:14 PM'] [refreshes='6:00 AM Daily'] [accent=#0078BF] [height=64].
    (Filter toggle + button click actions are a manual bookmark wire-up in Desktop.)"""
    title = o.get("title", "Dashboard Name")
    subtitle = o.get("subtitle", "View")
    accent = o.get("accent", "#0078BF")
    imported = o.get("imported", "1/8/2026 1:14 PM")
    refreshes = o.get("refreshes", "6:00 AM Daily")
    W = load(page_json(report, page)).get("width", 1280)
    H = int(o.get("height", 64)); z = 9000
    # pushContent: shift every existing visual down (for bare pages whose content starts at y=0,
    # so the nav doesn't cover it). Run BEFORE adding nav visuals. Watch bottom overflow.
    dy = float(o.get("pushContent", 0))
    if dy:
        for f in visual_files(report, page):
            d = load(f); p = d.get("position")
            if p and isinstance(p.get("y"), (int, float)):
                p["y"] += dy; save(f, d)
    # bar
    _shape(report, page, 0, 0, W, H, SURFACE, BORDER, z)
    # title block: blue name + slate subtitle (LOCUS spec). titlex clears a left logo.
    tx = int(o.get("titlex", 20))
    _textbox_multi(report, page, tx, 8, 600, H - 12,
                   [(title, accent, 14, True), (subtitle, SLATE, 11, False)], z + 1, align="left")
    # top-right refresh / import info line
    _refresh_line(report, page, W - 626, 6, 610, imported, refreshes, z + 1)
    # buttons row (lower-right, leaves room for the refresh line above) -- real actionButtons
    by = H - 38
    _action_button(report, page, W - 452, by, 96, 32, "Support", accent, z + 1)
    _action_button(report, page, W - 348, by, 156, 32, "Feature Request", accent, z + 1)
    _action_button(report, page, W - 184, by, 166, 32, "▾ Filters", accent, z + 1)
    return f"built LOCUS nav header (title='{title}', width={W}, h={H})"

# ============================================================ RESCALE
def rescale_page(report, page, **o):
    """Scale a page and every visual on it by a uniform ratio so the layout keeps its
    proportions on a larger canvas. --set width=1792 (target width) or --set ratio=1.4.
    Scales grouped visuals too -- uniform scaling is correct for both absolute and
    group-relative child coordinates."""
    pjp = page_json(report, page); pj = load(pjp)
    cur_w = pj.get("width", 1280)
    r = float(o["ratio"]) if "ratio" in o else float(o.get("width", 1792)) / cur_w
    pj["width"] = round(cur_w * r, 4)
    pj["height"] = round(pj.get("height", 720) * r, 4)
    save(pjp, pj)
    n = 0
    for f in visual_files(report, page):
        d = load(f); p = d.get("position")
        if not p: continue
        for k in ("x", "y", "width", "height"):
            if isinstance(p.get(k), (int, float)):
                p[k] = round(p[k] * r, 4)
        save(f, d); n += 1
    return f"rescaled page x{r:.4f} -> {pj['width']}x{pj['height']}, {n} visuals"

# ============================================================ BUILD VISUALS
def _measure_field(spec):
    """'Entity.Measure Name' -> a Measure field-ref dict + queryRef/nativeQueryRef."""
    e, p = spec.split(".", 1)
    return {"field": {"Measure": {"Expression": {"SourceRef": {"Entity": e}}, "Property": p}},
            "queryRef": spec, "nativeQueryRef": p}

def _column_field(spec, active=False):
    """'Entity.Column' -> a Column field-ref dict."""
    e, p = spec.split(".", 1)
    f = {"field": {"Column": {"Expression": {"SourceRef": {"Entity": e}}, "Property": p}},
         "queryRef": spec, "nativeQueryRef": p}
    if active: f["active"] = True
    return f

def add_card(report, page, **o):
    """Add a single-value KPI card bound to a measure, styled as a LOCUS white card (navy bold
    value + slate label, #C0CFDD rounded border). --set measure='ETL Success Rate %' x= y=
    [w=330 h=150 entity=_Measures z=1000]."""
    measure = o["measure"]; entity = o.get("entity", "_Measures")
    x = float(o["x"]); y = float(o["y"]); w = float(o.get("w", 330)); h = float(o.get("h", 150)); z = int(o.get("z", 1000))
    visual = {"visualType": "card",
        "query": {"queryState": {"Values": {"projections": [_measure_field(f"{entity}.{measure}")]}}},
        "objects": {
            "labels": [{"properties": {"color": litcolor(VALUE_NAVY), "fontSize": lit("30D"), "fontFamily": lit(BOLD)}}],
            "categoryLabels": [{"properties": {"show": lit("true"), "color": litcolor(SLATE),
                                "fontSize": lit("11D"), "fontFamily": lit(SEMI)}}]},
        "visualContainerObjects": {
            "background": [{"properties": {"show": lit("true"), "color": litcolor(SURFACE)}}],
            "border": [{"properties": {"show": lit("true"), "color": litcolor(BORDER), "radius": lit("8D")}}]},
        "drillFilterOtherVisuals": True}
    _write_visual(report, page, new_id(), _pos(x, y, w, h, z), visual)
    return f"added KPI card '{measure}' at ({x},{y})"

def add_chart(report, page, **o):
    """Add a bar/column/line chart bound to a category COLUMN + a measure VALUE, sorted by the
    value descending (great for Top-N). --set type=clusteredBarChart
    category='etl_executions.job_name' value='_Measures.Avg Run Time (min)' x= y= [w= h= z=]."""
    vt = o.get("type", "clusteredBarChart")
    cat = _column_field(o["category"], active=True)
    val = _measure_field(o["value"])
    x = float(o["x"]); y = float(o["y"]); w = float(o.get("w", 600)); h = float(o.get("h", 400)); z = int(o.get("z", 500))
    sort_field = cat["field"] if o.get("sortby") == "category" else val["field"]
    visual = {"visualType": vt,
        "query": {"queryState": {"Category": {"projections": [cat]}, "Y": {"projections": [val]}},
                  "sortDefinition": {"sort": [{"field": sort_field, "direction": o.get("sort", "Descending")}]}},
        "drillFilterOtherVisuals": True}
    _write_visual(report, page, new_id(), _pos(x, y, w, h, z), visual)
    return f"added {vt} {o['category']} x {o['value']} at ({x},{y})"

def add_matrix(report, page, **o):
    """Add a matrix heatmap: Rows = a column, Columns = a column, Values = a measure, with an
    optional conditional cell background (the heat). --set rows='etl_executions.job_name'
    cols='etl_executions.Run Date' value='_Measures.Total Runs' x= y= [w= h= z=]
    [heatmeasure='_Measures.Failed Runs' heatband=1 hot='#F8C9CC' cold='#C8EAD3'] -- when
    heatmeasure >= heatband the cell turns 'hot', otherwise 'cold' (blank cells stay blank)."""
    rows = _column_field(o["rows"], active=True)
    cols = _column_field(o["cols"], active=True)
    val = _measure_field(o["value"])
    x = float(o["x"]); y = float(o["y"]); w = float(o.get("w", 1000)); h = float(o.get("h", 600)); z = int(o.get("z", 500))
    visual = {"visualType": "pivotTable",
        "query": {"queryState": {"Rows": {"projections": [rows]},
                                 "Columns": {"projections": [cols]},
                                 "Values": {"projections": [val]}}},
        "drillFilterOtherVisuals": True}
    if "heatmeasure" in o:
        he, hp = o["heatmeasure"].split(".", 1)
        cond = _conditional(he, hp, [[float(o.get("heatband", 1)), o.get("hot", "#F8C9CC")]], o.get("cold", "#C8EAD3"))
        visual["objects"] = {"values": [{"properties": {"backColor": cond}, "selector": {"metadata": o["value"]}}]}
    _write_visual(report, page, new_id(), _pos(x, y, w, h, z), visual)
    return f"added matrix heatmap rows={o['rows']} cols={o['cols']} value={o['value']}"

# ============================================================ REPORT-LEVEL
def apply_theme(report, page=None, **o):
    """Register the Company Design System theme (LOCUS palette) as the report's custom theme:
    copies the theme into StaticResources/RegisteredResources and wires report.json
    (themeCollection.customTheme + resourcePackages). Report-level -- no --page needed.
    --set theme=<path to .json> overrides the default kit theme."""
    import shutil
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.abspath(o.get("theme") or os.path.join(here, "..", "theme", "CompanyDesignSystem.theme.json"))
    if not os.path.exists(src):
        raise SystemExit(f"theme not found: {src}")
    reg = os.path.join(report, "StaticResources", "RegisteredResources")
    os.makedirs(reg, exist_ok=True)
    fname = o.get("name", f"Company_Design_System{new_id()}.json")
    shutil.copyfile(src, os.path.join(reg, fname))
    rjp = os.path.join(report, "definition", "report.json"); rj = load(rjp)
    tc = rj.setdefault("themeCollection", {})
    # Power BI REQUIRES reportVersionAtImport on customTheme -- reuse the base theme's, else default.
    rvi = (tc.get("baseTheme") or {}).get("reportVersionAtImport") or {"visual": "2.9.0", "report": "3.3.0", "page": "2.3.1"}
    tc["customTheme"] = {"name": fname, "reportVersionAtImport": rvi, "type": "RegisteredResources"}
    pkgs = rj.setdefault("resourcePackages", [])
    regpkg = next((p for p in pkgs if p.get("name") == "RegisteredResources"), None)
    if regpkg is None:
        regpkg = {"name": "RegisteredResources", "type": "RegisteredResources", "items": []}
        pkgs.append(regpkg)
    regpkg["items"] = [it for it in regpkg.get("items", []) if it.get("type") != "CustomTheme"]
    regpkg["items"].append({"name": fname, "path": fname, "type": "CustomTheme"})
    save(rjp, rj)
    return f"applied custom theme -> {fname}"

# ============================================================ DUPLICATE
def duplicate_page(report, page, **o):
    """Duplicate a page as a CLEAN copy with regenerated visual ids (so bookmarks/originals are
    untouched), then register it in pages.json. Reskin the copy, keep the original. New
    displayName defaults to '<name> 2'. --set name='New Name'. This replaces the manual
    'duplicate page in Desktop' step."""
    import shutil
    src_id = resolve_page(report, page)
    pd = lib.pages_dir(report)
    new_pid = new_id()
    dst = os.path.join(pd, new_pid)
    shutil.copytree(os.path.join(pd, src_id), dst)
    vis_dir = os.path.join(dst, "visuals")
    idmap = {v: new_id() for v in os.listdir(vis_dir)} if os.path.isdir(vis_dir) else {}
    for old, newv in idmap.items():
        os.rename(os.path.join(vis_dir, old), os.path.join(vis_dir, newv))
    for newv in idmap.values():
        f = os.path.join(vis_dir, newv, "visual.json")
        d = load(f); d["name"] = newv
        if d.get("parentGroupName") in idmap: d["parentGroupName"] = idmap[d["parentGroupName"]]
        save(f, d)
    pjp = os.path.join(dst, "page.json"); pj = load(pjp)
    src_name = pj.get("displayName", "Page")
    pj["name"] = new_pid; pj["displayName"] = o.get("name", f"{src_name} 2")
    for it in pj.get("visualInteractions", []):
        for k in ("source", "target"):
            if it.get(k) in idmap: it[k] = idmap[it[k]]
    save(pjp, pj)
    pmp = os.path.join(pd, "pages.json"); pm = load(pmp)
    pm.setdefault("pageOrder", []).append(new_pid)
    save(pmp, pm)
    return f"duplicated '{src_name}' -> '{pj['displayName']}' ({new_pid}, {len(idmap)} visuals re-id'd)"

# ============================================================ PANEL HEADERS
def panel_header(report, page, **o):
    """LOCUS section header inside a panel's top band: bold blue title over a slate subtitle
    (matches DesignSystemsTemplate panel titles, e.g. 'CAMPUS SCORECARD / Performance
    Overview' = 14pt #0078bf bold + 10.5pt #607890). Pair with hide-title on the chart so the
    native title doesn't double up. --set x= y= title= [subtitle=] [w=320] [accent=#0078BF]
    [size=14] [divider=true]."""
    x = float(o["x"]); y = float(o["y"]); w = float(o.get("w", 320))
    title = o["title"]; subtitle = o.get("subtitle", "")
    accent = o.get("accent", "#0078BF"); size = float(o.get("size", 14))
    z = int(o.get("z", 8500))
    paras = [(title, accent, size, True)]
    if subtitle: paras.append((subtitle, SLATE, 10.5, False))
    h = float(o.get("h", 48 if subtitle else 30))
    _textbox_multi(report, page, x, y, w, h, paras, z, align="left")
    if o.get("divider", "false").lower() == "true":
        _shape(report, page, x, y + h + 2, w, 1, BORDER, BORDER, z - 1)
    return f"panel header '{title}'" + (f" / '{subtitle}'" if subtitle else "") + f" at ({x},{y})"

def panel_title(report, page, **o):
    """Apply the LOCUS *native* visual title band to a visual (the real LOCUS method): navy
    Segoe UI Semibold title (12pt #314259) on an #EDF3F8 background + slate subtitle (#47607E)
    + a matching divider, with LOCUS spacing (2/10/10). The native title reserves its own
    space inside the visual, so the plot shrinks automatically -- no manual nudging, no textbox
    scrollbars. --set visual=<id> title=.. [subtitle=..] [bg=#EDF3F8] [color=#314259]
    [size=12] [border=true]."""
    vid = o["visual"]; title = o["title"]; subtitle = o.get("subtitle", "")
    if subtitle:  # Title Case, but keep all-caps acronyms (QA, PBi) intact -> looks professional
        subtitle = " ".join(w if (len(w) > 1 and w.isupper()) else (w[:1].upper() + w[1:])
                            for w in subtitle.split())
    bg = o.get("bg", "#EDF3F8"); navy = o.get("color", "#314259"); slate = o.get("slate", "#47607E")
    size = o.get("size", "12")
    f = os.path.join(lib.pages_dir(report), page, "visuals", vid, "visual.json")
    d = load(f); vco = container(d)
    vco["title"] = [{"properties": {
        "show": lit("true"), "text": lit(f"'{title}'"), "heading": lit("'Heading2'"),
        "titleWrap": lit("true"), "fontColor": litcolor(navy), "background": litcolor(bg),
        "alignment": lit("'left'"), "fontSize": lit(f"{size}D"), "bold": lit("false"),
        "fontFamily": lit(SEMI)}}]
    if subtitle:
        vco["subTitle"] = [{"properties": {
            "show": lit("true"), "text": lit(f"'{subtitle}'"), "heading": lit("'Heading4'"),
            "fontColor": litcolor(slate), "fontSize": lit("10D")}}]
    vco["divider"] = [{"properties": {
        "show": lit("true"), "color": litcolor(o.get("divider", bg)), "ignorePadding": lit("true")}}]
    vco["spacing"] = [{"properties": {
        "customizeSpacing": lit("true"), "verticalSpacing": lit("2D"),
        "spaceBelowTitle": lit("2D"), "spaceBelowSubTitle": lit("10D"),
        "spaceBelowTitleArea": lit("10D")}}]
    if o.get("border", "false").lower() == "true":
        vco["border"] = [{"properties": {"show": lit("true"), "color": litcolor(BORDER), "radius": lit("8D")}}]
    save(f, d)
    return f"native LOCUS title on {vid}: '{title}'" + (f" / '{subtitle}'" if subtitle else "")

def strip_chrome(report, page, **o):
    """CLEAN-SLATE first step -- strip non-data decorative leftovers so a page starts as bare as
    the design template before the design system goes on. Removes enlightenDataStory /
    smart-narrative visuals by default; --set ids=<id>,<id> removes specific visuals too. Prints
    the SURVIVING shapes/images/textboxes so you can eyeball what is chrome vs real content."""
    import shutil
    ids = set(filter(None, o.get("ids", "").split(",")))
    removed = []; survivors = []
    for f in visual_files(report, page):
        d = load(f); vt = vtype(d); vid = os.path.basename(os.path.dirname(f))
        if vt.lower().startswith("enlighten") or "smartnarrative" in vt.lower() or vid in ids:
            shutil.rmtree(os.path.dirname(f)); removed.append(f"{vt[:18] or 'group'}:{vid[:8]}"); continue
        if vt in ("shape", "image", "textbox"):
            p = d.get("position", {})
            survivors.append(f"{vt}:{vid[:8]} ({p.get('x',0):.0f},{p.get('y',0):.0f},{p.get('width',0):.0f},{p.get('height',0):.0f})")
    out = f"stripped {len(removed)} chrome visual(s): {removed}"
    if survivors: out += "\n  surviving chrome (review): " + " | ".join(survivors)
    return out

def hide_title(report, page, **o):
    """Turn off native visual titles so an overlaid panel-header reads cleanly.
    --set visual=<id> targets one visual; otherwise hides titles on all titled visuals."""
    vid = o.get("visual"); n = 0
    for f in visual_files(report, page):
        if vid and os.path.basename(os.path.dirname(f)) != vid: continue
        d = load(f)
        if vtype(d) not in TITLE_TYPES: continue
        t = container(d).get("title") or [{}]
        props = t[0].setdefault("properties", {}); props["show"] = lit("false")
        container(d)["title"] = [{"properties": props}]
        save(f, d); n += 1
    return f"hid native title on {n} visuals"

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
    "rescale-page": rescale_page, "panel-header": panel_header, "hide-title": hide_title,
    "panel-title": panel_title, "strip-chrome": strip_chrome, "duplicate-page": duplicate_page,
    "apply-theme": apply_theme, "add-card": add_card, "add-chart": add_chart, "add-matrix": add_matrix,
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
    REPORT_LEVEL = {"apply-theme"}  # operate on the whole report, no --page
    if not a.report:
        raise SystemExit("--report is required")
    if a.recipe not in REPORT_LEVEL and not a.page:
        raise SystemExit("--report and --page are required")

    opts = dict(kv.split("=", 1) for kv in a.set)
    if a.recipe in REPORT_LEVEL:
        print("RESULT:", RECIPES[a.recipe](a.report, **opts))
    else:
        page = resolve_page(a.report, a.page)
        print("RESULT:", RECIPES[a.recipe](a.report, page, **opts))

    bad = validate(a.report); dangle = scan_dangling(a.report); schema = check_visual_schema(a.report)
    print(f"validate: {'OK' if not bad else bad}")
    print(f"dangling refs: {len(dangle)}" + (f" {dangle}" if dangle else ""))
    print(f"schema check: {'OK' if not schema else schema}")
    if bad or dangle or schema:
        raise SystemExit("WARNING: integrity check failed -- review before opening in Power BI")

if __name__ == "__main__":
    main()
