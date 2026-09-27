# Porto Enrichment — Schema Map (ENF / CEC / Shopify → Riven ERP)

Owner: Riven ERP `riven_erp_pes` (axis.pesdistribution.com). This document is the single
authority for WHERE each enrichment lands and WHICH module consumes it. No ad-hoc `x_`
dumps for data that has a native module home.

## Principles
- Enrichment lands in the native module that *consumes* it, so it is usable by RFQ/PO,
  e-commerce facets, document control, and customs/l;anded-cost flows — not just stored.
- Read-before-write on every field. Additive, idempotent, reversible.
- `x_*` custom fields are reserved for data with NO native home (e.g. an external URL
  reference). Everything else goes to the native model.

## The map

| Source data | ERP module.field | Consumer module | Notes |
|---|---|---|---|
| Vendor part number (MPN) | `product.supplierinfo.product_code` | **Purchase** | Keyed to `partner_id` (the vendor). Drives RFQ line matching + PO vendor part ref. `product.template.x_mpn` is the product-level display copy only. |
| Vendor unit cost | `product.supplierinfo.price` + `currency_id` | **Purchase** | Vendor price for RFQ comparison. |
| Vendor lead time | `product.supplierinfo.delay` | **Purchase** | Delivery scheduling. |
| Panel technology (TOPCon/HJT/bifacial), power range, cell type | `product.attribute` + `product.template.attribute.line` + `product.attribute.value` | **Website/Sales** | Catalog facets & filters. |
| Certifications (UL 1703/61730, TUV, IEC) | `product.attribute.value` (attr "Certification") | **Website/Sales** | Compliance filter. Also mirrored in `product.seller_delay` no — certs also feed `product.document`. |
| Spec-sheet PDF (manufacturer datasheet) | `product.document` (`datas`=base64, `mimetype=application/pdf`, `res_model=product.template`, `shown_on_product_page=True`) | **Document control / Website** | Product-page download + attach-to-email. |
| Product image | `product.template.image_1920` (+ `image_128` thobs) base64 JPEG | **Website/Sales** | Product image. (Already ~99% populated in this catalog.) |
| HS / HTS code | `product.template.hs_code` | **Purchase (landed cost) / Accounting** | Customs duty calc. Category-derived here, flagged DERIVED. |
| Country of origin | `product.template.country_of_origin` (→ res.country) | **Purchase / Legal** | AD/CVD + UFLPA customs risk. |
| Vendor company name, website, country, staff | `res.partner` | **CRM / Purchase** | Supplier directory. |
| CEC listing date + equipment type | `product.template.x_cec_listing_date` (date), `x_cec_kind` (char), `x_cec_cert` (char), `x_cec_mfr` (char) | **Sales (CA permit readiness)** | No native compliance module exists, so x_ custom fields are warranted here. |
| ENF / manufacturer profile URL | `product.template.x_enf_url`, `x_manufacturer_url` | **Reference** | External link, no native home. |
| MPN display | `product.template.x_mpn` | **Reference** | Product-level display of the canonical model. Vendor-scoped MPN goes to supplierinfo. |

## Consumer workflows this unlocks
1. **RFQ/PO**: supplierinfo.product_code + price lets procurement issue a PO with the
   vendor's exact part number and compare vendor prices side by side.
2. **E-commerce**: attributes turn Panel Technology / Power Range / Certification into
   filterable facets on the storefront.
3. **Document control**: `product.document` serves the manufacturer datasheet on the
   product page and attaches it to quote/sale emails.
4. **CA permit readiness**: `x_cec_listing_date` answers "is this LISTED and when" for
   California clients — the difference between a permitted install and a return.
5. **Landed cost**: hs_code + country_of_origin feed duty (Section 201/301) + AD/CVD.

## Field contract (verified against live ERP)
- `product.supplierinfo`: `product_tmpl_id` (many2one), `partner_id` (many2one),
  `product_code` (char), `price` (float), `delay` (int days), `currency_id`.
  MPN rows key on product_tmpl_id + partner_id.
- `product.document`: `name`, `datas` (base64 file bytes), `mimetype`,
  `res_model` ("product.template"), `res_id` (template id), `shown_on_product_page` (bool),
  `res_name`. Existing 76 PDFs use exactly this shape.
- `product.template.attribute.line`: `attribute_id` (product.attribute), `product_tmpl_id`,
  `value_ids` (many2many product.attribute.value). **0 attributes exist today** — the
  attribute system must be seeded before lines can be written.
- `product.template.image_1920`: base64 JPEG string (verified: starts `/9j/`).

## What already landed (this pass, native homes)
- `res.partner` website + country: 45 vendors.
- `product.template.hs_code`: 23,092 (category→HTS, DERIVED).
- `product.template.country_of_origin`: 6,285 (ENF manufacturer country).
- `product.template.x_enf_url` / `x_manufacturer_url`: 6,190.
- `product.template.x_cec_listing_date` / `x_cec_kind` / `x_cec_cert` / `x_cec_mfr`: 912
  (matched to CEC PV Module/Inverter/Battery/Meter lists, 906 with listing dates).

## Still to land (native, prioritized)
1. `product.supplierinfo.product_code` — backfill vendor MPN (from CEC model + ENF series)
   on the existing supplierinfo rows; currently 286/24,450 populated.
2. `product.document` — attach ENF manufacturer datasheet PDFs to the matched templates.
3. `product.attribute` system — seed attributes (Panel Technology, Power Range,
   Certification, Cell Type) + values; write attribute lines for ENF-matched products.
4. `product.supplierinfo.price` — vendor cost when the cost-source tier provides it.