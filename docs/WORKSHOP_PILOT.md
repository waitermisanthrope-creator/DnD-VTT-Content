> 2026-10-20 status update: the public CC0 Lanternfolk package and two Assets JSON demo packages are published and integrated in the experimental Unity source. C# storage/creation tests and public URL/hash checks pass; native runtime and AssetBundle publication still need verification. Earlier pilot notes below are historical.

# Мастерская DnD-VTT — пилот

## Для автора

Пока автоматическая отправка из Unity не реализована. Подготовьте **только данные**, укажите авторство, лицензию, ID, версию, тип материала, совместимую игровую систему и зависимости. Согласуйте с модератором **непубличный** канал передачи файла. Не публикуйте непроверенные архивы и чужие защищённые материалы в открытых Issues.

## Очередь модерации (пока ручная)

1. Получить пакет в закрытом канале и зафиксировать согласие автора на распространение.
2. Проверить лицензию, происхождение иллюстраций/моделей, вредоносные пути и исполняемый код, размер и зависимости.
3. Проверить manifest по JSON Schema и SHA-256, протестировать в Unity на поддерживаемой платформе.
4. Опубликовать **только одобренный** неизменяемый пакет и добавить его в `catalog/v1/index.json`.
5. Обновления — новая версия и новая ссылка, старые версии не заменять незаметно.

## Пилот проверки скачивания

- Каталог: `catalog/v1/index.json`.
- Пакет: `packages/demo-race.json`.
- Клиент Unity в `experiment/unity-vtt` настроен на оба URL.
- Подтверждено: обе ссылки и каталог 3D-ресурсов читаются через GitHub.
- **Не подтверждено:** успешная установка на телефоне, сборка APK 1.00.06 и загрузка AssetBundles.

## Публикация тяжёлых файлов

Тяжёлые бинарные модели не копировать в Git history. После проверки прав и зависимостей публиковать как Release assets в DnD-VTT-Assets. Для Android/Windows требуются отдельные Unity bundles и контрольные суммы.
