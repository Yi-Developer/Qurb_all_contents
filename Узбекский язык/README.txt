Qurb · языковой пакет: Узбекский язык (uz)
Файл: translations_uz.db  ·  1.78 МБ
Версия пакета: 10  ·  тег контента: main

Внутри (SQLite, данные — gzip):
  system     — строки интерфейса: 1328 (экраны v114: 368, названия сур: 114)
  quran      — переводы Корана: t_uzbek_mansour.json, t_uzbek_rwwad.json
  dua, azkar (азкары, утро и вечер, хадисы), names99, holidays,
  policies — тексты разделов
  geo_cities, geo_countries — названия городов и стран

Не редактируйте .db вручную: строки интерфейса правятся в
system/uz.json, содержимое — в dua/, azkar/, dhikr/, names/,
holidays/ (uz.json.gz), затем python3 tools/build_packs.py uz.
