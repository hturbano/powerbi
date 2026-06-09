#!/bin/bash
# Setup script for Power BI Report Factory MCP servers
# Run: bash scripts/setup-mcp.sh

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MCP_DIR="$REPO_ROOT/.mcp-servers"

echo "=== Power BI Report Factory MCP Setup ==="
echo ""

# Check prerequisites
command -v node >/dev/null 2>&1 || { echo "ERROR: Node.js 18+ required. Install from https://nodejs.org"; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "ERROR: npm required"; exit 1; }
command -v git >/dev/null 2>&1 || { echo "ERROR: git required"; exit 1; }

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "ERROR: Node.js 18+ required. Current: $(node -v)"
    exit 1
fi

echo "Node.js: $(node -v) ✓"
echo ""

# Create MCP directory
mkdir -p "$MCP_DIR"

# Install powerbi-report-mcp
echo "Installing powerbi-report-mcp..."
if [ -d "$MCP_DIR/powerbi-report-mcp" ]; then
    echo "  Already installed, pulling latest..."
    cd "$MCP_DIR/powerbi-report-mcp" && git pull
else
    git clone https://github.com/jonathan-pap/powerbi-report-mcp.git "$MCP_DIR/powerbi-report-mcp"
fi
cd "$MCP_DIR/powerbi-report-mcp"
npm install
npm run build
echo "  powerbi-report-mcp installed ✓"
echo ""

# Prepare powerbi-modeling-mcp
# NOTE: The microsoft/powerbi-modeling-mcp repo is docs-only (no package.json).
# The server ships as the npm package @microsoft/powerbi-modeling-mcp and is run
# via npx — npx downloads/caches it on first use, so there is nothing to build here.
echo "Preparing powerbi-modeling-mcp (npx)..."
echo "  Pre-warming npx cache (downloads the package)..."
npx -y @microsoft/powerbi-modeling-mcp@latest --help >/dev/null 2>&1 || {
    echo "  WARNING: could not pre-warm @microsoft/powerbi-modeling-mcp."
    echo "           It will still be fetched by npx at runtime."
}
echo "  powerbi-modeling-mcp ready ✓"
echo ""

# Generate MCP config
# Claude Code reads project MCP servers from .mcp.json at the repo root.
# Cursor reads them from .cursor/mcp.json. The report server runs from the built
# dist; the modeling server runs via npx (no local build).
echo "Generating MCP configuration..."

CLAUDE_MCP="$REPO_ROOT/.mcp.json"
CURSOR_SETTINGS="$REPO_ROOT/.cursor"

mkdir -p "$CURSOR_SETTINGS"

read -r -d '' MCP_JSON << EOF || true
{
    "mcpServers": {
        "powerbi-report": {
            "type": "stdio",
            "command": "node",
            "args": ["$MCP_DIR/powerbi-report-mcp/dist/index.js"]
        },
        "powerbi-modeling": {
            "type": "stdio",
            "command": "npx",
            "args": ["-y", "@microsoft/powerbi-modeling-mcp@latest", "--start"]
        }
    }
}
EOF

# Claude Code (.mcp.json) and Cursor (.cursor/mcp.json) use the same schema
printf '%s\n' "$MCP_JSON" > "$CLAUDE_MCP"
printf '%s\n' "$MCP_JSON" > "$CURSOR_SETTINGS/mcp.json"

echo "  Claude Code config: $CLAUDE_MCP"
echo "  Cursor config: $CURSOR_SETTINGS/mcp.json"
echo ""

echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "1. Open this project in Claude Code or Cursor"
echo "2. Ask: 'What Power BI tools do you have access to?'"
echo "3. Start building: 'Build a student attendance dashboard with KPI cards and trends'"
