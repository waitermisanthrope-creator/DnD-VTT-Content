# Атлас всех файлов DnD-VTT-Content — для ИИ и разработчиков

**Назначение:** точная карта каждого Git-отслеживаемого файла этого репозитория на момент 22.10.2026, + новые служебные файлы из текущего комплекта документации. Снимок построен из рекурсивного Git-дерева ветки `main`; для уже подготовленного `docs/FILE_ATLAS.md` размер указан `—` до коммита. **Всего записей: 207**. Файлы в GitHub Releases, сгенерированные бинарники и отсутствующие в Git файлы сюда не входят. При новых коммитах проверяй фактическое дерево и актуализируй атлас.

**Как использовать:** новому автору/ChatGPT сначала прочитать `README.md` и `AGENTS.md`. Для создания модов главным учебником является `docs/MOD_AUTHOR_GUIDE.md`. Для поиска «где живёт X» используй таблицу ниже; не дублируй существующий файл или ID. Для конфликтов таблицы с кодом/каталогом приоритет у **текущих файлов**.

## Категории и границы

- **Живой каталог:** `catalog/v3/index.json` (193 позиций). Старые каталоги `v1/v2` не переписывать. 
- **Физические пакеты:** `packages/*.json`; это данные, а не DLL/JS-скрипты. Полезная нагрузка и `packages[]` каталога — разные объекты.
- **Схемы:** `schemas/catalog-entry-v1.schema.json` описывает поля **записи каталога**, а `schemas/package-manifest-v1.schema.json` — архивное предложение, не читаемый APK ZIP.
- **Связь с Unity:** `DnD-VTT/experiment/unity-vtt/unity/Assets/Vtt/Runtime/WorkshopStore.cs` валидирует пакеты; `LegacySessionPanel.ContentManager.cs` читает каталог.
- **Смена мода:** вычислить SHA-256 и байты после последней правки, поднять `version`, обновить каталог и проверить скачивание.

Количество файлов по верхним разделам: `AGENTS.md` — 1; `catalog` — 3; `docs` — 5; `migration` — 1; `packages` — 194; `README.md` — 1; `schemas` — 2.

## Полная инвентаризация

