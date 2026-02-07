# Cross-Billing Rules - Cassilly Capital Structure

## Louisville Inner-City Billing (Kentucky Operations)

### Active Billing Relationships

| From Entity | To Entity | Service | Rate/Fee | Odoo Trigger |
|-------------|-----------|---------|----------|-------------|
| PES Supply US<br/>(1507 Portland Ave) | Portlandia Logistics<br/>(7735 National Turnpike) | Freight brokerage | **7% commission** on shipment value | Auto-invoice on Delivery Order |
| Big Sky Dynamics<br/>(815 W Market St) | PES Supply US | IT/CRM/Odoo services | **Cost-plus 20%** | Monthly service invoice |
| Big Sky Dynamics | PES Global SEZ (India/Pak/Bang) | Tech infrastructure | **Cost-plus 20%** | Quarterly intercompany |
| Portlandia Logistics | PES Supply US | Warehouse staging (30k sq ft) | **Flat fee/hour** TBD | Usage-based monthly |
| Portlandia Logistics | Big Sky Dynamics | Local staging | **Flat fee/hour** TBD | Usage-based monthly |

### Global Cross-Billing

| From Entity | To Entity | Service | Tax Treatment |
|-------------|-----------|---------|---------------|
| PES Global SEZ India | PES Supply US | Principal procurement profit | **0% India SEZ tax**<br/>20-28% margin |
| PES Supply US | US Contractors | Product sales | **26% US corporate tax**<br/>5% margin (sales only) |
| Joe's Electric (Partner) | End Customers | Catalog sales | **15% revenue share** to Joe's<br/>Auto-calculated in Odoo |

## Odoo Configuration

### Inter-Company Rules Setup

```yaml
Accounting → Configuration → Inter-Company Transactions:
  - Enable: ✓ Synchronize Invoice/Bill
  - Enable: ✓ Synchronize Sales Order/Purchase Order
  - Currency: USD (primary), INR/PKR/BDT (SEZ branches)
  - Journals: Auto-create AR/AP per company
  - Tax Mapping: SEZ 0% → US 26%
```

### Freight Commission (7%) - Automated

**Trigger**: PES Supply US creates Sales Order with delivery

**Flow**:
1. SO confirmed → Delivery Order created
2. Upon DO validation → Auto-generate supplier bill:
   - Supplier: Portlandia Logistics
   - Product: "Freight Brokerage Service"
   - Quantity: 1
   - Unit Price: SO Total × 0.07
   - Journal: PES Supply US Purchases
3. Portlandia receives auto-invoice (customer invoice side)

**Odoo Setup**:
- Product: "Freight - 7% Commission" (service type)
- Automated Action: Trigger on `stock.picking` state = done
- Python code: Calculate 7% of related SO, create purchase.order

### Tech Services (Cost-Plus 20%) - Monthly

**Trigger**: Manual monthly invoice from Big Sky Dynamics

**Flow**:
1. Big Sky tracks time/expenses in Project module
2. Month-end: Generate invoice to PES entities
   - Cost basis: Actual hours × $X/hour + expenses
   - Markup: Cost × 1.20
   - Product: "IT Services - Monthly"
3. PES entities auto-receive as supplier bills

**Odoo Setup**:
- Big Sky Dynamics → Sales → Customers → Add PES Supply US (Inter-company)
- Product: "IT Services" with cost-plus pricelist (20% markup)
- Timesheet integration: Project → Invoice automatically

### SEZ India Profit Flow (0% Tax)

**Trigger**: Purchase from manufacturer → Resale to PES US

**Flow**:
1. PES Global SEZ purchases inventory (FOB India)
2. Marks up 20-28% for principal profit
3. Sells to PES Supply US (intercompany transfer)
4. PES US resells to contractors (5% margin)

**Tax Treatment**:
- India SEZ: 0% corporate tax (SEZ holiday until 2035)
- PES US: 26% tax on 5% margin only
- **Result**: 60-75% of profit taxed at 0%

**Odoo Setup**:
- Fiscal Position: "SEZ Export" (0% tax)
- Fiscal Position: "US Domestic" (26% rate)
- Auto-apply based on company + customer location

## Revenue Share Partners

### Joe's Electric (Nashville)

**Model**: Partner accesses PES catalog via portal, sells to their customers

**Commission**: 15% of gross revenue on PES-generated sales

**Odoo Flow**:
1. Joe's creates quote via portal (PES products)
2. Upon SO confirmation → Commission rule triggers
3. Auto-calculate: SO Total × 0.15
4. Journal entry: Debit "Partner Commission Expense", Credit "Joe's Electric Payable"
5. Monthly payout via ACH

**Setup**:
- Contact: Joe's Electric (Partner type)
- Commission product: "Partner Revenue Share - 15%"
- Automated Action: On SO confirmation, create commission journal entry

## Consolidated Reporting

### Cassilly Capital View

All subsidiary P&Ls roll up to Cassilly:

```
Revenue:
  - PES Supply US Sales: $X
  - PES Global SEZ Sales: $Y
  - Big Sky Services: $Z
  
Cross-Billing Eliminations:
  - Big Sky → PES (internal): -$Z
  - PES US → Portlandia (commission): Expense line
  - SEZ → PES US (intercompany): Consolidated inventory
  
Net Profit After Tax:
  - Consolidated across all entities
  - Effective tax rate: ~10-15% (blended vs 26% all-US)
```

**Odoo Multi-Company Consolidation**:
- Accounting → Reporting → Consolidated Reports
- Parent company: Cassilly Capital
- Auto-eliminate intercompany transactions

## Billing Cycle

| Entity Pair | Frequency | Due Terms |
|-------------|-----------|----------|
| PES ↔ Portlandia | Per-shipment | Net 15 |
| Big Sky → PES/SEZ | Monthly | Net 30 |
| SEZ → PES US | Per-transfer | Net 30 |
| PES → Partners (Joe's) | Monthly payout | Net 15 |

## Dispute Resolution

All inter-entity disputes escalate to:
- **Cassilly Capital LLC** (Alex Cassilly - final authority)
- Governed by Wyoming LLC operating agreements
- Arbitration clause (Louisville, KY venue for Kentucky entities)

---
*Last Updated: February 7, 2026*
