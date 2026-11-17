Qurb · языковой пакет: Корейский язык (ko)
Файл: translations_ko.db  ·  1.53 МБ
Версия пакета: 8  ·  тег контента: main

Внутри (SQLite, данные — gzip):
  system     — строки интерфейса: 1309 (экраны v114: 364, названия сур: 114)
  quran      — переводы Корана: t_korean_hamedchoi.json, t_korean_rwwad.json
  dua, azkar (азкары, утро и вечер, хадисы), names99, holidays,
  policies — тексты разделов
  geo_cities, geo_countries — названия городов и стран

Не редактируйте .db вручную: строки интерфейса правятся в
system/ko.json, содержимое — в dua/, azkar/, dhikr/, names/,
holidays/ (ko.json.gz), затем python3 tools/build_packs.py ko.
