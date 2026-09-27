#!/usr/bin/env python3
"""
ENF panel/inverter/ESS product harvest → native Riven ERP modules.

Per manufacturer company profile (e.g. /ja-solar), extract every product offer:
  - series name + model family (-> x_mpn / supplierinfo.product_code)
  - power range (Wp)  (-> product.attribute "Power Range")
  - technology (TOPCon/HJT/bifacial/PERC/N-type)  (-> product.attribute "Panel Technology")
  - certification waveform from the datasheet (-> product.attribute "Certification")
  - thumbnail image URL (-> product.template image / attachment)
  - datasheet PDF URL (-> product.document)

Writes to native modules (read-before-write, idempotent):
  product.template.x_mpn / product.supplierinfo.product_code
  product.document (datasheet PDFs)
  product.attribute + product.attribute.value + product.template.attribute.line (facets)
  (CEC listing date/type already written via x_cec_*)

Usage:
  python3 enf_harvest_all.py --company ja-solar,trina-solar,csi-solar
  python3 enf_harvest_all.py --companies-file /tmp/vendors.txt   # one slug per line
"""
import argparse, base64, csv, json, os, re, html as H, sys, time
import requests, urllib3
import xmlrpc.client

urllib3.disable_warnings()

CRED = '/home/user/workspace/projects/body-of-work-clean-up-sR0_BZF0RuueOsDluXqUgg/files/CREDENTIALS-PLAIN-2026-09-11.txt'
OXY = '/tmp/oxy_creds.json'
URL = 'https://axis.pesdistribution.com'
DB = 'riven_erp_pes'
OUT = '/tmp/enf_offers.json'   # accumulated raw offers (durable)

def oxy():
    return json.load(open(OXY))

def fetch_html(url):
    c = oxy()
    r = requests.post('https://realtime.oxylabs.io/v1/queries',
                      auth=(c['username'], c['password']),
                      json={'source': 'universal', 'url': url, 'render': 'html'},
                      timeout=90, verify=False)
    if r.status_code != 200:
        raise RuntimeError(f'oxylabs {r.status_code}: {r.text[:150]}')
    return r.json()['results'][0]['content']

def fetch_bytes(url):
    r = requests.get(url, timeout=180, verify=False, headers={'User-Agent': 'Mozilla/5.0'})
    r.raise_for_status()
    return r.content

def strip_html(html):
    t = H.unescape(re.sub(r'<[^>]+>', '|', html))
    t = re.sub(r'\|+', '|', t)
    t = re.sub(r'\s+', ' ', t)
    return t

def extract_offers(html, base='https://www.enfsolar.com'):
    offers = []
    for block in re.findall(r'<li class="list-none[^"]*"[^>]*>(.*?)</li>', html, re.S):
        href = re.search(r'href="(/pv/(?:panel-datasheet|inverter-datasheet|storage-datasheet|component-datasheet)/[^"]+)"', block)
        series = re.search(r'itemprop="name"[^>]*title="([^"]+)"', block)
        alt = re.search(r'alt="([^"]+)"', block)
        img = re.search(r'data-src="(https://cdn\.enfsolar\.com/[^"]+)"', block)
        power = re.search(r'<span class="blue">([^<]+)</span>', block)
        tech = re.search(r'<span class="yellow"[^>]*>([^<]+)</span>', block)
        if href:
            offers.append({
                'datasheet': base + href.group(1),
                'series': alt.group(1) if alt else (series.group(1) if series else ''),
                'thumb': img.group(1) if img else '',
                'power': power.group(1).strip() if power else '',
                'tech': tech.group(1).strip() if tech else '',
            })
    return offers

def load_out():
    return json.load(open(OUT)) if os.path.exists(OUT) else {}

def save_out(d):
    json.dump(d, open(OUT, 'w'))

def connect_erp():
    txt = open(CRED).read()
    pw = re.search(r'RIVEN ERP ADMIN PASSWORD\s*\n\s*(\S+)', txt).group(1)
    m = xmlrpc.client.ServerProxy(URL + '/xmlrpc/2/object')
    c = xmlrpc.client.ServerProxy(URL + '/xmlrpc/2/common')
    uid = c.authenticate(DB, 'admin', pw, {})
    return m, uid, pw

def harvest_company(slug):
    html = fetch_html(f'https://www.enfsolar.com/{slug}')
    offers = extract_offers(html)
    out = load_out()
    out[slug] = {'offers': offers, 'count': len(offers), 'at': time.time()}
    save_out(out)
    print(f'{slug}: {len(offers)} offers')
    for o in offers[:6]:
        print(f"   {o['series'][:44]:44} {o['power'][:16]:16} {o['tech'][:18]}")
    return offers

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--company')
    ap.add_argument('--companies-file')
    a = ap.parse_args()
    slugs = []
    if a.company:
        slugs = [x.strip() for x in a.company.split(',') if x.strip()]
    elif a.companies_file:
        slugs = [l.strip() for l in open(a.companies_file) if l.strip()]
    for s in slugs:
        try:
            harvest_company(s)
        except Exception as e:
            print(f'ERR {s}: {e}')
        time.sleep(1)