# Ledger Base Execution Log — 2026-09-26

Live mutations against Riven ERP (`riven_erp_pes`, axis.pesdistribution.com). Read-before-write on every op; idempotent; nothing destructive.

## Completed (verified live)

| ID | Backlog item | Action | Verification |
|---|---|---|---|
| L1 | Fiscal year + periods | FY2026 confirmed exists (`account.fiscal.year` id 1, 2026-01-01 → 2026-12-31) | `fiscal.year` count = 1 |
| D6 | Duplicate AR accounts | Deactivated empty `101300` (id 209) — was 0 lines | `active=False` |
| D7 | Duplicate AP accounts | Deactivated empty `200000` (id 2) — was 0 lines | `active=False` |
| L2 | Opening balances (equity) | Posted `OPENING-EQUITY` entry: DR Bank $182,313.03 / CR Capital $182,313.03, dated 2026-01-01 | entry id 48, `state=posted`, amount $182,313.03 |
| D6/D7 | Partner defaults | Repointed 29 partners off legacy AR `110000` → canonical `121000`; 19 partners off legacy AP `200000` → canonical `211000` | legacy-AR remaining = 0, legacy-AP remaining = 0, canonical-AR = 3,852, canonical-AP = 3,852 |

## Bank balance after this pass

`101401 Bank` net = **$257,313.03** = $75,000 (Open Works receipt) + $182,313.03 (founder capital).

## Decisions documented (so the next agent doesn't relitigate)

1. **Canonical accounts:** AR = `121000` (id 213), AP = `211000` (id 233). The other AR/AP accounts (`101300`, `110000`, `200000`, `252000`) are legacy; `101300`/`200000` are now inactive. `110000` still carries 2 posted lines, which are **hash-protected** — do NOT force-edit; they self-resolve once the draft invoices on that account are cleaned up or reposted on 121000.

2. **No period sub-objects** — this engine has no `account.period`; the fiscal year is the boundary. Lock-date policy must be set at the company level (not yet configured).

3. **Opening equity already booked** — do NOT re-post founder capital. Idempotency key: `ref=OPENING-EQUITY`.

4. **AP opening is already real** — the 5 posted bills ($285,852.40) touch `211000`; no synthetic AP entry needed.

## Remaining P0 (not yet executed)

| ID | Item | Why still open |
|---|---|---|
| L3 | Outbound mail repair (32 exceptions) | Needs Azure/infra work + dedicated PES/Riven IPs |
| L4 | Product cost backfill (116/24,584) | Needs catalog source, pairs with landed costs |
| L5 | Fulfill 172 unfulfilled clients | Ops long-tail |
| L6 | Payment import Phase 2 (198 rows / $1.39M) | Queue safely behind the above |

## Evidence file

`finance/reports/ledger_base_verification.json` — machine-readable snapshot of every verification above.