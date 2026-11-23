#!/usr/bin/env python3
"""Пересборка языковых пакетов Qurb из исходников.

В приложении переводов нет (кроме экрана приветствия): всё, что видит
пользователь, приходит из пакета <Язык>/translations_<код>.db. Исходники
пакета лежат в этом репозитории, скрипт собирает из них базу.

Что делает (для каждого языка):
  1. берёт строки интерфейса из system/<код>.json и кладёт их в раздел
     `system` пакета <Язык>/translations_<код>.db (gzip, sha256, размеры);
  2. кладёт в пакет разделы содержимого из файлов <раздел>/<код>.json.gz:
     dua, azkar, dhikr, hadiths, names, holidays (см. SECTIONS ниже) —
     правьте эти файлы (tools/section.py распаковывает и упаковывает их);
  3. ставит metadata.pack_version и metadata.content_tag (см. ниже);
  4. сжимает базу (VACUUM), обновляет manifest.json, README.txt папки и
     index.json разделов;
  5. печатает, каких строк интерфейса в языке не хватает по сравнению с
     английским — их нужно перевести.

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

PACK_VERSION = 9
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

# Разделы содержимого: (папка в репозитории, раздел пакета, имя ресурса).
# Файл <папка>/<код>.json.gz — исходник; в пакет попадает как есть.
SECTIONS = [
    ('dua', 'dua', '{c}.json'),             # {"cat":{…}, "dua":{titleEn:{t,tr,s,tl}}}
    ('azkar', 'azkar', 'azkar_{c}.json'),   # {titleEn:{t,tl,tr,s}} — после намаза, перед сном
    ('dhikr', 'azkar', 'dhikr_{c}.json'),   # {номер:{tl,nar,s}} — утро и вечер
    ('hadiths', 'azkar', 'hadiths_{c}.json'),
    ('names', 'names99', '{c}.json'),       # {номер: значение}
    ('holidays', 'holidays', '{c}.json'),   # {ключ: строка}
]


def sync_sections(cur, code):
    """Положить в пакет разделы содержимого из файлов репозитория."""
    done = []
    for folder, section, name in SECTIONS:
        src = os.path.join(ROOT, folder, f'{code}.json.gz')
        if not os.path.exists(src):
            continue
        with open(src, 'rb') as f:
            raw = gzip.decompress(f.read())
        json.loads(raw)  # проверка, что это JSON
        packed = gzip.compress(raw, compresslevel=9, mtime=0)
        res = name.format(c=code)
        old = cur.execute(
            'SELECT sha256 FROM resources WHERE section=? AND resource_name=?',
            (section, res)).fetchone()
        sha = hashlib.sha256(raw).hexdigest()
        if old and old[0] == sha:
            continue
        cur.execute('DELETE FROM resources WHERE section=? AND resource_name=?',
                    (section, res))
        cur.execute(
            'INSERT INTO resources (section, resource_name, content_type, compression,'
            ' data, original_size, stored_size, sha256) VALUES (?,?,?,?,?,?,?,?)',
            (section, res, 'json', 'gzip', packed, len(raw), len(packed), sha))
        done.append(folder)
    # раздел есть в пакете — пометка «встроено в приложение» больше не нужна
    for (sec,) in cur.execute('SELECT section FROM builtin_sections').fetchall():
        if cur.execute('SELECT 1 FROM resources WHERE section=? LIMIT 1',
                       (sec,)).fetchone():
            cur.execute('DELETE FROM builtin_sections WHERE section=?', (sec,))
    return done


def write_indexes():
    """index.json разделов: сколько записей у каждого языка."""
    for folder in ('dua', 'azkar', 'dhikr', 'hadiths', 'names'):
        langs = {}
        for fn in sorted(os.listdir(os.path.join(ROOT, folder))):
            if not fn.endswith('.json.gz'):
                continue
            with open(os.path.join(ROOT, folder, fn), 'rb') as f:
                data = json.loads(gzip.decompress(f.read()))
            langs[fn[:-8]] = len(data.get('dua', data)) if folder == 'dua' else len(data)
        with open(os.path.join(ROOT, folder, 'index.json'), 'w', encoding='utf-8') as f:
            json.dump({folder: {
                'languages': langs,
                'note': 'Исходник раздела языкового пакета. В приложение не встроен: '
                        'скачивается вместе с языком (tools/build_packs.py).',
            }}, f, ensure_ascii=False, indent=2)
            f.write('\n')


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
    synced = sync_sections(cur, code)
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
    if code == 'ar':  # в арабском интерфейсе перевода названий сур нет
        missing = [k for k in missing if not k.startswith('surah_meaning.')]

    with open(os.path.join(ROOT, folder, 'README.txt'), 'w', encoding='utf-8') as f:
        f.write(
            f'Qurb · языковой пакет: {folder} ({code})\n'
            f'Файл: translations_{code}.db  ·  {size / 1024 / 1024:.2f} МБ\n'
            f'Версия пакета: {PACK_VERSION}  ·  тег контента: {CONTENT_TAG}\n\n'
            'Внутри (SQLite, данные — gzip):\n'
            f'  system     — строки интерфейса: {len(strings)}'
            f' (экраны v114: {len(ui)}, названия сур: 114)\n'
            f'  quran      — переводы Корана: {", ".join(quran) if quran else "нет (арабский текст встроен)"}\n'
            '  dua, azkar (азкары, утро и вечер, хадисы), names99, holidays,\n'
            '  policies — тексты разделов\n'
            '  geo_cities, geo_countries — названия городов и стран\n\n'
            'Не редактируйте .db вручную: строки интерфейса правятся в\n'
            f'system/{code}.json, содержимое — в dua/, azkar/, dhikr/, names/,\n'
            f'holidays/ ({code}.json.gz), затем python3 tools/build_packs.py {code}.\n')

    return {
        'folder': folder,
        'database': f'{folder}/translations_{code}.db',
        'resources': resources,
        'builtin_sections': builtin,
        'size_bytes': size,
        'quran_translations': quran,
        'system_strings': len(strings),
        'ui114_strings': len(ui),
        'ui114_missing': len([k for k in missing if k.startswith('ui114.')]),
        'system_missing': len(missing),
    }, missing


def main():
    only = sys.argv[1:] or list(LANGS)
    # Английский пакет — эталон набора ключей: в приложении запасного
    # языка нет, строка без перевода останется на экране пустой.
    # Старые ключи app_strings.*, которые есть только в en/ar, приложение
    # не запрашивает — в эталон они не входят.
    en_all = load_system('en')
    others = set()
    for c in LANGS:
        if c not in ('en', 'ar'):
            others |= set(load_system(c))
    unused = ('qibla_fallback_strings.', 'qibla_precision_strings.',
              'calendar_strings.')  # разделы, которые приложение не читает
    en_keys = {k for k in en_all
               if not k.startswith(unused)
               and (not k.startswith('app_strings.') or k in others)}
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
        note = (f'  НЕТ ПЕРЕВОДА: {len(missing)} ({", ".join(missing[:4])}'
                f'{" …" if len(missing) > 4 else ""})') if missing else ''
        print(f'{code}: {info["size_bytes"]:>9} байт, строк {info["system_strings"]}{note}')
    manifest['languages'] = {k: langs[k] for k in LANGS if k in langs}
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write('\n')
    write_indexes()
    print('\nkPackBytes для LanguagePackStore:')
    for code in LANGS:
        if code in langs:
            print(f"    '{code}': {langs[code]['size_bytes']},")


if __name__ == '__main__':
    main()
