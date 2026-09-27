# Review Request Email Copy — Post-Fulfillment

Two channels: Judge.me auto-request (fires 1 day after fulfillment, needs "Send automatic reminders" ON), and a Klaviyo follow-up (you hold the Klaviyo key).

## Judge.me in-email form (default, 2-click)

Subject: How's your order from Portlandia Electric Supply?

Body (Judge.me's built-in copy is fine; if you customize, use this):
> Thanks for your order! We hope everything landed exactly as expected. It'd mean a lot if you took 30 seconds to let us know how it went — it helps other installers and crews buy with confidence.

## Klaviyo follow-up (send ~4 days after first request, only to non-responders)

Subject: One quick question about your order

Body:
> Hi {{ first_name }},
>
> A quick note from Portlandia Electric Supply — we saw your recent order shipped and wanted to make sure it arrived exactly as ordered.
>
> If it did, a fast review helps the next installer find the right gear:
> [Leave a review →]
>
> If anything fell short — wrong item, late arrival, a blemish — reply here and I'll get it fixed directly. Your word matters to us more than a rating.
>
> — The PES team

## Rules

- "Leave a review" links to the Judge.me review form, NOT a Google review link (owned surface, richer compliance).
- Only send the follow-up to orders marked fulfilled. Never to the 172 unfulfilled.
- No incentive, discount, or gating for a review (FTC + platform terms).
- 5★-intent reviewers go to Judge.me; sub-5★ are routed to "make it right" (reply), never suppressed.

## Send cadence

- Initial: Judge.me auto, day 1 post-fulfillment.
- Reminder: Judge.me auto-reminder, day 7 (needs toggle ON).
- Klaviyo: day ~4, non-responders only.