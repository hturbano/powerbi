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

# Install powerbi-modeling-mcp
echo "Installing powerbi-modeling-mcp..."
if [ -d "$MCP_DIR/powerbi-modeling-mcp" ]; then
    echo "  Already installed, pulling latest..."
    cd "$MCP_DIR/powerbi-modeling-mcp" && git pull
else
    git clone https://github.com/microsoft/powerbi-modeling-mcp.git "$MCP_DIR/powerbi-modeling-mcp"
fi
cd "$MCP_DIR/powerbi-modeling-mcp"
npm install
npm run build
echo "  powerbi-modeling-mcp installed ✓"
echo ""

# Generate MCP config
echo "Generating MCP configuration..."

CLAUDE_SETTINGS="$REPO_ROOT/.claude"
CURSOR_SETTINGS="$REPO_ROOT/.cursor"

mkdir -p "$CLAUDE_SETTINGS" "$CURSOR_SETTINGS"

# Claude Code settings
cat > "$CLAUDE_SETTINGS/settings.json" << EOF
{
    "mcpServers": {
        "powerbi-report": {
            "command": "node",
            "args": ["$MCP_DIR/powerbi-report-mcp/dist/index.js"]
        },
        "powerbi-modeling": {
            "command": "node",
            "args": ["$MCP_DIR/powerbi-modeling-mcp/dist/index.js"]
        }
    }
}
EOF

# Cursor settings
cat > "$CURSOR_SETTINGS/mcp.json" << EOF
{
    "mcpServers": {
        "powerbi-report": {
            "command": "node",
            "args": ["$MCP_DIR/powerbi-report-mcp/dist/index.js"]
        },
        "powerbi-modeling": {
            "command": "node",
            "args": ["$MCP_DIR/powerbi-modeling-mcp/dist/index.js"]
        }
    }
}
EOF

echo "  Claude Code settings: $CLAUDE_SETTINGS/settings.json"
echo "  Cursor settings: $CURSOR_SETTINGS/mcp.json"
echo ""

echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "1. Open this project in Claude Code or Cursor"
echo "2. Ask: 'What Power BI tools do you have access to?'"
echo "3. Start building: 'Build a student attendance dashboard with KPI cards and trends'"
