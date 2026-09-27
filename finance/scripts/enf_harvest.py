#!/usr/bin/env python3
"""
ENF datasheet harvest → Riven ERP enrichment.

For each ENF datasheet URL (from a company profile's product listing), pull:
  - series name + model numbers (-> x_mpn)
  - spec keys (power range, dimensions, weight, cell tech, certs) -> stored
  - product image URL + manufacturer PDF URL -> attachments/images

Sources:
  - Oxylabs Web Scraper API (realtime) for HTTP-bot-walled page HTML (auth: username:password)
  - cdn.enfsolar.com direct for image/PDF bytes (public, no auth)

Auth for Oxylabs lives in custom-cred / session file (NOT committed).

Usage:
  python3 enf_harvest.py --datasheet-urls u1 u2 u3 ...      # harvest specific datasheets
  python3 enf_harvest.py --company-slug ja-solar            # list + harvest a vendor's datasheets
  python3 enf_harvest.py --resume                            # resume from /tmp/enf_harvest_state.json

Writes (read-before-write, idempotent):
  product.template.x_mpn  (first model / series token)
  product.template.x_enf_url, x_manufacturer_url (if unfilled)
  product.template.image_1920/image_128 (JPEG bytes) via ir.attachment when appropriate
  product.template.product_document_ids  (manufacturer PDF) via product.document
"""
import argparse, base64, csv, json, os, re, html as H, sys, time
import requests, urllib3
import xmlrpc.client

urllib3.disable_warnings()

CRED = '/home/user/workspace/projects/body-of-work-clean-up-sR0_BZF0RuueOsDluXqUgg/files/CREDENTIALS-PLAIN-2026-09-11.txt'
OXY = '/tmp/oxy_creds.json'
URL = 'https://axis.pesdistribution.com'
DB = 'riven_erp_pes'
STATE = '/tmp/enf_harvest_state.json'


def oxy():
    return json.load(open(OXY))


def fetch_html(url):
    c = oxy()
    r = requests.post('https://realtime.oxylabs.io/v1/queries',
                      auth=(c['username'], c['password']),
                      json={'source': 'universal', 'url': url, 'render': 'html'},
                      timeout=90, verify=False)
    if r.status_code != 200:
        raise RuntimeError(f'oxylabs {r.status_code}: {r.text[:120]}')
    return r.json()['results'][0]['content']


def fetch_bytes(url):
    r = requests.get(url, timeout=120, verify=False, headers={'User-Agent': 'Mozilla/5.0'})
    r.raise_for_status()
    return r.content


def strip(text):
    t = H.unescape(re.sub(r'<[^>]+>', '|', text))
    t = re.sub(r'\|+', '|', t)
    t = re.sub(r'\s+', ' ', t)
    return t


def grab(html, key, span=90):
    text = strip(html)
    i = text.find(key)
    if i < 0:
        return ''
    seg = text[i:i + span]
    seg = re.sub(r'\|\s*\|', '|', seg)
    return seg


def extract_datasheet(url, html):
    """Return dict: series, models[], specs{}, image_url, pdf_url, manufacturer."""
    d = {'url': url, 'models': [], 'specs': {}, 'image': '', 'pdf': ''}
    m = re.search(r'<title>([^<]+)</title>', html)
    d['series'] = m.group(1).strip() if m else ''
    # model numbers
    txt = strip(html)
    mi = txt.find('Model No.')
    if mi >= 0:
        seg = txt[mi:mi + 300].split('Product Warranty')[0]
        d['models'] = [x for x in re.findall(r'[A-Z][A-Z0-9\.\-/]{2,30}', seg)
                       if len(x) >= 4 and re.search(r'\d', x)]
    # specs
    for key in ['Technology', 'Power Range', 'Weight', 'Panel Dimension', 'Product Warranty',
                'Power Warranty', 'Maximum System Voltage', 'Series Fuse Rating', 'Region']:
        g = grab(html, key)
        if g:
            d['specs'][key] = g
    # image (product logo / photo)
    im = re.findall(r'(https://cdn\.enfsolar\.com/Product/(?:logo|panel)[^"\']+)', html)
    d['image'] = im[0] if im else ''
    # PDF datasheet
    pd = re.search(r'href="(https://cdn\.enfsolar\.com/[^"]*\.pdf[^"]*)"', html)
    d['pdf'] = pd.group(1) if pd else ''
    return d


def connect_erp():
    txt = open(CRED).read()
    pw = re.search(r'RIVEN ERP ADMIN PASSWORD\s*\n\s*(\S+)', txt).group(1)
    m = xmlrpc.client.ServerProxy(URL + '/xmlrpc/2/object')
    c = xmlrpc.client.ServerProxy(URL + '/xmlrpc/2/common')
    uid = c.authenticate(DB, 'admin', pw, {})
    return m, uid, pw


def write_mpn(m, uid, pw, tmpl_id, mpn):
    cur = m.execute_kw(DB, uid, pw, 'product.template', 'read', [tmpl_id, ['x_mpn']])
    if not (cur and cur[0].get('x_mpn')):
        m.execute_kw(DB, uid, pw, 'product.template', 'write', [[tmpl_id], {'x_mpn': mpn}])
        return True
    return False


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--datasheet-urls', nargs='*')
    ap.add_argument('--company-slug')
    ap.add_argument('--resume', action='store_true')
    a = ap.parse_args()

    if a.datasheet_urls:
        urls = a.datasheet_urls
        print(f'harvesting {len(urls)} datasheets')
        for u in urls:
            try:
                html = fetch_html(u)
                d = extract_datasheet(u, html)
                print(json.dumps(d, indent=1)[:1500])
            except Exception as e:
                print(f'ERR {u}: {e}')
    elif a.company_slug:
        u = f'https://www.enfsolar.com/{a.company_slug}'
        html = fetch_html(u)
        ds = sorted(set(re.findall(r'"/?(pv/[\w\-/]+datasheet/[\w\-/]+)"', html)))
        print(f'{a.company_slug}: {len(ds)} datasheet links')
        for x in ds[:40]:
            print(' ', x)
    else:
        print('pass --datasheet-urls or --company-slug')