# Operations Playbook — Fulfillment, Mail, and Stock Truth

Owner: Warehouse / Logistics / Procurement. Read before assuming anything is "live."

## The single highest-leverage repair

**Outbound mail is broken** — 32 messages in `exception` state. Failure modes:

- 20 × AADSTS50011 — OAuth redirect URI mismatch.
- 6 × 554 SMTPSenderRefused — staff send-as (`sushil@`, `byzid@`, `alex@`, `tanya@`, `connect@`) via an SMTP account that doesn't own those addresses.
- 2 × 535 — the SMTP account itself blocked.
- 4 × connection refused (past outage).

This blocks RFQ, PO, vendor-reminder, quote, and invoice sends — the whole order flow. Fix the sending identity first (one licensed sender with send-on-behalf, or per-user OAuth), then replay the 32 queued.

## Stock truth (do not trust the catalog)

- **24,583 products** in the catalog.
- **0 on-hand stock** (`stock.quant = 0`). No valuation layers, no COGS.
- The catalog is live-sellable; **inventory operations are not configured**.

So "product published" ≠ "in stock." Never promise delivery lead time from the catalog alone until reorder rules (`orderpoints`) exist — there are 0.

## Fulfillment reality check

7 pickings exist but there are no stock quants to pick. The 172 unfulfilled paid clients in the Sales playbook are stranded here — not a sales problem, an operations gap. Open orders with a vendor first, then move the picking.

## EPA 608 gate (compliance)

The refrigerant lane (`pes-refrigerant-resale`) requires an EPA 608 cert-gate on the storefront. Verified 2026-09-16: the gate exists on the live theme (product template `refrigerant`, form POST to `/cart/add`). Do not remove or bypass it; hazmat items must stay ground-only.

## Files

- The mail-transport diagnosis lives in `SYNTHESIS_pes_requirements_map.md` (fleet lane).
- `manual_capture_triage.csv` — the un-captured order queue (108 orders / $125,905) that Ops needs to confirm before capture.