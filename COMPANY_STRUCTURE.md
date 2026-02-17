# Corporate Legal Structure — Cassilly Capital Group

> **Canonical Reference Document** | Last Updated: February 17, 2026
>
> This is the single source of truth for the Cassilly Capital corporate hierarchy,
> inter-company billing relationships, and Odoo 19 `res.company` mapping.
>
> **Notion Mirror**: [Corporate Legal Ownership Tree & Inter-Company Billing](https://www.notion.so/30a0639f545181f8b512e74855205c7a)

---

## Entity Name Reference

| Internal Shorthand | Correct Legal Name | DBA / Brand |
|---|---|---|
| "PES Supply" | **Portlandia Electric Supply LLC** | dba Portlandia Electric Solar Supply |
| "DDS" | **Dynamic Distribution Solutions LLC** | dba Portlandia Logistics |
| "BSD" | **Big Sky Dynamics LLC** | Brand: BSDyno |
| "PL Standalone" | **Portlandia Logistics LLC** | *(own entity, own EIN)* |

> **IMPORTANT**: Never use "PES Supply LLC" or "DDS LLC" in legal, banking, or investor documents.
> Those are not real entity names.

---

## Level 0 — Beneficial Owner

**Alex Cassilly** — sole member / manager of both root entities

---

## Level 1 — Two Standalone Wyoming LLCs (Parallel Roots)

```
Alex Cassilly (beneficial owner)
|
+-- Cassilly Capital LLC (WY, foreign-filed KY) -- HoldCo, equity owner of all operating subs
|
+-- STR Capital LLC (WY) -- Asset bank, internal leasing, Entra tenant root
    WARNING: NOT a DBA of Cassilly Capital. The DBA was cancelled.
    These are two separate standalone LLCs.
```

---

## Level 2 — Direct Cassilly Capital Subsidiaries

```
Cassilly Capital LLC
+-- PES Global Group LLC              [Supply Universe]
+-- Big Sky Dynamics LLC               [IT / AI Universe]
+-- Dynamic Distribution Solutions LLC [Logistics Universe]
+-- Portlandia Logistics LLC           [US External Logistics - standalone]
+-- Villeside Realty LLC               [Real Estate Holding]
```

---

## Full Corporate Hierarchy

```
Alex Cassilly (beneficial owner)
|
+-- Cassilly Capital LLC --------------------------------- [Level 1 - HoldCo]
|   |
|   +-- PES Global Group LLC ----------------------------- [Level 2 - Supply Universe]
|   |   +-- Portlandia Electric Supply LLC ---------------- [Level 3 - US Distribution]
|   |   |   dba Portlandia Electric Solar Supply
|   |   |   Ops: 1507 Portland Ave, Louisville KY
|   |   |   Domain: pes.supply / portlandiaelectric.supply
|   |   |   Catalog: 7,880 products (Odoo), 4,942 (Shopify)
|   |   |
|   |   +-- PES Global India HP --------------------------- [Level 3 - India Country Parent]
|   |   |   |   SEZ Tax Principal (0% on export of services)
|   |   |   |   Key person: Amit Pathania
|   |   |   |
|   |   |   +-- PES Supply Kangra ------------------------- [Level 4 - Global Sales Hub]
|   |   |   |   Staff: 5 | Subdomain: kangra.pes.supply
|   |   |   |
|   |   |   +-- PES Supply Lucknow ----------------------- [Level 4 - Data Ops]
|   |   |       Staff: 10-11 | Subdomain: lucknow.pes.supply
|   |   |
|   |   +-- PES Global Pakistan -------------------------- [Level 3 - Pakistan Country Parent]
|   |   |   +-- PES Supply Pakistan ---------------------- [Level 4 - ERP/Dev Hub]
|   |   |
|   |   +-- PES Global Bangladesh ------------------------ [Level 3 - Bangladesh Country Parent]
|   |   |   +-- PES Supply Bangladesh -------------------- [Level 4 - Ops Support]
|   |   |
|   |   +-- PES Caribbean -------------------------------- [Level 3 - DORMANT]
|   |
|   +-- Big Sky Dynamics LLC ----------------------------- [Level 2 - IT/AI Universe]
|   |   dba BSDyno
|   |   Ops: 815 W Market St, Louisville KY
|   |   Domain: bsdyno.com
|   |   Dual identity: Internal PES infra + External SaaS sales
|   |   |
|   |   +-- BSD India HP --------------------------------- [Level 3 - India Country Parent]
|   |   |   +-- BSD India Kangra ------------------------- [Level 4]
|   |   |   +-- BSD India Lucknow ----------------------- [Level 4]
|   |   |   +-- BSD India Chandigarh --------------------- [Level 4]
|   |   |   +-- BSD India Delhi -------------------------- [Level 4]
|   |   |
|   |   +-- BSD Pakistan --------------------------------- [Level 3]
|   |   +-- BSD Bangladesh ------------------------------- [Level 3]
|   |
|   +-- Dynamic Distribution Solutions LLC --------------- [Level 2 - Logistics Universe]
|   |   dba Portlandia Logistics (internal 5PL brand)
|   |   |
|   |   +-- Portlandia Logistics India HP ---------------- [Level 3 - India Country Parent]
|   |   |   +-- Portlandia Logistics Kangra -------------- [Level 4]
|   |   |   +-- Portlandia Logistics Lucknow ------------- [Level 4]
|   |   |
|   |   +-- Portlandia Logistics Pakistan ---------------- [Level 3]
|   |   +-- Portlandia Logistics Bangladesh --------------- [Level 3]
|   |
|   +-- Portlandia Logistics LLC [standalone] ------------ [Level 2 - US External Logistics]
|   |   Ops: 7735 National Turnpike, Louisville KY (30k sqft)
|   |   Own EIN, own credit profile (seasoning independently)
|   |   [No subsidiaries - US-only leaf node]
|   |
|   +-- Villeside Realty LLC ----------------------------- [Level 2 - Real Estate]
|       Owns: 1507 Portland Ave, 7735 National Turnpike, 815 W Market St
|       Revenue: Inter-company rent to PES Supply, DDS, BSD
|       [No subsidiaries - leaf node]
|
+-- STR Capital LLC ------------------------------------- [Level 1 - Asset Bank]
    Owns: Trucks, forklifts, servers, racking, tools, licenses
    Revenue: Recurring inter-company lease invoices
    Also: Microsoft Entra tenant root (NETORGFT10633924)
    [No subsidiaries - leaf node]
```

---

## Inter-Company Billing Matrix

| Seller | Buyer | Product/Service | Trigger |
|---|---|---|---|
| PES Global India HP | Portlandia Electric Supply LLC | Export of Services (SEZ, 0% tax) | Monthly allocation of Amit's team work |
| Dynamic Distribution Solutions LLC | Portlandia Electric Supply LLC | Internal Freight | Per-shipment, auto on delivery confirmation |
| Big Sky Dynamics LLC | All operating nodes | AI Platform Usage / IT Retainer | Monthly, based on agent utilization |
| Portlandia Logistics LLC (standalone) | Portlandia Electric Supply LLC | Vendor Freight (arm's length) | Per-shipment (NOT eliminated - real vendor transaction) |
| STR Capital LLC | All operating nodes | Equipment Lease | Monthly recurring |
| Villeside Realty LLC | Portlandia Electric Supply LLC, Dynamic Distribution Solutions LLC, Big Sky Dynamics LLC | Property Rent | Monthly recurring |

All inter-company flows (except Portlandia Logistics LLC standalone) are eliminated at Cassilly Capital consolidation level.

---

## Asset Ownership Split

| Entity | Owns | Revenue Model |
|---|---|---|
| **STR Capital LLC** | Movable: trucks, forklifts, servers, racking, tools, licenses | Inter-company lease invoices |
| **Villeside Realty LLC** | Real estate: 1507 Portland Ave, 7735 National Turnpike, 815 W Market St | Inter-company rent invoices |

---

## Three Workforce Modes (per operating entity)

| Mode | Legal Relationship | Odoo Object | Example |
|---|---|---|---|
| **Direct Hire** | Employee of entity | `hr.employee` | Amit's 5 staff in Kangra |
| **DBA Storefront** | Same entity, different brand | Same `res.company` | Portlandia Electric Solar Supply (Shopify) |
| **Independent Agent** | Separate LLC/sole prop | `res.partner` with Agent tag | Matt Powell Brokerage, Flores PV |

---

## Partner Lifecycle

```
Stage 1: INDEPENDENT PARTNER (res.partner)
  Uses PES platform as purchasing agent (5% margin)
  Own brand, own customers

Stage 2: MANAGED PARTNER (res.partner, deeper integration)
  PES handles back-office (10-15% margin)

Stage 3: ACQUISITION (res.partner -> res.company)
  Entity becomes subsidiary, full triad deploys
```

---

## Triad Grid by Territory

| Territory | Supply Node | Logistics Node | BSD Node | Status |
|---|---|---|---|---|
| US (KY) | Portlandia Electric Supply LLC | Portlandia Logistics LLC | Big Sky Dynamics LLC | **Active Phase 1** |
| India - Kangra | PES Supply Kangra | Portlandia Logistics Kangra | BSD India Kangra | **Active Phase 1** |
| India - Lucknow | PES Supply Lucknow | Portlandia Logistics Lucknow | BSD India Lucknow | **Active Phase 1** |
| Pakistan | PES Supply Pakistan | Portlandia Logistics Pakistan | BSD Pakistan | Dormant |
| Bangladesh | PES Supply Bangladesh | Portlandia Logistics Bangladesh | BSD Bangladesh | Dormant |

---

## Legacy / Litigation Entities (NOT in Cassilly Tree)

| Entity | Notes |
|---|---|
| Greentech United Ltd (UAE) | Prior venture - Rozana 45% stake dispute |
| US Solar Supplier LLC | Prior venture - Alex squeezed out |

---

## Odoo Phase 1 Active Companies (11 of 28)

| Company | Parent | Role |
|---|---|---|
| Cassilly Capital LLC | *(root)* | Consolidation only |
| STR Capital LLC | *(root - parallel)* | Asset leases only |
| PES Global Group LLC | Cassilly Capital LLC | IP holding + parent |
| Portlandia Electric Supply LLC | PES Global Group LLC | Primary operating company |
| PES Global India HP | PES Global Group LLC | SEZ service exporter |
| PES Supply Kangra | PES Global India HP | Global Sales Hub |
| PES Supply Lucknow | PES Global India HP | Data Ops |
| Big Sky Dynamics LLC | Cassilly Capital LLC | Internal AI/IT + external SaaS |
| Dynamic Distribution Solutions LLC | Cassilly Capital LLC | Internal freight |
| Portlandia Logistics LLC | Cassilly Capital LLC | External 3PL |
| Villeside Realty LLC | Cassilly Capital LLC | Rent invoices only |

Remaining 17 entities: configured but dormant until Phase 2+.

See `odoo/data/res_company_hierarchy.csv` for complete import-ready data.
