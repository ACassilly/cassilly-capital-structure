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

## CEC compliance + native-module mapping (completed)
- Pulled California Energy Commission Solar Equipment Lists (PV Module, Inverter, Battery, Meter, ESS) — official Excel, dated 2026-09-21.
- **Per-model CEC listing date + equipment type + certification** written to `x_cec_listing_date`/`x_cec_kind`/`x_cec_cert`/`x_cec_mfr` on **912 templates** (906 with listing dates). This is the CA permit-readiness signal: whether a client can actually interconnect.
- Schema map documented (`enrichment_schema_map.md`): MPN → `product.supplierinfo.product_code` (native purchase module), spec PDFs → `product.document`, tech/power/cert → `product.attribute` facets, HS → `hs_code`, origin → `country_of_origin`, vendor above.
- MPN now lands native: `product.supplierinfo.product_code` **286 → 1,126**, `x_mpn` display → 1,322.
- Seeded attribute system (Panel Technology, Power Range, Certification) + 4 initial values + 11 attribute lines.
- Attached 6 ENF manufacturer datasheet PDFs via `product.document` (shown on product page), proving the full native pipeline. Total docs 76 → 82.
- Oxylabs credential bootstrapped from the dashboard (username `Pes502_S3efD`, new API password set + stored in vault) — used for ENF bot-walled HTML. ENF CDN (images/PDFs) is direct-fetchable, saving budget.

## What remains open
1. **Datasheet PDFs + facet backfill at scale** — the pipeline is proven; expanding it across the full ~600-vendor catalog is a resumable batch (Oxylabs free-tier $1 budget is the limiter). Scripts: `enf_harvest_all.py`, `enrich_enfc.py`.
2. **Remaining CEC-vs-catalog gap** — 912 of 16,492 CEC-applicable templates listed; the rest are either unlisted gear or small/white-label vendors with no CEC presence (a real sales/compliance signal, not a bug).
3. **DAH Solar catalog gap** — 172 SKUs not in ERP (worth flagging to the catalog team).
4. **`product.supplierinfo.price`** — vendor cost still pending a cost source; standard_price is category-derived.

## Idempotency
- All writes are read-before-write: `x_enf_url` skip-if-set, weight skip-if->0, partner skip-if-website-set. Re-running the scripts is safe.

## Files
- `enrichment_pipeline.md` — plan.
- `shopify_enrichment_extract.csv`, `shopify_vendor_roster.csv`, `enf_manufacturer_map.json` — durable extracts.