| № | Путь | Размер Git blob | Роль / назначение |
|---:|---|---:|---|
| 1 | `AGENTS.md` | 4866 B | Правила поведения ИИ при создании модификаций; стартовая инструкция для ChatGPT. |
| 2 | `catalog/v1/index.json` | 806 B | Индекс Content v1; исторический снимок для совместимости со старыми клиентами; не изменять устаревшие версии без причины. |
| 3 | `catalog/v2/index.json` | 162970 B | Индекс Content v2; исторический снимок для совместимости со старыми клиентами; не изменять устаревшие версии без причины. |
| 4 | `catalog/v3/index.json` | 171363 B | Индекс Content v3; исторический снимок для совместимости со старыми клиентами; не изменять устаревшие версии без причины. |
| 5 | `docs/FILE_ATLAS.md` | — | Этот полный реестр путей и назначений файлов; обновлять при изменении дерева. |
| 6 | `docs/MOD_AUTHOR_GUIDE.md` | 18929 B | Пошаговое создание, публикация и тестирование JSON-пакетов; инструкция для ИИ и новичка. |
| 7 | `docs/PUBLISHING.md` | 2454 B | Правила публикации, ручной модерации, авторства и целостности пакетов. |
| 8 | `docs/TEST-PACKAGES.md` | 307 B | Условия происхождения и лицензии демонстрационных оригинальных пакетов. |
| 9 | `docs/WORKSHOP_PILOT.md` | 2762 B | Отчёт о первоначальном пилоте мастерской; исторические ограничения могут устареть. |
| 10 | `migration/main-content-inventory.json` | 14887 B | Инвентаризация содержимого исходного приложения при выделении отдельного Content-репозитория. |
| 11 | `packages/demo-race.json` | 299 B | Исторический прототип тестовой расы; отсутствует в активном каталоге и не является самостоятельным готовым модом. |
| 12 | `packages/demo.race.lanternfolk.json` | 1037 B | Раса персонажа: **Фонарники — тестовая раса**; id demo.race.lanternfolk; запись есть в текущем каталоге. |
| 13 | `packages/dnd.alchemy.ingredients.1.json` | 30349 B | Крафт/алхимия: **Алхимия 2.0 — ингредиенты 1**; id dnd.alchemy.ingredients.1; запись есть в текущем каталоге. |
| 14 | `packages/dnd.alchemy.ingredients.2.json` | 30331 B | Крафт/алхимия: **Алхимия 2.0 — ингредиенты 2**; id dnd.alchemy.ingredients.2; запись есть в текущем каталоге. |
| 15 | `packages/dnd.alchemy.ingredients.3.json` | 30452 B | Крафт/алхимия: **Алхимия 2.0 — ингредиенты 3**; id dnd.alchemy.ingredients.3; запись есть в текущем каталоге. |
| 16 | `packages/dnd.alchemy.rules.json` | 7300 B | Крафт/алхимия: **Алхимия 2.0 — правила и катализаторы**; id dnd.alchemy.rules; запись есть в текущем каталоге. |
| 17 | `packages/dnd.class.accursed.json` | 2148 B | Класс персонажа (первый уровень/metadata): **Аккурсд**; id dnd.class.accursed; запись есть в текущем каталоге. |
| 18 | `packages/dnd.class.alchemist.json` | 2137 B | Класс персонажа (первый уровень/metadata): **Алхимик**; id dnd.class.alchemist; запись есть в текущем каталоге. |
| 19 | `packages/dnd.class.artificer.json` | 4527 B | Класс персонажа (первый уровень/metadata): **Изобретатель**; id dnd.class.artificer; запись есть в текущем каталоге. |
| 20 | `packages/dnd.class.beastheart.json` | 2142 B | Класс персонажа (первый уровень/metadata): **Бистхарт**; id dnd.class.beastheart; запись есть в текущем каталоге. |
| 21 | `packages/dnd.class.blood_hunter.json` | 2232 B | Класс персонажа (первый уровень/metadata): **Кровавый охотник**; id dnd.class.blood_hunter; запись есть в текущем каталоге. |
| 22 | `packages/dnd.class.geist.json` | 2102 B | Класс персонажа (первый уровень/metadata): **Гайст**; id dnd.class.geist; запись есть в текущем каталоге. |
| 23 | `packages/dnd.class.ghost.json` | 2429 B | Класс персонажа (первый уровень/metadata): **Призрак**; id dnd.class.ghost; запись есть в текущем каталоге. |
| 24 | `packages/dnd.class.illrigger.json` | 2160 B | Класс персонажа (первый уровень/metadata): **Иллиригер**; id dnd.class.illrigger; запись есть в текущем каталоге. |
| 25 | `packages/dnd.class.martyr.json` | 2128 B | Класс персонажа (первый уровень/metadata): **Мученик**; id dnd.class.martyr; запись есть в текущем каталоге. |
| 26 | `packages/dnd.class.necromancer.json` | 2164 B | Класс персонажа (первый уровень/metadata): **Некромант**; id dnd.class.necromancer; запись есть в текущем каталоге. |
| 27 | `packages/dnd.class.occultist.json` | 2785 B | Класс персонажа (первый уровень/metadata): **Оккультист**; id dnd.class.occultist; запись есть в текущем каталоге. |
| 28 | `packages/dnd.class.parasite.json` | 2445 B | Класс персонажа (первый уровень/metadata): **Паразит**; id dnd.class.parasite; запись есть в текущем каталоге. |
| 29 | `packages/dnd.class.psion.json` | 2932 B | Класс персонажа (первый уровень/metadata): **Псионик**; id dnd.class.psion; запись есть в текущем каталоге. |
| 30 | `packages/dnd.class.pugilist.json` | 2144 B | Класс персонажа (первый уровень/metadata): **Пугилист**; id dnd.class.pugilist; запись есть в текущем каталоге. |
| 31 | `packages/dnd.class.rune_keeper.json` | 2223 B | Класс персонажа (первый уровень/metadata): **Рунный хранитель**; id dnd.class.rune_keeper; запись есть в текущем каталоге. |
| 32 | `packages/dnd.class.savant.json` | 2118 B | Класс персонажа (первый уровень/metadata): **Савант**; id dnd.class.savant; запись есть в текущем каталоге. |
| 33 | `packages/dnd.class.shifter.json` | 3156 B | Класс персонажа (первый уровень/metadata): **Шифтер**; id dnd.class.shifter; запись есть в текущем каталоге. |
| 34 | `packages/dnd.class.swarm.json` | 2405 B | Класс персонажа (первый уровень/metadata): **Рой**; id dnd.class.swarm; запись есть в текущем каталоге. |
| 35 | `packages/dnd.class.vessel.json` | 2114 B | Класс персонажа (первый уровень/metadata): **Сосуд**; id dnd.class.vessel; запись есть в текущем каталоге. |
| 36 | `packages/dnd.class.walter_parasite.json` | 2632 B | Класс персонажа (первый уровень/metadata): **Паразит доктора Вальтера**; id dnd.class.walter_parasite; запись есть в текущем каталоге. |
| 37 | `packages/dnd.class.warden.json` | 2790 B | Класс персонажа (первый уровень/metadata): **Страж**; id dnd.class.warden; запись есть в текущем каталоге. |
| 38 | `packages/dnd.class.warlord.json` | 2817 B | Класс персонажа (первый уровень/metadata): **Военачальник**; id dnd.class.warlord; запись есть в текущем каталоге. |
| 39 | `packages/dnd.class.witch.json` | 2112 B | Класс персонажа (первый уровень/metadata): **Ведьма**; id dnd.class.witch; запись есть в текущем каталоге. |
| 40 | `packages/dnd.craft.core.json` | 25950 B | Крафт/алхимия: **Мастерская — 47 рецептов и материалы**; id dnd.craft.core; запись есть в текущем каталоге. |
| 41 | `packages/dnd.feat.aberrant_dragonmark.json` | 730 B | Черта персонажа: **Чужеродная драконья метка**; id dnd.feat.aberrant_dragonmark; запись есть в текущем каталоге. |
| 42 | `packages/dnd.feat.actor.json` | 566 B | Черта персонажа: **Актёр**; id dnd.feat.actor; запись есть в текущем каталоге. |
| 43 | `packages/dnd.feat.alchemist.json` | 585 B | Черта персонажа: **Алхимик**; id dnd.feat.alchemist; запись есть в текущем каталоге. |
| 44 | `packages/dnd.feat.alert.json` | 516 B | Черта персонажа: **Бдительный**; id dnd.feat.alert; запись есть в текущем каталоге. |
| 45 | `packages/dnd.feat.arcane_defender.json` | 607 B | Черта персонажа: **Магический страж**; id dnd.feat.arcane_defender; запись есть в текущем каталоге. |
| 46 | `packages/dnd.feat.arcane_marksman.json` | 581 B | Черта персонажа: **Магический стрелок**; id dnd.feat.arcane_marksman; запись есть в текущем каталоге. |
| 47 | `packages/dnd.feat.arcane_recovery_feat.json` | 615 B | Черта персонажа: **Магический резерв**; id dnd.feat.arcane_recovery_feat; запись есть в текущем каталоге. |
| 48 | `packages/dnd.feat.artisan_genius.json` | 664 B | Черта персонажа: **Гениальный ремесленник**; id dnd.feat.artisan_genius; запись есть в текущем каталоге. |
| 49 | `packages/dnd.feat.athlete.json` | 615 B | Черта персонажа: **Атлет**; id dnd.feat.athlete; запись есть в текущем каталоге. |
| 50 | `packages/dnd.feat.bardic_inspiration_feat.json` | 647 B | Черта персонажа: **Звучный голос**; id dnd.feat.bardic_inspiration_feat; запись есть в текущем каталоге. |
| 51 | `packages/dnd.feat.beast_tamer.json` | 565 B | Черта персонажа: **Укротитель зверей**; id dnd.feat.beast_tamer; запись есть в текущем каталоге. |
| 52 | `packages/dnd.feat.berserker_rage.json` | 608 B | Черта персонажа: **Неистовый**; id dnd.feat.berserker_rage; запись есть в текущем каталоге. |
| 53 | `packages/dnd.feat.berserker.json` | 515 B | Черта персонажа: **Берсерк**; id dnd.feat.berserker; запись есть в текущем каталоге. |
| 54 | `packages/dnd.feat.blood_hunter.json` | 584 B | Черта персонажа: **Адепт кровавой охоты**; id dnd.feat.blood_hunter; запись есть в текущем каталоге. |
| 55 | `packages/dnd.feat.bountiful_luck.json` | 590 B | Черта персонажа: **Обильная удача**; id dnd.feat.bountiful_luck; запись есть в текущем каталоге. |
| 56 | `packages/dnd.feat.brawler.json` | 517 B | Черта персонажа: **Головорез**; id dnd.feat.brawler; запись есть в текущем каталоге. |
| 57 | `packages/dnd.feat.charger.json` | 506 B | Черта персонажа: **Наскок**; id dnd.feat.charger; запись есть в текущем каталоге. |
| 58 | `packages/dnd.feat.chef.json` | 621 B | Черта персонажа: **Шеф-повар**; id dnd.feat.chef; запись есть в текущем каталоге. |
| 59 | `packages/dnd.feat.crossbow_expert.json` | 582 B | Черта персонажа: **Эксперт по арбалетам**; id dnd.feat.crossbow_expert; запись есть в текущем каталоге. |
| 60 | `packages/dnd.feat.defensive_duelist.json` | 620 B | Черта персонажа: **Защитный дуэлянт**; id dnd.feat.defensive_duelist; запись есть в текущем каталоге. |
| 61 | `packages/dnd.feat.divine_interventionist.json` | 597 B | Черта персонажа: **Божественная защита**; id dnd.feat.divine_interventionist; запись есть в текущем каталоге. |
| 62 | `packages/dnd.feat.dragon_fear.json` | 713 B | Черта персонажа: **Драконий страх**; id dnd.feat.dragon_fear; запись есть в текущем каталоге. |
| 63 | `packages/dnd.feat.dragon_hide.json` | 713 B | Черта персонажа: **Драконья шкура**; id dnd.feat.dragon_hide; запись есть в текущем каталоге. |
| 64 | `packages/dnd.feat.dual_wielder.json` | 547 B | Черта персонажа: **Парное оружие**; id dnd.feat.dual_wielder; запись есть в текущем каталоге. |
| 65 | `packages/dnd.feat.duelist_master.json` | 558 B | Черта персонажа: **Мастер дуэлей**; id dnd.feat.duelist_master; запись есть в текущем каталоге. |
| 66 | `packages/dnd.feat.dungeon_delver.json` | 597 B | Черта персонажа: **Исследователь подземелий**; id dnd.feat.dungeon_delver; запись есть в текущем каталоге. |
| 67 | `packages/dnd.feat.durable.json` | 592 B | Черта персонажа: **Выносливый**; id dnd.feat.durable; запись есть в текущем каталоге. |
| 68 | `packages/dnd.feat.dwarven_fortitude.json` | 694 B | Черта персонажа: **Дворфийская стойкость**; id dnd.feat.dwarven_fortitude; запись есть в текущем каталоге. |
| 69 | `packages/dnd.feat.eldritch_adept.json` | 604 B | Черта персонажа: **Мистический адепт**; id dnd.feat.eldritch_adept; запись есть в текущем каталоге. |
| 70 | `packages/dnd.feat.elemental_adept.json` | 586 B | Черта персонажа: **Адепт стихий**; id dnd.feat.elemental_adept; запись есть в текущем каталоге. |
| 71 | `packages/dnd.feat.elven_accuracy.json` | 763 B | Черта персонажа: **Эльфийская меткость**; id dnd.feat.elven_accuracy; запись есть в текущем каталоге. |
| 72 | `packages/dnd.feat.empath.json` | 568 B | Черта персонажа: **Эмпат**; id dnd.feat.empath; запись есть в текущем каталоге. |
| 73 | `packages/dnd.feat.fast_movement.json` | 597 B | Черта персонажа: **Спринтер**; id dnd.feat.fast_movement; запись есть в текущем каталоге. |
| 74 | `packages/dnd.feat.fey_teleportation.json` | 731 B | Черта персонажа: **Фейская телепортация**; id dnd.feat.fey_teleportation; запись есть в текущем каталоге. |
| 75 | `packages/dnd.feat.fey_touched.json` | 675 B | Черта персонажа: **Меченый феями**; id dnd.feat.fey_touched; запись есть в текущем каталоге. |
| 76 | `packages/dnd.feat.fighting_initiate.json` | 630 B | Черта персонажа: **Адепт боевого стиля**; id dnd.feat.fighting_initiate; запись есть в текущем каталоге. |
| 77 | `packages/dnd.feat.flame_touched.json` | 597 B | Черта персонажа: **Огненное касание**; id dnd.feat.flame_touched; запись есть в текущем каталоге. |
| 78 | `packages/dnd.feat.flames_of_phlegethos.json` | 725 B | Черта персонажа: **Пламя Флегетоса**; id dnd.feat.flames_of_phlegethos; запись есть в текущем каталоге. |
| 79 | `packages/dnd.feat.gladiator.json` | 529 B | Черта персонажа: **Гладиатор**; id dnd.feat.gladiator; запись есть в текущем каталоге. |
| 80 | `packages/dnd.feat.gourmand.json` | 578 B | Черта персонажа: **Гурман**; id dnd.feat.gourmand; запись есть в текущем каталоге. |
| 81 | `packages/dnd.feat.great_weapon_master.json` | 602 B | Черта персонажа: **Мастер тяжелого оружия**; id dnd.feat.great_weapon_master; запись есть в текущем каталоге. |
| 82 | `packages/dnd.feat.greater_dragonmark.json` | 643 B | Черта персонажа: **Великая драконья метка**; id dnd.feat.greater_dragonmark; запись есть в текущем каталоге. |
| 83 | `packages/dnd.feat.gunner.json` | 578 B | Черта персонажа: **Стрелок**; id dnd.feat.gunner; запись есть в текущем каталоге. |
| 84 | `packages/dnd.feat.harper_agent.json` | 552 B | Черта персонажа: **Агент Арфистов**; id dnd.feat.harper_agent; запись есть в текущем каталоге. |
| 85 | `packages/dnd.feat.healer.json` | 511 B | Черта персонажа: **Целитель**; id dnd.feat.healer; запись есть в текущем каталоге. |
| 86 | `packages/dnd.feat.heavily_armored.json` | 695 B | Черта персонажа: **Тяжелобронированный**; id dnd.feat.heavily_armored; запись есть в текущем каталоге. |
| 87 | `packages/dnd.feat.heavy_armor_master.json` | 715 B | Черта персонажа: **Мастер тяжелых доспехов**; id dnd.feat.heavy_armor_master; запись есть в текущем каталоге. |
| 88 | `packages/dnd.feat.holy_warrior.json` | 626 B | Черта персонажа: **Святой воитель**; id dnd.feat.holy_warrior; запись есть в текущем каталоге. |
| 89 | `packages/dnd.feat.infernal_constitution.json` | 701 B | Черта персонажа: **Адское телосложение**; id dnd.feat.infernal_constitution; запись есть в текущем каталоге. |
| 90 | `packages/dnd.feat.initiate_of_high_sorcery.json` | 627 B | Черта персонажа: **Адепт Высшего Волшебства**; id dnd.feat.initiate_of_high_sorcery; запись есть в текущем каталоге. |
| 91 | `packages/dnd.feat.inspiring_leader.json` | 629 B | Черта персонажа: **Вдохновляющий лидер**; id dnd.feat.inspiring_leader; запись есть в текущем каталоге. |
| 92 | `packages/dnd.feat.keen_mind.json` | 592 B | Черта персонажа: **Острый ум**; id dnd.feat.keen_mind; запись есть в текущем каталоге. |
| 93 | `packages/dnd.feat.knight_of_the_rose.json` | 601 B | Черта персонажа: **Рыцарь Розы**; id dnd.feat.knight_of_the_rose; запись есть в текущем каталоге. |
| 94 | `packages/dnd.feat.knight_of_the_sword.json` | 604 B | Черта персонажа: **Рыцарь Меча**; id dnd.feat.knight_of_the_sword; запись есть в текущем каталоге. |
| 95 | `packages/dnd.feat.lightly_armored.json` | 691 B | Черта персонажа: **Легкобронированный**; id dnd.feat.lightly_armored; запись есть в текущем каталоге. |
| 96 | `packages/dnd.feat.linguist.json` | 587 B | Черта персонажа: **Лингвист**; id dnd.feat.linguist; запись есть в текущем каталоге. |
| 97 | `packages/dnd.feat.lucky.json` | 508 B | Черта персонажа: **Везунчик**; id dnd.feat.lucky; запись есть в текущем каталоге. |
| 98 | `packages/dnd.feat.mage_slayer.json` | 540 B | Черта персонажа: **Убийца магов**; id dnd.feat.mage_slayer; запись есть в текущем каталоге. |
| 99 | `packages/dnd.feat.magic_initiate.json` | 545 B | Черта персонажа: **Адепт магии**; id dnd.feat.magic_initiate; запись есть в текущем каталоге. |
| 100 | `packages/dnd.feat.martial_adept.json` | 584 B | Черта персонажа: **Мастер боевых искусств**; id dnd.feat.martial_adept; запись есть в текущем каталоге. |
| 101 | `packages/dnd.feat.master_of_disguise.json` | 580 B | Черта персонажа: **Мастер маскировки**; id dnd.feat.master_of_disguise; запись есть в текущем каталоге. |
| 102 | `packages/dnd.feat.medic.json` | 531 B | Черта персонажа: **Полевой медик**; id dnd.feat.medic; запись есть в текущем каталоге. |
| 103 | `packages/dnd.feat.medium_armor_master.json` | 649 B | Черта персонажа: **Мастер средних доспехов**; id dnd.feat.medium_armor_master; запись есть в текущем каталоге. |
| 104 | `packages/dnd.feat.metamagic_adept.json` | 599 B | Черта персонажа: **Адепт метамагии**; id dnd.feat.metamagic_adept; запись есть в текущем каталоге. |
| 105 | `packages/dnd.feat.mobile.json` | 515 B | Черта персонажа: **Подвижный**; id dnd.feat.mobile; запись есть в текущем каталоге. |
| 106 | `packages/dnd.feat.moderately_armored.json` | 756 B | Черта персонажа: **Умеренно бронированный**; id dnd.feat.moderately_armored; запись есть в текущем каталоге. |
| 107 | `packages/dnd.feat.monastic_training.json` | 661 B | Черта персонажа: **Монастырская выучка**; id dnd.feat.monastic_training; запись есть в текущем каталоге. |
| 108 | `packages/dnd.feat.mounted_combatant.json` | 540 B | Черта персонажа: **Всадник**; id dnd.feat.mounted_combatant; запись есть в текущем каталоге. |
| 109 | `packages/dnd.feat.necromantic_scholar.json` | 663 B | Черта персонажа: **Знаток некромантии**; id dnd.feat.necromantic_scholar; запись есть в текущем каталоге. |
| 110 | `packages/dnd.feat.nomad.json` | 617 B | Черта персонажа: **Странник пустошей**; id dnd.feat.nomad; запись есть в текущем каталоге. |
| 111 | `packages/dnd.feat.observant.json` | 657 B | Черта персонажа: **Наблюдательный**; id dnd.feat.observant; запись есть в текущем каталоге. |
| 112 | `packages/dnd.feat.orcish_aggression.json` | 673 B | Черта персонажа: **Орочья агрессия**; id dnd.feat.orcish_aggression; запись есть в текущем каталоге. |
| 113 | `packages/dnd.feat.orcish_fury.json` | 690 B | Черта персонажа: **Орочья ярость**; id dnd.feat.orcish_fury; запись есть в текущем каталоге. |
| 114 | `packages/dnd.feat.perceptive.json` | 613 B | Черта персонажа: **Соколиный глаз**; id dnd.feat.perceptive; запись есть в текущем каталоге. |
| 115 | `packages/dnd.feat.piercer.json` | 636 B | Черта персонажа: **Пронзатель**; id dnd.feat.piercer; запись есть в текущем каталоге. |
| 116 | `packages/dnd.feat.poisoner.json` | 526 B | Черта персонажа: **Отравитель**; id dnd.feat.poisoner; запись есть в текущем каталоге. |
| 117 | `packages/dnd.feat.polearm_master.json` | 595 B | Черта персонажа: **Мастер древкового оружия**; id dnd.feat.polearm_master; запись есть в текущем каталоге. |
| 118 | `packages/dnd.feat.prodigy.json` | 574 B | Черта персонажа: **Вундеркинд**; id dnd.feat.prodigy; запись есть в текущем каталоге. |
| 119 | `packages/dnd.feat.pyromaniac.json` | 588 B | Черта персонажа: **Пироман**; id dnd.feat.pyromaniac; запись есть в текущем каталоге. |
| 120 | `packages/dnd.feat.resilient.json` | 709 B | Черта персонажа: **Закаленный**; id dnd.feat.resilient; запись есть в текущем каталоге. |
| 121 | `packages/dnd.feat.revenant_blade.json` | 708 B | Черта персонажа: **Клинок ревенанта**; id dnd.feat.revenant_blade; запись есть в текущем каталоге. |
| 122 | `packages/dnd.feat.ritual_caster.json` | 672 B | Черта персонажа: **Заклинатель ритуалов**; id dnd.feat.ritual_caster; запись есть в текущем каталоге. |
| 123 | `packages/dnd.feat.runic_carver.json` | 622 B | Черта персонажа: **Рунный резчик**; id dnd.feat.runic_carver; запись есть в текущем каталоге. |
| 124 | `packages/dnd.feat.savage_attacker.json` | 576 B | Черта персонажа: **Зверский атакующий**; id dnd.feat.savage_attacker; запись есть в текущем каталоге. |
| 125 | `packages/dnd.feat.scion_of_the_outer_planes.json` | 758 B | Черта персонажа: **Наследник Внешних Планов**; id dnd.feat.scion_of_the_outer_planes; запись есть в текущем каталоге. |
| 126 | `packages/dnd.feat.sea_faring.json` | 544 B | Черта персонажа: **Морской волк**; id dnd.feat.sea_faring; запись есть в текущем каталоге. |
| 127 | `packages/dnd.feat.second_chance.json` | 705 B | Черта персонажа: **Второй шанс**; id dnd.feat.second_chance; запись есть в текущем каталоге. |
| 128 | `packages/dnd.feat.sentinel.json` | 513 B | Черта персонажа: **Часовой**; id dnd.feat.sentinel; запись есть в текущем каталоге. |
| 129 | `packages/dnd.feat.shadow_dancer.json` | 629 B | Черта персонажа: **Теневой танцор**; id dnd.feat.shadow_dancer; запись есть в текущем каталоге. |
| 130 | `packages/dnd.feat.shadow_strike.json` | 619 B | Черта персонажа: **Удар из тени**; id dnd.feat.shadow_strike; запись есть в текущем каталоге. |
| 131 | `packages/dnd.feat.shadow_touched.json` | 684 B | Черта персонажа: **Меченый тенью**; id dnd.feat.shadow_touched; запись есть в текущем каталоге. |
| 132 | `packages/dnd.feat.sharpshooter.json` | 525 B | Черта персонажа: **Снайпер**; id dnd.feat.sharpshooter; запись есть в текущем каталоге. |
| 133 | `packages/dnd.feat.shield_bash_master.json` | 559 B | Черта персонажа: **Щитовой удар**; id dnd.feat.shield_bash_master; запись есть в текущем каталоге. |
| 134 | `packages/dnd.feat.shield_master.json` | 546 B | Черта персонажа: **Мастер щитов**; id dnd.feat.shield_master; запись есть в текущем каталоге. |
| 135 | `packages/dnd.feat.silver_tongue.json` | 625 B | Черта персонажа: **Язык без костей**; id dnd.feat.silver_tongue; запись есть в текущем каталоге. |
| 136 | `packages/dnd.feat.skill_expert.json` | 737 B | Черта персонажа: **Эксперт навыков**; id dnd.feat.skill_expert; запись есть в текущем каталоге. |
| 137 | `packages/dnd.feat.skilled.json` | 506 B | Черта персонажа: **Умелец**; id dnd.feat.skilled; запись есть в текущем каталоге. |
| 138 | `packages/dnd.feat.skulker.json` | 548 B | Черта персонажа: **Шпион**; id dnd.feat.skulker; запись есть в текущем каталоге. |
| 139 | `packages/dnd.feat.spell_sniper.json` | 617 B | Черта персонажа: **Заклинательный снайпер**; id dnd.feat.spell_sniper; запись есть в текущем каталоге. |
| 140 | `packages/dnd.feat.squat_nimbleness.json` | 743 B | Черта персонажа: **Приземистая ловкость**; id dnd.feat.squat_nimbleness; запись есть в текущем каталоге. |
| 141 | `packages/dnd.feat.squire_of_solamnia.json` | 607 B | Черта персонажа: **Соламнийский оруженосец**; id dnd.feat.squire_of_solamnia; запись есть в текущем каталоге. |
| 142 | `packages/dnd.feat.stealthy.json` | 546 B | Черта персонажа: **Теневой лазутчик**; id dnd.feat.stealthy; запись есть в текущем каталоге. |
| 143 | `packages/dnd.feat.storm_herald.json` | 546 B | Черта персонажа: **Буревестник**; id dnd.feat.storm_herald; запись есть в текущем каталоге. |
| 144 | `packages/dnd.feat.strike_of_the_giants.json` | 706 B | Черта персонажа: **Удар великанов**; id dnd.feat.strike_of_the_giants; запись есть в текущем каталоге. |
| 145 | `packages/dnd.feat.survivalist.json` | 607 B | Черта персонажа: **Выживальщик**; id dnd.feat.survivalist; запись есть в текущем каталоге. |
| 146 | `packages/dnd.feat.tactician.json` | 601 B | Черта персонажа: **Полевой командир**; id dnd.feat.tactician; запись есть в текущем каталоге. |
| 147 | `packages/dnd.feat.tavern_brawler.json` | 678 B | Черта персонажа: **Тавернный драчун**; id dnd.feat.tavern_brawler; запись есть в текущем каталоге. |
| 148 | `packages/dnd.feat.telekinetic.json` | 669 B | Черта персонажа: **Телекинетик**; id dnd.feat.telekinetic; запись есть в текущем каталоге. |
| 149 | `packages/dnd.feat.telepathic.json` | 650 B | Черта персонажа: **Телепат**; id dnd.feat.telepathic; запись есть в текущем каталоге. |
| 150 | `packages/dnd.feat.tough_hide.json` | 604 B | Черта персонажа: **Толстокожий**; id dnd.feat.tough_hide; запись есть в текущем каталоге. |
| 151 | `packages/dnd.feat.tough.json` | 500 B | Черта персонажа: **Крепыш**; id dnd.feat.tough; запись есть в текущем каталоге. |
| 152 | `packages/dnd.feat.unarmored_defense_feat.json` | 579 B | Черта персонажа: **Боевая закалка**; id dnd.feat.unarmored_defense_feat; запись есть в текущем каталоге. |
| 153 | `packages/dnd.feat.war_caster.json` | 595 B | Черта персонажа: **Боевой заклинатель**; id dnd.feat.war_caster; запись есть в текущем каталоге. |
| 154 | `packages/dnd.feat.warlock_pact_initiate.json` | 575 B | Черта персонажа: **Адепт договора**; id dnd.feat.warlock_pact_initiate; запись есть в текущем каталоге. |
| 155 | `packages/dnd.feat.weapon_master.json` | 663 B | Черта персонажа: **Мастер оружия**; id dnd.feat.weapon_master; запись есть в текущем каталоге. |
| 156 | `packages/dnd.feat.wood_elf_magic.json` | 608 B | Черта персонажа: **Магия лесных эльфов**; id dnd.feat.wood_elf_magic; запись есть в текущем каталоге. |
| 157 | `packages/dnd.feat.zealot.json` | 506 B | Черта персонажа: **Фанатик**; id dnd.feat.zealot; запись есть в текущем каталоге. |
| 158 | `packages/dnd.items.armor.json` | 35024 B | Набор инвентаря: **Сборник: Броня**; id dnd.items.armor; запись есть в текущем каталоге. |
| 159 | `packages/dnd.items.consumables.json` | 19577 B | Набор инвентаря: **Сборник: Расходники**; id dnd.items.consumables; запись есть в текущем каталоге. |
| 160 | `packages/dnd.items.junk.json` | 10363 B | Набор инвентаря: **Сборник: Хлам**; id dnd.items.junk; запись есть в текущем каталоге. |
| 161 | `packages/dnd.items.materials.json` | 14045 B | Набор инвентаря: **Сборник: Материалы**; id dnd.items.materials; запись есть в текущем каталоге. |
| 162 | `packages/dnd.items.weapons.json` | 59617 B | Набор инвентаря: **Сборник: Оружие**; id dnd.items.weapons; запись есть в текущем каталоге. |
| 163 | `packages/dnd.race.aarakocra.json` | 3420 B | Раса персонажа: **Ааракрира**; id dnd.race.aarakocra; запись есть в текущем каталоге. |
| 164 | `packages/dnd.race.aasimar.json` | 3514 B | Раса персонажа: **Аасимар**; id dnd.race.aasimar; запись есть в текущем каталоге. |
| 165 | `packages/dnd.race.autognome.json` | 3722 B | Раса персонажа: **Автоном**; id dnd.race.autognome; запись есть в текущем каталоге. |
| 166 | `packages/dnd.race.bugbear.json` | 3398 B | Раса персонажа: **Багбир**; id dnd.race.bugbear; запись есть в текущем каталоге. |
| 167 | `packages/dnd.race.centaur.json` | 3562 B | Раса персонажа: **Кентавр**; id dnd.race.centaur; запись есть в текущем каталоге. |
| 168 | `packages/dnd.race.changeling.json` | 6160 B | Раса персонажа: **Перевертыш (Чейнджлинг)**; id dnd.race.changeling; запись есть в текущем каталоге. |
| 169 | `packages/dnd.race.dhampir.json` | 6074 B | Раса персонажа: **Дампир**; id dnd.race.dhampir; запись есть в текущем каталоге. |
| 170 | `packages/dnd.race.fairy.json` | 3512 B | Раса персонажа: **Фея (Fairy)**; id dnd.race.fairy; запись есть в текущем каталоге. |
| 171 | `packages/dnd.race.firbolg.json` | 3813 B | Раса персонажа: **Фирболг**; id dnd.race.firbolg; запись есть в текущем каталоге. |
| 172 | `packages/dnd.race.full_orc.json` | 3594 B | Раса персонажа: **Орк**; id dnd.race.full_orc; запись есть в текущем каталоге. |
| 173 | `packages/dnd.race.genasi_air.json` | 3536 B | Раса персонажа: **Дженази (Воздух)**; id dnd.race.genasi_air; запись есть в текущем каталоге. |
| 174 | `packages/dnd.race.genasi_earth.json` | 3532 B | Раса персонажа: **Дженази (Земля)**; id dnd.race.genasi_earth; запись есть в текущем каталоге. |
| 175 | `packages/dnd.race.genasi_fire.json` | 3609 B | Раса персонажа: **Дженази (Огонь)**; id dnd.race.genasi_fire; запись есть в текущем каталоге. |
| 176 | `packages/dnd.race.genasi_water.json` | 3740 B | Раса персонажа: **Дженази (Вода)**; id dnd.race.genasi_water; запись есть в текущем каталоге. |
| 177 | `packages/dnd.race.githyanki.json` | 6047 B | Раса персонажа: **Гитъянки**; id dnd.race.githyanki; запись есть в текущем каталоге. |
| 178 | `packages/dnd.race.githzerai.json` | 3278 B | Раса персонажа: **Гитцерай**; id dnd.race.githzerai; запись есть в текущем каталоге. |
| 179 | `packages/dnd.race.goblin.json` | 3642 B | Раса персонажа: **Гоблин**; id dnd.race.goblin; запись есть в текущем каталоге. |
| 180 | `packages/dnd.race.goliath.json` | 3391 B | Раса персонажа: **Голиаф**; id dnd.race.goliath; запись есть в текущем каталоге. |
| 181 | `packages/dnd.race.hadozee.json` | 6116 B | Раса персонажа: **Хадози**; id dnd.race.hadozee; запись есть в текущем каталоге. |
| 182 | `packages/dnd.race.harengon.json` | 4062 B | Раса персонажа: **Харенгон (Зайцелюд)**; id dnd.race.harengon; запись есть в текущем каталоге. |
| 183 | `packages/dnd.race.hexblood.json` | 3605 B | Раса персонажа: **Ведьмокровный (Хексблад)**; id dnd.race.hexblood; запись есть в текущем каталоге. |
| 184 | `packages/dnd.race.hobgoblin.json` | 3738 B | Раса персонажа: **Хобгоблин**; id dnd.race.hobgoblin; запись есть в текущем каталоге. |
| 185 | `packages/dnd.race.kalashtar.json` | 6151 B | Раса персонажа: **Калаштар**; id dnd.race.kalashtar; запись есть в текущем каталоге. |
| 186 | `packages/dnd.race.kender.json` | 3263 B | Раса персонажа: **Кендер**; id dnd.race.kender; запись есть в текущем каталоге. |
| 187 | `packages/dnd.race.kenku.json` | 3260 B | Раса персонажа: **Кенku**; id dnd.race.kenku; запись есть в текущем каталоге. |
| 188 | `packages/dnd.race.kobold.json` | 3654 B | Раса персонажа: **Кобольд**; id dnd.race.kobold; запись есть в текущем каталоге. |
| 189 | `packages/dnd.race.lizardfolk.json` | 3986 B | Раса персонажа: **Людощур (Лизардфолк)**; id dnd.race.lizardfolk; запись есть в текущем каталоге. |
| 190 | `packages/dnd.race.loxodon.json` | 3829 B | Раса персонажа: **Локсадон**; id dnd.race.loxodon; запись есть в текущем каталоге. |
| 191 | `packages/dnd.race.minotaur.json` | 3415 B | Раса персонажа: **Минотавр**; id dnd.race.minotaur; запись есть в текущем каталоге. |
| 192 | `packages/dnd.race.myconid.json` | 3562 B | Раса персонажа: **Миконид (Гриболюд)**; id dnd.race.myconid; запись есть в текущем каталоге. |
| 193 | `packages/dnd.race.owlin.json` | 6742 B | Раса персонажа: **Совлин (Совоподобный)**; id dnd.race.owlin; запись есть в текущем каталоге. |
| 194 | `packages/dnd.race.plasmoid.json` | 6702 B | Раса персонажа: **Плазмоид**; id dnd.race.plasmoid; запись есть в текущем каталоге. |
| 195 | `packages/dnd.race.reborn.json` | 6215 B | Раса персонажа: **Возрожденный (Риборн)**; id dnd.race.reborn; запись есть в текущем каталоге. |
| 196 | `packages/dnd.race.satyr.json` | 3402 B | Раса персонажа: **Сатир**; id dnd.race.satyr; запись есть в текущем каталоге. |
| 197 | `packages/dnd.race.shifter.json` | 3622 B | Раса персонажа: **Шифтер**; id dnd.race.shifter; запись есть в текущем каталоге. |
| 198 | `packages/dnd.race.simic_hybrid.json` | 3552 B | Раса персонажа: **Симикский гибрид**; id dnd.race.simic_hybrid; запись есть в текущем каталоге. |
| 199 | `packages/dnd.race.tabaxi.json` | 5995 B | Раса персонажа: **Табакси**; id dnd.race.tabaxi; запись есть в текущем каталоге. |
| 200 | `packages/dnd.race.tortle.json` | 3324 B | Раса персонажа: **Тортл**; id dnd.race.tortle; запись есть в текущем каталоге. |
| 201 | `packages/dnd.race.triton.json` | 3605 B | Раса персонажа: **Тритон**; id dnd.race.triton; запись есть в текущем каталоге. |
| 202 | `packages/dnd.race.vedalken.json` | 6312 B | Раса персонажа: **Ведилк**; id dnd.race.vedalken; запись есть в текущем каталоге. |
| 203 | `packages/dnd.race.warforged.json` | 6461 B | Раса персонажа: **Кованый (Варфорджед)**; id dnd.race.warforged; запись есть в текущем каталоге. |
| 204 | `packages/dnd.race.yuan_ti.json` | 3984 B | Раса персонажа: **Юань-ти (Чистокровный)**; id dnd.race.yuan_ti; запись есть в текущем каталоге. |
| 205 | `README.md` | 2565 B | Обзор и статус реестра, ограничения и ссылки для разработчиков. |
| 206 | `schemas/catalog-entry-v1.schema.json` | 2876 B | JSON Schema каталожной записи (обязательные поля манифеста, URL, платформа, SHA-256). |
| 207 | `schemas/package-manifest-v1.schema.json` | 1910 B | Старый/проектируемый формат пакетного архива; не путать с исполняемым JSON каталога. |

