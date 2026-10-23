## Профильные инструменты и сломанные вещи

56 новых профессиональных инструментов и 2798 связанных сломанных вариантов
долговечного снаряжения/предметов. Данные для будущего ремесленного ремонта
и «Починки», с сохранением ограничений заклинания. 37 опциональных пакетов;
автоматическое исполнение ремонта пока не добавлено.
[PROFESSIONAL_TOOLS_AND_REPAIR.md](docs/PROFESSIONAL_TOOLS_AND_REPAIR.md).

## Бытовые находки и общая анатомия

В живой мастерской опубликовано расширение: 464 уникальных новых предмета и 219 исследуемых
алхимических профилей общих частей существ, 25 опциональных дополнений.
Нож для масла, инструменты 15 профессий/мест, органы и ткани включая
селезёнку гуманоида. Существующие тома и сохранения не заменяются.
Всего со всеми прежними ингредиентами: 3875 предметов.
Подробности и реальные границы автоматизации:
[WORLD_LOOT_AND_ANATOMY.md](docs/WORLD_LOOT_AND_ANATOMY.md).

## Опциональные сборники для Unity1.00.34

В живом каталоге `catalog/v3/index.json` опубликованы 36 самостоятельных томов пяти
серий: 3291 предмет (оружие, броня/одежда, материалы, расходники, хлам).
Каждый том устанавливается отдельно, без зависимостей и обновления приложения.
Ещё 120 прежних алхимических ингредиентов остаются отдельными дополнениями.
Инструкция, реальные механики и результаты проверок:
[WORKSHOP_ITEM_VOLUMES.md](docs/WORKSHOP_ITEM_VOLUMES.md).

# DnD-VTT-Content

> **Новый участник команды / ChatGPT:** начни с [AGENTS.md](AGENTS.md), [пошагового руководства](docs/MOD_AUTHOR_GUIDE.md) и [атласа всех файлов](docs/FILE_ATLAS.md). Они учат создавать, публиковать, скачивать и тестировать модификации без пересборки Unity. Живой каталог: `catalog/v3/index.json`.

Public curated data registry for DnD-VTT Unity.

- `catalog/v1/index.json`: live catalog, including the original CC0 Lanternfolk test race.
- `packages/`: small declarative JSON, exact bytes and SHA-256 in catalog entries.
- `schemas/catalog-entry-v1.schema.json`: runtime manifest shared with Assets.
- Existing `demo-race.json` is retained as a historical prototype; it is no longer advertised as active content.

Unity integration is in `DnD-VTT/experiment/unity-vtt`. Storage and character integration have executable tests; device QA remains pending. Unsupported gameplay categories are shown as unavailable. No JavaScript, DLLs or user executable mods are accepted.

## Modular client 1.00.08

`catalog/v2/index.json` is consumed by Unity 1.00.08+. The v1 catalog remains unchanged for 1.00.07 and earlier clients. New packages are individual declarative race/class/feat records and project map documents; manifests pin exact SHA-256 and byte lengths. Existing character IDs remain unchanged. No executable plugins are included.

The mechanical metadata has newly written short descriptions, without republishing sourcebook prose or art. Stat changes, initial character parameters and pending choices use the currently supported Unity handlers; full combat automation and class advancement are not provided by these data packages. Extra classes that replace a race remain import-only in Unity. Feat stat bonuses are applied; other feat effects and additional prerequisites require manual handling.

Legacy third-party PNG/model files have NOT been relicensed or republished. Their exact provenance review remains BLOCKED. The new map-surface package provides original procedural checker patterns under the same legacy map keys; these are replacements, not byte-identical copies of the original images. The original files stay in the application's source repository, outside the minimal player's dependency graph. Maps preserve model references and show placeholders when a model package is missing.

## Modular client 1.00.11

`catalog/v3/index.json` adds ten small data packages: five inventory collections (188 item records), 47 crafting recipes and 29 materials, Alchemy 2.0 rules, and three collections of 40 ingredients. v1/v2 remain unchanged. Descriptive item prose is newly generated short metadata; original source snapshots stay in the application repository. Trusted native Unity handlers execute these data; downloaded JavaScript or assemblies are never used. Catalog byte lengths and SHA-256 refer to the exact published JSON.
