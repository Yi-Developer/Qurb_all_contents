Qurb · языковой пакет: Азербайджанский язык (az)
Файл: translations_az.db  ·  1.08 МБ
Версия пакета: 3  ·  тег контента: main

Внутри (SQLite, данные — gzip):
  system     — строки интерфейса: 650 (экраны v114: 5, названия сур: 114)
  quran      — переводы Корана: t_azeri_musayev.json
  dua, azkar, names99, holidays, policies — тексты разделов
  geo_cities, geo_countries — названия городов и стран

Не редактируйте .db вручную: строки интерфейса правятся в
system/az.json, затем python3 tools/build_packs.py az.
