#!/usr/bin/env python3
"""
Porto enrichment — durable, resumable ERP writer.

Feeds the Riven ERP enrichment fields from Shopify + ENF extracts.

  shopify extract:  /tmp/shopify_enrichment_extract.csv  (sku, barcode, vendor, product_type, tags, weight, unit_cost)
  enf map:          /tmp/enf_manufacturer_map.json        (shopify_vendor, enf_slug, legal name, country, website, ...)

Writes (all read-before-write / idempotent):
  - product.product.weight      (kg, from Shopify pounds)   where weight<=0
  - product.template.x_enf_url  (https://www.enfsolar.com/<slug>)
  - product.template.x_manufacturer_url
  - res.partner.website / country_id for matched vendor partners

Usage:
  python3 enrich_porto.py           # full resumable run (weight + ENF)
  python3 enrich_porto.py --weight-only
  python3 enrich_porto.py --enf-only
"""
import csv, json, re, sys, time, os, argparse
import xmlrpc.client
from collections import defaultdict

CRED = '/home/user/workspace/projects/body-of-work-clean-up-sR0_BZF0RuueOsDluXqUgg/files/CREDENTIALS-PLAIN-2026-09-11.txt'
URL = 'https://axis.pesdistribution.com'
DB = 'riven_erp_pes'
SHOP = '/tmp/shopify_enrichment_extract.csv'
ENFMAP = '/tmp/enf_manufacturer_map.json'

def connect():
    txt = open(CRED).read()
    pw = re.search(r'RIVEN ERP ADMIN PASSWORD\s*\n\s*(\S+)', txt).group(1)
    m = xmlrpc.client.ServerProxy(URL + '/xmlrpc/2/object')
    c = xmlrpc.client.ServerProxy(URL + '/xmlrpc/2/common')
    uid = c.authenticate(DB, 'admin', pw, {})
    return m, uid, pw

def load_shop():
    shop = {}
    for row in csv.DictReader(open(SHOP, encoding='utf-8')):
        sku = row['sku']
        if sku and sku not in shop:
            shop[sku] = row
    return shop

def weight_backfill(m, uid, pw):
    shop = load_shop()
    erp = m.execute_kw(DB, uid, pw, 'product.product', 'search_read',
        [[['default_code', '!=', False], ['weight', '<=', 0]], ['id', 'default_code', 'weight']],
        {'limit': 40000})
    groups = defaultdict(list)
    for p in erp:
        s = shop.get(p['default_code'])
        if not s:
            continue
        try:
            sw = float(s['weight_value'])
        except (TypeError, ValueError):
            sw = 0
        if sw > 0:
            kg = round(sw * 0.453592 if s['weight_unit'] == 'POUNDS' else sw, 3)
            groups[kg].append(p['id'])
    n = 0
    for kg, ids in groups.items():
        for i in range(0, len(ids), 1000):
            m.execute_kw(DB, uid, pw, 'product.product', 'write', [ids[i:i+1000], {'weight': kg}])
            n += len(ids[i:i+1000])
    print(f"weight: wrote {n} variants")

def enf_backfill(m, uid, pw):
    shop = load_shop()
    enf = json.load(open(ENFMAP))
    vendor_skus = defaultdict(set)
    for row in csv.DictReader(open(SHOP, encoding='utf-8')):
        if row['vendor'] and row['sku']:
            vendor_skus[row['vendor']].add(row['sku'])
    erp = m.execute_kw(DB, uid, pw, 'product.product', 'search_read',
        [[['default_code', '!=', False]], ['default_code', 'product_tmpl_id']], {'limit': 40000})
    dc2tmpl = {p['default_code']: (p['product_tmpl_id'][0] if p['product_tmpl_id'] else None) for p in erp}
    filled = {x['id'] for x in m.execute_kw(DB, uid, pw, 'product.template', 'search_read',
        [[['x_enf_url', '!=', False]], ['id']])}

    countries = m.execute_kw(DB, uid, pw, 'res.country', 'search_read', [[], ['code', 'name']])
    cn = {c['name'].strip().lower(): c['id'] for c in countries}
    allp = m.execute_kw(DB, uid, pw, 'res.partner', 'search_read',
        [[['is_company', '=', True]], ['id', 'name', 'website', 'country_id']], {'limit': 5000})
    byname = {p['name'].strip().lower(): p for p in allp}

    tot = 0
    for e in enf:
        tids = {dc2tmpl[s] for s in vendor_skus.get(e['shopify_vendor'], set()) if dc2tmpl.get(s)}
        todo = [t for t in tids if t not in filled]
        if todo:
            enf_url = f"https://www.enfsolar.com/{e['enf_slug']}"
            mf_url = e['website'] if e['website'].startswith('http') else enf_url
            for i in range(0, len(todo), 500):
                m.execute_kw(DB, uid, pw, 'product.template', 'write',
                    [todo[i:i+500], {'x_enf_url': enf_url, 'x_manufacturer_url': mf_url}])
            tot += len(todo)
        # partner enrichment
        hit = None
        for k in {e['shopify_vendor'].strip().lower(), e['enf_name'].split(',')[0].strip().lower()}:
            if k in byname:
                hit = byname[k]; break
        if hit:
            vals = {}
            if e['website'] and not (hit.get('website') or '').strip():
                vals['website'] = e['website']
            cid = cn.get(e['country'].strip().lower())
            if cid and not hit.get('country_id'):
                vals['country_id'] = cid
            if vals:
                m.execute_kw(DB, uid, pw, 'res.partner', 'write', [[hit['id']], vals])
        print(f"  {e['shopify_vendor']:18} templ={len(todo)}")
    print(f"enf: wrote x_enf_url on {tot} templates")

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--weight-only', action='store_true')
    ap.add_argument('--enf-only', action='store_true')
    a = ap.parse_args()
    m, uid, pw = connect()
    if not a.enf_only:
        weight_backfill(m, uid, pw)
    if not a.weight_only:
        enf_backfill(m, uid, pw)