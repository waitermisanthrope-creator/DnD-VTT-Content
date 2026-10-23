"""Full catalog coverage, immutable base entries, and actual public delivery."""
import argparse,concurrent.futures,hashlib,json,subprocess,urllib.request
from pathlib import Path
import jsonschema
from build_mod_collections import category
p=argparse.ArgumentParser();p.add_argument('--assets',type=Path,required=True);p.add_argument('--public-payloads',action='store_true');p.add_argument('--public',action='store_true');args=p.parse_args()
content=Path(__file__).resolve().parents[1];allmods={};new=[];catalogs=[]
for root,repo,path,key,baseline,schema in [(content,'Content','catalog/v3/index.json','packages','43e3043','schemas/catalog-entry-v1.schema.json'),(args.assets,'Assets','catalog/v9/index.json','packs','8cf392a','schemas/catalog-entry-v3.schema.json')]:
 raw=(root/path).read_bytes();entries=json.loads(raw)[key];byid={m['id']:m for m in entries};assert len(byid)==len(entries)
 old=json.loads(subprocess.check_output(['git','show',baseline+':'+path],cwd=root))[key];assert all(byid[m['id']]==m for m in old)
 sch=json.loads((root/schema).read_text());catalogs.append((f'https://raw.githubusercontent.com/waitermisanthrope-creator/DnD-VTT-{repo}/main/{path}',raw))
 for m in entries:
  assert m['id'] not in allmods;allmods[m['id']]=(m,root)
  if m.get('modCategoryCollection'):
   jsonschema.validate(m,sch);b=(root/'packages'/m['url'].split('/')[-1]).read_bytes();assert len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256'];d=json.loads(b)
   jsonschema.validate(d,json.loads((content/'schemas/mod-collection-v1.schema.json').read_text()))
   assert set(d)=={'schemaVersion','id','version','type','collectionCategory','members'} and d['members']==m['dependencies'] and d['collectionCategory']==m['collectionCategory'] and 0<len(d['members'])<=50 and m['minClientVersionCode']==10036
   new.append(m)
roots=[m for m,r in allmods.values() if m.get('collectionRole')=='category'];assert len(roots)==15 and len(new)==13
covered=set()
for root in roots:
 seen=set();active=set();leaves=set()
 def visit(pid):
  assert pid in allmods and pid not in active
  if pid in seen:return
  active.add(pid);m,_=allmods[pid]
  for dep in m['dependencies']:visit(dep)
  if m['type']!='collection':leaves.add(pid)
  active.remove(pid);seen.add(pid)
 visit(root['id']);covered.update(leaves)
 if root.get('modCategoryCollection'):
  assert len(leaves)==root['packageCount'] and all(category(allmods[i][0])==root['collectionCategory'] or root['collectionCategory']=='maps' and i=='dnd.appearance.map-surfaces' for i in leaves)
maproot=next(m for m in roots if m.get('collectionCategory')=='maps');assert 'dnd.appearance.map-surfaces' in maproot['dependencies']
assert covered=={i for i,(m,r) in allmods.items() if m['type']!='collection'} and len(covered)==397
if args.public_payloads or args.public:
 def verify(m):
  b=urllib.request.urlopen(m['url'],timeout=45).read();assert len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256']
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(verify,new))
 print('PUBLIC_MOD_COLLECTION_PAYLOADS_PASS:13')
if args.public:
 for url,raw in catalogs:assert urllib.request.urlopen(url,timeout=45).read()==raw
 print('PUBLIC_MOD_COLLECTION_CATALOGS_PASS: Content v3 and Assets v9')
print('ALL_MOD_COLLECTIONS_PASS:15 libraries cover all397 existing mods; all previous catalog entries unchanged')
