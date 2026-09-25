# Finance Lane — AR Opening Balance & Customer Master Hand-off

**Prepared:** 2026-09-16
**For:** Riven ERP finance lane (accounting build in progress)
**Source files:** `ar_and_customer_master_seed.csv` (customer master + opening balance), `open_obligation_register.csv` (open obligations detail), `capture_execution_list.csv` (manual-capture queue).

## What this is

A load-ready seed for the Riven ERP finance lane, built from the **legacy** PES customer estate
(Shopify + legacy ERP / Mercury / Stripe records). The new ERP (`riven_erp_pes`) currently has 0 posted
invoices, 0 payments, and a 4-account stub — this seed is the opening truth it should start from.

## Key totals

| Metric | Value | Source |
|---|---|---|
| Paying customers (deduped) | 283 | `ar_and_customer_master_seed.csv` |
| Lifetime collected revenue | $1,083,826 | same |
| **Opening customer-credit (goods owed)** | **$328,179** | same (177 recovery rows) |
| **Opening AR (owed to company)** | **≈ $605,000** (15 invoices, unnamed) | Mercury reconciliation |
| **Unbooked deposits received (Mercury, Jan 2024–)** | $784,731 | Mercury reconciliation |
| **Unbooked supplier payments** | $489,859 | Mercury reconciliation |
| **Supplier/AP paid (legacy ERP outbound)** | $437,331 (69 suppliers) | `supplier_ap_seed.csv` |
| **Bank deposits total (Jan 2024–present)** | $2,165,341 | Mercury reconciliation |

> **CORRECTION (2026-09-16):** the prior seed said opening AR ≈ $0. That was wrong — there are **15 invoices ≈ $605,000** with no matching payment (outstanding receivables), distinct from the customer-credit position. See `financial_reconciliation_corrected.md`. The 15 customer identities are not yet recoverable from accessible files (need Mercury API or the collection emails).
| Open obligations (paid, unfulfilled) | 175 accounts, $316,992 | `open_obligation_register.csv` |
| Manual-capture queue (authorized, uncaptured) | 108 orders, $125,905 | `manual_capture_triage.csv` |

## Critical accounting framing (read before posting)

The opening position is a **liability, not a receivable.** These customers **paid** and were not
fulfilled. When the finance lane is built:

- Book the 177 recovery rows to a **customer-credit / unearned-revenue / customer-deposit** account,
  NOT accounts receivable. Each is "cash received, goods not yet delivered."
- Seed AR from the Mercury reconciliation, NOT from this file: **≈ $605K outstanding (15 invoices)**.
  This file's `opening_ar_usd` is a placeholder; the real AR lives in 15 invoices that need to be
  named via Mercury once access is restored.
- `lifetime_revenue_usd` is a **reference metric** (historical revenue), not a balance; do not post it.

## Top open obligations (start the recovery queue here)

| Customer | Paid | Owed | Days |
|---|---|---|---|
| Vladimir Tkach | $64,755 | 19 line items | 19 |
| Dennis Willett | $42,647 | generator | — |
| Leon Russell (Wolf River) | $17,674 | 3 items | 232 |
| Theodore Nye | $8,243 | 1 item | 223 |

## Load order when the lane is live

1. Install `l10n_us_account` + US tax setup (per platform requirements map §6).
2. Import `ar_and_customer_master_seed.csv` as `res.partner` customer master (email-keyed, deduped).
3. Post one opening journal entry crediting the customer-credit account $328,179, with per-customer
   detail from the 177 recovery rows.
4. Reconcile the `capture_execution_list.csv` (10 clean Authorize.Net captures = $30,697.82) and
   `manual_capture_triage.csv` (108 orders) before they age out of the authorization window.