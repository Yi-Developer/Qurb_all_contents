Qurb · языковой пакет: Турецкий язык (tr)
Файл: translations_tr.db  ·  1.68 МБ
Версия пакета: 8  ·  тег контента: main

Внутри (SQLite, данные — gzip):
  system     — строки интерфейса: 1348 (экраны v114: 364, названия сур: 114)
  quran      — переводы Корана: t_turkish_rwwad.json, t_turkish_shaban.json, t_turkish_shahin.json
  dua, azkar (азкары, утро и вечер, хадисы), names99, holidays,
  policies — тексты разделов
  geo_cities, geo_countries — названия городов и стран

Не редактируйте .db вручную: строки интерфейса правятся в
system/tr.json, содержимое — в dua/, azkar/, dhikr/, names/,
holidays/ (tr.json.gz), затем python3 tools/build_packs.py tr.
