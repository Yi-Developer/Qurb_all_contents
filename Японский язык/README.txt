Qurb · языковой пакет: Японский язык (ja)
<<<<<<< HEAD
Файл: translations_ja.db  ·  1.25 МБ
=======
Файл: translations_ja.db  ·  1.26 МБ
>>>>>>> d1cc76aff930b65e92ad16b044043d8b055d054d
Версия пакета: 9  ·  тег контента: main

Внутри (SQLite, данные — gzip):
  system     — строки интерфейса: 1309 (экраны v114: 364, названия сур: 114)
  quran      — переводы Корана: t_japanese_saeedsato.json
  dua, azkar (азкары, утро и вечер, хадисы), names99, holidays,
  policies — тексты разделов
  geo_cities, geo_countries — названия городов и стран

Не редактируйте .db вручную: строки интерфейса правятся в
system/ja.json, содержимое — в dua/, azkar/, dhikr/, names/,
holidays/ (ja.json.gz), затем python3 tools/build_packs.py ja.
