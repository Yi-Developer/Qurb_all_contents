Qurb · языковой пакет: Арабский язык (ar)
Файл: translations_ar.db  ·  0.99 МБ
Версия пакета: 10  ·  тег контента: main

Внутри (SQLite, данные — gzip):
  system     — строки интерфейса: 1583 (экраны v114: 368, названия сур: 114)
  quran      — переводы Корана: нет (арабский текст встроен)
  dua, azkar (азкары, утро и вечер, хадисы), names99, holidays,
  policies — тексты разделов
  geo_cities, geo_countries — названия городов и стран

Не редактируйте .db вручную: строки интерфейса правятся в
system/ar.json, содержимое — в dua/, azkar/, dhikr/, names/,
holidays/ (ar.json.gz), затем python3 tools/build_packs.py ar.
