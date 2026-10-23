"""Publish optional <=100-entry item volumes compatible with Unity 1.00.34.

Source v2 packs remain immutable. Revisions use separate URLs. v1/v2 catalogs
are never touched. The new volumes have no dependencies or automatic installs.
"""
import copy
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
BASE_URL = 'https://raw.githubusercontent.com/waitermisanthrope-creator/DnD-VTT-Content/main/'
CATEGORIES = ['weapons','armor','materials','consumables','junk']
LABELS = dict(zip(CATEGORIES,['Оружие','Броня и одежда','Материалы для крафта','Расходники','Хлам']))

def load(path): return json.loads((ROOT/path).read_text())
def write(path, data):
    p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def additions():
    out={c:[] for c in CATEGORIES}
    def add(c,key,name,weight,description,**fields):
        out[c].append(dict(id=f'dnd.items.{c}.expanded.{key}',name=name,weight=f'{weight} кг',description=description,inventoryCategory=c,**fields))
    weapons=[('Фальката','1d8','рубящий',1.3),('Копис','1d6','рубящий',1),('Кхопеш','1d8','рубящий',1.6),('Махайра','1d6','рубящий',1.1),('Сакс','1d6','колющий',.8),('Мессер','1d8','рубящий',1.2),('Эсток','1d8','колющий',1.4),('Пата','1d8','колющий',1.5),('Катар','1d6','колющий',.7),('Джамбия','1d4','колющий',.4),('Крис','1d4','колющий',.5),('Фламберг','2d6','рубящий',3.2),('Нагината','1d10','рубящий',2.5),('Гуаньдао','1d10','рубящий',3),('Совня','1d10','рубящий',2.7),('Рогатина','1d8','колющий',2),('Бек-де-корбен','1d10','колющий',2.8),('Чекан','1d8','колющий',1.5),('Шестопёр','1d8','дробящий',1.7),('Тонфа','1d6','дробящий',.8)]
    for n,(name,dmg,typ,w) in enumerate(weapons):
        two=n in [11,12,13,14,15,16]
        add('weapons',str(n),name,w,f'{name}: авторская игровая трактовка исторического оружия. Урон {dmg}, {typ}. '+('Двуручное.' if two else 'Одноручное.')+' Специальная боевая автоматика не добавляется пакетом.',category='Воинское рукопашное (хоумбрю)',groupKey='martial',typeKey='melee',hands='2 руки' if two else '1 рука',damage=dmg,damageType=typ,properties=['Двуручное'] if two else [],proficiencies=['p_weapon_martial'],toHit=0)
    clothes=[('Фартук кузнеца',1),('Роба писца',.7),('Камзол картографа',.8),('Куртка егеря',1.2),('Балахон послушника',.9),('Плащ караванщика',1.4),('Капюшон следопыта',.2),('Жилет рыбака',.6),('Перчатки стеклодува',.3),('Шляпа странника',.2),('Маска пылезащитная',.1),('Нарукавники ремесленника',.3),('Гетры болотника',.4),('Портянки походные',.1),('Чулки шерстяные',.1),('Пелерина лекаря',.5),('Платок пустынника',.2),('Передник травника',.4),('Парадная перевязь',.2),('Шахтёрский подшлемник',.3)]
    for n,(name,w) in enumerate(clothes):add('armor',str(n),name,w,f'{name}. Одежда для путешествий и ремесла, без бонуса к КД и без скрытых бонусов навыков.',category='Одежда',acBase=0,proficiencyType='none',equipmentSlot='clothing')
    mats=[('Пчелиный воск',.1),('Сосновая канифоль',.1),('Берёзовый дёготь',.2),('Костяной клей',.2),('Рыбий клей',.2),('Льняная пакля',.1),('Конопляное волокно',.1),('Дубильный экстракт',.2),('Поташ',.2),('Жидкое стекло',.2),('Пемза',.2),('Абразивный корунд',.2),('Полировальная паста',.1),('Лаковая смола',.1),('Краситель индиго',.05),('Краситель марены',.05),('Писчая сажа',.05),('Камедь акации',.1),('Железистые галлы',.1),('Шеллачные хлопья',.1)]
    for n,(name,w) in enumerate(mats):add('materials',str(n),name,w,f'{name}. Ремесленное сырьё; рецепты и выход задаёт мастер. У этого нового материала пока нет автоматического рецепта.',category='Ремесленное сырьё',craftMaterialId=f'workshop_supply_{n:02}')
    supplies=[('Свеча восковая',.05),('Факел смоляной',.5),('Благовоние храмовое',.02),('Мыло дорожное',.1),('Мел разметочный',.01),('Чернила писчие',.05),('Бумага писчая',.01),('Пергаментный лист',.01),('Бинт льняной',.03),('Компресс чистый',.05),('Порция лампового масла',.2),('Пакет соли',.1),('Пакет пряностей',.05),('Корм для лошади',2),('Сухой паёк на день',1),('Табак трубочный',.05),('Порошок для чистки оружия',.05),('Воск для тетивы',.02),('Смола для ремонта',.1),('Уголь для рисования',.02)]
    for n,(name,w) in enumerate(supplies):add('consumables',str(n),name,w,f'{name}. Одно применение списывает единицу запаса. Освещение, уход, лечение, питание и прочие эффекты учитывает мастер.',category='Походный расходник',effects=[],useMode='manual')
    trinkets=['Письмо без адресата','Карта затопленного подвала','Сломанная печать гильдии','Пустой флакон духов','Обрывок морского флага','Треснувшая маска актёра','Половина медного жетона','Детская деревянная лошадка','Потёртая счётная дощечка','Ржавый дверной номер','Кожаный футляр без застёжки','Керамический грузик','Потерянная серьга без камня','Засохшая сургучная печать','Старая театральная афиша','Рваный кошелёк','Кусочек витража','Сломанный камертон','Неполная колода карт','Глиняная свистулька без язычка']
    for n,name in enumerate(trinkets):add('junk',str(n),name,.05,f'{name}. Бытовая находка для продажи или сюжетной зацепки. Автоматического эффекта нет.',category='Находки и безделушки')
    return out

