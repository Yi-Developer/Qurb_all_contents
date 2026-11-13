Qurb · языковой пакет: Узбекский язык (uz)
Файл: translations_uz.db  ·  1.75 МБ
Версия пакета: 4  ·  тег контента: main

Внутри (SQLite, данные — gzip):
  system     — строки интерфейса: 1021 (экраны v114: 361, названия сур: 114)
  quran      — переводы Корана: t_uzbek_mansour.json, t_uzbek_rwwad.json
  dua, azkar, names99, holidays, policies — тексты разделов
  geo_cities, geo_countries — названия городов и стран

Не редактируйте .db вручную: строки интерфейса правятся в
system/uz.json, затем python3 tools/build_packs.py uz.