## Правила для ChatGPT

1. Объясни человеку, как устроены каталоги и пакеты, **на примере реального файла из этого списка**. Прочитай руководство и смежные схемы.
2. Всегда найди ID в актуальном каталоге, прежде чем создавать новый файл. Для изменения одной расы не переписывай сотни других записей.
3. Изменения в `packages/` и `catalog/` должны соответствовать друг другу по ID, версии, доступному URL, точной длине и SHA-256. Выдуманные хеши/результаты тестов запрещены.
4. Отмечай, что проверено фактически, а что ещё нужно проверить устройством. Не обещай совместимость для неизвестных эффектов Unity.
5. Публикация в `main` — публикация для **всех пользователей**, не приватный тестовый режим. Черновик до публикации держи в рабочей ветке.

Обновление22.10.2026: MOD_AUTHOR_GUIDE теперь указывает Assets v5 для Unity1.00.24+; v4 сохранён для старых клиентов. Собственные пакеты/каталог Content v3 и их SHA не изменялись.

## Подготовленные расширенные сборники v4

- `catalog/v4/index.json` — 169663 B; расширенные сборники, только для нового клиента v4.
- `packages/dnd.items.weapons-2.0.0.json` — 1398669 B; расширенные сборники, только для нового клиента v4.
- `packages/dnd.items.armor-2.0.0.json` — 622470 B; расширенные сборники, только для нового клиента v4.
- `packages/dnd.items.materials-2.0.0.json` — 380897 B; расширенные сборники, только для нового клиента v4.
- `packages/dnd.items.consumables-2.0.0.json` — 125041 B; расширенные сборники, только для нового клиента v4.
- `packages/dnd.items.junk-2.0.0.json` — 181683 B; расширенные сборники, только для нового клиента v4.
- `tools/build_item_collections.py` — 14811 B; расширенные сборники, только для нового клиента v4.
- `tools/verify_item_collections.py` — 1693 B; расширенные сборники, только для нового клиента v4.
- `docs/ITEM_COLLECTIONS_V4.md` — 4980 B; расширенные сборники, только для нового клиента v4.

