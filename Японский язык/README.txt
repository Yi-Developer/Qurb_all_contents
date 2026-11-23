Qurb · языковой пакет: Японский язык (ja)
Файл: translations_ja.db  ·  1.27 МБ
Версия пакета: 12  ·  тег контента: main

Внутри (SQLite, данные — gzip):
  system     — строки интерфейса: 1313 (экраны v114: 368, названия сур: 114)
  quran      — переводы Корана: t_japanese_saeedsato.json
  dua, azkar (азкары, утро и вечер, хадисы), names99, holidays,
  policies — тексты разделов
  geo_cities, geo_countries — названия городов и стран

Не редактируйте .db вручную: строки интерфейса правятся в
system/ja.json, содержимое — в dua/, azkar/, dhikr/, names/,
holidays/ (ja.json.gz), затем python3 tools/build_packs.py ja.
