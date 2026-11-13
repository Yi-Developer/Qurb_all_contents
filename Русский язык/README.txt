Qurb · языковой пакет: Русский язык (ru)
Файл: translations_ru.db  ·  2.04 МБ
Версия пакета: 6  ·  тег контента: main

Внутри (SQLite, данные — gzip):
  system     — строки интерфейса: 1048 (экраны v114: 364, названия сур: 114)
  quran      — переводы Корана: t_russian_abuadel.json, t_russian_kuliev.json
  dua, azkar, names99, holidays, policies — тексты разделов
  geo_cities, geo_countries — названия городов и стран

Не редактируйте .db вручную: строки интерфейса правятся в
system/ru.json, затем python3 tools/build_packs.py ru.
