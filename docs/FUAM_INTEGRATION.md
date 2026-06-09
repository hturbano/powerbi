# FUAM Integration (Future Section)

## What is FUAM?

FUAM (Fabric Unified Admin Monitoring) is a monitoring and analytics solution for Microsoft Fabric tenants. Originally built by GT-Analytics (https://github.com/GT-Analytics/fuam-basic) and now adopted into Microsoft's official fabric-toolbox (https://github.com/microsoft/fabric-toolbox).

## Why It Pairs With This Repo

While this report factory focuses on **building** reports, FUAM focuses on **monitoring** them. Together, they form a complete Power BI operations lifecycle:

```
FUAM (Monitor) → Identify Issues → Report Factory (Build/Update) → fabric-cli (Deploy)
```

### FUAM Provides:
- **30+ days of usage analytics** — which reports are being opened, by whom, how often
- **Capacity metrics** — CU utilization, refresh duration, bottleneck identification
- **Activity logs** — who created, modified, or deleted reports
- **Workspace analytics** — sprawl detection, orphaned workspaces
- **Refresh monitoring** — success rates, duration trends, failure patterns

### This Repo Provides:
- **Design system** — consistent, on-brand reports
- **AI generation** — fast report creation from natural language
- **Validation** — automated quality checks before deployment
- **Deployment** — fabric-cli integration for CI/CD

## How to Integrate

### Step 1: Deploy FUAM

Deploy FUAM to a monitoring workspace in your Fabric tenant:
```bash
# Follow the deployment guide at:
# https://github.com/microsoft/fabric-toolbox/tree/main/monitoring/fabric-unified-admin-monitoring
```

### Step 2: Let Data Accumulate

FUAM needs 30-60 days of data collection before it provides meaningful insights.

### Step 3: Connect Report Factory

Use the usage data from FUAM to drive report prioritization:

1. **Low usage reports** → Archive or redesign using this factory
2. **High usage reports** → Apply design system for consistency
3. **Failed refreshes** → Build monitoring dashboards using this factory
4. **Capacity trends** → Create capacity planning reports

### Step 4: Build FUAM Dashboards

Use this report factory to build executive dashboards on top of FUAM's Lakehouse data:

```
"Build a Fabric Tenant Health dashboard showing:
- Report usage trends (top 10 most/least used)
- Capacity utilization heatmap
- Refresh failure rate by workspace
- Workspace growth over time
- Use the dark mode theme"
```

## Architecture

```
┌─────────────────────────────────────────────────┐
│              Microsoft Fabric Tenant              │
│                                                   │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐   │
│  │  FUAM    │    │  Report  │    │ fabric-  │   │
│  │ Monitoring│───▶│ Factory  │───▶│   cli    │   │
│  │(observe) │    │ (build)  │    │(deploy)  │   │
│  └──────────┘    └──────────┘    └──────────┘   │
│       │              │                │           │
│       ▼              ▼                ▼           │
│  Lakehouse     .pbip files     Live reports      │
│  (raw data)   (versioned)    (in production)     │
└─────────────────────────────────────────────────┘
```

## Roadmap for Full Integration

- [ ] Create FUAM data source connector for the report factory
- [ ] Build FUAM-to-Report-Factory data pipeline
- [ ] Add FUAM-specific layout templates (tenant health, capacity planning)
- [ ] Create FUAM-aware validation checks (flag reports with low usage)
- [ ] Integrate FUAM data into example reports

## References

- FUAM Basic: https://github.com/GT-Analytics/fuam-basic
- Microsoft fabric-toolbox: https://github.com/microsoft/fabric-toolbox
- FUAM Module: https://github.com/microsoft/fabric-toolbox/tree/main/monitoring/fabric-unified-admin-monitoring
