# Cassilly Capital LLC - Corporate Structure

> **📚 CANONICAL DOCUMENTATION:** This repository contains the single source of truth for Cassilly Capital Group corporate structure.
> 
> - **[COMPANY_STRUCTURE.md](./COMPANY_STRUCTURE.md)** - Complete 28-entity legal hierarchy with correct entity names
> - **Entity Name Reference** - Always use full legal names (e.g., "Portlandia Electric Supply LLC", NOT "PES Supply")
> - **Odoo Import Data** - See `res_company_hierarchy.csv` (coming soon)

---

**Ultimate Holding Company** | Wyoming LLC → Foreign Filed Kentucky

## Overview
Cassilly Capital LLC serves as the top-tier holding company for a diversified portfolio spanning supply chain distribution (PES Global Group), technology services (Big Sky Dynamics), logistics partnerships (Portlandia), and strategic partner acquisitions.

## Entity Structure

```
Cassilly Capital LLC (Wyoming)
├── WY Registered Agent: 30 N Gould St Ste N, Sheridan, WY 82801
├── KY Main Office: Louisville, Kentucky (operational hub)
└── Subsidiaries:
    ├── PES Global Group LLC (Wyoming)
    │   ├── PES Global Group SEZ (India HP/Lucknow - 0% tax principal)
    │   │   ├── PES Supply Lucknow SEZ (10-11 staff)
    │   │   ├── PES Supply Kangra SEZ (5 staff)
    │   │   ├── PES Supply Lahore SEZ (14-15 staff)
    │   │   └── PES Supply Dhaka SEZ (2-4 staff)
    │   └── PES Supply US
    │       ├── Main: 1507 Portland Ave, Louisville KY
    │       └── Branch: 7735 National Turnpike (warehouse/staging)
    ├── Big Sky Dynamics LLC (Wyoming)
    │   ├── Main: 815 W Market St Suite 303, Louisville KY 40202
    │   ├── EIN: 99-4212842
    │   └── Bank: Stock Yards #083000564 / Acct 430161859
    └── Partner Network
        ├── Portlandia Logistics (freight broker - 7% commission)
        └── Joe's Electric (Nashville - 15% revenue share)
```

## Key Advantages
- **Tax Optimization**: Wyoming 0% state tax on holding company profits
- **SEZ Benefits**: India operations at 0% tax (10-year holiday); UAE migration planned
- **Privacy**: Wyoming LLC shields ownership details
- **Consolidation**: Unified P&L across 10+ global entities
- **Cross-Billing**: Automated intercompany invoicing via Odoo ERP

## Documentation
- `/docs/org-chart.md` - Visual hierarchy diagrams
- `/odoo-config/` - Company setup JSON exports
- `/billing/` - Cross-billing templates and rules
- `/migration/` - SEZ tax migration roadmap (4 phases)
- `/staff/` - Branch directories and org structure
- `/legal/` - Operating agreements, foreign filing status

## Quick Links
- [Odoo Setup Guide](./odoo-config/SETUP.md)
- [Cross-Billing Rules](./billing/RULES.md)
- [Migration Strategy](./migration/PHASES.md)
- [Staff Directory](./staff/DIRECTORY.md)

## Contact
**Cassilly Capital LLC**
Louisville, Kentucky
Alex Cassilly - CEO

---
*Last Updated: February 7, 2026*