## Совместимые опциональные тома 1.1.0 для живого v3

Каталог v3: 224 записи; 36 томов, 3291 предмет. См. `docs/WORKSHOP_ITEM_VOLUMES.md`.

- `.gitignore` — 32 B; совместимая опциональная поставка предметов.
- `docs/WORKSHOP_ITEM_VOLUMES.md` — 8422 B; совместимая опциональная поставка предметов.
- `sources/workshop-volumes-1.1.0.json` — 577111 B; совместимая опциональная поставка предметов.
- `tools/build_workshop_volumes.py` — 11004 B; совместимая опциональная поставка предметов.
- `tools/verify_workshop_volumes.py` — 3101 B; совместимая опциональная поставка предметов.
- `tools/compatibility-tests/ContentCompatibility.csproj` — 399 B; совместимая опциональная поставка предметов.
- `tools/compatibility-tests/Program.cs` — 5654 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.armor-1.1.0.json` — 86910 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.consumables-1.1.0.json` — 60948 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.junk-1.1.0.json` — 44105 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.materials-1.1.0.json` — 51492 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.volume02.armor-1.1.0.json` — 97547 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.volume02.consumables-1.1.0.json` — 60121 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.volume02.junk-1.1.0.json` — 43416 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.volume02.materials-1.1.0.json` — 49596 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.volume02.weapons-1.1.0.json` — 103436 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.volume03.armor-1.1.0.json` — 97863 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.volume03.consumables-1.1.0.json` — 32912 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.volume03.junk-1.1.0.json` — 43785 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.volume03.materials-1.1.0.json` — 47822 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.volume03.weapons-1.1.0.json` — 105056 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.volume04.armor-1.1.0.json` — 98876 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.volume04.junk-1.1.0.json` — 43961 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.volume04.materials-1.1.0.json` — 44556 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.volume04.weapons-1.1.0.json` — 101626 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.volume05.armor-1.1.0.json` — 99016 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.volume05.junk-1.1.0.json` — 19005 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.volume05.materials-1.1.0.json` — 40507 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.volume05.weapons-1.1.0.json` — 103276 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.volume06.armor-1.1.0.json` — 89535 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.volume06.materials-1.1.0.json` — 11222 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.volume06.weapons-1.1.0.json` — 111572 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.volume07.armor-1.1.0.json` — 43733 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.volume07.weapons-1.1.0.json` — 109382 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.volume08.armor-1.1.0.json` — 25563 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.volume08.weapons-1.1.0.json` — 110228 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.volume09.weapons-1.1.0.json` — 115200 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.volume10.weapons-1.1.0.json` — 111068 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.volume11.weapons-1.1.0.json` — 114748 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.volume12.weapons-1.1.0.json` — 116602 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.volume13.weapons-1.1.0.json` — 108444 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.volume14.weapons-1.1.0.json` — 18056 B; совместимая опциональная поставка предметов.
- `packages/dnd.items.weapons-1.1.0.json` — 98009 B; совместимая опциональная поставка предметов.
