"""Build optional libraries for every non-item mod in Content v3 and Assets v9."""
import argparse,hashlib,json,subprocess
from pathlib import Path
CONTENT=Path(__file__).resolve().parents[1]
GROUPS={'races':'Расы','classes':'Классы','feats':'Черты','icons':'Иконки','wallpapers':'Обои','dice':'Дайсы и 3D-наборы','dice-trays':'Лотки и башни для дайсов','maps':'3D-карты','models':'3D-объекты','surfaces':'Материалы поверхностей'}
def write(root,path,data):
 raw=(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode()
 if path.startswith('packages/'):
  old=subprocess.run(['git','show','HEAD:'+path],cwd=root,capture_output=True)
  if old.returncode==0 and old.stdout!=raw:raise RuntimeError('Immutable payload needs a new version: '+path)
 (root/path).parent.mkdir(parents=True,exist_ok=True);(root/path).write_bytes(raw)
def category(m):
 t=m['type']
 if t in ('race','class','feat'):return {'race':'races','class':'classes','feat':'feats'}[t]
 if t=='map':return 'maps'
 if t=='model':return 'models'
 if t=='appearance':return {'icon':'icons','wallpaper':'wallpapers','dice':'dice','dice-tray':'dice-trays'}.get(m.get('imageKind'),'surfaces')
 return None
def main():
 p=argparse.ArgumentParser();p.add_argument('--assets',type=Path,required=True);args=p.parse_args()
 for root,repo,version,key in [(CONTENT,'Content','v3','packages'),(args.assets,'Assets','v9','packs')]:
  path='catalog/'+version+'/index.json';catalog=json.loads((root/path).read_text());catalog[key]=[m for m in catalog[key] if not m.get('modCategoryCollection')]
  groups={}
  for m in catalog[key]:
   c=category(m)
   if c:groups.setdefault(c,[]).append(m['id'])
   elif m['type'] not in ('item','craft','collection'):raise ValueError('Uncovered mod: '+m['id'])
  def pack(pid,c,members,role,count):
   revision='1.0.1' if c=='maps' else '1.0.0'
   payload=dict(schemaVersion=1,id=pid,version=revision,type='collection',collectionCategory=c,members=members)
   rel=f'packages/{pid}-{revision}.json';write(root,rel,payload);b=(root/rel).read_bytes()
   manifest=dict(schemaVersion=1,id=pid,name=('Полный сборник: ' if role=='category' else 'Часть сборника: ')+GROUPS[c]+(' / '+pid.rsplit('.',1)[-1] if role=='internal' else ''),version=revision,type='collection',author='DnD-VTT contributors',license='CC0-1.0 (collection metadata only; member licenses unchanged)',format='json',platform='any',unityVersion='*',dependencies=members,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),url=f'https://raw.githubusercontent.com/waitermisanthrope-creator/DnD-VTT-{repo}/main/{rel}',minClientVersionCode=10036,collectionCategory=c,collectionRole=role,modCategoryCollection=True,packageCount=count,description='Все доступные дополнения категории «'+GROUPS[c]+'» одной кнопкой. Установленные проверенные версии пропускаются; прерванную загрузку можно продолжить. Требуется Unity1.00.36+. Лицензии исходных модов сохраняются.')
   catalog[key].append(manifest);return pid
  for c in GROUPS:
   if c not in groups:continue
   members=groups[c]
   if len(members)>50:members=[pack(f'dnd.collections.{c}.part{i//50+1:02}',c,members[i:i+50],'internal',len(members[i:i+50])) for i in range(0,len(members),50)]
   if c=='maps':members=members+['dnd.appearance.map-surfaces']
   pack('dnd.collections.'+c,c,members,'category',len(groups[c])+(1 if c=='maps' else 0))
  write(root,path,catalog);write(root,'sources/mod-category-collections-1.0.0.json',dict(schemaVersion=1,minClientVersionCode=10036,categories=groups))
  print(repo,{c:len(m) for c,m in groups.items()})
if __name__=='__main__':main()
