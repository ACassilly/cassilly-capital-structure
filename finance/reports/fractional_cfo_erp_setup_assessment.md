# Fractional-CFO Assessment — Riven ERP Finance Setup

Prepared 2026-09-25 against the live ERP (`riven_erp_pes`). Every number below was read from the live system this session, not recalled.

## Headline

The ERP's **skeleton is healthy — the body isn't on it yet.** Chart of accounts, taxes, journals, and payment terms exist, but the finance lane has no fiscal calendar, no opening balances, no bank statements, and an AP/AR stack that exists only as a few posted documents. ~$1.8M of real money history is sitting outside the system in Mercury + Stripe.

## What's already configured (do not rebuild)

| Layer | Live state |
|---|---|
| Chart of accounts | 111 accounts (assets/liabilities/equity/income/expense; 18 reconcilable) |
| Taxes | 46 (23 sale + 23 purchase, all percent-based, price-excluded) |
| Fiscal positions | 2 |
| Journals | 11 (incl. Bank BNK1, Cash CSH, Legacy Customer Invoices LINV) |
| Payment methods | 9 |
| Payment terms | 14 |
| Payment providers | 25 records |
| Currency | USD (1 active) |
| Company | 1 (single-company) |

## Critical gaps — money path (P0)

1. **Zero payments recorded.** The system has never marked a single dollar received or paid. Merchant cash sits in Mercury, card volume in Stripe — none of it is in Riven ERP.
2. **No fiscal year.** `fiscal.years = 0`. No accounting periods, no period lock, no way to close a month or run a period-on-period P&L. This is the single most blocking config item for any real bookkeeping.
3. **No opening balances.** One journal entry exists total. Equity/retained-earnings and every balance-sheet opening line are missing, so even after payments are imported the balance sheet won't balance to the bank.
4. **Duplicate AR / AP accounts.** Three AR accounts (`101300`, `110000`, `121000`) and multiple AP (`200000`, `211000`, `252000`). Consolidate to one canonical AR (121000) and one canonical AP before importing anything, or the ledger will scatter.
5. **No bank statements (0), one recorded bank account.** Reconciliation can't run until Mercury and the operating bank exist as `res.partner.bank` + journals and statements are posted.

## Payables — ready to configure, currently dark (P1)

- **5 posted bills = $285,852.40**, all `not_paid`. No outbound payment has ever been recorded against them.
- **29 purchase orders = $307,604.52** (8 confirmed, 9 sent). No receiving → bill → pay flow has completed end-to-end.
- Setup needed: AP aging view, vendor payment batches against Bank/Cash journals, and a 3-way-match habit (PO → receipt → bill).

## Receivables — ready to load, currently dark (P1)

- **2 posted customer invoices; 14 legacy collectable invoices ($422,126) not migrated.** Post them to the `LINV` journal so collection finally happens inside the system.
- Stripe disabled; Mercury absent. To accept money natively: enable Stripe (or a Mercury-transfer payment method) and wire `payment.provider` to the restored mail transport so receipts auto-post.

## Inventory & COGS — misconfigured (P1)

- **24,584 products, but only 116 carry a cost** (`standard_price > 0`) and **1 stock quant on hand**.
- Consequence: no COGS, no margin per order, no landed-cost. Until product costs + reordering rules land, every sale invoices at revenue with a blank cost line.

## HR / payroll — absent (P2)

- No `hr.contract` or `hr.payslip` models, though salary/tax payable accounts exist. Payroll can't run until the HR+Payroll apps are installed and the fiscal year + payroll accounts are wired.

## Governance & controls (P2)

- Approval matrix incomplete (12 approval requests sitting). Define who can confirm PO, post payment, and lock a period.
- No fiscal-period close policy. Establish monthly close + opening-balance reconciliation before the first real ledger month.
- Duplicate AR/AP cleanup must precede any import (see P0 #4).

## Recommended sequence

1. **Consolidate AR/AP accounts** to single canonical accounts (121000 AR, 200000 AP).
2. **Create the fiscal year + periods** and set period-lock policy.
3. **Load opening balances** (bank cash, founder capital $182,313, equity) from Mercury + Stripe opening positions.
4. **Post the migration** per `legacy_finance_migration_plan.md` — Mercury/Stripe history into Bank journal, 14 AR invoices into LINV.
5. **Enable native pay-in** (Stripe provider) + **post vendor payments** for the 5 open bills.
6. **Fix inventory costing** (product costs + reordering) so COGS exists.
7. **Install HR/Payroll** and run first payroll once fiscal year is live.

## Supporting files

- `legacy_finance_migration_plan.md` — phased money migration.
- `payment_import_manifest.csv` — row-level source→partner map for the payment import.
- `PES_BodyOfWork_Master_Export.xlsx` — full finance picture + guides.
