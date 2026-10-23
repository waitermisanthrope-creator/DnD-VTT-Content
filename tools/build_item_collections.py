"""Build immutable v2 collections and the next-client catalog; leave v3 intact."""
import copy
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def load(path): return json.loads((ROOT / path).read_text())
def write(path, value):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def main():
    catalog = load('catalog/v3/index.json')
    catalog['packages'] = [m for m in catalog['packages'] if not m.get('collectionVolume') or m['collectionVolume'] == 1]
    packs = {c: load(f'packages/dnd.items.{c}.json') for c in ['weapons', 'armor', 'materials', 'consumables', 'junk']}
    for c, p in packs.items():
        p['version'] = '2.0.0'
        for item in p['items']:
            item['description'] = item.get('description') or item['name']
    def add(c, key, name, weight, desc, **fields):
        packs[c]['items'].append(dict(id=f'dnd.items.{c}.{key}', name=name, weight=weight,
            description=desc, inventoryCategory=c, **fields))
    # Actual base weapon statistics, with material weight and explicit enchantment.
    materials = [('steel','Сталь',1),('iron','Железо',1.1),('bronze','Бронза',1.15),('silver','Посеребрение',1),('mithral','Мифрил',.5)]
    for base in list(packs['weapons']['items']):
        for mat, label, ratio in materials:
            for bonus in range(4):
                item = copy.deepcopy(base)
                item.update(id=f"dnd.items.weapons.forge.{base['id'].split('.')[-1]}.{mat}.{bonus}",
                    name=f"{base['name']} — {label}" + (f' +{bonus}' if bonus else ''),
                    weight=f"{float(str(base['weight']).split()[0]) * ratio:g} фунтов", toHit=bonus,
                    description=f"{base['name']}. Исполнение: {label.lower()}; вес изменён относительно основы. " +
                    (f'Магический бонус атаки +{bonus}; бонус урона указан в формуле.' if bonus else 'Использует параметры базового оружия. Особые свойства учитывает мастер.'))
                if bonus: item['damage'] = base['damage'] + f'+{bonus}'
                packs['weapons']['items'].append(item)
    for base in list(packs['armor']['items']):
        for i, finish in enumerate(['Походное','Зимнее','Парадное','Городское','Дорожное','Морское','Горное','Пустынное','Лесное','Гвардейское','Ремесленное','Ритуальное']):
            item = copy.deepcopy(base)
            item.update(id=f"dnd.items.armor.style.{base['id'].split('.')[-1]}.{i}",name=f"{base['name']} — {finish.lower()} исполнение",
                description=f"{base['name']}. {finish} исполнение с собственной отделкой. Защита и владение как у основы; дополнительных магических эффектов отделка не даёт.")
            item['equipmentSlot'] = 'shield' if 'щит' in base.get('category','').lower() else 'body' if base.get('acBase',0)>0 else 'accessory'
            packs['armor']['items'].append(item)
    for i, garment in enumerate(['Рубаха','Куртка','Плащ','Штаны','Сапоги','Перчатки','Капюшон','Жилет','Мантия','Пояс','Шарф','Туника','Платье','Кафтан','Накидка']):
        for j, textile in enumerate(['Лён','Шерсть','Хлопок','Шёлк','Кожа','Мех','Сукно','Бархат','Парусина','Замша']):
            add('armor',f'clothes.{i}.{j}',f'{garment} — {textile.lower()}',f'{.2+(i%4)*.3:g} кг',
                f'{garment} из материала «{textile.lower()}». Повседневная одежда; не повышает КД.',category='Одежда',acBase=0,proficiencyType='none',equipmentSlot='clothing')
    core = load('packages/dnd.craft.core.json')
    packs['materials']['materials'] = copy.deepcopy(core['materials'])
    for m in core['materials']:
        add('materials','craft.'+m['id'].lower(),m['name'],m['weight'],f"{m['name']}: материал для рецептов ремесленной мастерской.",craftMaterialId=m['id'],category='Ремесленный материал')
    packs['materials']['ingredients'] = []
    for n in range(1,4):
        legacy = load(f'packages/dnd.alchemy.ingredients.{n}.json')
        packs['materials']['ingredients'] += legacy['ingredients']
        for old in legacy['items']:
            item = copy.deepcopy(old)
            item['id'] = 'dnd.items.materials.alchemy.'+old['alchemyId']
            packs['materials']['items'].append(item)
    # Shared parts: no rabbit/wolf/boar-specific item IDs.
    parts = [('heart','Сердце',.3),('blood','Кровь',.25),('bone','Кость',.2),('hide','Шкура',2),('meat','Мясо',.5),('fat','Жир',.25),('eye','Глаз',.02),('tooth','Зуб',.01),('claw','Коготь',.02),('sinew','Сухожилие',.1),('liver','Печень',.4),('gland','Железа',.05),('horn','Рог',.4),('scale','Чешуя',.1),('marrow','Костный мозг',.1),('fur','Мех',.3),('feather','Перо',.01),('venom','Яд',.02)]
    for group, label in [('animal','животного'),('monster','монстра'),('humanoid','гуманоида')]:
        for part, name, weight in parts:
            mid=f'harvest_{group}_{part}'
            add('materials',mid,f'{name} {label}',f'{weight} кг',f'{name} {label}. Общий материал разделки; вид существа не меняет ID. Выход и доступность части определяет таблица добычи.',craftMaterialId=mid,harvestGroup=group,harvestPart=part,category='Материал разделки')
            packs['materials']['materials'].append(dict(id=mid,name=f'{name} {label}',weight=f'{weight} кг',cat='harvest',price=1,rarity='common'))
    for i, resource in enumerate(['Железо','Медь','Олово','Серебро','Золото','Мифрил','Адамантин','Обсидиан','Кварц','Янтарь','Гранит','Мрамор','Малахит','Лазурит','Сера','Соль','Уголь','Глина','Мел','Гипс','Охра','Нефрит','Агат','Гематит','Пирит','Базальт','Слюда','Тальк','Кремень','Селитра']):
        for j, form in enumerate(['Крошка','Порошок','Кусок','Заготовка','Смесь','Паста','Концентрат','Образец']):
            mid=f'resource_{i}_{j}'
            add('materials',mid,f'{resource} — {form.lower()}','0.5 кг',f'{form} материала «{resource.lower()}». Заготовка для будущих рецептов; автоматического рецепта пока нет.',category='Минеральное сырьё',craftMaterialId=mid)
            packs['materials']['materials'].append(dict(id=mid,name=f'{resource} — {form.lower()}',weight='0.5 кг',cat='mineral',price=1,rarity='common'))
    for i, herb in enumerate(['Мята','Шалфей','Ромашка','Полынь','Крапива','Чабрец','Можжевельник','Тысячелистник','Лаванда','Календула','Зверобой','Вереск','Папоротник','Клевер','Подорожник','Дягиль','Валериана','Одуванчик','Лопух','Аир','Солодка','Кипрей','Мелисса','Душица','Пижма']):
        for j, form in enumerate(['Сушёный сбор','Порошок','Настой','Масло','Экстракт','Семена']):
            add('materials',f'herb.{i}.{j}',f'{herb} — {form.lower()}','0.1 кг',f'{form}: {herb.lower()}. Растительное сырьё; свойства и рецепты назначает мастер.',category='Растительное сырьё')
    for item in packs['consumables']['items']:
        item['useMode']='manual'
        item['description'] += ' Применение списывает одну единицу; описанный эффект учитывает мастер.'
    for item, dice in zip(packs['consumables']['items'][:4], ['2d4+2','4d4+4','8d4+8','10d4+20']):
        item['effects'] = [dict(kind='heal',dice=dice)]
        item.pop('useMode',None)
        item['description'] = f"{item['name']}. Восстанавливает {dice} ОЗ броском костей до максимума; расходует одну единицу."
    for i, hp in enumerate([2,4,6,8,10,12,16,20,24,30]):
        for j, form in enumerate(['Микстура','Бальзам','Отвар','Настойка','Эссенция','Эликсир','Пилюля','Сироп','Мазь','Порошок']):
            add('consumables',f'healing.{i}.{j}',f'{form} восстановления ({hp} ОЗ)','0.1 кг',f'При применении восстанавливает {hp} ОЗ, не превышая максимум, и расходует одну единицу.',category='Лечебный расходник',effects=[dict(kind='heal',amount=hp)])
    for i, food in enumerate(['Хлеб','Сухари','Вяленое мясо','Сыр','Сушёные яблоки','Орехи','Каша','Суп','Похлёбка','Лепёшка','Пирог','Сушёная рыба','Мёд','Чай','Вода','Сок','Компот','Пиво','Вино','Молоко']):
        for j, portion in enumerate(['Малая порция','Дорожная порция','Большая порция','Походный запас','Праздничная порция']):
            add('consumables',f'provision.{i}.{j}',f'{food} — {portion.lower()}',f'{.15*(j+1):g} кг',f'{portion}: {food.lower()}. Применение списывает одну единицу. Питание и прочие эффекты учитывает мастер.',category='Провизия',useMode='manual')
    for i, obj in enumerate(['Пуговица','Пряжка','Ключ','Замок','Колокольчик','Подсвечник','Медальон','Фигурка','Бусина','Напёрсток','Гребень','Зеркальце','Кубок','Ложка','Вилка','Тарелка','Чаша','Цепочка','Шестерёнка','Пластина','Печать','Монета','Жетон','Игральная кость','Свисток','Кольцо','Брошь','Рамка','Чернильница','Табличка','Футляр','Шкатулка','Подкова','Гвоздь','Крючок','Катушка','Ручка','Перо для письма','Обломок статуи','Дверная петля']):
        for j, material in enumerate(['Медь','Латунь','Железо','Олово','Дерево','Кость','Керамика','Стекло','Серебро','Камень']):
            add('junk',f'salvage.{i}.{j}',f'{obj} — {material.lower()}','0.05 кг',f'{obj}, материал: {material.lower()}. Бытовая находка или товар для продажи; автоматического игрового эффекта нет.',category='Бытовой хлам')
    # Stable legacy IDs keep their chemistry; displayed body-part names are shared.
    stems = [('сердц','heart'),('кров','blood'),('кост','bone'),('кость','bone'),('шкур','hide'),('мяс','meat'),('жир','fat'),('глаз','eye'),('клык','tooth'),('зуб','tooth'),('ког','claw'),('сухож','sinew'),('печен','liver'),('желез','gland'),('желч','gland'),('рог','horn'),('чешу','scale'),('мех','fur'),('перья','feather'),('перо','feather'),('яд','venom')]
    canonical = {i['craftMaterialId']:i for i in packs['materials']['items'] if 'harvestGroup' in i}
    for item in packs['materials']['items']:
        if 'harvestGroup' in item: continue
        name=item['name'].lower()
        animal=any(x in name for x in ['волк','волч','зая','кабан','сов','ворон','летуч','паук','пауч','скорпион','медвед','зме','лягуш'])
        humanoid=any(x in name for x in ['гуманоид','хобгоблин','гоблин','человек','эльф','дворф'])
        monster=any(x in name for x in ['монстр','дракон','оборот','вампир','василиск','демон','исчад','тролл','кракен'])
        if not (animal or humanoid or monster): continue
        part=next((part for stem,part in stems if stem in name),None)
        if part is None: continue
        group='humanoid' if humanoid else 'animal' if animal else 'monster'
        target=canonical[f'harvest_{group}_{part}']
        item['legacyName']=item['name'];item['name']=target['name']
        if item.get('alchemyId'):
            target.setdefault('alchemyIds',[]).append(item['alchemyId'])
            for profile in packs['materials']['ingredients']:
                if profile['id']==item['alchemyId']: profile['name']=target['name']
        elif item.get('craftMaterialId'):
            target.setdefault('craftMaterialIds',[]).append(item['craftMaterialId'])
        else:
            item['craftMaterialId']=target['craftMaterialId']
    labels={'weapons':'Оружие','armor':'Броня и одежда','materials':'Материалы для крафта и разделки','consumables':'Расходники','junk':'Хлам'}
    for c,p in packs.items():
        path=f'packages/dnd.items.{c}-2.0.0.json'
        write(path,p)
        b=(ROOT/path).read_bytes()
        entry=next(e for e in catalog['packages'] if e['id']==p['id'])
        entry.update(version=p['version'],name=f"Сборник: {labels[c]} ({len(p['items'])})",bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),url='https://raw.githubusercontent.com/waitermisanthrope-creator/DnD-VTT-Content/main/'+path,
            description='Расширенный сборник для нового клиента с каталогом Content v4. Сохранены старые ID. Варианты снаряжения используют базовые характеристики; ручные эффекты помечены в описании.')
    # The materials collection now carries ingredient profiles and inventory records.
    catalog['packages']=[p for p in catalog['packages'] if not p['id'].startswith('dnd.alchemy.ingredients.')]
    write('catalog/v4/index.json',catalog)
    print({c:len(p['items']) for c,p in packs.items()})
if __name__ == '__main__': main()
