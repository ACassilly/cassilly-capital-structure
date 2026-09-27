# PES Review Backfill Program — 12-Week Plan

System of record: Riven ERP · Storefront: Shopify (Judge.me embedded) · Review platforms: Judge.me → Google Shopping/Meta/rich snippets, plus Google Business Profile.

## Ground truth (verified live this thread)

- Published reviews today: **0** on Judge.me (widget loads `average-rating=0.00`, hides itself).
- Google Business Profile: **~9 reviews / 2.8★** (stale, unconfirmed without scraper).
- Happy & fulfilled customers (solicit-now): **32**.
- Not-happy / unfulfilled (cannot solicit): **172**.
- Realistic B2B electrical response: 10–15% → the 32 yield ~3–5 reviews, not 30.

So the backfill is not a replay — it is the FIRST play, and its real gate is how fast Ops clears the 172 unfulfilled.

## Phase 1 — Scraper pull (day 1, once Oxylabs funded)

One-time extraction of every existing public review across 6 targets: Google Business Profile, Trustpilot, Yelp, BBB, Judge.me, TrustShop. Confirms the true external baseline and imports GBP's 9 into the storefront via the Judge.me GBP integration.

## Phase 2 — Owned-surface solicitation (Judge.me first, weeks 1–2)

- 32 happy customers, 3/day, jittered (see `solicit_now_schedule.csv`).
- Judge.me's 2-click in-email form = highest response, and each review syndicates to Google Shopping + Meta + rich snippets automatically.
- Enable "Send automatic reminders" + a 7-day reminder (the single largest response multiplier).

## Phase 3 — Fulfillment-clearance engine (weeks 2–8)

Clear the 172 unfulfilled in priority order (open-obligation register, balance desc: Vladimir T. $64,755 → Leon R. $17,674 → …). Each client becomes solicitable ~3 days after delivery confirmation.

## Phase 4 — Sustained drip + GBP climb (weeks 8–12)

- Newly-fulfilled wave lands on Judge.me and refreshes the Google Shopping stars.
- Separate, slower Google Business Profile climb (velocity-safe) from the same genuinely-fulfilled set.

## Hard rules

- Real transacting customers only. No fabricated reviews, no IP/account spoofing (FTC-illegal; violates Judge.me/Google terms), regardless of enforcement posture.
- Solicit only after fulfillment. The 172 are off-limits until shipped.
- Velocity: a few invites/day; a rating spike reads as fraud and gets flagged.

## Files

- `solicit_now_schedule.csv` — 32 names, dated, jittered, with review links.
- `review_solicitation_segments.csv` — happy/partial/not-happy split.
- `open_obligation_register.csv` — the fulfillment queue that feeds Phase 3.