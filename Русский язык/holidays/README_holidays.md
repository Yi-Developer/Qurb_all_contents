# holidays — строки праздников и важных дней (по языкам)

Дополнение к репозиторию Qurb-content. Кладётся в папку `holidays/`.
Приложение докачивает `holidays/<lang>.json.gz` при установке языка и кэширует.

## Файлы
- `holidays/<lang>.json.gz` — {ключ: текст} для языка (10 языков).
- `holidays/index.json` — манифест.

Ключи: `holiday.*`, `greeting.*`, `reminder.*`, `friday.*`, `event.*`, `arafah.*` и т.п.
Отсутствующий ключ в языке => английский fallback (встроен в приложение).

## Ссылки jsDelivr (после релиза тега)
```
https://cdn.jsdelivr.net/gh/Yi-Developer/Qurb-content@1.1.0/holidays/ru.json.gz
https://cdn.jsdelivr.net/gh/Yi-Developer/Qurb-content@1.1.0/holidays/index.json
```
