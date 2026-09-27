# Handoff — State of PES Body of Work (2026-09-26)

For the next agent (Kimi) to take over with zero re-discovery. Everything below is verified live as of the date above.

## System of record (do not get this wrong)

- **Active surface:** Riven ERP at `axis.pesdistribution.com`, DB `riven_erp_pes`.
- **Legacy:** old Odoo 18 (`erp.portlandiaelectric.supply`) — still queryable, frame as "legacy ERP (pre-Riven ERP)". NOT the live book.
- Money history lives in **Mercury** (bank) + **Stripe** (card); Riven ERP holds ~0 payment history.

## Credentials & access

- Riven ERP: XML-RPC `https://axis.pesdistribution.com`, db `riven_erp_pes`, user `admin`. Admin password lives in project file `CREDENTIALS-PLAIN-2026-09-11.txt` (label "RIVEN ERP ADMIN PASSWORD"). Never print it.
- Mercury: custom-cred handle `custom-cred:227ffbeb-f08f-4f8c-aeaa-970100f69415@api.mercury.com`.
- Stripe: `custom-cred:f2995df7-ea19-4281-8696-f2ef425f3b79@api.stripe.com`.
- Shopify Admin API: `custom-cred:portlandiaelectricsupply.myshopify.com` (still valid for API).
- Microsoft Graph: `riven-m365-graph` skill (app-only, tenant 7a47afd6) + `/home/user/workspace/riven_access/.secrets/graph_env`.
- Oxylabs: account registered, but **Web Scraper API not funded** (free-trial pending); no API credential in vault.

## What's DONE (do not redo)

1. **Finance reconciliation** — full Mercury (5,538 txns) + Stripe (150 charges) + Shopify history cross-referenced. Master export: `reports/PES_BodyOfWork_Master_Export.xlsx` (27 sheets).
2. **AR clarified** — 14 real collectable invoices ($422,126); Aaron T. $182,952 is VOID (cancelled order).
3. **Payment import manifest** — `reports/payment_import_manifest.csv` (289 rows, tagged MATCHED/NEW_PARTNER/FOUNDER/INTERNAL/QUARANTINE).
4. **46 customer partners created** in Riven ERP (additive, id 3271+).
5. **Guides** — `guides/` (Finance, Sales, Ops, Marketing playbooks).
6. **Review program** — `reports/solicit_now_schedule.csv`, `review_backfill_program.md`, `review_request_email_copy.md`.

## What's BLOCKED (needs a human)

1. Riven ERP fiscal year + opening balances (I scoped it; not yet executed).
2. Outbound mail repair (32 exceptions) — dedicated clean IPs for PES + Riven staff.
3. **Judge.me "Send automatic reminders"** toggle — cross-origin iframe I couldn't drive; owner must click it.
4. **Google Business Profile OAuth** in Judge.me (owner Google account consent).
5. **Oxylabs Web Scraper API funding** (free trial).

## What's NEXT (pick up here)

### Finance lane (Riven ERP, XML-RPC)
- Consolidate AR → 121000, AP → 200000 (move balances, don't delete).
- Create fiscal year + periods, load opening balances (cash, founder capital $182,313, AP $285,852, AR $422,126).
- Then run `payment_import_manifest.csv` Phase 2 (post payments to Bank journal, memo `source·date·counterparty`, idempotent on partner+date+amount).
- Install `stock_landed_costs` + `account_budget`.

### Review lane (once humans unblock #3–#5)
- `review-ops/review_backfill.py --dry-run` (sandbox), then full pull.
- `review-ops/daily_monitor.py` for the daily rating/count snapshot.
- Verify storefront Judge.me widget leaves 0 reviews after GBP sync.

### Compliance/tying threads
- ~$257K payroll/contractors on Cash App + Upwork → 1099/W-2 cleanup.
- Sales-tax nexus, inter-company rules, deferred-revenue account.

## Repo layout

- `finance/reports/` — all CSVs + master export + narratives.
- `finance/guides/` — department playbooks + review runbook/schema.
- `finance/scripts/` — review backfill + daily monitor.
- `finance/review-ops/` — full review-ops scaffold (targets.json needs real listing URLs).

## Non-negotiables

- Real transacting customers only for reviews. No fabricated reviews, no IP/account spoofing (FTC + platform terms) — regardless of enforcement posture.
- Riven ERP is the live book; legacy is read-only history.
- Read-before-write on every ERP mutation; idempotent re-runs only.
## Deprecation & Illumination Backlog

The full kill-list + light-up register (35 items, prioritized, with live evidence and owners) is in `finance/DEPRECATION-ILLUMINATION-BACKLOG.md`. Start there for the complete execution surface beyond the finance lane.
