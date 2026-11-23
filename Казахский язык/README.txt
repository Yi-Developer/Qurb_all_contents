Qurb · языковой пакет: Казахский язык (kk)
Файл: translations_kk.db  ·  1.38 МБ
Версия пакета: 12  ·  тег контента: main

Внутри (SQLite, данные — gzip):
  system     — строки интерфейса: 1352 (экраны v114: 368, названия сур: 114)
  quran      — переводы Корана: t_kazakh_altai.json
  dua, azkar (азкары, утро и вечер, хадисы), names99, holidays,
  policies — тексты разделов
  geo_cities, geo_countries — названия городов и стран

Не редактируйте .db вручную: строки интерфейса правятся в
system/kk.json, содержимое — в dua/, azkar/, dhikr/, names/,
holidays/ (kk.json.gz), затем python3 tools/build_packs.py kk.
