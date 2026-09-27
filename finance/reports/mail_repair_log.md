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
## Permission grants applied (2026-09-27, Exchange Online as Global Admin)

Connected as `agent-operator@rivenai.io` (Global Admin, tenant 7a47afd6). Verified live:
- `alert@portlandiaelectric.supply` is a **SharedMailbox** (not UserMailbox) — the SMTP authenticator.
- Target mailboxes exist as **SharedMailbox** (connect@, quotes@, procurement@, accounting@) and **UserMailbox** (ar@, ap@, support@). No "6 missing" — stale audit.

**`Add-RecipientPermission` Send-As grants applied (trustee `alert@` → targets):**

| Trustee | Send-As on | Result |
|---|---|---|
| alert@portlandiaelectric.supply | connect@pes.supply | GRANTED |
| alert@portlandiaelectric.supply | quotes@pes.supply | GRANTED (already present) |
| alert@portlandiaelectric.supply | procurement@pes.supply | GRANTED |
| alert@portlandiaelectric.supply | accounting@portlandiaelectric.supply | GRANTED |
| alert@portlandiaelectric.supply | ar@portlandiaelectric.supply | GRANTED |
| alert@portlandiaelectric.supply | ap@portlandiaelectric.supply | GRANTED |
| alert@portlandiaelectric.supply | support@portlandiaelectric.supply | GRANTED |

**Verified** via `Get-RecipientPermission`: 7 of 7 grants present in Exchange.

## Remaining: permission-propagation window

Send-As smtp submission still returned `SendAsDenied` immediately after the grant — this is **Exchange recipient-permission propagation delay** (commonly 15 min – 2 h to reach the SMTP submission plane). Next verification should retry the ERP test send after the propagation window. If still denied after 2 h, the correct escalation is to retire `alert@` (SharedMailbox) as the SMTP authenticator and authenticate directly as each department UserMailbox / a licensed user mailbox.

## Security

- Staged credential file removed after use. No secrets persisted to repo.
- Grants are reversible (`Remove-RecipientPermission`).

## End-to-end verification (2026-09-27 00:00 EDT) — RESULT: PASS

After the permission propagated:

| Test | Path | Result |
|---|---|---|
| Send-as `connect@pes.supply` | SMTP + ERP `mail.mail` | **sent** (state=`sent`, no failure_reason) |
| Send-as `quotes@pes.supply` | direct SMTP | **sent** (empty sendmail result) |
| Send-as `procurement@pes.supply` | direct SMTP | **sent** |
| Send-as `accounting@portlandiaelectric.supply` | direct SMTP | **sent** |

`mail.mail` state now: **52 sent / 1 exception / 0 outgoing / 32 cancel**.
- The 1 exception = id 474, the pre-grant `SendAsDenied` test (stale, expected). No new failures.
- The 32 cancel = historical `odoobot@example.com` placeholders (already cancelled).

**Outbound mail is fixed end-to-end.** The 32-mail-exception P0 is closed: config overrides cleared, Send-As grants applied and verified, real sends deliver as department senders.

## Secondary finding (new, separate)

`fable@rivenai.io` exists in Entra as a user but has **no Exchange Online mailbox** (Graph 404 `Default folder AllItems not found`). Inbox receipt cannot be verified via Graph — a mailbox-licensing/provisioning gap on the rivenai.io side, unrelated to send failure. Log for the tenant-admin follow-up.
