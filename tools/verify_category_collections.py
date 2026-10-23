import concurrent.futures
"""Five-category coverage and delivery verifier; requires collection-aware client."""
import collections
import concurrent.futures
import hashlib
import json
import sys
import urllib.request
from pathlib import Path
import jsonschema
ROOT=Path(__file__).resolve().parents[1]
raw=(ROOT/'catalog/v3/index.json').read_bytes();catalog=json.loads(raw);by_id={m['id']:m for m in catalog['packages']}
roots=[m for m in by_id.values() if m.get('collectionRole')=='category' and m.get('itemCategoryCollection')];assert len(roots)==5
members=[m for m in by_id.values() if m.get('itemCategoryCollection')];assert len(members)==7
schema=json.loads((ROOT/'schemas/catalog-entry-v1.schema.json').read_text())
for m in by_id.values():
 jsonschema.validate(m,schema);b=(ROOT/'packages'/m['url'].split('/')[-1]).read_bytes();assert len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256']
 if m.get('itemCategoryCollection'):
  p=json.loads(b);assert p['members']==m['dependencies'] and p['inventoryCategory']==m['inventoryCategory']
  assert 0<len(p['members'])<=50 and len(set(p['members']))==len(p['members'])
  assert m['minClientVersionCode']==10035
all_modules=set();all_items=set()
for root in roots:
 seen=set();visiting=set();items={}
 def visit(pid):
  assert pid in by_id and pid not in visiting
  if pid in seen:return
  visiting.add(pid);m=by_id[pid]
  for dep in m['dependencies']:visit(dep)
  if m['type']=='collection':assert m['inventoryCategory']==root['inventoryCategory']
  else:
   assert m['type'] in ['item','craft'];all_modules.add(pid)
   p=json.loads((ROOT/'packages'/m['url'].split('/')[-1]).read_bytes())
   for i in p.get('items',[]):
    assert i['inventoryCategory']==root['inventoryCategory'] and i['id'] not in items
    items[i['id']]=i
  visiting.remove(pid);seen.add(pid)
 visit(root['id']);assert len(items)==root['itemCount'];all_items.update(items)
assert len(all_items)==6729 and len(all_modules)==103
assert all_modules=={m['id'] for m in by_id.values() if m['type'] in ['item','craft']}
if '--public-payloads' in sys.argv or '--public' in sys.argv:
 def verify(m):
  b=urllib.request.urlopen(m['url'],timeout=45).read();assert len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256']
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(verify,members))
 print('PASS: seven actual public collection metadata payloads')
if '--public' in sys.argv:
 assert urllib.request.urlopen('https://raw.githubusercontent.com/waitermisanthrope-creator/DnD-VTT-Content/main/catalog/v3/index.json',timeout=45).read()==raw
 print('PASS: actual live catalog matches local index')
print('CATEGORY_COLLECTIONS_PASS: five categories, 103 original modules, 6729 stable item IDs; no duplicated items')