def build():
    catalog=load('catalog/v3/index.json')
    # Idempotent regeneration keeps original non-volume entries untouched.
    catalog['packages']=[m for m in catalog['packages'] if not m.get('collectionVolume') or m['collectionVolume']==1]
    templates={c:copy.deepcopy(next(m for m in catalog['packages'] if m['id']==f'dnd.items.{c}')) for c in CATEGORIES}
    extra=additions();published=[];mapping=[]
    for c in CATEGORIES:
        source=load(f'packages/dnd.items.{c}-2.0.0.json')
        # Existing ingredient packs already expose these 120 inventory entries on v3.
        items=[copy.deepcopy(i) for i in source['items'] if not i.get('alchemyId')]+extra[c]
        for item in items:
            if c=='consumables':
                if item.get('effects') and all('amount' in e and e['kind']=='heal' for e in item['effects']):
                    # Old trusted UseProduct heals round(potency/20)+potency/20.
                    hp=item['effects'][0]['amount'];assert hp%2==0
                    item['potency']=hp*10
                else:
                    # Empty effects is the supported stock-spending/manual-use path.
                    item['effects']=[];item['useMode']='manual'
                    item['description']=item.get('effect',item['description'])+' Применение списывает одну единицу; эффект учитывает мастер.'
        pages=[items[i:i+100] for i in range(0,len(items),100)]
        for page_no,page in enumerate(pages,1):
            package_id=f'dnd.items.{c}' if page_no==1 else f'dnd.items.volume{page_no:02}.{c}'
            for item in page:
                original=item['id']
                if page_no>1:
                    item['id']=package_id+'.'+original.removeprefix(f'dnd.items.{c}.')
                mapping.append(dict(sourceId=original,publishedId=item['id'],packageId=package_id))
            payload=dict(schemaVersion=1,id=package_id,version='1.1.0',type='item',items=page)
            path=f'packages/{package_id}-1.1.0.json';write(path,payload)
            raw=(ROOT/path).read_bytes();manifest=copy.deepcopy(templates[c])
            manifest.update(id=package_id,version='1.1.0',name=f'Сборник: {LABELS[c]} — том {page_no:02}/{len(pages):02}',
                description=f'Необязательный самостоятельный том: {len(page)} предметов. Вес и описание у каждого. Совместим с Unity1.00.34; установите только нужные тома. Для поиска всех предметов используйте строку поиска справочника. '+('Расходники с ручными эффектами списываются кнопкой применения.' if c=='consumables' else 'Особые свойства разрешает мастер.'),
                type='item',dependencies=[],bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),url=BASE_URL+path,collectionSeries=c,collectionVolume=page_no,collectionVolumeCount=len(pages),minClientVersionCode=10034)
            if page_no==1:
                idx=next(n for n,m in enumerate(catalog['packages']) if m['id']==package_id);catalog['packages'][idx]=manifest
            else:catalog['packages'].append(manifest)
            published.append(manifest)
    write('catalog/v3/index.json',catalog)
    write('sources/workshop-volumes-1.1.0.json',dict(schemaVersion=1,clientSource='e99d922aeab38dde49ba4268a1db8a895a4f053e',packages=[p['id'] for p in published],itemCount=len(mapping),items=mapping))
    print({c:sum(1 for m in published if m['collectionSeries']==c) for c in CATEGORIES},'items:',len(mapping))
if __name__=='__main__':build()
