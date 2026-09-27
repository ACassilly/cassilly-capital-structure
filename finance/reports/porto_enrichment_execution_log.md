# Porto Enrichment — Shopify + ENF Solar → Riven ERP (Execution Log)

Date: 2026-09-27. Active book: Riven ERP `riven_erp_pes` (axis.pesdistribution.com).

## Cost backfill (completed)
- Variants with cost: 459 → **24,472 / 24,599 (99.5%)**. The 127 remainder have no sell price (nothing to derive). See `product_cost_backfill_log.md`.

## Shopify bulk export (completed)
- GraphQL `bulkOperationRunQuery` → 170,839 JSONL rows (85,411 products / 85,428 variants), 46.9 MB.
- Parsed → `shopify_enrichment_extract.csv` (variant-level: sku, barcode, vendor, product_type, tags, weight, unit_cost, hs_code, country_origin).
- 1,988 distinct vendors. **HS code = 0, country-of-origin = 0** — Shopify doesn't have them (ENF gap).
- Join key: Shopify `sku` ↔ ERP `product.product.default_code` = **24,353 exact matches**.

## Shopify → ERP backfill (completed)
| Field | Delta applied |
|---|---|
| weight (kg, lb→kg converted) | 4,846 → **18,635** variants |
| barcode | skipped — 892 wouldn't apply; uniqueness conflicts with existing ERP barcodes |

## ENF Solar enrichment (completed — 47 manufacturers)
- 47 manufacturer profiles fetched from enfsolar.com slug URLs (disambiguated by search: `/solaredge-technologies` not the Pakistan installer).
- `x_enf_url` + `x_manufacturer_url` written on **6,190 product.template** rows.
- `res.partner` enriched (website + country) for **45 vendors** (Enphase→US, SolarEdge→Israel, Victron→Netherlands, JA Solar→China, SMA→Germany, REC→Singapore, Huasun→China, Waaree→India, BYD→China, Jinko→China, SolarSpace→China, Trina→China, AIKO→China, CSI Solar→Canada, Anker→China, VSUN→Japan, K2→Germany, …).
- DAH Solar partner created (id 4126) — its 172 Shopify SKUs have no ERP default_code match (not yet in catalog).
- Disambiguation catches: Go Power (US) ≠ ENF `gopower` (Poland) — skipped; `/solaredge` (Pakistan installer) → `/solaredge-technologies`.
- Full map: `enf_manufacturer_map.json` (shopify_vendor, enf_slug, legal name, country, website, staff, parent, certs, categories).

## What remains open
1. **HS code + country_of_origin** — genuinely absent in Shopify; requires ENF datasheet-level fetch (per-model) or the paid ENF directory Excel (€500 min, 63,600 companies).
2. **`x_mpn`** — only 421/24k filled; needs ENF product-datasheet join per model.
3. **Remaining vendors** — 47 mapped top manufacturers cover the headline brands; ~600 smaller/tier-2 and white-label vendors remain, batch-able with the same search→slug→fetch→write pattern.
4. **DAH Solar catalog gap** — 172 SKUs not in ERP (worth flagging to the catalog team).

## Idempotency
- All writes are read-before-write: `x_enf_url` skip-if-set, weight skip-if->0, partner skip-if-website-set. Re-running the scripts is safe.

## Files
- `enrichment_pipeline.md` — plan.
- `shopify_enrichment_extract.csv`, `shopify_vendor_roster.csv`, `enf_manufacturer_map.json` — durable extracts.