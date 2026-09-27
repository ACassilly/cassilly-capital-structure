# Deprecation & Illumination Execution Backlog

Prepared 2026-09-26 · Target: Riven ERP (axis.pesdistribution.com) · Every item observed live this thread, none speculative. Owner column is a placeholder; assign per org.

Priority convention: P0 = blocks money/trust · P1 = blocks measurement · P2 = hygiene/structure · P3 = optional/confirm.

---

## DEPRECATE (P0)

| # | Item | Evidence (live) | Action | Owner | State |
|---|---|---|---|---|---|
| D1 | Legacy Odoo 18 | Still answers at erp.portlandiaelectric.supply; framed legacy | Read-only archive → MX cutover → decommission after backfill lands | Ops | Not started |
| D2 | Outbound mail exceptions | 32 in exception (20 AADSTS50011, 6 SMTPSenderRefused, 2 blocked SMTP, 4 refused) | Repair sending identity + dedicated PES/Riven IPs; replay queue | Infra | Not started |
| D3 | Shopify Payments / AuthNet capture queue | 108 orders / $125,905 uncaptured; only COD live | Capture-or-void decision per order; then retire manual-capture rail | Finance/Ops | Not started |
| D4 | Off-ledger payroll rails (Cash App $152K + Upwork $72K) | $257K flushed off-book over 20 mo | Migrate to hr_payroll / 1099 path; deprecate consumer rails | Finance/HR | Not started |
| D5 | Founder capital mixed into revenue | Mercury "cassilly"/"str capital" inbound $182K | Post to Owner's Equity, not revenue; keep distinct | Finance | Not started |

## DEPRECATE (P1)

| # | Item | Evidence | Action | Owner | State |
|---|---|---|---|---|---|
| D6 | Duplicate AR accounts | 101300 / 110000 / 121000 all carry activity | Reclassify balances → canonical 121000, de-activate dupes | Finance | Not started |
| D7 | Duplicate AP accounts | 200000 / 211000 / 252000 | Reclassify → 200000 | Finance | Not started |
| D8 | Mercury Credit mis-classified as AP | $676K outbound is card settlement | Rebook as credit-card liability, not vendor AP | Finance | Not started |
| D9 | Junk product categories | "Food", "Events", "Goods", "Services" | Rationalize to real taxonomy (modules/inverters/racking/storage/etc.) | Catalog | Not started |
| D10 | Dead Shopify apps | eBay, 17TRACK, Simprosys, Matrixify, Agentic, TikTok, G&Y installed | Uninstall all not feeding Riven storefront headless path | Ops | Not started |
| D11 | Intercom channel | 322 convos → 14 emails | Deprecate or wire to real support lane | Ops | Not started |

## DEPRECATE (confirm only, P3)

| # | Item | State today | Action |
|---|---|---|---|
| D12 | Oxylabs daily monitor | deleted (legacy_48e02dd4) | confirmed dead — do not recreate until funded |
| D13 | Sealed old Azure sub | read-only, ticket 2609060040000541 | leave sealed; no writes |
| D14 | glm-onprem lane | parked/inactive | confirm retired or keep parked |
| D15 | 3CX/PBX lane | parked 0/0 | keep parked; rebuild path retained |

---

## ILLUMINATE (P0)

| # | Item | Evidence (live) | Action | Owner | State |
|---|---|---|---|---|---|
| L1 | Fiscal year + periods | `fiscal.years = 0`, no lock date | Create 2026 FY, monthly periods, lock policy | Finance | Not started |
| L2 | Opening balances | 1 journal entry total | Post bank cash, founder $182,313 equity, AP $285,852, AR $422,126 | Finance | Not started |
| L3 | Outbound mail repair (light the send path) | 32 exceptions block billing | Repair sending identity + IPs; replay 32 | Infra | Not started |
| L4 | Product cost backfill | 116 / 24,584 SKUs carry cost | Backfill standard_price + landed costs before any margin read | Catalog/Finance | Not started |
| L5 | 172 unfulfilled paid clients | open-obligation register | Fulfill or refund in balance-desc order | Ops | Not started |

