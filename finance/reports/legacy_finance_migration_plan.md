# Legacy Finance Migration Plan — Mercury + Stripe → Riven ERP

**Prepared:** 2026-09-25 · **Target:** Riven ERP (`riven_erp_pes`, live at axis.pesdistribution.com)
**Source rails:** Mercury (bank) + Stripe (card) + legacy ERP (pre-Riven, historical ledger).

## Objective

Move the whole historical money record into Riven ERP so the ERP becomes a complete
book — payments, AR, and counterparties — rather than a fresh pipeline with a $0 ledger.

## Verified current-state (2026-09-25, live ERP)

| Thing | Live value |
|---|---|
| sale.orders | 68 (11 sale / 38 sent / 19 draft) — $2,241,915 pipeline |
| invoices | 12 — zero paid |
| account.payment | 1 (Open Works $75,000) |
| bank statements | 0 |
| journals | 11 (incl. Bank BNK1, Cash CSH, **Legacy Customer Invoices LINV**) |
| payment.provider | 25 records |
| partners | 2,999 |

**Key constraint:** the finance lane is structurally present (Bank/Cash journals, AR
account 121000, manual-payment method, a dedicated `LINV` legacy invoice journal) but
carries no history. The migration loads history into that lane.

## Manifest (final, 289 rows)

| Status | Count | Amount |
|---|---|---|
| MATCHED (partner exists) | 198 | $1,391,160.65 |
| ALREADY_APPLIED (Open Works) | 2 | $75,000.00 |
| NEW_PARTNER (partner created this session) | 10 | $33,493.83 |
| FOUNDER (not customer revenue) | 5 | $182,313.03 |
| INTERNAL (inter-company) | 7 | $25,000.14 |
| QUARANTINE (eBay/Upwork/misc) | 67 | $22,357.28 |

`payment_import_manifest.csv` carries the full row-level status + partner id for every row.

## Open Works — reconciliation result

Already correct in live ERP, no write needed:

- Mercury: **$70,000 (2026-08-13) + $5,000 (2026-08-18)** = **$75,000** wires, note SO1329.
- Riven ERP: payment `INV1016212` $75,000 (Bank/Manual, partner Open Works) already posted,
  applied against `INV/2026/00002` ($371,189.34).
- Invoice residual = **$296,189.34** — matches Mercury to the penny.
- Verdict: **reconciled.** Remaining $296,189.34 is genuinely unpaid (not a data gap).

## Phased plan

### Phase 1 — Done this session
- Built row-level manifest (Mercury 180 direct deposits + Stripe 103 charges).
- Created 46 missing customer partners (Solux, Trinity, Tenco, NJ Solar, Sync Renewables, etc.)
  with `is_company=True, customer_rank=1`.
- Verified Open Works already reconciled.

### Phase 2 — Post payments (next approved write)
For each `MATCHED` + `NEW_PARTNER` manifest row, create one inbound `account.payment`
against the Bank journal (or Cash journal for cash), `payment_method_line_id` = Manual Payment (Bank),
memo = `{source} {date} {counterparty}`. Then register the payment against AR so it
lands as customer credit, reconciling to the matching posted invoice when one exists.

- Idempotency: skip any row whose (partner, date, amount) already has a payment —
  this is how reruns stay safe.
- Amount guard: never post a payment without first reading the partner id back.

### Phase 3 — Legacy invoice journal (LINV)
Post the 14 collectable AR invoices into `Legacy Customer Invoices` (LINV) so the
$422,126 real AR becomes visible in the ERP as open items, each linked to its partner
(from `ar_register_named.csv`). This gives Finance actual open-invoice objects to collect,
rather than a CSV outside the system.

### Phase 4 — Stripe pass
Import the 86 Stripe-resolution rows (`stripe_charge_resolution.csv`) as card-payment
history against the same partners, memo `stripe <charge date>`. Stripe is disabled in ERP,
so these are historical card receipts imported as manual-payment records — not live provider.

### Phase 5 — Reconciliation + close
- Reconcile every imported payment against its invoice or leave as AR credit.
- Produce a variance report: ERP posted vs Mercury/Stripe source totals must match to the cent.
- Mark the migration complete in a dated ledger entry.

## Hard rules

1. Read-before-write on every row; log every create with source + source id.
2. Never touch the sealed legacy Odoo store — this plan reads its *export* only, and
   the target is Riven ERP (axis.pesdistribution.com), not erp.portlandiaelectric.supply.
3. FOUNDER / INTERNAL / QUARANTINE rows are excluded from payment posting — they are not customer revenue.
4. Payments post to Bank journal with the manual method; no live Stripe/Mercury provider is being enabled.
5. Idempotent re-runs only; all creates are additive, nothing destructive.

## Deliverables

- `payment_import_manifest.csv` — row-level source → partner → status.
- `ar_register_named.csv` — 14 collectable AR invoices for Phase 3.
- This plan.
