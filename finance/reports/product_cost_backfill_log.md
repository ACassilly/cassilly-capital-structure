# Product Cost Backfill — Completion Log (2026-09-27)

## Result
- Variants with cost (`standard_price`): **459 → 24,472** of 24,599 (99.5%).
- The 127 without cost have no sell price — nothing to derive from; left blank.

## Method (observed-ratio, category-derived, FLAGGED)
- Computed median cost-as-% of sell from the 422 "sane" variants that already carried both cost and price.
- Category medians (n>=3 samples): Solar Panels 45.2%, Inverters 87.6%, Electrical Supplies 87.5%, Generators 77.9%, Batteries & Storage 98.5%, Cabinets 93.9%, ATS 87.7%, Chargers 89.5%, Kits 94.6%.
- Fallback (overall median) = 76.9% cost of sell.
- Every derived value is marked `DERIVED_category_median` in `derived_cost_backfill.csv`. NOT vendor truth.

## Idempotency
- read-before-write on every fill (skip where cost already > 0). Re-runs safe.

## Files
- `derived_cost_backfill.csv` — 24,013 rows, full derived plan (variant_id, sku, category, ratio, sell, cost, flag).
