Qurb · языковой пакет: Русский язык (ru)
Файл: translations_ru.db  ·  2.07 МБ
Версия пакета: 9  ·  тег контента: main

Внутри (SQLite, данные — gzip):
  system     — строки интерфейса: 1348 (экраны v114: 364, названия сур: 114)
  quran      — переводы Корана: t_russian_abuadel.json, t_russian_kuliev.json
  dua, azkar (азкары, утро и вечер, хадисы), names99, holidays,
  policies — тексты разделов
  geo_cities, geo_countries — названия городов и стран

Не редактируйте .db вручную: строки интерфейса правятся в
system/ru.json, содержимое — в dua/, azkar/, dhikr/, names/,
holidays/ (ru.json.gz), затем python3 tools/build_packs.py ru.
