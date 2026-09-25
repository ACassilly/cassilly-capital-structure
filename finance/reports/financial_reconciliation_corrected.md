# PES Supply — Consolidated Financial Reconciliation (corrected)

**Prepared:** 2026-09-16 · Corrects the earlier "July 2025 floor / AR = $0" conclusions.

## The true floor is January 2024, but per-customer detail bottom out at July/Aug 2025

Two different data depths exist:

| Source | Window | What's accessible |
|---|---|---|
| **Mercury bank** (authoritative cash) | **Jan 2024 → present** | Aggregate only (from prior agent's Aug 8 report) — raw 5,105-txn dump was NOT saved in the project |
| Shopify paid orders | Jul 2025 → Aug 2026 | Full per-customer (237 orders, 463 total) |
| legacy ERP payments (reconciliation_data) | **Aug 2025 → Aug 2026** | Full per-customer (102 inbound, 161 outbound) |
| legacy ERP partners / CRM leads | n/a (no date field) | 2,000 partners, 605 leads |

## Confirmed per-customer figures (what's actually in hand)

| Metric | Value |
|---|---|
| Paying customers (Shopify 206 + legacy ERP 77, deduped) | 283 |
| Lifetime collected (confirmed) | $1,083,826 |
| legacy ERP inbound payments (102 payments / 77 partners) | $748,525 |
| legacy ERP outbound supplier payments (161 payments / 69 suppliers) | $437,331 |
| Open obligations (paid, unfulfilled) | 175 accounts / $316,992 |
| Manual-capture queue (Authorize.Net authorized, uncaptured) | 108 orders / $125,905 |

## Mercury-reported aggregates (Jan 2024 → present, from prior reconciliation)

| Metric | Value |
|---|---|
| Total bank deposits | $2,165,341 |
| Total withdrawals | $2,677,431 |
| Net cash flow | −$512,091 |
| Customer deposits **received but never booked** in the legacy ERP | **$784,731** |
| Supplier payments **made but never booked** | $489,859 |
| Outstanding AR (15 invoices, no matching payment) | **≈ $605,000** |

## The reconciliation gap (why $1.08M ≠ $2.17M)

My confirmed $1.08M lands inside Mercury's $2.17M, but ~$1.07M is unaccounted for:

1. **$784,731** — deposits that hit the bank but were never entered in the legacy ERP (Hopi $87K, YellowLite $115K, Diamond Properties $158K, Clean Power Store $39.5K, etc.).
2. **~$59K** — a Stripe payout never reconciled to the bank.
3. **Jan–Jul 2025 window** — pre-Shopify activity that predates the legacy ERP payment records (which start Aug 2025).
4. **Founder/inter-company noise** — William Cassilly $99,950, Michael Cassilly $27,845, internal transfers (1,680 txns).

## Corrected AR position (this is the material error)

The earlier seed said `opening_ar_usd ≈ $0`. That was **wrong**. There are **15 invoices ≈ $605,000** with no matching payment — genuine accounts receivable. These are:
- Distinct from the $328K "customer-credit" (paid-but-unfulfilled) position.
- Currently **unnamed** — the "AR Collection Emails" artifact carries only the 15 amounts, and the collection-statement PDF + the sales/accounting mailboxes did not yield the customer identities in this pass.

**Blockers to naming + extending to Jan 2024:**
1. Mercury API credentials are not in the credential vault (prior agent used access I don't have).
2. Legacy ERP (`OddoERP`) is sealed; the full export in the project has partners/leads but not sale orders or pre-Aug-2025 payments.

## What changing now

- `supplier_ap_seed.csv` — 69 suppliers / $437,331 (legacy ERP-recorded outbound), for the AP side.
- `ar_and_customer_master_seed.csv` — opening customer-credit $328K stays; opening AR is corrected to **≈ $605K** (15 invoices, to be named once Mercury or email access is restored).
- Finance hand-off note updated to reflect the corrected AR.

## To fully close this, I need one of

1. **Mercury API access** → re-pull the Jan-2024 deposit stream + the 15 AR invoices with names.
2. **The prior agent's raw Mercury dump** (if a JSON/CSV of the 5,105 transactions exists, point me at it).
3. **Read access to the 15 collection emails** (correct shared-mailbox path) → recover the 15 AR customer identities.