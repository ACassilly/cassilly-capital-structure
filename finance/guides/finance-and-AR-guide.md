# Finance Playbook — AR, Payments, and the Money Migration

Owner: Finance / Accounting / Collections. Source of truth: Riven ERP. Historical money lives in Mercury + Stripe (not yet in the ERP).

## The money picture (verified 2026-09-25)

- Mercury inbound: **485 deposits / $1,870,853** (Jan 24 2025 → Sep 16 2026).
- Mercury outbound: **2,192 withdrawals / $1,776,688**.
- Stripe succeeded: **103 charges / $319,260** across 86 customers.
- Real collectable AR: **$422,126 across 14 invoices**.
- VOID (do not collect): **$182,952 — Aaron T.** (order #111481 was cancelled; invoice orphaned).

## Working the AR queue

1. Open `ar_register_named.csv` — the 14 collectable invoices, named and verified against both Mercury and Stripe.
2. Collection order = balance descending. Skiop nothing below $1k without a call.
3. **Never** chase Aaron T. ($182,952) — the order is `cancel` in the system; the invoice posted without voiding. If a collection letter went out, retract it.
4. When a payment arrives, match it to the posted invoice before marking anything paid. Prefer the Bank journal + Manual Payment method in Riven ERP.

## Wire Mercury + Stripe history into the ERP

Follow `legacy_finance_migration_plan.md`. The safe order:

1. Read the manifest (`payment_import_manifest.csv`) — every row already tagged MATCHED / NEW_PARTNER / FOUNDER / INTERNAL / QUARANTINE.
2. **Exclude** FOUNDER ($182K), INTERNAL ($25K), QUARANTINE ($22K) — not customer revenue.
3. Post one inbound `account.payment` per MATCHED/NEW_PARTNER row against the Bank journal, manual method, memo = `{source} {date} {name}`.
4. Skip any (partner, date, amount) you've already posted — rerun-safe.
5. After posting, reconcile against the open invoice (Phase 3 posts the 14 AR invoices to the LINV journal first).

## The cardinal rules

- Riven ERP has **zero payments recorded** — the book opens fresh. Don't assume anything is in it.
- Open Works is **already correct** (see below) — don't double-post it.
- Stripe is **disabled in the ERP**; only COD is enabled. Import Stripe as historical manual payments, not a live provider.

## Open Works — the worked example

- Mercury wires: $70,000 (2026-08-13) + $5,000 (2026-08-18) = **$75,000**, note SO1329.
- ERP already holds payment `INV1016212` ($75,000) applied to `INV/2026/00002` ($371,189.34).
- Invoice residual = **$296,189.34**, which matches Mercury to the penny.
- **Reconciled already.** The remaining $296k is genuinely unpaid — collect it, but don't touch the $75k.

## Files

- `ar_register_named.csv` — the collectable queue.
- `payment_import_manifest.csv` — money migration row-level map.
- `legacy_finance_migration_plan.md` — the phased plan.
- `PES_BodyOfWork_Master_Export.xlsx` — everything in one workbook.