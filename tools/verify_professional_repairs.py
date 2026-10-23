"""Verify professional roles, inert broken states, exact links and public delivery."""
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
def read(p):return json.loads((ROOT/p).read_text())
raw=(ROOT/'catalog/v3/index.json').read_bytes();catalog=json.loads(raw)
packages={m['id']:m for m in catalog['packages']};assert len(packages)==len(catalog['packages'])
ms=[m for m in packages.values() if m.get('professionalRepairRevision')=='1.0.0']
assert len(ms)==37
items={};new=[];broken=[];tools=[];baseline=[]
manifest_schema=read('schemas/catalog-entry-v1.schema.json');trait_schema=read('schemas/item-traits-v1.schema.json');repair_schema=read('schemas/repair-profile-v1.schema.json')
for m in packages.values():
 jsonschema.validate(m,manifest_schema);b=(ROOT/'packages'/m['url'].split('/')[-1]).read_bytes();p=json.loads(b)
 assert len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256']
 assert all(p[k]==m[k] for k in ['id','version','type','schemaVersion'])
 assert all(d in packages for d in m['dependencies'])
 for i in p.get('items',[]):
  assert i['id'] not in items;iid=i['id'];items[iid]=(i,m)
  if m not in ms:baseline.append(i);continue
  assert not m['dependencies'] and 1<=len(p['items'])<=100
  assert i['id'].startswith(m['id']+'.') and re.fullmatch('[a-z0-9][a-z0-9._-]{0,119}',i['id'])
  assert 'weight' in i and i['description'] and i['cost']
  jsonschema.validate(i['itemTraits'],trait_schema);new.append(i)
  if m['professionalRepairKind']=='tools':tools.append(i)
  else:broken.append(i)
assert len(tools)==56 and len(broken)==2798 and len(items)==6729
for i in tools:
 t=i['professionalTool'];assert t['professionId'] and t['role'] and t['operations'] and t['grantsProficiency'] is False and t['execution']=='manual'
 if 'containerSpec' in i:assert i['containerSpec']['initialContents']==[] and i['containerSpec']['capacityMl']>0
for i in broken:
 jsonschema.validate(i['repairProfile'],repair_schema)
 assert i['inventoryCategory']=='junk' and i['condition']=='broken' and i['itemTraits']['stateDefaults']['condition']=='broken'
 assert all(k not in i for k in ['damage','damageType','toHit','ac','acBase','effects','effect','alchemyId','craftMaterialId','materialId','bonuses','proficiencies','professionalTool','containerSpec'])
 t=i['repairProfile']['target'];target,m=items[t['itemId']]
 assert t['itemId']==i['brokenVariantOf'] and target.get('condition')!='broken' and target.get('brokenVariantOf') is None
 assert (t['packageId'],t['packageVersion'],t['packageSha256'],t['packageUrl'])==(m['id'],m['version'],m['sha256'],m['url'])
 assert target['inventoryCategory'] in ['weapons','armor','junk'] and i['weight']==target['weight']
 assert i['name']!=target['name']
links=read('sources/repair-links-1.0.0.json');assert links['brokenCount']==len(broken)
assert {x['brokenItemId'] for x in links['links']}=={i['id'] for i in broken}
assert len({i['brokenVariantOf'] for i in broken})==len(broken)
index=read('sources/professional-tools-1.0.0.json');assert index['newToolCount']==len(tools) and index['reusedToolCount']==6
for entry in index['tools']:assert entry['itemId'] in items and items[entry['itemId']][0]['name']==entry['name']
for name in ['Кузнечный молот','Нож для мездрения шкур','Точильный камень','Пустой алхимический сосуд']:
 target=next(i for i in tools if i['name']==name);assert any(i['brokenVariantOf']==target['id'] for i in broken)
assert not {i['name'] for i in new}.intersection(i['name'] for i in baseline)
vessel=next(i for i in tools if i['name']=='Пустой алхимический сосуд')
vessel_broken=next(i for i in broken if i['brokenVariantOf']==vessel['id'])
assert vessel_broken['repairProfile']['craft']['professionIds']==['glasswork']
assert vessel_broken['repairProfile']['craft']['toolUseProfessionIds']==['alchemy']
for field,value in [('maxBreakDimensionFt',2),('restoresMagic',True),('restoresCharges',True),('requiresAllOriginalPieces',False)]:
 import copy
 bad=copy.deepcopy(broken[0]['repairProfile']);bad['mending'][field]=value
 try:jsonschema.validate(bad,repair_schema)
 except jsonschema.ValidationError:pass
 else:raise AssertionError('Unsafe Mending declaration accepted: '+field)
if '--public-payloads' in sys.argv or '--public' in sys.argv:
 def verify(m):
  b=urllib.request.urlopen(m['url'],timeout=45).read();assert len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256'],m['url']
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(verify,ms))
 print('PASS: 37 actual public payload URLs, exact SHA-256/bytes')
if '--public' in sys.argv:
 assert urllib.request.urlopen('https://raw.githubusercontent.com/waitermisanthrope-creator/DnD-VTT-Content/main/catalog/v3/index.json',timeout=45).read()==raw
 print('PASS: actual public catalog matches validated index')
print('PROFESSIONAL_REPAIRS_PASS:',len(tools),'new tools,',len(broken),'inert linked broken variants,',len(items),'total inventory records,',len(packages),'catalog entries')
