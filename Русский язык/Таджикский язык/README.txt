Qurb · языковой пакет: Таджикский язык (tg)
Файл: translations_tg.db  ·  1.46 МБ
Версия пакета: 9  ·  тег контента: main

Внутри (SQLite, данные — gzip):
  system     — строки интерфейса: 1309 (экраны v114: 364, названия сур: 114)
  quran      — переводы Корана: t_tajik_arifi.json
  dua, azkar (азкары, утро и вечер, хадисы), names99, holidays,
  policies — тексты разделов
  geo_cities, geo_countries — названия городов и стран

Не редактируйте .db вручную: строки интерфейса правятся в
system/tg.json, содержимое — в dua/, azkar/, dhikr/, names/,
holidays/ (tg.json.gz), затем python3 tools/build_packs.py tg.
