"""Validate every catalog payload, stable IDs, independent volumes and source map.

With --public, fetch actual public raw bytes before reporting publication.
"""
import concurrent.futures
import hashlib
import json
import re
import sys
import urllib.request
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
raw=(ROOT/'catalog/v3/index.json').read_bytes();catalog=json.loads(raw)
ids=[m['id'] for m in catalog['packages']];assert len(ids)==len(set(ids))
volumes=[m for m in catalog['packages'] if m.get('collectionVolume')]
assert len(volumes)==36
all_items=[]
for m in catalog['packages']:
    path=ROOT/'packages'/m['url'].split('/')[-1];b=path.read_bytes();p=json.loads(b)
    assert len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256'],path
    assert all(p[k]==m[k] for k in ['id','type','version','schemaVersion'])
    assert all(d in ids for d in m['dependencies'])
    if not m.get('collectionVolume'):continue
    assert not m['dependencies'] and m['minClientVersionCode']==10034
    assert m['type']=='item' and p['version']=='1.1.0'
    assert 1<=len(p['items'])<=100
    for i in p['items']:
        assert i['id'].startswith(m['id']+'.') and re.fullmatch('[a-z0-9][a-z0-9._-]{0,119}',i['id'])
        assert i.get('description') and 'weight' in i and i['inventoryCategory']==m['collectionSeries']
        if i['inventoryCategory']=='consumables': assert isinstance(i.get('effects'),list)
    all_items+=p['items']
keys=[i['id'] for i in all_items];assert len(keys)==3291 and len(set(keys))==len(keys)
for c in ['weapons','armor','materials','consumables','junk']:
    legacy=json.loads((ROOT/f'packages/dnd.items.{c}.json').read_bytes())
    assert {i['id'] for i in legacy['items']}<=set(keys)
source=json.loads((ROOT/'sources/workshop-volumes-1.1.0.json').read_bytes())
assert source['itemCount']==len(keys) and {i['publishedId'] for i in source['items']}==set(keys)
try:
    import jsonschema
except ImportError:
    raise SystemExit('Install jsonschema to run the complete manifest check')
schema=json.loads((ROOT/'schemas/catalog-entry-v1.schema.json').read_bytes())
for m in catalog['packages']:jsonschema.validate(m,schema)
if '--public-payloads' in sys.argv or '--public' in sys.argv:
    def verify(m):
        b=urllib.request.urlopen(m['url'],timeout=45).read()
        assert len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256'],m['url']
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(verify,volumes))
    print('PASS: 36 actual public payload URLs, exact hashes and byte counts')
if '--public' in sys.argv:
    url='https://raw.githubusercontent.com/waitermisanthrope-creator/DnD-VTT-Content/main/catalog/v3/index.json'
    assert urllib.request.urlopen(url,timeout=45).read()==raw,'Public catalog differs'
    print('PASS: actual live public catalog matches local catalog')
print('PASS:',len(ids),'catalog entries; optional volumes',dict(Counter(m['collectionSeries'] for m in volumes)),
      '; items',dict(Counter(i['inventoryCategory'] for i in all_items)))
