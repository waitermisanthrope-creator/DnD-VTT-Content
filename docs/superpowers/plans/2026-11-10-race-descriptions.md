# Race Descriptions Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Все47 рас общего сборника имеют содержательное описание и возраст в создании и сохранённом листе.
**Architecture:** Существующий формат race/collection Content v3; версия каждого изменённого payload повышается, старый URL сохраняется.
**Tech Stack:** JSON, Python verification, реальные C# WorkshopStore/CharacterCreation.
**Spec:** docs/superpowers/specs/2026-11-10-race-descriptions-design.md

## Global Constraints

42 обновления описаний, пять водных пакетов неизменны; ID/имена/механики/choices сохраняются; общий сборник47, версия1.0.2. Возрастные ориентиры без выдуманной каноничности и без автоматических эффектов.

## Review Focus

Возраст искусственных существ и родословных; неподдержанные способности не обещаются; отсутствие изменения механик; сохранение описаний после выбора языка/сохранения; обновление зависимостей уже установленного общего сборника.

## Task 1: Data and verification

- [x] Воспроизвести отсутствие описаний проверкой всех47 пакетов.
- [x] Подготовить42 описания с возрастом, версии и общий сборник1.0.2.
- [x] Проверить schema/SHA/bytes, старые payloads и все игровые поля против201c107.
- [x] Проверить установку/обновление/создание/сохранение всех47 рас через C# для двух платформенных селекторов.
- [x] Ревью текстов/совместимости, обновление документации и атласа.

## Task 2: Delivery

- [ ] Опубликовать в живой Content v3 с проверкой вершины ветки.
- [ ] Проверить живой каталог и43 скачиваемых новых payloads; дать инструкцию обновления.

Task 1: complete. RED: old demo lacked lore/age. GREEN: RACE_DESCRIPTIONS_CONTENT_PASS; RACE_DESCRIPTIONS_RUNTIME_PASS1188; AQUATIC_RUNTIME_PASS189. Independent review found a false UI-selection implication for simic hybrid; corrected to narrative-only wording in source/payload/manifest and reverified. No mechanical or historical payload changes. Native device GUI not tested.
