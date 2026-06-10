"""
Shared helpers for Company Design System recipes.

All recipes operate on an *enhanced PBIR* report (a `.Report` folder containing a
`definition/` subfolder). Power BI Desktop MUST be closed while recipes run, or it
will clobber the edits on its next save.

PBIR primer:
  <Report>/definition/pages/<pageId>/page.json                 page-level settings
  <Report>/definition/pages/<pageId>/visuals/<id>/visual.json  one visual
Visuals are discovered by folder; there is no central manifest. A visual's `name`
must equal its folder name. Cross-filter relationships live in page.json
`visualInteractions` and reference visual ids -- keep them consistent.
"""
import json, os, glob, secrets

# ---------------------------------------------------------------- io
def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)

def save(path, data):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)

def new_id():
    """20-hex-char id matching Power BI's visual id format."""
    return secrets.token_hex(10)

# ---------------------------------------------------------------- paths
def pages_dir(report):
    return os.path.join(report, "definition", "pages")

def page_json(report, page_id):
    return os.path.join(pages_dir(report), page_id, "page.json")

def visual_files(report, page_id):
    return glob.glob(os.path.join(pages_dir(report), page_id, "visuals", "*", "visual.json"))

def resolve_page(report, name_or_id):
    """Accept a page display name OR a page id; return the page id."""
    pd = pages_dir(report)
    if os.path.isdir(os.path.join(pd, name_or_id)):
        return name_or_id
    for pj in glob.glob(os.path.join(pd, "*", "page.json")):
        if load(pj).get("displayName") == name_or_id:
            return os.path.basename(os.path.dirname(pj))
    raise SystemExit(f"page not found: {name_or_id}")

# ---------------------------------------------------------------- expr builders
def lit(value):
    """Power BI literal expr. value is the raw literal string, e.g. \"true\", \"14D\", \"'aboveValue'\"."""
    return {"expr": {"Literal": {"Value": value}}}

def litcolor(hexv):
    return {"solid": {"color": {"expr": {"Literal": {"Value": "'%s'" % hexv}}}}}

def quote(s):
    return "'%s'" % s

# ---------------------------------------------------------------- visual helpers
def vtype(d):
    return d.get("visual", {}).get("visualType", "")

def objects(d):
    return d.get("visual", {}).setdefault("objects", {})

def container(d):
    return d.get("visual", {}).setdefault("visualContainerObjects", {})

def title_text(d):
    """Return the existing title text literal (with quotes) if present, else None."""
    for item in d.get("visual", {}).get("visualContainerObjects", {}).get("title", []):
        t = item.get("properties", {}).get("text")
        if t:
            return t
    return None

def measure_ref(d):
    """First measure queryRef on the visual, e.g. '_Measures.Total'. None if not found."""
    import re
    m = re.search(r'"queryRef"\s*:\s*"([^"]+)"', json.dumps(d.get("visual", {})))
    return m.group(1) if m else None

# ---------------------------------------------------------------- safety
def validate(report):
    """Return list of files that fail to parse as JSON."""
    bad = []
    for f in glob.glob(os.path.join(report, "definition", "**", "*.json"), recursive=True):
        try:
            load(f)
        except Exception as e:
            bad.append((f, str(e)))
    return bad

def scan_dangling(report):
    """Return page visualInteractions that reference visuals not present on the page."""
    out = []
    for pj in glob.glob(os.path.join(pages_dir(report), "*", "page.json")):
        pid = os.path.basename(os.path.dirname(pj))
        present = {os.path.basename(os.path.dirname(f)) for f in visual_files(report, pid)}
        for it in load(pj).get("visualInteractions", []):
            for k in ("source", "target"):
                if k in it and it[k] not in present:
                    out.append((pid, it[k]))
    return out

CHART_TYPES = {"clusteredColumnChart", "columnChart", "clusteredBarChart", "barChart",
               "lineChart", "pieChart", "donutChart", "hundredPercentStackedBarChart",
               "areaChart", "ribbonChart", "scatterChart", "waterfallChart"}
TITLE_TYPES = CHART_TYPES | {"tableEx", "pivotTable", "card", "cardVisual", "slicer", "matrix"}
