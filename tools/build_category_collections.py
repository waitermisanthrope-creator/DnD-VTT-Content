"""Five one-click categories, retaining existing payloads and IDs. Requires client 10035."""
import collections
import hashlib
import json
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
VERSION='1.0.0'
LABELS={'weapons':'Оружие','armor':'Броня и одежда','materials':'Материалы для крафта и алхимии','consumables':'Расходники','junk':'Хлам, инструменты и сломанные вещи'}
def read(p):return json.loads((ROOT/p).read_text())
def write(p,d):
 raw=(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode()
 if p.startswith('packages/'):
  previous=subprocess.run(['git','show','HEAD:'+p],cwd=ROOT,capture_output=True)
  if previous.returncode==0 and previous.stdout!=raw:raise RuntimeError('New immutable revision required: '+p)
 target=ROOT/p;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
def main():
 catalog=read('catalog/v3/index.json');previous={m['id']:m for m in catalog['packages']};catalog['packages']=[m for m in catalog['packages'] if not m.get('itemCategoryCollection')]
 members={c:[] for c in LABELS};counts=collections.Counter()
 for m in catalog['packages']:
  if m['type'] not in ['item','craft']:continue
  p=read('packages/'+m['url'].split('/')[-1]);cats={i['inventoryCategory'] for i in p.get('items',[])}
  if m['type']=='craft':cats.add('materials')
  for cat in cats:members[cat].append(m['id'])
  for i in p.get('items',[]):counts[i['inventoryCategory']]+=1
 def pack(pid,cat,children,role):
  payload=dict(schemaVersion=1,id=pid,version=VERSION,type='collection',inventoryCategory=cat,members=children)
  path=f'packages/{pid}-{VERSION}.json';write(path,payload);b=(ROOT/path).read_bytes()
  manifest=dict(schemaVersion=1,id=pid,name=('Полный сборник: '+LABELS[cat]) if role=='category' else 'Часть сборника: '+LABELS[cat]+' / '+pid.rsplit('.',1)[-1],version=VERSION,type='collection',author='DnD-VTT contributors',license='CC0-1.0 (project collection metadata)',format='json',platform='any',unityVersion='*',dependencies=children,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),url='https://raw.githubusercontent.com/waitermisanthrope-creator/DnD-VTT-Content/main/'+path,minClientVersionCode=10035,inventoryCategory=cat,itemCategoryCollection=True,collectionRole=role,itemCount=counts[cat] if role=='category' else 0,description=f'Все предметы категории «{LABELS[cat]}» одной кнопкой. Клиент сам установит недостающие тома, уже проверенные пропустит. Требуется Unity1.00.35+. Старые ID и предметы персонажей сохраняются.' if role=='category' else 'Внутренняя группа загрузки; устанавливается автоматически полным сборником.')
  manifest.update({k:previous[pid][k] for k in ('publishedAt','updatedAt') if pid in previous and k in previous[pid]})
  catalog['packages'].append(manifest);return pid
 for cat in LABELS:
  parts=members[cat]
  if len(parts)>50:
   parts=[pack(f'dnd.collections.{cat}.part{n//50+1:02}',cat,parts[n:n+50],'internal') for n in range(0,len(parts),50)]
  pack('dnd.collections.'+cat,cat,parts,'category')
 write('catalog/v3/index.json',catalog)
 write('sources/item-category-collections-1.0.0.json',dict(schemaVersion=1,minClientVersionCode=10035,roots=['dnd.collections.'+c for c in LABELS],categories={c:dict(itemCount=counts[c],packages=members[c]) for c in LABELS}))
 print('Collections:',dict(counts),'leaf packages:',{c:len(members[c]) for c in LABELS})
if __name__=='__main__':main()
