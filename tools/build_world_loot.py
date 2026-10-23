"""Original everyday loot and generic anatomy; data-only Unity 1.00.34 packs.

Names determine stable household resource keys; anatomy uses canonical part IDs.
Published payloads are immutable. Add a new revision rather than overwriting.
"""
import copy
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
URL='https://raw.githubusercontent.com/waitermisanthrope-creator/DnD-VTT-Content/main/'
REVISION='1.0.0'
GROUPS={
'kitchen':('Кухня','junk','kitchen','cook', '''
Нож для масла|0.06|steel|намазывать масло и резать мягкую пищу
Поварской нож|0.22|steel|шинковать продукты и разделывать пищу
Хлебный нож|0.18|steel|резать хлеб зубчатым лезвием
Кухонный тесак|0.7|steel|рубить пищевые заготовки
Мясницкий нож|0.3|steel|отделять мясо от костей
Нож для снятия шкуры|0.16|steel|снимать шкуру при ручной разделке
Скалка|0.45|wood|раскатывать тесто
Чугунная сковорода|2|iron|жарить пищу и удерживать жар
Деревянная ложка|0.04|wood|есть и перемешивать пищу
Половник|0.15|copper|разливать суп и отмерять жидкость
Дуршлаг|0.3|copper|отделять твёрдые продукты от жидкости
Кухонное сито|0.2|wood|просеивать муку
Тёрка|0.18|steel|измельчать пищевые продукты
Щипцы для углей|0.4|iron|перекладывать горячие угли
Разделочная доска|0.8|wood|подкладывать под продукты при нарезке
Глиняная жаровня|1.8|ceramic|готовить на углях
Горшок для тушения|1.2|ceramic|тушить пищу на слабом огне
Маслобойка|2.5|wood|взбивать сливки ручной работой
Пресс для сыра|3|wood|отжимать сырную массу
Мерный ковшик|0.12|copper|отмерять жидкие ингредиенты
'''),
'smithy':('Кузница','junk','smithy','smith','''
Кузнечные клещи|1.1|iron|удерживать раскалённую заготовку
Кузнечная бородка|0.35|steel|пробивать отверстия в горячем металле
Подбойный молоток|0.8|steel|осаживать и выравнивать металл
Кузнечная гладилка|0.7|steel|выравнивать поверхность поковки
Обжимка для заклёпок|0.4|steel|формовать головки заклёпок
Кузнечный зубильник|0.6|steel|надрубать металлическую заготовку
Напильник плоский|0.25|steel|опиливать плоские поверхности
Напильник круглый|0.18|steel|расширять круглые отверстия
Рашпиль|0.22|steel|грубо обрабатывать мягкие материалы
Кузнечный мех малый|2.4|leather|нагнетать воздух в горн
Пробойник для листа|0.3|steel|пробивать тонкий металлический лист
Литейная ложка|0.9|iron|переносить небольшую порцию расплава
Тигель графитовый|0.6|graphite|удерживать металл при плавке
Форма для пряжки|0.5|stone|отливать небольшую пряжку
Волочильная доска|0.7|steel|вытягивать проволоку через отверстия
Кузнечный шаблон|0.2|iron|проверять форму изделия
'''),
'healer':('Лекарь и разделка','junk','healer','healer','''
Пинцет|0.03|steel|захватывать небольшие предметы
Хирургический скальпель|0.04|steel|делать тонкие разрезы при ручной работе
Зонд лекаря|0.02|steel|осматривать небольшие полости
Костная пила|0.4|steel|перепиливать кость при ручной разделке
Игла для шва|0.005|steel|накладывать шов нитью
Зажим лекаря|0.06|steel|пережимать ткань при ручной работе
Ложечка для мази|0.02|bone|отбирать мазь из сосуда
Лекарская лопаточка|0.03|wood|смешивать и наносить мазь
Чаша для промывания|0.25|ceramic|удерживать воду при промывании
Шина деревянная|0.25|wood|фиксировать повреждённую конечность вручную
Лекарская воронка|0.04|glass|переливать жидкость в узкий сосуд
Ланцет|0.03|steel|делать небольшой разрез
Крючок для ткани|0.02|steel|удерживать край ткани при разделке
Банка для образцов|0.15|glass|хранить один образец с ручной маркировкой
Доска для разделки органов|1|wood|выкладывать и сортировать органы
Футляр лекарских инструментов|0.2|leather|переносить небольшой комплект инструментов
'''),
'scribe':('Писец и картограф','junk','study','scribe','''
Перо гусиное писчее|0.005|feather|писать чернилами
Перо тростниковое|0.008|reed|наносить широкие чернильные штрихи
Писчий нож|0.04|steel|очинять перья и подрезать листы
Песочница писца|0.1|ceramic|посыпать свежие чернила сухим песком
Линейка чертёжная|0.1|wood|проводить прямые линии
Циркуль картографа|0.06|brass|переносить расстояния на карту
Угольник чертёжный|0.1|wood|проверять прямой угол
Рейсфедер|0.03|brass|проводить ровные линии чернилами
Восковая табличка|0.2|wax|делать стираемые записи стилусом
Стилус писца|0.02|bone|писать на восковой табличке
Скребок для пергамента|0.05|steel|соскабливать поверхность пергамента
Пресс переплётчика|2|wood|сжимать листы при переплёте
Папка для карт|0.4|leather|защищать сложенные карты
Счёты купеческие|0.3|wood|считать вручную
Лупа писца|0.08|glass|рассматривать мелкие надписи
Шнур для разметки карты|0.03|linen|размечать расстояния на чертеже
'''),
'tailor':('Портной и кожевник','junk','tailor','tailor','''
Шило|0.05|steel|прокалывать кожу и плотную ткань
Игла портновская|0.002|steel|шить ткань нитью
Игла костяная|0.005|bone|сшивать грубую ткань
Ножницы портновские|0.18|steel|кроить ткань
Нож кожевника|0.14|steel|резать кожу по выкройке
Копирное колёсико|0.06|steel|переносить линию выкройки
Колодка сапожника|0.5|wood|формовать обувь
Молоточек сапожника|0.25|steel|прибивать мелкие крепления обуви
Крючок сапожника|0.03|steel|протягивать нить через кожу
Пяльцы|0.12|wood|натягивать ткань для вышивки
Веретено|0.08|wood|прясть волокно
Челнок ткацкий|0.1|wood|пропускать нить через основу
Гребень для шерсти|0.22|iron|расчёсывать волокно
Распорка для шкуры|1.4|wood|растягивать шкуру при сушке
Скребок мездрильный|0.3|steel|снимать мездру со шкуры
Утюг угольный|2|iron|разглаживать ткань нагретым корпусом
'''),
'fishing':('Рыбак и охотник','junk','fishing','fisher','''
Рыболовный крючок|0.002|steel|цеплять приманку и удерживать рыбу
Поплавок пробковый|0.005|cork|показывать поклёвку
Грузило свинцовое|0.02|lead|утяжелять рыболовную оснастку
Удилище бамбуковое|0.35|bamboo|забрасывать снасть
Катушка для лески|0.05|wood|хранить намотанную леску
Рыбацкий подсачек|0.35|linen|подхватывать пойманную рыбу
Рыболовная верша|1.2|wicker|удерживать вошедшую рыбу
Кукан|0.12|iron|удерживать пойманную рыбу в воде
Сеть кастинговая|2|linen|ловить рыбу забрасыванием сети
Игла для вязания сетей|0.04|wood|вязать и чинить сеть
Рыбочистка|0.1|steel|снимать чешую с рыбы
Свисток манковый|0.03|bone|издавать звук приманки вручную
Силок проволочный|0.06|copper|ставить небольшую петлевую ловушку по решению мастера
Приманочный мешочек|0.04|linen|переносить приманку
Рамка для сушки рыбы|0.6|wood|развешивать рыбу для сушки
Крючок для копчения|0.08|iron|подвешивать продукт в коптильне
'''),
'carpenter':('Плотник и столяр','junk','carpentry','carpenter','''
Стамеска|0.18|steel|выбирать углубления в древесине
Долото|0.3|steel|выдалбливать глубокое гнездо
Рубанок|0.8|wood|снимать тонкую стружку
Лучковая пила|0.7|steel|пилить древесину
Ножовка обушковая|0.45|steel|делать точный короткий пропил
Коловорот|0.6|steel|сверлить отверстие ручным вращением
Сверло ложечное|0.12|steel|высверливать древесину
Струбцина деревянная|0.5|wood|сжимать детали при склейке
Киянка|0.5|wood|ударять по инструменту без стального бойка
Рейсмус столярный|0.2|wood|размечать параллельные линии
Отвес каменщика|0.15|lead|определять вертикаль
Шнур разметочный|0.08|linen|переносить прямую линию на заготовку
Скобель|0.4|steel|снимать кору и стружку
Цикля|0.08|steel|соскабливать тонкую стружку
Клещевой гвоздодёр|0.4|iron|вытаскивать гвозди
Бондарная скоба|0.15|iron|удерживать клёпки при сборке бочки
'''),
'farmer':('Фермер и конюх','junk','farm','farmer','''
Садовый совок|0.3|iron|копать небольшие лунки
Мотыга|1.4|iron|рыхлить землю
Грабли деревянные|1|wood|сгребать сено и листву
Садовый секатор|0.2|steel|обрезать небольшие ветви
Диббер посадочный|0.15|wood|делать отверстия под семена
Корзина для сбора урожая|0.5|wicker|переносить собранные плоды
Ситомойка для зерна|0.45|wood|отделять примеси от зерна
Цеп для обмолота|1.2|wood|обмолачивать колосья вручную
Подкова без гвоздей|0.25|iron|подковывать подходящее копыто работой кузнеца
Щётка для лошади|0.15|bristle|чистить шерсть животного
Крючок для копыт|0.07|steel|удалять грязь из копыта
Скребница|0.2|iron|чистить шерсть и кожу животного
Недоуздок|0.3|leather|вести подходящее животное
Торба кормовая|0.25|linen|подавать корм животному
Сырная форма|0.3|wood|придавать форму сырной массе
Ковш для зерна|0.15|wood|отмерять сыпучий корм
'''),
'miner':('Шахтёр и камнерез','junk','mine','miner','''
Клин камнекольный|0.7|steel|раскалывать камень в подготовленной щели
Молоток геолога|0.7|steel|отбивать небольшой образец породы
Зубило камнереза|0.4|steel|обтёсывать камень
Промывочный лоток|0.6|wood|промывать россыпь
Сито рудокопа|0.7|iron|сортировать мелкую породу
Рудная корзина|0.8|wicker|переносить небольшую порцию руды
Рудная лопатка|0.4|iron|собирать породу в ёмкость
Масляная лампа шахтёра|0.4|iron|освещать рабочее место при наличии масла
Кожаная наколенная подкладка|0.2|leather|подкладывать под колено при работе
Мешочек для проб|0.03|linen|хранить подписанный образец породы
Черта минералога|0.1|ceramic|проверять цвет порошка минерала
Лупа минералога|0.08|glass|рассматривать структуру породы
Шаблон каменщика|0.3|wood|проверять форму блока
Гладилка каменщика|0.4|steel|разравнивать раствор
Кельма|0.3|steel|наносить кладочный раствор
Камнерезная тёрка|0.5|stone|шлифовать поверхность камня
'''),
'merchant':('Лавка и торговля','junk','shop','merchant','''
Весы чашечные|0.8|brass|сравнивать массу товара с гирями
Набор малых гирь|0.5|brass|взвешивать товар на весах
Лоток менялы|0.4|wood|раскладывать монеты для счёта
Пробирный камень|0.1|stone|оставлять пробную черту металла
Пломбир купеческий|0.2|iron|зажимать торговую пломбу
Бирка для товара|0.005|wood|подписывать единицу товара
Дощечка долговая|0.08|wood|вести ручную запись долга
Торговый счётчик бусинный|0.15|wood|считать небольшие партии вручную
Футляр для печати|0.08|leather|переносить личную печать
Складская мерка|0.4|wood|отмерять объём сыпучего товара
Шнур для опечатывания|0.03|linen|перевязывать опечатываемую упаковку
Купеческий совок|0.2|copper|набирать сыпучий товар
Пробка для бочонка|0.02|cork|закрывать подходящее отверстие
Кран для бочки|0.12|wood|сливать жидкость из подходящей бочки
Товарная полочная табличка|0.04|wood|указывать цену и название вручную
Мешочек для размена|0.06|leather|хранить мелкие монеты
'''),
'household':('Дом и уборка','junk','home','householder','''
Щётка одежная|0.15|bristle|чистить ткань от пыли
Веник берёзовый|0.3|wood|подметать пол
Совок для золы|0.3|iron|собирать остывшую золу
Кочерга|0.7|iron|ворошить угли в очаге
Ведро деревянное|0.8|wood|переносить жидкость вручную
Таз медный|1|copper|мыть вещи и удерживать воду
Доска стиральная|0.7|wood|оттирать ткань при стирке
Щётка для посуды|0.08|bristle|чистить посуду
Прищепка деревянная|0.01|wood|закреплять ткань на верёвке
Щипцы для свечного нагара|0.06|iron|подрезать обгоревший фитиль
Огнивная коробочка|0.12|iron|хранить огниво и трут
Грелка постельная|0.8|copper|согревать постель закрытым нагретым сосудом
Горшок ночной|0.6|ceramic|использовать как бытовую санитарную ёмкость
Дверной клин|0.08|wood|подпирать дверь без автоматического запирания
Катушка бельевой верёвки|0.2|linen|развешивать бельё
Рожок обувной|0.05|horn|помогать надевать обувь
'''),
'apothecary':('Алхимик и травник','junk','apothecary','alchemist','''
Ступка|0.7|stone|растирать сухое сырьё пестиком
Пестик|0.25|stone|измельчать сырьё в ступке
Реторта стеклянная|0.3|glass|перегонять жидкость с подходящим оборудованием
Алхимический холодильник|0.5|glass|охлаждать пары при перегонке
Шпатель алхимика|0.03|steel|отбирать порошок
Фильтровальная воронка|0.08|glass|фильтровать жидкость через расходный фильтр
Капельница стеклянная|0.02|glass|дозировать небольшое количество жидкости
Пробиркодержатель|0.08|wood|удерживать небольшой сосуд
Сушильная рамка для трав|0.4|wood|раскладывать травы для сушки
Пресс для растений|0.6|wood|высушивать плоские образцы растений
Ложечка для реактивов|0.02|bone|отмерять небольшую порцию порошка
Банка с притёртой крышкой|0.2|glass|хранить реагент в закрытом сосуде
Склянка тёмного стекла|0.1|glass|хранить светочувствительный образец
Медная перегонная трубка|0.2|copper|направлять пары в перегонном аппарате
Алхимическая тренога|0.4|iron|удерживать сосуд над нагревом
Гербарная папка|0.3|wood|переносить плоские растительные образцы
'''),
'camp':('Дорога и лагерь','junk','camp','outfitter','''
Котелок походный|0.65|iron|готовить порцию пищи на костре
Тренога костровая|1.2|iron|подвешивать котелок над огнём
Колышек палаточный|0.08|wood|крепить растяжку палатки
Лопатка складная|0.7|iron|копать небольшую яму вручную
Игла парусная|0.01|steel|шить парусину и толстую ткань
Крюк подвесной|0.1|iron|подвешивать груз к подходящей опоре
Кожаная фляга|0.2|leather|переносить небольшой запас жидкости
Дорожная кружка|0.15|tin|пить из переносного сосуда
Соломенная подстилка|0.8|straw|подкладывать под спальное место
Свёрток для инструментов|0.25|leather|переносить инструменты в ткани
Чехол для топора|0.12|leather|закрывать лезвие подходящего топора
Шило походное|0.06|steel|прокалывать кожу при ремонте снаряжения
Песочные часы малые|0.2|glass|отмерять заданный интервал вручную
Дорожный компас|0.1|brass|определять направление по решению мастера
Сигнальное зеркальце|0.08|glass|подавать отражённый световой сигнал
Свисток сигнальный|0.03|brass|подавать слышимый сигнал
'''),
'music':('Музыка и сцена','junk','theatre','performer','''
Камертон|0.08|steel|задавать тон для настройки
Смычок|0.06|wood|извлекать звук из струнного инструмента
Медиатор костяной|0.002|bone|защипывать струны
Колокольчик сценический|0.08|brass|подавать звуковой знак
Театральная полумаска|0.08|wood|менять внешний облик в представлении
Погремушка|0.08|wood|отбивать ритм
Барабанная палочка|0.04|wood|ударять по барабану
Свирель тростниковая|0.05|reed|играть простую мелодию
Футляр для флейты|0.15|leather|переносить подходящую флейту
Гримировальная кисть|0.015|bristle|наносить сценический грим
Шаблон для теневого театра|0.08|leather|создавать силуэт в свете
Щётка для струн|0.03|bristle|очищать струны инструмента
'''),
'shrine':('Храм и обряд','junk','shrine','temple','''
Кадильница малая|0.25|brass|воскурять благовоние на углях
Кропило|0.12|bristle|разбрызгивать жидкость вручную
Чётки деревянные|0.04|wood|считать молитвы или упражнения
Алтарный колокольчик|0.12|brass|подавать обрядовый сигнал
Сосуд для подношений|0.35|ceramic|выкладывать подношения
Дорожная молитвенная дощечка|0.07|wood|хранить записанный молитвенный текст
Кисть для обрядовых знаков|0.02|bristle|наносить краску при обряде
Подставка для благовоний|0.1|ceramic|удерживать тлеющее благовоние
Щипцы кадильные|0.15|iron|перекладывать угли в кадильницу
Пустой футляр реликвария|0.2|brass|хранить небольшой памятный предмет
Обрядовая чашечка|0.1|ceramic|отмерять жидкость при обряде
Свечной гасильник|0.1|brass|гасить свечу колпачком
'''),
}
# New parts only. Original 18 parts/group remain in the existing stable volumes.
PARTS='''
spleen|Селезёнка|0.15|Vitality,Recovery
kidney|Почка|0.12|Antidote,Stability
lung|Лёгкое|0.5|Breathing,Vitality
stomach|Желудок|0.4|Acid,Constitution
intestine|Кишечная ткань|0.25|Nausea,Stability
brain|Головной мозг|0.6|Mind,Hallucination
spinal_cord|Спинной мозг|0.12|Mind,Speed
pituitary|Гипофиз|0.005|Magic,Vitality
thyroid|Щитовидная железа|0.02|Speed,Constitution
adrenal|Надпочечник|0.015|Strength,Fear
pancreas|Поджелудочная железа|0.08|Vitality,Stability
bladder|Мочевой пузырь|0.06|Acid,Stability
gallbladder|Жёлчный пузырь|0.04|Acid,Venom
tongue|Язык|0.08|Perception,Mind
ear|Ухо|0.02|Perception,Stability
skin|Кожа|0.2|Constitution,Stability
cartilage|Хрящ|0.08|Regeneration,Stability
nerve|Нервная ткань|0.03|Speed,Mind
lymph_node|Лимфатический узел|0.01|Antidote,Vitality
lymph|Лимфа|0.1|Antidote,Recovery
bile|Жёлчь|0.05|Acid,Venom
saliva|Слюна|0.03|Acid,Breathing
gastric_juice|Желудочный сок|0.05|Acid,Volatility
lens|Хрусталик|0.005|Perception,Blindness
retina|Сетчатка|0.005|Perception,Hallucination
cornea|Роговица|0.005|Perception,Stability
blood_clot|Сгусток крови|0.03|Hemorrhage,Vitality
vein|Венозная ткань|0.03|Recovery,Hemorrhage
artery|Артериальная ткань|0.03|Speed,Hemorrhage
ligament|Связка|0.05|Dexterity,Strength
membrane|Соединительная оболочка|0.02|Stability,Breathing
muscle|Мышечная ткань|0.15|Strength,Constitution
skull|Череп|1|Mind,Necrotic
jaw|Челюсть|0.2|Strength,Earth
rib|Ребро|0.08|Constitution,Earth
vertebra|Позвонок|0.08|Stability,Earth
scapula|Лопаточная кость|0.12|Constitution,Stability
pelvis|Тазовая кость|0.4|Constitution,Earth
fat_gland|Жировая железа|0.03|Fire,Stability
mucus|Слизь|0.05|Breathing,Nausea
tear|Слёзная жидкость|0.01|Recovery,Perception
eye_fluid|Стекловидное тело|0.01|Perception,Cold
hair|Волос|0.01|Magic,Stability
nail|Ноготь|0.005|Earth,Stability
placenta|Плацента|0.2|Regeneration,Vitality
umbilical|Пуповина|0.03|Recovery,Vitality
'''
SPECIAL_PARTS={
'animal': """
crop|Зоб|0.05|Recovery,Stability
gizzard|Мускульный желудок|0.1|Strength,Constitution
swim_bladder|Плавательный пузырь|0.03|Breathing,Stability
chitin|Хитиновый панцирь|0.2|Constitution,Earth
quill|Игла покровная|0.01|Hemorrhage,Earth
hoof|Копыто|0.1|Earth,Strength
web_gland|Паутинообразующая железа|0.02|Dexterity,Stability
ink_sac|Чернильный мешок|0.03|Blindness,Invisibility
egg|Яйцо|0.06|Vitality,Recovery
eggshell|Яичная скорлупа|0.02|Earth,Stability
antler|Ветвистый рог|0.3|Earth,Regeneration
milk|Молоко|0.1|Recovery,Constitution
""",
'monster': """
acid_sac|Кислотный мешок|0.08|Acid,Volatility
venom_sac|Ядовитый мешок|0.05|Venom,Weakness
luminescent|Светящийся орган|0.03|Radiant,Perception
electric|Электрический орган|0.1|Speed,Volatility
phase_membrane|Фазовая мембрана|0.02|Invisibility,Magic
petrifying|Каменеющая железа|0.05|Petrification,Earth
regenerative|Регенеративный узел|0.04|Regeneration,Vitality
fire_sac|Огненный мешок|0.1|Fire,Volatility
frost_crystal|Морозный кристалл|0.04|Cold,Stability
necrotic|Некротическая ткань|0.06|Necrotic,Weakness
ectoplasm|Эктоплазма|0.03|Invisibility,Necrotic
elemental_core|Стихийное ядро|0.2|Magic,Volatility
adhesive|Клейкий секрет|0.05|Stability,Dexterity
paralytic|Паралитическая железа|0.04|Weakness,Venom
sensory_tendril|Чувствительный усик|0.02|Perception,Mind
""",
'humanoid': ''}
OLD_PART_PROPERTIES={
'heart':['Vitality','Strength'],'blood':['Vitality','Hemorrhage'],'bone':['Earth','Necrotic'],
'hide':['Constitution','Stability'],'meat':['Recovery','Constitution'],'fat':['Fire','Stability'],
'eye':['Perception','Mind'],'tooth':['Strength','Earth'],'claw':['Dexterity','Hemorrhage'],
'sinew':['Dexterity','Strength'],'liver':['Antidote','Recovery'],'gland':['Venom','Volatility'],
'horn':['Earth','Magic'],'scale':['Constitution','Earth'],'marrow':['Recovery','Vitality'],
'fur':['Cold','Stability'],'feather':['Speed','Breathing'],'venom':['Venom','Weakness']}
EXTRA_CLOTHES='''
Кожаный напальчник лучника|0.02|leather|защищать палец при работе с тетивой
Налобная повязка ремесленника|0.04|linen|удерживать пот при работе
Защитные очки стеклодува|0.1|glass|прикрывать глаза при ручной работе
Нарукавник писца|0.04|linen|защищать рукав от чернил
Плотницкий пояс для инструментов|0.3|leather|носить инструменты на поясе
Пастушеские краги|0.35|leather|прикрывать голени при ходьбе
Лекарский передник клеёнчатый|0.4|linen|защищать одежду при ручной разделке
Сетчатый колпак пчеловода|0.12|linen|прикрывать лицо при работе с насекомыми
Меховые наушники|0.08|fur|прикрывать уши от холода
Рабочие рукавицы брезентовые|0.15|linen|защищать руки при грубой работе
Путевой плащ от дождя|0.8|linen|прикрывать одежду от осадков
Обмотки для голеней|0.1|linen|закреплять одежду вокруг голеней
'''
EXTRA_CONSUMABLES='''
Трут сухой|0.02|plant|использовать порцию при разведении огня
Фитиль хлопковый|0.01|cotton|заменять фитиль светильника
Фильтр бумажный|0.005|paper|фильтровать одну небольшую порцию жидкости
Чистая тряпица|0.02|linen|протирать или перевязывать предмет
Сургучная палочка|0.03|wax|запечатывать письмо
Кусочек портновского мела|0.01|chalk|наносить стираемую разметку
Швейная нить на починку|0.005|linen|сшивать небольшую прореху
Рыбацкая наживка|0.02|organic|насаживать одну порцию на крючок
Порция коптильной щепы|0.2|wood|создавать дым при копчении
Соломенная обёртка|0.03|straw|упаковывать хрупкую вещь
Мешочек сушёной закваски|0.03|organic|заквашивать пищевую заготовку
Пекарские дрожжи|0.02|organic|поднимать тесто при приготовлении
Порция зубного порошка|0.02|chalk|чистить зубы вручную
Порция стиральной золы|0.1|ash|использовать щёлочной зольный раствор при стирке
Салфетка для линз|0.005|linen|очищать линзу от пыли
Вата перевязочная|0.02|cotton|подкладывать впитывающий материал
Лист сусального золота|0.001|gold|покрывать небольшую поверхность при отделке
Вощёная обёртка|0.02|wax|заворачивать продукт
Порция сапожной смазки|0.03|fat|ухаживать за кожаной обувью
Порция сценического грима|0.02|pigment|наносить грим для представления
'''
EXTRA_RAW='''
Солома пшеничная|0.2|straw|набивать подстилку или плести
Лыко липовое|0.1|bast|плести ленты и верёвки
Береста листовая|0.1|bark|делать обёртку или короб
Ивовый прут|0.1|wood|плести корзины
Тростниковый стебель|0.05|reed|делать простую трубку или перо
Бамбуковая трубка|0.1|bamboo|делать полую заготовку
Пробковая кора|0.1|cork|вырезать поплавок или пробку
Дубовая кора|0.1|bark|готовить дубильное сырьё
Льняная костра|0.1|plant|использовать растительные отходы производства
Хлопковое волокно|0.1|cotton|прясть нить
Шерсть вычесанная|0.1|wool|прясть или валять
Конский волос|0.05|hair|делать щётку или плетение
Щетина сырьевая|0.05|bristle|делать кисть или щётку
Кость полированная|0.1|bone|вырезать небольшую деталь
Роговая пластина|0.1|horn|вырезать накладку или гребень
Кожаный лоскут|0.1|leather|латать или вырезать ремешок
Полоса сыромятной кожи|0.1|leather|делать крепление
Сухожильная нить|0.02|sinew|сшивать или связывать вручную
Льняная ветошь|0.1|linen|готовить наполнитель или бумажное сырьё
Стеклянный бой|0.2|glass|переплавлять по будущему рецепту
Керамический черепок|0.1|ceramic|использовать как абразив или заполнитель
Латунный обрезок|0.1|brass|переплавлять по будущему рецепту
Медная стружка|0.05|copper|использовать металлическое сырьё
Железная окалина|0.1|iron|использовать побочный продукт ковки
Древесная стружка|0.1|wood|использовать наполнитель или растопку
Опилки столярные|0.1|wood|готовить наполнитель
Пыль костяная|0.05|bone|готовить состав по будущему рецепту
Воск забрусный|0.1|wax|готовить свечу или восковую смесь
Песок формовочный|0.2|sand|готовить литейную форму
Глина огнеупорная|0.2|clay|формовать жаростойкую заготовку
Шерстяной войлок|0.1|wool|вырезать подкладку
Невыделанная кожа|0.3|hide|выделывать кожу по будущему рецепту
'''