## ILLUMINATE (P1)

| # | Item | Evidence | Action | Owner | State |
|---|---|---|---|---|---|
| L6 | Payment import (Phase 2) | manifest 198 MATCHED / $1.39M not posted | Post to Bank journal (memo source·date·counterparty), idempotent | Finance | Not started |
| L7 | AR aging + dunning | account_followup installed, never armed (no periods) | Arm after L1; establish aging + dunning cadence | Finance | Not started |
| L8 | Deferred revenue | Open Works $75K draw booked as AR credit | Create deposit liability account; rebook prepayments | Finance | Not started |
| L9 | Native pay-in | Stripe disabled; Mercury absent; COD only | Enable Stripe provider post mail repair | Finance | Not started |
| L10 | Landed costs | freight lines (FRT) never allocate to SKU | Install stock_landed_costs; wire freight landings (LTL/FTL/container) | Catalog | Not started |
| L11 | Budgets | account_budget not installed | Install + per-department caps | Finance | Not started |
| L12 | Sales teams + pipelines | 601 leads, no stage/team ownership | Define teams, assign, per-stage targets | Sales | Not started |
| L13 | GoDaddy/Shopify SaaS spend | $60K + $58K unmapped | Budget line + owner for comms/SaaS | Finance | Not started |
| L14 | Inter-company protocol | $25K "portlandia electric" internal transfers in quarantine | Define I/C AP/AR for PES↔Logistics↔Capital | Finance | Not started |
| L15 | Sales-tax nexus | KY home + 50-state DC, l10n_us only | Define nexus + register before volume | Finance/Legal | Not started |

## ILLUMINATE (P2)

| # | Item | Evidence | Action | Owner | State |
|---|---|---|---|---|---|
| L16 | CFO cockpit | spreadsheet_dashboard installed, 0 dashboards | Build cash runway / AR aging / GM-by-line / bill aging | Finance | Not started |
| L17 | Payroll register | hr_payroll installed, 0 contracts/payslips | Onboard staff, 1099 taxonomy, first payroll | Finance/HR | Not started |
| L18 | Review solicitation engine | Judge.me 0 reviews; flow OFF | Enable reminders (owner), GBP OAuth (owner), scraper funding (owner), then run `solicit_now_schedule.csv` | Marketing | Blocked (human) |
| L19 | Borrowing-base prep | blocked on AR aging + inventory valuation | Unblock via L1/L4/L7 then report | Finance | Not started |
| L20 | Inter-company + cap table | multi-entity diligence flag | Formalize entity structure + I/C | Legal | Not started |

---

## Execution order (dependency-consistent)

1. **L1 + L2 + D6 + D7** (close the ledger base) — same sprint, read-before-write.
2. **L3** (mail) — parallel, unblocks billing → AR.
3. **L4 + L10 + D9** (cost + landed + taxonomy) — makes margin real.
4. **L6 + L7 + L8 + D5 + D8** (post history, arm aging, fix classification).
5. **L5** (fulfill the 172) — runs concurrent, longest tail.
6. **L9 + L11 + L13 + L14 + L15** (bring money online, budget, SaaS, I/C, nexus).
7. **L12 + L16 + L17 + L20** (people, dashboards, structure).
8. **L18 + L19 + L20** (reviews + borrow base) — gated on humans + prior steps.

## Blocked-by-human (owner-only)

- Judge.me "Send automatic reminders" toggle (cross-origin iframe; agent cannot toggle).
- Judge.me → Google Business Profile OAuth (listing owner's Google account).
- Oxylabs Web Scraper API funding (free trial).
- Any definitive decision to retire Shopify Payments / capture or void the $125K queue.

## Non-negotiables

- Riven ERP is the live book; legacy is read-only history.
- Real transacting customers only for reviews — no fabrication, no spoofing (FTC + platform terms), regardless of enforcement posture.
- Read-before-write on every ERP mutation; idempotent re-runs only; never delete — quarantine.