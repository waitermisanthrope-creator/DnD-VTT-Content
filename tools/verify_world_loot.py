"""Audit coverage, metadata and real optional downloads; --public verifies delivery."""
import collections
import concurrent.futures
import hashlib
import json
import re
import sys
import urllib.request
from pathlib import Path
import jsonschema
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())
raw=(ROOT/'catalog/v3/index.json').read_bytes();catalog=json.loads(raw)
ms=[m for m in catalog['packages'] if m.get('worldLootRevision')=='1.0.0']
assert len(ms)==25
items=[];before=[];profiles=[];all_ids=set();package_ids={m['id'] for m in catalog['packages']}
schema=load('schemas/catalog-entry-v1.schema.json');traits_schema=load('schemas/item-traits-v1.schema.json')
for m in catalog['packages']:
    jsonschema.validate(m,schema)
    b=(ROOT/'packages'/m['url'].split('/')[-1]).read_bytes();p=json.loads(b)
    assert len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256']
    assert all(p[k]==m[k] for k in ['schemaVersion','id','version','type'])
    assert all(d in package_ids for d in m['dependencies'])
    if m not in ms:
        before+=p.get('items',[])
        continue
    assert m['minClientVersionCode']==10034
    if m['type']=='craft':
        assert m['dependencies']==['dnd.alchemy.rules'] and p['mode']=='alchemy-ingredients' and p['items']==[]
        profiles+=p['ingredients'];continue
    assert not m['dependencies'] and 0<len(p['items'])<=100
    for i in p['items']:
        assert i['id'].startswith(m['id']+'.') and re.fullmatch('[a-z0-9][a-z0-9._-]{0,119}',i['id'])
        assert i['id'] not in all_ids;all_ids.add(i['id'])
        assert re.fullmatch(r'\d+(?:\.\d+)? кг',i['weight']) and i['description'] and i['cost']
        jsonschema.validate(i['itemTraits'],traits_schema)
        if i['itemTraits'].get('anatomy'):
            a=i['itemTraits']['anatomy'];mid=f"harvest_{a['group']}_{a['part']}"
            assert i['alchemyId']==i['craftMaterialId']==mid==i['itemTraits']['research']['ingredientId']
            assert 'properties' not in i and 'effects' not in i
        if i['inventoryCategory']=='consumables':assert i['effects']==[]
    items+=p['items']
assert len(items)==464 and len(profiles)==219
assert len({i['name'] for i in items})==len(items)
before_names={i['name'] for i in before};assert not before_names.intersection(i['name'] for i in items)
stock=before+items;stock_names={i['name'] for i in stock}
ids=[i['id'] for i in stock];assert len(ids)==len(set(ids))
profile_ids=[p['id'] for p in profiles];assert len(profile_ids)==len(set(profile_ids))
effects=load('packages/dnd.alchemy.rules.json')['effects']
for p in profiles:
    assert p['name'] in stock_names
    assert 2<=len(p['properties'])<=4 and len(set(p['properties']))==len(p['properties'])
    assert all(k in effects for k in p['properties'])
    assert all(0<=p[k]<=100 for k in ['potency','stability','volatility','purity'])
source=load('sources/world-loot-1.0.0.json');assert source['newItemCount']==len(items)
assert {i['id'] for i in source['items']}=={i['id'] for i in items}
examples=['Нож для масла','Пинцет','Шило','Игла портновская','Стамеска','Рыболовный крючок','Ступка','Селезёнка гуманоида','Селезёнка животного','Селезёнка монстра','Кислотный мешок монстра','Плавательный пузырь животного','Скальпель']
# The UI name is explicit rather than the ambiguous short alias.
examples[-1]='Хирургический скальпель'
assert all(name in stock_names for name in examples)
audit=dict(schemaVersion=1,revision='1.0.0',baseline=dict(items=len(before),uniqueNames=len(before_names),duplicateNameCount=sum(n>1 for n in collections.Counter(i['name'] for i in before).values())),
    expansion=dict(items=len(items),uniqueNames=len(items),optionalPackages=len(ms),researchProfiles=len(profiles),categories=dict(collections.Counter(i['inventoryCategory'] for i in items))),
    combinedItems=len(stock),examples=[dict(name=n,before=n in before_names,after=n in stock_names) for n in examples],
    anatomyProfilesByGroup=dict(collections.Counter(p['id'].split('_')[1] for p in profiles)),coverage=source['coverage'],remaining=['automatic creature drop tables','harvesting interface and organ availability by creature','freshness timers and per-provenance stack isolation','automatic craft recipes and shop transactions for new metadata','physical device GUI QA'])
audit_path=ROOT/'sources/world-loot-audit-1.0.0.json'
if '--write-audit' in sys.argv:audit_path.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
assert json.loads(audit_path.read_bytes())==audit,'Audit snapshot is stale; run --write-audit'
if '--public-payloads' in sys.argv or '--public' in sys.argv:
    def verify(m):
        b=urllib.request.urlopen(m['url'],timeout=45).read();assert len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256'],m['url']
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(verify,ms))
    print('PASS: 25 actual public payload URLs and exact SHA-256/bytes')
if '--public' in sys.argv:
    b=urllib.request.urlopen('https://raw.githubusercontent.com/waitermisanthrope-creator/DnD-VTT-Content/main/catalog/v3/index.json',timeout=45).read()
    assert b==raw,'Actual public index differs';print('PASS: actual public catalog equals validated local index')
print('WORLD_LOOT_PASS:',len(items),'new distinct names;',len(profiles),'research profiles;',len(stock),'combined items;',len(catalog['packages']),'catalog entries')
