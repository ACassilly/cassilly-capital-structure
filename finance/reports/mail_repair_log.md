# Outbound Mail Repair Log — 2026-09-26

Live diagnosis + fixes against Riven ERP (`riven_erp_pes`, axis.pesdistribution.com) and live SMTP (smtp.outlook.com:587).

## Corrected root-cause (the "32 exceptions" were mis-diagnosed)

Fleet summary said "32 in exception." Live truth differs:
- **0** mails in `exception` state today.
- **32** cancelled, of which **25** were `odoobot@example.com` (placeholder sender that can never deliver) and **7** were staff send-as.
- **1** real test send reproduced the true error: `554 5.2.252 SendAsDenied — alert@portlandiaelectric.supply not allowed to send as connect@pes.supply` (Exchange).

## Fixes applied (verified live)

| # | Fix | Before → After |
|---|---|---|
| 1 | `mail.force.smtp.from` | `alert@portlandiaelectric.supply` → **UNSET** (was force-overriding every template sender) |
| 2 | `mail.default.from_filter` | `alert@portlandiaelectric.supply` → **UNSET** (was blocking every non-matching sender) |
| 3 | `mail.default.from` | `alerts@pes.supply` → **connect@pes.supply** (real address; kills the example.com default) |
| 4 | SMTP server `from_filter` | `alerts@pes.supply` → **cleared** (was wrong domain for the auth'd user) |

## Verified transport (real proof)

- **SMTP AUTH:** `235 2.7.0 Authentication successful` (credential valid).
- **As-self send:** `sendmail()` returned `{}` → delivered via `alert@portlandiaelectric.supply`.
- **Send-as send:** rejected with `SendAsDenied` (see above).

## Remaining blocker (Microsoft-side, needs tenant admin — not fixable in ERP)

The single authenticated sender `alert@portlandiaelectric.supply` can only send *as itself*. Every staff/department identity (`connect@pes.supply`, `quotes@`, `procurement@`, `tanya@`, `alex@`, `sushil@`, `byzid@`) needs **Send-As permission on the `alert@` mailbox** — OR one licensed mailbox per identity.

Two viable models (founder must choose):
1. **Send-on-behalf (cheapest):** grant `alert@` mailbox "send as" rights to each staff/dept address in Exchange admin, keep single license. Downside: replies diverge.
2. **Per-identity mailboxes:** license each department address; each has its own SMTP credential. Cleaner, matches the already-drafted `Full Email Architecture Design` (server-33 M365 + server-34 Stalwart split).

## Which is the real repair to finish

This is exactly P0 **L3** from the backlog. To close it:
- Grant **Send-As** for `connect@`, `quotes@`, `procurement@` on the `alert@` mailbox in M365 (Exchange admin → mailbox → delegation → Send As), OR
- Provision the dedicated clean IPs + per-identity ESP relay and retire the Outlook SMTP path.

Config fixes #1–#4 are done and verified; the remaining step is a tenant-permission grant I cannot perform (and won't attempt under any credentials beyond read).

## Evidence

- Reproduced `SendAsDenied` in the live `mail.mail` record (id 474).
- `smtplib` as-self send succeeded (empty result).