Qurb · языковой пакет: Арабский язык (ar)
Файл: translations_ar.db  ·  0.98 МБ
Версия пакета: 4  ·  тег контента: main

Внутри (SQLite, данные — gzip):
  system     — строки интерфейса: 1385 (экраны v114: 361, названия сур: 114)
  quran      — переводы Корана: нет (арабский текст встроен)
  dua, azkar, names99, holidays, policies — тексты разделов
  geo_cities, geo_countries — названия городов и стран

Не редактируйте .db вручную: строки интерфейса правятся в
system/ar.json, затем python3 tools/build_packs.py ar.
