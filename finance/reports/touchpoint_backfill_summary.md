# Client Point-of-Entry & Conversation Backfill — 2026-09-17

Built a unified index stitching every client's first contact and full touchpoint trail across the live and legacy systems. One row per identity (deduplicated by email), with the earliest event across all sources as the point of entry.

**Provenance note:** the active surface and system of record is **Riven ERP** (rivenai/riven-business + catalog). Historical CRM/partner/order data is read from the **legacy ERP (pre-Riven ERP)** — still queryable, used only as the backfill source for pre-migration history, not as the live system.

## Coverage

**1,401 deduplicated client identities** from:

| Source | Records mined |
|---|---|
| Legacy ERP CRM leads | 605 |
| Legacy ERP partners | 2,000 |
| Shopify paid orders | 237 |
| Stripe charges/customers | 150 charges / 248 customers |
| Mercury transactions | 5,538 |
| M365 email history | 624 contacts |
| Email Control Register | 1,029 |
| Intercom conversations | 322 |
| Sales tracker (call/outreach notes) | 1,095 rows |

## Point-of-entry distribution

| First channel | Clients |
|---|---|
| Email (M365) | 602 |
| CRM lead | 419 |
| Shopify | 217 |
| Mercury (wire/ACH) | 93 |
| Stripe | 56 |
| Intercom | 13 |

## Conversation/outreach coverage added

- **624 clients** with M365 email history (first/last seen, subject lines, source mailbox).
- **333 clients** with sales-tracker call/outreach notes (Casey/Tanya call logs, VM notes, text-outreach entries).
- **Intercom** conversation counts per client.
- Per-client CRM stage (Qualify/Propose/Negotiate/Closed Won/Lost), lead count, and lifetime paid total.

## What this enables

1. **Point-of-entry attribution** — know whether each client walked in via email, an RFQ, Shopify, or a wire.
2. **Full conversation lineage** — first touch → CRM stage → email thread count → call notes → order → payment, in one row.
3. **Gap identification** — 1 client still has no first-touch date; ~333 have tracker call notes but no email record, and vice versa — the join surface for further mining.

## Data notes / caveats

- Mercury has no email on the API, so 93 Mercury-first clients are keyed by counterparty name and will need name→email resolution from legacy partner records (the join is available; those rows carry `NAME:`-style keys resolved to partner names where found).
- 97 CRM leads had no email and no partner_id — keyed by lead name; some are duplicates that will merge once email is recovered.
- Tracker "call notes" are unstructured free text (e.g. "Casey called 6/1 left VM"), so the call count is conservative — it counts rows, not individual calls.

File: `client_touchpoint_index.csv` (1,401 rows).
