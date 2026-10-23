"""Validate the next-client catalog against exact local payloads and legacy IDs."""
import hashlib
import json
import re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
read=lambda p:json.loads((root/p).read_text())
catalog=read('catalog/v4/index.json');old=read('catalog/v3/index.json')
ids=[m['id'] for m in catalog['packages']]
assert len(ids)==len(set(ids))
total=0
for m in catalog['packages']:
    path='packages/'+m['url'].split('/')[-1]
    raw=(root/path).read_bytes()
    assert len(raw)==m['bytes'] and hashlib.sha256(raw).hexdigest()==m['sha256'],path
    p=json.loads(raw)
    assert all(p[k]==m[k] for k in ['id','version','type','schemaVersion'])
    assert all(d in ids for d in m['dependencies'])
    if not (m['type']=='item' and m['id'].startswith('dnd.items.')):continue
    entries=p['items']; keys=[i['id'] for i in entries]
    assert 100<len(entries)<=5000 and len(keys)==len(set(keys))
    assert all(re.fullmatch('[a-z0-9][a-z0-9._-]{0,119}',k) for k in keys)
    assert all(i.get('description') and 'weight' in i and i['inventoryCategory']==m['id'].split('.')[-1] for i in entries)
    legacy=read('packages/'+m['id']+'.json')
    assert {i['id'] for i in legacy['items']}<=set(keys)
    total+=len(entries)
assert total==3311
p=read('packages/dnd.items.materials-2.0.0.json')
for group in ['animal','monster','humanoid']:
    assert any(i.get('craftMaterialId')==f'harvest_{group}_heart' for i in p['items'])
assert len(p['ingredients'])==120
assert not any(m['id'].startswith('dnd.alchemy.ingredients.') for m in catalog['packages'])
print(f'PASS: {len(ids)} catalog entries, {total} items, exact hashes, legacy IDs and 120 ingredient profiles')
