# Sales Playbook — Customers, Point of Entry, and the Board

Owner: Sales (SDRs, AEs, inbound RFQ). The daily board is the tracker; the system of record is Riven ERP.

## Know your customers (1,401 identities)

Every client now has a **point of entry** and a touchpoint trail. The full index is `client_touchpoint_index.csv`.

Point-of-entry split (verified):

| Channel | Count | Meaning |
|---|---|---|
| Email | 602 | inbound mail first |
| Legacy CRM lead | 419 | logged opportunity |
| Shopify | 217 | self-serve web order |
| Mercury | 93 | wire/ACH first |
| Stripe | 56 | card first |
| Intercom | 13 | chat first |

When working a contact, check the point-of-entry column first — it tells you whether they walked in (Shopify/email) or were prospected (CRM lead), and that changes the right opening move.

## The board's blind spot (fix this)

The team tracker (19 sheets, 1,095 rows) tracks **pre-sale** opportunities, not post-sale fulfillment. Verified consequence:

- **154 of 283 paid clients** are in the tracker; **129 are not**.
- 8 of the top-10 paid customers are missing from the board.
- **Vladimir Tkach ($64,755, 19 lines unfulfilled)** is nowhere in the tracker.

Rule: a *paid* customer is never "Lost." Move paid-but-unfulfilled clients to a recovery row, not the Lost sheet.

## Happy vs not-happy split

Of 283 paid clients: **32 happy** (fully fulfilled), 2 partial, **172 not-happy** (unfulfilled), 77 unknown. Do not solicit reviews from the 172 — fix delivery first. Full split in `review_solicitation_segments.csv`.

## The sales blocker (P0)

Outbound mail is broken in Riven ERP (32 mail-exceptions) — quote send, PO send, and invoice send all fail. Until that's fixed, quotes can't actually leave the system. Flag it; don't promise quote delivery by email until it's live.

## Files

- `client_touchpoint_index.csv` — point of entry + channels per client.
- `review_solicitation_segments.csv` — happy/not-happy split.
- `sales_tracker_crossref.md` — paid clients vs the board.