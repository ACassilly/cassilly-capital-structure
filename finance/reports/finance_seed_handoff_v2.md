# Finance Lane Hand-off v2 — verified vs Mercury + Stripe (2026-09-16)

Three workstreams closed this pass. All figures backed by the live bank (Mercury) and card (Stripe), not estimates.

## 1. Accounts Payable (withdrawals) — mined

- **2,192 external outbound transactions / $1,776,688** since 2025-01-24.
- Top suppliers paid: Starworld Electronics $112,605, Fortune Energy $66,476, Pearce Worldwide Logistics $58,135, 1Solar Direct $52,375, Forklift Parts Unlimited $51,838, Solwel $50,263, SOLU Solar $44,712, Krannich Solar East $41,463, Hahn and Associates $32,671, Instant Trading $20,792, Hightec Solar $20,125, BayWa r.e. $16,800, plus ~345 more.
- Non-supplier outbound (reclassified): Mercury Credit $379,596 (card), Cash App $121,214 (600 txns), Portlandia Electric Supply $130,572 (inter-company), Wise $17,885, Upwork $13,811, STR Capital $47,746 (inter-company).
- File: `mercury_ap_register.csv` (358 counterparties).

## 2. Inbound deposits — fully attributed

- **485 external deposits / $1,870,853**, 100 counterparties.
- Attributed: $357K named customers + $455K Stripe/Shopify payouts (individuals resolved via Shopify) + $182K founder capital.
- **~$850K recovered as new/uncategorized customer deposits** across ~40 names — the big ones: YellowLite $114,846, Diamond Properties $137,170, SOLUX $81,657, Open Works $75,000, Schiavoni $80,192, 21C $25,612, New Jersey Solar $18,408, Sync Renewables $18,030, Metco $11,250.
- Reclassified as non-client: inter-company $25K, supplier refunds $9K, cashback $7K, eBay settlements $20K.
- File: `mercury_deposit_ledger.csv` (485 deposits).

## 3. Accounts Receivable — recovered and verified

**15 invoices / $605,078 — all verified UNPAID against both Mercury and Stripe.**

| Invoice | Customer | Amount |
|---|---|---|
| INV/2025/00045 | Aaron T. | $182,952.00 |
| INV/2026/00204 | AECOM USA INC | $78,645.00 |
| INV/2026/00152 | Pomptonian Food Service | $42,650.00 |
| INV/2026/00010 | Blue Angel | $41,261.05 |
| INV/2026/00084 | Kelley K. | $38,801.35 |
| INV/2026/00272 | CapitalPWL | $38,295.02 |
| INV/2026/00224 | Anup M. | $32,210.97 |
| INV/2025/00081 | K2 Space | $29,386.10 |
| INV/2026/00078 | Poipu Beach Athletic Club | $23,842.48 |
| INV/2026/00072 | Axiom360 | $23,409.96 |
| INV/2026/00263 | Evan S. | $22,976.36 |
| INV/2026/00094 | Energetic Solutions | $17,096.85 |
| INV/2026/00012 | Jorge A. | $17,057.46 |
| INV/2025/00170 | Loomis Design Services | $8,582.80 |
| INV/2025/00096 | CalSolar Inc., Bryce Berggre | $7,910.83 |

### Stripe resolution (major correction)

The prior "AR" was inflated by invoices thought unpaid but actually settled via card. **Stripe holds 103 succeeded charges / $319,260 across 86 customers** — including Dennis Willett $42,647, Rhew Contracting $21,636, Pawan Kumar $33,403, Tenco Solar $15,878, Ian Clark $11,538. These are **PAID**, not AR. The 15 above are the true outstanding balance.

## Net position (corrected)

- Lifetime collected: **~$1.33M** (283 dossier + new-found), against $1.87M external inbound (remainder = founder capital + unreconciled).
- Outstanding AR: **$605,078 (15 named invoices)**, led by Aaron T. $182,952.
- AP outbound: **$1.78M** since Jan 2025.

Files: `ar_register_named.csv`, `mercury_ap_register.csv`, `mercury_deposit_ledger.csv`, `stripe_charge_resolution.csv`.

---

## Appendum — Aaron T. payment-history verification (2026-09-16 21:00)

**Verdict: the $182,952 "AR" is VOID. It is a cancelled order, not an unpaid receivable.**

Investigated every available payment record for Aaron Twombly (atwombly@gmail.com / INV/2025/00045, order #111481):

| Source | Result |
|---|---|
| Mercury (5,538 txns, all 15 accounts) | **Zero** transactions referencing Twombly/atwombly/182952; no deposit within $600 of $182,952 in 2025 |
| Stripe (charges + customers) | **Zero** charges or customers for atwombly/Twombly |
| Shopify (paid orders + customers) | **Zero** orders or customers for atwombly/Twombly |
| Legacy ERP export (partner 6001) | Partner exists; **order #111481 state = `cancel`**; invoice INV/2025/00045 `state=posted`, `amount_residual=182,952`, `payment_state=in_payment` — invoice was never reconciled to the cancelled order |

**Root cause:** the sales order #111481 was cancelled in the legacy ERP, but its invoice was already `posted` and never voided, leaving a $182,952 residual balance ghosting as "in_payment." The AR-collection email was generated off this stale residual. There is no customer obligation — the deal never went through.

**Do NOT send a collection email to Aaron Twombly.** If already sent, issue a correction.

## Corrected AR position

- **Genuine collectable AR: $422,126 across 14 invoices.** (Led by AECOM USA $78,645, Pomptonian $42,650, Blue Angel $41,261, Kelley K. $38,801, CapitalPWL $38,295.)
- **VOID: $182,952 (Aaron T.)** — cancelled order, remove from AR.
- Total corrected from $605,078 → **$422,126** collectable.

Related: CalSolar Inc. also shows one cancelled order (S00850) in its history, but its billed invoice INV/2025/00096 ($7,910.83) is separate and remains open.
