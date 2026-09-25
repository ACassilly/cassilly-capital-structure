# Mercury Bank Verification — verified against live API, 2026-09-16

Pulled the full Mercury history directly (15 accounts, live API). This **replaces** the prior agent's Aug 8 estimates, which over-counted by including internal transfers.

## Verified numbers

| Metric | Verified value |
|---|---|
| Transactions | 5,538 (deduped) |
| **Date floor** | **2025-01-24 → 2026-09-16** (accounts opened ~late Jan 2025) |
| External inbound (deposits, excl. internal) | **485 txns / $1,870,853** |
| External outbound (withdrawals, excl. internal) | 2,192 txns / $1,776,688 |

Corrections to the prior record:
- The Aug 8 report's "$2,165,341 deposits since Jan 2024" was **wrong two ways**: the floor is Jan 2025 (accounts didn't exist in 2024), and the total double-counted internal transfers. True external inbound is **$1.87M**.

## Composition of inbound ($1.87M)

| Channel | Amount | Note |
|---|---|---|
| Stripe payouts (2 names) | $378,588 | Shopify customers settling via Stripe |
| Shopify payouts | $74,316 | Shopify Payments (legacy) |
| Founder capital (William Cassilly, STR Capital) | $154,468 | not customer revenue |
| **Direct customer wires/ACH** | **~$1.26M** | the real customer deposits |

## New customers this surface (not in the 283-client dossier)

| Customer | Inbound |
|---|---|
| SOLUX LLC | $81,657 |
| OPEN WORKS, INC. | $75,000 |
| 21C LLC | $25,612 |
| SOLAR ENERGY OPE | $25,235 |
| NEW JERSEY SOLAR | $18,408 |
| SYNC RENEWABLES | $18,030 |
| METCO ENGINEERING | $11,250 |
| GRAY DUCK SOLAR | $10,610 |
| COOL EARTH SOLAR | $9,725 |
| SMUCKERS ENERGY / California Solar / THOMAS W HAUGEN / E2SOL / RETI SOLAR | ~$21,000 combined |

≈ **$250,000 of additional customer revenue** and ~15 named customers absent from the dossier.

## AR cross-check — Dennis Willett is a real discrepancy

`INV/2026/00172` (S01211, **$42,647.12**) — The legacy ERP records it as "paid" but **no matching Mercury deposit exists**. Same pattern on a handful of other legacy ERP payments: the legacy ERP "paid" ledger marks some invoices collected that never actually settled at the bank. These are the genuine outstanding-receivable candidates, and they line up with the prior agent's "15 collection emails ≈ $605K".

## Net position (corrected, for the finance lane)

- Lifetime collected: **$1,083,826 (dossier) + ~$250K newly-found = ~$1.33M**, still under the $1.87M external inbound because a slice is founder capital + not-yet-reconciled.
- Outstanding AR: **≈ $605K** flagged (15 invoices), with Dennis Willett $42,647 now **confirmed unpaid-discrepancy** rather than "paid and fulfilled".

Supporting file: `mercury_deposit_ledger.csv` (485 deposits, counterparty + date + amount).