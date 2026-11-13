#!/usr/bin/env python3
"""Пересборка языковых пакетов Qurb из исходников.

Что делает (для каждого языка):
  1. берёт строки интерфейса из system/<код>.json и кладёт их в раздел
     `system` пакета <Язык>/translations_<код>.db (gzip, sha256, размеры);
  2. ставит metadata.pack_version и metadata.content_tag (см. ниже);
  3. сжимает базу (VACUUM), обновляет manifest.json и README.txt папки;
  4. печатает, каких строк интерфейса v114 (ui114.*) в языке не хватает
     по сравнению с английским — их нужно перевести.

Запуск из корня репозитория:
    python3 tools/build_packs.py            # пересобрать все языки
    python3 tools/build_packs.py ru kk      # только указанные

После сборки: закоммитить и отправить в main (тегов не нужно — приложение
читает ветку main, как 114). Если пакет должен перекачаться у всех,
поднимите PACK_VERSION здесь и kPackVersion в приложении; kPackBytes —
размеры, которые скрипт печатает в конце.
"""
import gzip
import hashlib
import json
import os
import sqlite3
import sys

PACK_VERSION = 6
CONTENT_TAG = 'main'

LANGS = {
    'ar': 'Арабский язык',
    'en': 'Английский язык',
    'ru': 'Русский язык',
    'kk': 'Казахский язык',
    'ky': 'Кыргызский язык',
    'az': 'Азербайджанский язык',
    'uz': 'Узбекский язык',
    'tg': 'Таджикский язык',
    'tr': 'Турецкий язык',
    'ja': 'Японский язык',
    'ko': 'Корейский язык',
}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_system(code):
    with open(os.path.join(ROOT, 'system', f'{code}.json'), encoding='utf-8') as f:
        data = json.load(f)
    bad = [k for k, v in data.items() if not isinstance(v, str)]
    if bad:
        raise SystemExit(f'system/{code}.json: не строки у ключей {bad[:5]}')
    return dict(sorted(data.items()))


def build(code, en_keys):
    folder = LANGS[code]
    db_path = os.path.join(ROOT, folder, f'translations_{code}.db')
    strings = load_system(code)
    raw = json.dumps(strings, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    packed = gzip.compress(raw, compresslevel=9, mtime=0)

    con = sqlite3.connect(db_path)
    cur = con.cursor()
    name = f'system_{code}.json'
    cur.execute("DELETE FROM resources WHERE section='system'")
    cur.execute(
        'INSERT INTO resources (section, resource_name, content_type, compression,'
        ' data, original_size, stored_size, sha256) VALUES (?,?,?,?,?,?,?,?)',
        ('system', name, 'json', 'gzip', packed, len(raw), len(packed),
         hashlib.sha256(raw).hexdigest()))
    meta = {
        'pack_version': str(PACK_VERSION),
        'content_tag': CONTENT_TAG,
        'system_string_count': str(len(strings)),
        'resource_count': str(cur.execute('SELECT COUNT(*) FROM resources').fetchone()[0]),
    }
    for k, v in meta.items():
        cur.execute('INSERT OR REPLACE INTO metadata (key, value) VALUES (?,?)', (k, v))
    con.commit()
    sections = cur.execute(
        'SELECT section, resource_name FROM resources ORDER BY section, resource_name').fetchall()
    quran = [r for s, r in sections if s == 'quran']
    resources = len(sections)
    builtin = cur.execute('SELECT COUNT(*) FROM builtin_sections').fetchone()[0]
    con.execute('VACUUM')
    con.close()

    size = os.path.getsize(db_path)
    ui = [k for k in strings if k.startswith('ui114.') and not k.startswith('ui114.surah.')]
    missing = sorted(k for k in en_keys if k not in strings)

    with open(os.path.join(ROOT, folder, 'README.txt'), 'w', encoding='utf-8') as f:
        f.write(
            f'Qurb · языковой пакет: {folder} ({code})\n'
            f'Файл: translations_{code}.db  ·  {size / 1024 / 1024:.2f} МБ\n'
            f'Версия пакета: {PACK_VERSION}  ·  тег контента: {CONTENT_TAG}\n\n'
            'Внутри (SQLite, данные — gzip):\n'
            f'  system     — строки интерфейса: {len(strings)}'
            f' (экраны v114: {len(ui)}, названия сур: 114)\n'
            f'  quran      — переводы Корана: {", ".join(quran) if quran else "нет (арабский текст встроен)"}\n'
            '  dua, azkar, names99, holidays, policies — тексты разделов\n'
            '  geo_cities, geo_countries — названия городов и стран\n\n'
            'Не редактируйте .db вручную: строки интерфейса правятся в\n'
            f'system/{code}.json, затем python3 tools/build_packs.py {code}.\n')

    return {
        'folder': folder,
        'database': f'{folder}/translations_{code}.db',
        'resources': resources,
        'builtin_sections': builtin,
        'size_bytes': size,
        'quran_translations': quran,
        'system_strings': len(strings),
        'ui114_strings': len(ui),
        'ui114_missing': len(missing),
    }, missing


def main():
    only = sys.argv[1:] or list(LANGS)
    en_keys = {k for k in load_system('en')
               if k.startswith('ui114.') and not k.startswith('ui114.surah.')}
    manifest_path = os.path.join(ROOT, 'manifest.json')
    with open(manifest_path, encoding='utf-8') as f:
        manifest = json.load(f)
    manifest['version'] = PACK_VERSION
    manifest['content_tag'] = CONTENT_TAG
    langs = manifest.setdefault('languages', {})
    sizes = {}
    for code in only:
        info, missing = build(code, en_keys)
        old = langs.get(code, {})
        old.update(info)
        langs[code] = old
        sizes[code] = info['size_bytes']
        note = f'  не переведено ui114: {len(missing)}' if missing else ''
        print(f'{code}: {info["size_bytes"]:>9} байт, строк {info["system_strings"]}{note}')
    manifest['languages'] = {k: langs[k] for k in LANGS if k in langs}
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print('\nkPackBytes для LanguagePackStore:')
    for code in LANGS:
        if code in langs:
            print(f"    '{code}': {langs[code]['size_bytes']},")


if __name__ == '__main__':
    main()
