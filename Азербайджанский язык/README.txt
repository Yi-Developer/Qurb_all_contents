Qurb · языковой пакет: Азербайджанский язык (az)
Файл: translations_az.db  ·  1.12 МБ
Версия пакета: 9  ·  тег контента: main

Внутри (SQLite, данные — gzip):
  system     — строки интерфейса: 1312 (экраны v114: 367, названия сур: 114)
  quran      — переводы Корана: t_azeri_musayev.json
  dua, azkar (азкары, утро и вечер, хадисы), names99, holidays,
  policies — тексты разделов
  geo_cities, geo_countries — названия городов и стран

Не редактируйте .db вручную: строки интерфейса правятся в
system/az.json, содержимое — в dua/, azkar/, dhikr/, names/,
holidays/ (az.json.gz), затем python3 tools/build_packs.py az.
