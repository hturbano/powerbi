#!/usr/bin/env python3
"""
Validate a Power BI .pbip report file for design system compliance and MCP gotchas.

Usage:
    python scripts/validate-pbip.py <path-to-report-directory>

Checks:
    - No invalid visual types (e.g., stackedBarChart)
    - All actionButton visuals have howCreated field
    - No hardcoded colors (should use theme references)
    - Required files present (report.json, [Content_Types].xml)
    - Valid JSON structure
    - Schema version is current
"""

import json
import os
import sys
from pathlib import Path
from typing import List, Tuple

# Invalid visual types that should be replaced
INVALID_VISUAL_TYPES = {
    "stackedBarChart": "Use 'barChart' with stacked orientation",
    "stackedColumnChart": "Use 'columnChart' with stacked orientation",
    "stackedAreaChart": "Use 'areaChart' with stacked orientation",
}

# Required fields for specific visual types
REQUIRED_FIELDS = {
    "actionButton": ["howCreated"],
}

# Required files in a .pbip package
REQUIRED_FILES = [
    "definition/report.json",
    "[Content_Types].xml",
]

# Current PBIR schema version
CURRENT_SCHEMA_VERSION = "1.0"


def find_json_files(directory: str) -> List[str]:
    """Find all JSON files in the report directory."""
    json_files = []
    for root, dirs, files in os.walk(directory):
        # Skip node_modules and .git
        dirs[:] = [d for d in dirs if d not in ("node_modules", ".git", "__pycache__")]
        for f in files:
            if f.endswith(".json"):
                json_files.append(os.path.join(root, f))
    return json_files


def check_required_files(directory: str) -> List[Tuple[str, str]]:
    """Check that all required files are present."""
    issues = []
    for req_file in REQUIRED_FILES:
        full_path = os.path.join(directory, req_file)
        if not os.path.exists(full_path):
            issues.append(("ERROR", f"Missing required file: {req_file}"))
    return issues


def check_visual_types(json_data: dict, file_path: str) -> List[Tuple[str, str]]:
    """Check for invalid visual types in report JSON."""
    issues = []

    def traverse(obj, path=""):
        if isinstance(obj, dict):
            # Check visual type
            vtype = obj.get("visualType", "")
            if vtype in INVALID_VISUAL_TYPES:
                issues.append((
                    "ERROR",
                    f"[{file_path}] Invalid visual type '{vtype}' at {path}. {INVALID_VISUAL_TYPES[vtype]}"
                ))

            # Check required fields for visual types
            if vtype in REQUIRED_FIELDS:
                for field in REQUIRED_FIELDS[vtype]:
                    if field not in obj:
                        issues.append((
                            "ERROR",
                            f"[{file_path}] Visual type '{vtype}' missing required field '{field}' at {path}"
                        ))

            # Check for hardcoded colors
            for key, value in obj.items():
                if isinstance(value, str) and value.startswith("#") and len(value) == 7:
                    issues.append((
                        "WARNING",
                        f"[{file_path}] Possible hardcoded color '{value}' at {path}.{key}. Use theme reference instead."
                    ))

                traverse(value, f"{path}.{key}")

        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                traverse(item, f"{path}[{i}]")

    traverse(json_data)
    return issues


def check_schema_version(json_data: dict, file_path: str) -> List[Tuple[str, str]]:
    """Check that the schema version is current."""
    issues = []
    version = json_data.get("version", json_data.get("schemaVersion", ""))
    if version and str(version) != CURRENT_SCHEMA_VERSION:
        issues.append((
            "WARNING",
            f"[{file_path}] Schema version '{version}' may be outdated. Current: {CURRENT_SCHEMA_VERSION}"
        ))
    return issues


def validate_report(directory: str) -> List[Tuple[str, str]]:
    """Run all validation checks on a report directory."""
    all_issues = []

    # Check required files
    all_issues.extend(check_required_files(directory))

    # Check JSON files
    json_files = find_json_files(directory)
    if not json_files:
        all_issues.append(("ERROR", "No JSON files found in report directory"))
        return all_issues

    for jf in json_files:
        try:
            with open(jf, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            all_issues.append(("ERROR", f"Invalid JSON in {jf}: {e}"))
            continue

        all_issues.extend(check_visual_types(data, jf))
        all_issues.extend(check_schema_version(data, jf))

    return all_issues


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    report_dir = sys.argv[1]
    if not os.path.isdir(report_dir):
        print(f"ERROR: '{report_dir}' is not a directory")
        sys.exit(1)

    print(f"Validating: {report_dir}")
    print("=" * 60)

    issues = validate_report(report_dir)

    errors = [i for i in issues if i[0] == "ERROR"]
    warnings = [i for i in issues if i[0] == "WARNING"]

    if not issues:
        print("✓ All checks passed!")
        sys.exit(0)

    for severity, message in issues:
        icon = "✗" if severity == "ERROR" else "⚠"
        print(f"  {icon} [{severity}] {message}")

    print("")
    print(f"Results: {len(errors)} error(s), {len(warnings)} warning(s)")

    if errors:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
