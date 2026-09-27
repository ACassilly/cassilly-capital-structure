# Porto Enrichment — Shopify + ENF → Riven ERP

Prepared 2026-09-27. Live book: Riven ERP `riven_erp_pes`.

## What the data showed

### Join key (solved)
Shopify `sku` ↔ ERP `product.product.default_code` = **24,353 exact matches** (of 24,446 coded variants). 93 ERP variants have no Shopify mirror.

### Shopify bulk export (GraphQL `bulkOperationRunQuery`)
- 85,411 products / 85,428 variants, 46.9 MB JSONL (parsed → `shopify_enrichment_extract.csv`).
- 1,988 distinct `vendor` values (Enphase 1425, SolarEdge 1115, Generac 989, Victron 772, JA Solar 332, …).
- barcode on 10%, weight on 54%, SKU on 68%. **HS code = 0, country-of-origin = 0** (Shopify doesn't have them).

### Backfill deltas identified (ERP empty → Shopify has it)
| Field | Delta |
|---|---|
| weight (kg) | 18,634 variants |
| barcode | 892 variants |

### ENF Solar (enfsolar.com) — authoritative manufacturer/spec source
- Fetchable via slug URLs (`/victron-energy`, `/ja-solar`, `/fronius`).
- Carries: legal name, country, address, website, phone, staff count, certifications (TÜV/UL/IEC/CEC), product categories.
- Slug ambiguity: `/solaredge` matched a Pakistani installer, not SolarEdge Technologies → must disambiguate by country/website cross-check.
- Full directory available as paid Excel export (63,600 companies; GDPR-compliant; €500 min).

### ERP already has ENF plumbing (empty, ready to fill)
`product.template`: `x_enf_url` (0/24k), `x_manufacturer_url` (0/24k), `x_mpn` (421/24k), `x_competitor_url` (0), `x_eol_status` (10). Also `country_of_origin`, `hs_code`, `weight` (kg), `barcode`, `seller_ids`.

## Execution order
1. **Shopify weight + barcode backfill** — mass, idempotent (kg conversion: POUNDS × 0.453592). ✅ doing now.
2. **Vendor → manufacturer map** — 1,988 vendors → canonical manufacturer partner + `x_manufacturer_url`.
3. **ENF manufacturer enrichment** — fetch top-N vendors from ENF slugs (country, website, certs, staff), write `res.partner` + `x_enf_url`.
4. **Spec backfill** — `x_mpn` / `country_of_origin` / `hs_code` where ENF datasheet provides.