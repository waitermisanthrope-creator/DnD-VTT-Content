# Aquatic Races Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Пять описанных подводных рас доступны для создания листа через мастерскую.
**Architecture:** Существующие JSON race и collection пакеты, без изменений Unity.
**Tech Stack:** UTF-8 JSON, Python для проверки байтов, C# WorkshopStore.
**Spec:** docs/superpowers/specs/2026-11-10-aquatic-races-design.md

## Global Constraints

Стабильный triton ID, неизменные старые payloads; новые URL для новых версий; Content v3; никаких 3D, скриптов и автоматизации возрастных эффектов.

## Review Focus

Описание остаётся в сохранённом листе; возраст без перекрытий и ложной каноничности; мерроу сохраняет большой размер и водное дыхание; сборники имеют одинаковые members/dependencies; старые файлы и посторонние записи неизменны.

## Task 1: Payloads and catalog

Files: packages/dnd.race.{kuo_toa,merrow,sahuagin,locathah}-1.0.0.json; packages/dnd.race.triton-1.0.1.json; packages/dnd.collections.aquatic-races-1.0.0.json; packages/dnd.collections.races-1.0.1.json; catalog/v3/index.json; docs/AQUATIC_RACES.md; docs/FILE_ATLAS.md.

- [x] Подготовить оригинальные описания, справочные возрастные этапы и поддержанные параметры seed.
- [x] Сохранить версии/ID; вычислить точные UTF-8 bytes и SHA-256; расширить общий сборник.
- [x] Проверить все новые записи схемой, все ссылки/зависимости и неизменность других записей.
- [x] Запустить реальные обработчики установки/создания/сохранения, если доступен .NET; записать пределы проверки.
- [x] Обновить документацию и атлас, провести независимое ревью.

## Task 2: Publish and verify

- [ ] Опубликовать проверенный снимок через GitHub с проверкой текущей вершины ветки.
- [ ] Скачать живой каталог и семь payloads, проверить размеры и SHA-256, записать результат.
- [ ] Сообщить пользователю название сборника и действия в мастерской.

Task 1: complete. Проверки: AQUATIC_CONTENT_PASS; AQUATIC_RUNTIME_PASS189 (независимо повторён); PUBLISHED_CLIENT_COMPATIBILITY_PASS1096; CHARACTER_DELETE_PASS119. Ревью: существенных замечаний нет. Общий workshop test остановился на отсутствующем release-only spiral tray, не заявлен пройденным.
