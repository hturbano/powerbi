# Setup Guide

## Prerequisites

- Node.js 18+ (for MCP servers)
- Python 3.10+ (for validation scripts)
- Claude Code or Cursor
- Git

## Clone the Repository

```bash
git clone <repo-url>
cd powerbi-report-factory
```

## Set Up MCP Servers

### Option 1: Automated Setup

```bash
bash scripts/setup-mcp.sh
```

This script installs and configures both MCP servers for Claude Code.

### Option 2: Manual Setup

#### powerbi-report-mcp

```bash
# Clone the MCP server
git clone https://github.com/jonathan-pap/powerbi-report-mcp.git
cd powerbi-report-mcp
npm install
npm run build
```

Add to your Claude Code MCP settings (`~/.claude/settings.json` or project `.claude/settings.json`):

```json
{
    "mcpServers": {
        "powerbi-report": {
            "command": "node",
            "args": ["/absolute/path/to/powerbi-report-mcp/dist/index.js"]
        }
    }
}
```

#### powerbi-modeling-mcp

```bash
# Clone the MCP server
git clone https://github.com/microsoft/powerbi-modeling-mcp.git
cd powerbi-modeling-mcp
npm install
npm run build
```

Add to MCP settings:

```json
{
    "mcpServers": {
        "powerbi-modeling": {
            "command": "node",
            "args": ["/absolute/path/to/powerbi-modeling-mcp/dist/index.js"]
        }
    }
}
```

### Cursor Setup

For Cursor, add the MCP servers to `.cursor/mcp.json` in the project root:

```json
{
    "mcpServers": {
        "powerbi-report": {
            "command": "node",
            "args": ["/absolute/path/to/powerbi-report-mcp/dist/index.js"]
        },
        "powerbi-modeling": {
            "command": "node",
            "args": ["/absolute/path/to/powerbi-modeling-mcp/dist/index.js"]
        }
    }
}
```

## Verify Setup

1. Open the project in Claude Code or Cursor
2. Ask: "What Power BI tools do you have access to?"
3. You should see tools from both powerbi-report-mcp and powerbi-modeling-mcp

## Generate Your First Report

```
Build a student attendance dashboard with:
- KPI cards for total enrollment, attendance rate, and ADA percentage
- Monthly trend line for attendance
- Campus breakdown bar chart
- Date slicer for school year filtering
- Use the corporate theme
```

## Clone an Example Report

To use an example report as a starting point:

```bash
cp -r examples/report-1-sales-dashboard my-new-report
# Edit the report.json to match your data source
# Open in Claude Code and describe your modifications
```

## Deploy a Report (Optional)

If you have Microsoft Fabric access:

```bash
# Install fabric-cli
pip install ms-fabric-cli

# Authenticate
fab auth login

# Import report to workspace
fab report import --workspace <workspace-id> --file my-new-report/
```

## Troubleshooting

### MCP tools not showing up
- Restart Claude Code/Cursor after updating MCP settings
- Check that paths in settings are absolute, not relative
- Verify the MCP server builds without errors

### .pbip fails to import
- Run `python scripts/validate-pbip.py <path>` to check for issues
- Ensure `[Content_Types].xml` is present
- Check schema version in report.json

### Theme not applying
- Verify theme JSON is valid (no trailing commas)
- Check that color format includes alpha channel: `#FF605E5C`
- Ensure theme is applied to `definition/report.json`, not just individual visuals
