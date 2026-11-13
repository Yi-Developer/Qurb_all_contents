Qurb · языковой пакет: Казахский язык (kk)
Файл: translations_kk.db  ·  1.35 МБ
Версия пакета: 7  ·  тег контента: main

Внутри (SQLite, данные — gzip):
  system     — строки интерфейса: 1048 (экраны v114: 364, названия сур: 114)
  quran      — переводы Корана: t_kazakh_altai.json
  dua, azkar, names99, holidays, policies — тексты разделов
  geo_cities, geo_countries — названия городов и стран

Не редактируйте .db вручную: строки интерфейса правятся в
system/kk.json, затем python3 tools/build_packs.py kk.