def read(path):return json.loads((ROOT/path).read_text())
def write(path,data):
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def rows(text):
 for line in text.strip().splitlines():
  name,weight,material,use=line.split('|');yield name,float(weight),material,use

def main():
 catalog=read('catalog/v3/index.json')
 catalog['packages']=[m for m in catalog['packages'] if m.get('worldLootRevision')!=REVISION]
 baseline_items=[]
 for m in catalog['packages']:
  if m['type'] in ['item','craft']:baseline_items+=read('packages/'+m['url'].split('/')[-1]).get('items',[])
 existing={i['name'] for i in baseline_items};created=[];manifests=[];profiles=[];coverage=[];skipped=[]
 def publish(pid,label,items,category,extra=None,typ='item',deps=None):
  payload=dict(schemaVersion=1,id=pid,version=REVISION,type=typ,items=items)
  if extra:payload.update(extra)
  path=f'packages/{pid}-{REVISION}.json';write(path,payload);raw=(ROOT/path).read_bytes()
  m=dict(schemaVersion=1,id=pid,name=label,version=REVISION,author='DnD-VTT contributors',license='CC0-1.0 (project original loot metadata)',type=typ,format='json',platform='any',unityVersion='*',dependencies=deps or [],bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),url=URL+path,minClientVersionCode=10034,worldLootRevision=REVISION,worldLootFamily=category,description='Опциональное дополнение: быт, ремесло и общая анатомия. Совместимо с Unity1.00.34. Особые применения и будущие рецепты разрешает мастер.' if typ=='item' else 'Алхимические профили общих частей. Установите правила алхимии; образцы добавляются из сборников материалов. Исследование раскрывает свойства в существующем интерфейсе.')
  catalog['packages'].append(m);manifests.append(m);return m
 def action_for(use):
  for word,action in [('снимать шкуру','skin'),('отделять мясо','butcher'),('шинковать','cut'),('резать','cut'),('рубить','chop'),('сшивать','sew'),('шить','sew'),('прокалывать','pierce'),('пилить','saw'),('сверлить','drill'),('шлифовать','polish'),('опиливать','file'),('измельчать','grind'),('растирать','grind'),('взвешивать','weigh'),('сравнивать массу','weigh'),('отмерять','measure'),('фильтровать','filter'),('перегонять','distill'),('переплавлять','smelt'),('прясть','spin'),('плести','weave'),('писать','write'),('подписывать','label'),('чистить','clean'),('очищать','clean'),('мыть','wash'),('сушить','dry'),('сушки','dry'),('удерживать','hold'),('переносить','carry'),('хранить','store'),('подвешивать','hang'),('крепить','fasten'),('сжимать','clamp'),('пробивать','punch')]:
   if word in use:return action
  return 'manual_use'
 def trait(material,location,merchant,use,price,anatomy=None):
  t=dict(schemaVersion=1,materialTags=[material],lootTags=[location],uses=[dict(action=action_for(use),execution='manual',text=use)],stateDefaults=dict(condition='intact'),trade=dict(basePriceGp=price,merchantTags=[merchant]),processing=dict(execution='planned',materialTags=[material],recipeTags=[location]))
  if anatomy:t['anatomy']=anatomy;t['stateDefaults']['freshness']='fresh';t['uses'][0]['action']='alchemy_sample'
  return t
 def ordinary(family,label,category,location,merchant,text):
  buckets={}
  for name,weight,material,use in rows(text):
   if name in existing:skipped.append(name);continue
   cat='weapons' if family=='kitchen' and name in ['Нож для масла','Поварской нож','Хлебный нож','Кухонный тесак','Мясницкий нож','Нож для снятия шкуры','Скалка','Чугунная сковорода'] else category
   buckets.setdefault(cat,[]).append((name,weight,material,use))
  for cat,entries in buckets.items():
   pid=f'dnd.items.world.{family}.{cat}';out=[]
   for name,weight,material,use in entries:
    key='butter_knife' if name=='Нож для масла' else hashlib.sha256(name.encode()).hexdigest()[:12]
    price=round(max(.01,weight*(3 if material in ['steel','glass','brass'] else .5)),2)
    i=dict(id=pid+'.'+key,name=name,inventoryCategory=cat,category=label,weight=f'{weight:g} кг',cost=f'{price:g} зм',description=f'{name}. Назначение: {use}. Применение разрешается вручную; предмет не даёт скрытых бонусов.',itemTraits=trait(material,location,merchant,use,price))
    if cat=='weapons':
     cutting=name in ['Поварской нож','Хлебный нож','Кухонный тесак','Мясницкий нож','Нож для снятия шкуры']
     i.update(damage='1d4',damageType='рубящий' if cutting else 'дробящий',toHit=0,hands='1 рука',groupKey='improvised',typeKey='melee',properties=['Импровизированное оружие'],proficiencies=[])
     i['itemTraits']['uses'][0]['action']='cut_soft_food' if name=='Нож для масла' else 'skin' if name=='Нож для снятия шкуры' else 'butcher' if name=='Мясницкий нож' else 'cut_food' if cutting else i['itemTraits']['uses'][0]['action']
     i['itemTraits']['uses'].append(dict(action='improvised_attack',execution='manual',damage='1d4',damageType=i['damageType']))
     i['description']+=' Можно экипировать как импровизированное оружие: 1d4 '+i['damageType']+'; попадание и обстоятельства разрешает мастер.'
    elif cat=='armor':i.update(acBase=0,proficiencyType='none',equipmentSlot='clothing');i['description']+=' Бонуса к КД нет.'
    elif cat=='consumables':i.update(effects=[],useMode='manual');i['description']+=' Кнопка применения списывает одну порцию без автоматического эффекта.'
    elif cat=='materials':i['craftMaterialId']='world_'+key;i['description']+=' Автоматический рецепт пока не назначен.'
    out.append(i);created.append(i);existing.add(name)
   publish(pid,f'Сборник: {label} — {len(out)} предметов',out,family)
   coverage.append(dict(family=family,packageId=pid,itemCount=len(out),category=cat))
 for family,(label,category,location,merchant,text) in GROUPS.items():ordinary(family,label,category,location,merchant,text)
 ordinary('workwear','Рабочая одежда','armor','workshop','tailor',EXTRA_CLOTHES)
 ordinary('supplies','Бытовые расходники','consumables','supplies','general',EXTRA_CONSUMABLES)
 ordinary('raw','Природное и вторичное сырьё','materials','raw','artisan',EXTRA_RAW)
 new_parts=[]
 for line in PARTS.strip().splitlines():
  part,name,weight,props=line.split('|');new_parts.append((part,name,float(weight),props.split(',')))
 # Existing 54 shared records are reused by name/id, never duplicated in new item packs.
 old={i.get('craftMaterialId'):i for i in baseline_items if i.get('harvestGroup')}
 for group,label in [('animal','животного'),('monster','монстра'),('humanoid','гуманоида')]:
  pid=f'dnd.items.world.anatomy.{group}.materials';out=[];ingredient_profiles=[]
  all_parts=[(part,old[f'harvest_{group}_{part}']['name'],None,properties) for part,properties in OLD_PART_PROPERTIES.items()]
  group_parts=list(new_parts)
  for row in SPECIAL_PARTS[group].strip().splitlines():
   part,name,weight,props=row.split('|');group_parts.append((part,name,float(weight),props.split(',')))
  for part,name,weight,properties in group_parts:
   full=f'{name} {label}';mid=f'harvest_{group}_{part}'
   assert full not in existing,full
   applicability=['requires_compatible_anatomy']
   if part in ['placenta','umbilical']:applicability.extend(['placental_anatomy','gestation_or_birth'])
   t=trait('organic.'+part,'harvest.'+group,'alchemist','использовать как алхимический образец после исследования',2,dict(group=group,part=part,requires=applicability,unit='sample'))
   if part in ['frost_crystal','ectoplasm','elemental_core','phase_membrane']:t['materialTags']=['magical.'+part]
   t['stateDefaults']['condition']='unprocessed'
   t['research']=dict(ingredientId=mid,profilePackageId=f'dnd.alchemy.ingredients.world.anatomy.{group}',knowledgeStore='alchemyState.discovered')
   t['provenanceFields']=['creatureName','harvestedAt','harvesterId']
   i=dict(id=pid+'.'+part,name=full,inventoryCategory='materials',category='Органы и ткани',weight=f'{weight:g} кг',cost='2 зм',description=f'{full}. Необработанный образец разделки существа с подходящей анатомией. Алхимические свойства открываются исследованием при установленном дополнении профилей. Происхождение и состояние образца учитывает мастер.',craftMaterialId=mid,alchemyId=mid,harvestGroup=group,harvestPart=part,itemTraits=t)
   out.append(i);created.append(i);existing.add(full);all_parts.append((part,full,weight,properties))
  publish(pid,f'Сборник: Органы и ткани {label} — {len(out)}',out,'anatomy.'+group)
  coverage.append(dict(family='anatomy.'+group,packageId=pid,itemCount=len(out),category='materials'))
  for part,full,weight,properties in all_parts:
   mid=f'harvest_{group}_{part}';props=list(properties)
   group_property='Constitution' if group=='animal' else 'Magic' if group=='monster' else 'Mind'
   if group_property not in props:props.append(group_property)
   ingredient_profiles.append(dict(id=mid,name=full,category='anatomy',rarity='uncommon' if group=='monster' else 'common',properties=props,extra=None,potency=45 if group=='monster' else 30,stability=65,volatility=30 if group=='monster' else 20,purity=65,tags=['anatomy',group,part,'alchemy']))
  profiles+=ingredient_profiles
  publish(f'dnd.alchemy.ingredients.world.anatomy.{group}',f'Алхимия: исследование органов {label}',[],'research.'+group,extra=dict(mode='alchemy-ingredients',ingredients=ingredient_profiles),typ='craft',deps=['dnd.alchemy.rules'])
 write('catalog/v3/index.json',catalog)
 write('sources/world-loot-1.0.0.json',dict(schemaVersion=1,revision=REVISION,clientSource='e99d922aeab38dde49ba4268a1db8a895a4f053e',packages=[m['id'] for m in manifests],newItemCount=len(created),newProfileCount=len(profiles),existingSharedPartsReused=54,coverage=coverage,skippedExistingNames=skipped,items=[dict(id=i['id'],name=i['name'],category=i['inventoryCategory']) for i in created]))
 print('World loot:',len(created),'new items;',len(profiles),'research profiles;',len(manifests),'optional packages;',len(skipped),'existing names skipped')
if __name__=='__main__':main()
