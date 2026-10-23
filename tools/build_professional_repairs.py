"""Optional professional tools and linked, inert broken variants.

Do not overwrite a published revision: this 1.0.0 source is frozen on publication.
Repair execution is a future client feature, not executable code in these JSONs.
"""
import collections
import hashlib
import json
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REV='1.0.0'
URL='https://raw.githubusercontent.com/waitermisanthrope-creator/DnD-VTT-Content/main/'
TOOLS={
'smith':('Кузнечное дело','p_tool_smith','''
Кузнечный молот|1.5|steel|forge_hammer|ковать и осаживать нагретую металлическую заготовку|8
Кузнечный молот с поперечным бойком|1.3|steel|cross_peen|вытягивать металл поперечным бойком|9
Кузнечная наковальня|25|iron|anvil|поддерживать заготовку при ковке|50
Кузнечные клещи|1.1|iron|forge_tongs|удерживать горячую заготовку|3
Кузнечная кочерга|1.2|iron|forge_poker|распределять уголь в горне|2
Закалочная ванна малая|4|iron|quench_bath|погружать заготовку в подходящую закалочную среду|8
Кузнечный вороток|0.6|steel|twist_bar|скручивать нагретую полосу металла|5
Правильная плита кузнеца|5|iron|straightening_plate|проверять и править плоскость поковки|12
'''),
'leatherwork':('Кожевенное дело','p_tool_leatherworker','''
Нож для мездрения шкур|0.5|steel|fleshing_knife|снимать мездру двуручным тянущим резом на колоде|5
Колодка мездрильная|5|wood|fleshing_beam|подпирать шкуру при мездрении|3
Нож для шерфования кожи|0.12|steel|skiving_knife|утончать край кожи перед соединением|3
Кромкорез кожевника|0.09|steel|edge_beveler|снимать фаску с края ремня|2
Гладилка для уреза кожи|0.1|wood|edge_burnisher|заглаживать урез обработанной кожи|1
Седельный зажим|1.2|wood|stitching_clamp|удерживать кожаные детали при ручном шитье|4
Скребок мездрильный|0.3|steel|fleshing_scraper|соскабливать остатки ткани со шкуры|2
Шило|0.05|steel|leather_awl|прокалывать кожу под шов|1
'''),
'alchemy':('Алхимия','p_tool_alchemist','''
Пустой алхимический сосуд|0.2|glass|empty_vessel|принимать до 250 мл вещества; содержимое добавляется отдельно|2
Пустая алхимическая колба|0.25|glass|empty_flask|удерживать до 500 мл смеси в ручной работе|3
Пустая узкогорлая склянка|0.08|glass|empty_vial|хранить до 50 мл отдельного образца|1
Пустой флакон с притёртой пробкой|0.12|glass|stoppered_bottle|закрывать до 100 мл отдельного образца|2
Термостойкая алхимическая чашка|0.15|ceramic|evaporating_dish|выпаривать небольшую порцию раствора|2
Стеклянная мешалка алхимика|0.03|glass|stirring_rod|перемешивать совместимый состав вручную|1
Тигель графитовый|0.6|graphite|crucible|удерживать вещество при подходящем нагреве|4
Штатив для алхимических сосудов|0.8|iron|retort_stand|закреплять подходящую посуду при работе|6
'''),
'jeweler':('Ювелирное дело','p_tool_jeweler','''
Ювелирный молоток|0.12|steel|jeweler_hammer|наносить точные небольшие удары по металлу|4
Ригель для колец|0.35|steel|ring_mandrel|формовать и проверять кольцо|5
Ювелирный надфиль|0.03|steel|needle_file|опиливать мелкие детали|2
Пинцет ювелира|0.025|steel|fine_tweezers|удерживать маленький камень или деталь|2
Штихель ювелира|0.04|steel|engraver|прорезать тонкую линию на металле|3
Гладилка для закрепки камней|0.06|steel|stone_burnisher|заглаживать металл оправы вокруг камня|3
'''),
'woodwork':('Столярное дело','p_tool_carpenter','''
Тесло плотника|0.8|steel|adze|стёсывать поверхность древесины поперечным лезвием|4
Полукруглая стамеска|0.16|steel|gouge|выбирать округлые углубления в древесине|2
Ручная дрель с маховичком|0.5|steel|hand_drill|вращать небольшое сверло вручную|5
Шаблон для шипового соединения|0.12|wood|joint_template|размечать сопрягаемые элементы деревянного соединения|1
Доска для изготовления шкантов|0.4|steel|dowel_plate|калибровать небольшие деревянные шканты|3
Стамеска|0.18|steel|chisel|выбирать древесину плоским лезвием|2
'''),
'weaver':('Ткачество и пошив','p_tool_weaver','''
Ткацкое бердо|0.5|wood|weaving_reed|уплотнять уточную нить на ручном станке|3
Навой ручного станка|1.8|wood|warp_beam|удерживать намотанную основу ткани|4
Шпуля ткацкая|0.04|wood|weaving_bobbin|хранить рабочую нить для челнока|0.2
Ручная чесалка для шерсти|0.25|iron|wool_carder|подготавливать шерсть к прядению|2
Ножницы закройщика|0.3|steel|cutting_shears|кроить несколько слоёв подходящей ткани|4
Веретено|0.08|wood|spindle|скручивать подготовленное волокно в нить|0.5
'''),
'glasswork':('Стеклодувное дело','p_tool_glassblower','''
Стеклодувная трубка|1.2|iron|blowpipe|набирать и выдувать нагретое стекло|8
Понтия стеклодува|0.8|iron|punty|поддерживать стеклянное изделие при формовании|5
Ножницы стеклодува|0.35|steel|glass_shears|подрезать мягкую нагретую стеклянную массу|5
Щипцы стеклодува|0.4|steel|glass_jacks|формовать нагретое стекло щипцами|5
Мокрая формовочная колодка|0.5|wood|glass_block|обкатывать нагретую стеклянную заготовку при ручной работе|2
Форма для стеклянного флакона|0.7|wood|bottle_mold|задавать наружную форму флакона|4
'''),
'pottery':('Гончарное дело','p_tool_potter','''
Гончарный круг ручной|12|wood|potter_wheel|вращать заготовку при ручном формовании|15
Гончарный стек|0.03|wood|modeling_tool|формовать глину небольшим рабочим концом|0.5
Гончарная струна|0.02|copper|clay_wire|отрезать заготовку от глиняной массы|0.5
Петля для обточки глины|0.04|steel|trimming_loop|снимать излишек подсохшей глины|1
Гончарная почка|0.05|wood|potter_rib|заглаживать форму глиняного сосуда|0.5
Полка для обжиговой печи|2|ceramic|kiln_shelf|поддерживать изделия при подходящем обжиге|3
'''),
'maintenance':('Заточка и обслуживание',None,'''
Точильный камень|0.6|stone|whetstone|править режущую кромку без восстановления утраченного металла|1
Оселок мелкозернистый|0.2|stone|fine_hone|тонко доводить подходящую режущую кромку|2
Ремень для правки лезвий|0.15|leather|razor_strop|править подходящее лезвие на кожаном ремне|1
Ручной точильный круг|4|stone|grinding_wheel|затачивать инструмент при ручном вращении|8
Пустая маслёнка для инструмента|0.08|copper|empty_oiler|дозировать масло после отдельного заполнения|1
Ёрш для чистки ствола|0.12|bristle|barrel_brush|чистить подходящий разряженный ствол вручную|1
Ручные тиски|0.6|iron|hand_vise|зажимать небольшую деталь при ремонте|4
Полировальная колодка|0.15|wood|polishing_block|поддерживать абразивную ткань при полировании|0.5
''')}
CAPACITY={'Пустой алхимический сосуд':250,'Пустая алхимическая колба':500,'Пустая узкогорлая склянка':50,'Пустой флакон с притёртой пробкой':100,'Пустая маслёнка для инструмента':50}
ALREADY_DAMAGED=['сломан','тресну','разбит','рван','ржав','обрыв','облом','оскол','фрагмент','половина','неполная','без язычка','без застёжки']
NATURAL_TRINKETS=['засушенный цветок','сухой лист','зуб животного','кость животного']
def read(p):return json.loads((ROOT/p).read_text())
def write(p,d):
 raw=(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode()
 if p.startswith('packages/'):
  previous=subprocess.run(['git','show','HEAD:'+p],cwd=ROOT,capture_output=True)
  if previous.returncode==0 and previous.stdout!=raw:raise RuntimeError('Immutable tracked payload would change; create a new revision: '+p)
 path=ROOT/p;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
def stable(value):return hashlib.sha256(value.encode()).hexdigest()[:16]
def main():
 catalog=read('catalog/v3/index.json');catalog['packages']=[m for m in catalog['packages'] if m.get('professionalRepairRevision')!=REV]
 baseline=[]
 for m in catalog['packages']:
  if m['type'] in ['item','craft']:
   baseline.extend((i,m) for i in read('packages/'+m['url'].split('/')[-1]).get('items',[]))
 by_name={i['name']:(i,m) for i,m in baseline};added=[];manifests=[];professional_index=[];tool_lookup={};reused=[]
 def publish(pid,label,items,kind):
  p=dict(schemaVersion=1,id=pid,version=REV,type='item',items=items);path=f'packages/{pid}-{REV}.json';write(path,p);b=(ROOT/path).read_bytes()
  m=dict(schemaVersion=1,id=pid,name=label,version=REV,author='DnD-VTT contributors',license='CC0-1.0 (project original loot metadata)',type='item',format='json',platform='any',unityVersion='*',dependencies=[],bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),url=URL+path,minClientVersionCode=10034,professionalRepairRevision=REV,professionalRepairKind=kind,description='Опциональный сборник профессиональных инструментов.' if kind=='tools' else 'Сломанные вещи без экипировки и эффектов. Связь с исправным предметом и условия будущего ремонта/Починки сохранены в данных; автоматический ремонт ещё не реализован.')
  catalog['packages'].append(m);manifests.append(m);return m
 for profession,(label,proficiency,rows) in TOOLS.items():
  items=[];pid=f'dnd.items.professional.{profession}.junk'
  for row in rows.strip().splitlines():
   name,w,material,role,use,price=row.split('|')
   tool=dict(schemaVersion=1,professionId=profession,associatedProficiencyId=proficiency,role=role,operations=[use],execution='manual',grantsProficiency=False,requiresServiceableTool=True)
   if name in by_name:
    i,m=by_name[name];reused.append(i['id'])
   else:
    i=dict(id=pid+'.'+role,name=name,inventoryCategory='junk',category='Профессиональный инструмент: '+label,weight=f'{float(w):g} кг',cost=f'{float(price):g} зм',description=f'{name}. Профиль: {label.lower()}. Назначение: {use}. Профессиональное применение разрешается мастером; инструмент не выдаёт владение или автоматический бонус.',professionalTool=tool,itemTraits=dict(schemaVersion=1,materialTags=[material],lootTags=['profession.'+profession],uses=[dict(action=role,execution='manual',text=use)],stateDefaults=dict(condition='intact'),trade=dict(basePriceGp=float(price),merchantTags=[profession]),processing=dict(execution='planned',materialTags=[material],recipeTags=['tool.'+profession])))
    if name in CAPACITY:i['containerSpec']=dict(capacityMl=CAPACITY[name],initialContents=[],execution='planned');i['description']+=' Сосуд пуст; вещества и жидкости в комплект не входят. Автоматическое наполнение пока не реализовано.'
    items.append(i);added.append(i)
   professional_index.append(dict(itemId=i['id'],name=name,professionalTool=tool));tool_lookup[i['id']]=tool
  if items:
   m=publish(pid,f'Сборник: Профессиональные инструменты — {label}',items,'tools');baseline.extend((i,m) for i in items)
 selected=[];excluded=collections.Counter();excluded_records=[]
 for i,m in baseline:
  name=i['name'].casefold();reason=None
  if i.get('brokenVariantOf') or 'сломано' in name:reason='already_broken_variant'
  elif i['inventoryCategory'] not in ['weapons','armor','junk']:reason='consumable_or_raw_material'
  elif any(s in name for s in ALREADY_DAMAGED):reason='already_damaged_or_incomplete'
  elif any(s in name for s in NATURAL_TRINKETS):reason='natural_nonmanufactured_remains'
  if reason:excluded[reason]+=1;excluded_records.append(dict(id=i['id'],reason=reason));continue
  selected.append((i,m))
 assert len({i['id'] for i,m in selected})==len(selected)
 selected.sort(key=lambda pair:pair[0]['id'])
 mapping=[];broken=[]
 for page_no,start in enumerate(range(0,len(selected),100),1):
  pid=f'dnd.items.broken.volume{page_no:02}.junk';out=[]
  for target,source in selected[start:start+100]:
   bid=pid+'.'+stable(target['id']);name=target['name']+' — сломано'
   material=(target.get('itemTraits',{}).get('materialTags') or ['unknown_or_mixed'])
   profession=tool_lookup.get(target['id'],target.get('professionalTool',{})).get('professionId')
   repair_professions=sorted({{'steel':'smith','iron':'smith','copper':'smith','brass':'smith','wood':'woodwork','bamboo':'woodwork','glass':'glasswork','ceramic':'pottery','leather':'leatherwork','linen':'weaver','wool':'weaver','cotton':'weaver','paper':'scribe'}[x] for x in material if x in ['steel','iron','copper','brass','wood','bamboo','glass','ceramic','leather','linen','wool','cotton','paper']})
   tear=any(x in material for x in ['leather','linen','wool','cotton','paper']) or any(x in target['name'].casefold() for x in ['письмо','карта','плащ','мантия','сеть','лассо','свиток'])
   repair=dict(schemaVersion=1,execution='planned',target=dict(itemId=target['id'],packageId=source['id'],packageVersion=source['version'],packageSha256=source['sha256'],packageUrl=source['url']),damage=dict(kind='single_tear' if tear else 'single_break',breakCount=1,maxBreakDimensionFt=1,allOriginalPiecesPresent=True,missingMaterial=False),craft=dict(recipeStatus='planned',professionIds=repair_professions,toolUseProfessionIds=[profession] if profession else [],materialTags=material,requiresServiceableTools=True),mending=dict(eligibleForDeclaredDamage=True,castingMinutes=1,maxBreakDimensionFt=1,requiresAllOriginalPieces=True,replacesMissingMaterial=False,restoresMagic=False,restoresCharges=False),preserveInstanceState=['owner','provenance','craftQuality','remainingCharges','magicState'],restoreOnlyPhysicalCondition=True,preserveUnknownInstanceFields=True)
   price=target.get('itemTraits',{}).get('trade',{}).get('basePriceGp')
   b=dict(id=bid,name=name,inventoryCategory='junk',category='Сломанные вещи',weight=target['weight'],cost='Оценивает мастер',description=f'Сломанный вариант предмета «{target["name"]}». Один излом или разрыв до 1 фута; исходные части сохранены. Не используется как исправное снаряжение, инструмент или расходник. Подготовлены ссылки для будущего ремонта ремеслом и «Починкой». Утраченные материалы, магия и заряды таким ремонтом не восстанавливаются.',brokenVariantOf=target['id'],condition='broken',repairProfile=repair,itemTraits=dict(schemaVersion=1,materialTags=material,lootTags=['broken',target['inventoryCategory']],uses=[dict(action='repair_candidate',execution='manual',text='передать мастеру для разрешения ремонта')],stateDefaults=dict(condition='broken'),trade=dict(basePriceGp=0,priceStatus='unappraised',merchantTags=['repairer','salvage']),processing=dict(execution='planned',materialTags=material,recipeTags=['repair'])))
   out.append(b);broken.append(b);mapping.append(dict(brokenItemId=bid,brokenPackageId=pid,targetItemId=target['id'],targetPackageId=source['id']))
  publish(pid,f'Сборник: Сломанные вещи — том {page_no:02}/{(len(selected)+99)//100:02}',out,'broken')
 write('catalog/v3/index.json',catalog)
 write('sources/professional-tools-1.0.0.json',dict(schemaVersion=1,revision=REV,newToolCount=len(added),reusedToolCount=len(reused),tools=professional_index))
 write('sources/repair-links-1.0.0.json',dict(schemaVersion=1,revision=REV,brokenCount=len(broken),packages=[m['id'] for m in manifests],links=mapping,excludedCounts=dict(excluded),excluded=excluded_records))
 print('New professional tools:',len(added),'reused:',len(reused),'broken variants:',len(broken),'packages:',len(manifests),'excluded:',dict(excluded))
if __name__=='__main__':main()
