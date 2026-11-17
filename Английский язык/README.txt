Qurb · языковой пакет: Английский язык (en)
Файл: translations_en.db  ·  1.69 МБ
Версия пакета: 8  ·  тег контента: main

Внутри (SQLite, данные — gzip):
  system     — строки интерфейса: 1739 (экраны v114: 364, названия сур: 114)
  quran      — переводы Корана: t_english_hilali_khan.json, t_english_rwwad.json, t_english_saheeh.json
  dua, azkar (азкары, утро и вечер, хадисы), names99, holidays,
  policies — тексты разделов
  geo_cities, geo_countries — названия городов и стран

Не редактируйте .db вручную: строки интерфейса правятся в
system/en.json, содержимое — в dua/, azkar/, dhikr/, names/,
holidays/ (en.json.gz), затем python3 tools/build_packs.py en.
