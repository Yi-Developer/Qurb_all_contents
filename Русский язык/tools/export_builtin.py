#!/usr/bin/env python3
"""Встроить языковые пакеты в приложение Qurb (assets/l10n).

Приложение берёт строки и содержимое так: встроенное (assets/l10n) — основа,
скачанный пакет — поверх него. Поэтому интерфейс и содержимое всех языков
работают сразу и без интернета, а свежие правки приходят из этого
репозитория. После изменения переводов запускайте:

    python3 tools/export_builtin.py ../qurb

Скрипт пишет assets/l10n/<раздел>/<код>.json.gz:
  system   — из system/<код>.json (строки интерфейса);
  dua, azkar, names, holidays, hadiths — из SQLite-пакета языка (то же,
  что пользователь получает при установке); если в пакете раздела нет —
  из отдельного файла <раздел>/<код>.json.gz.
"""
import gzip
import json
import os
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ['ar', 'en', 'ru', 'kk', 'ky', 'az', 'uz', 'tg', 'tr', 'ja', 'ko']
SECTIONS = ['dua', 'azkar', 'names', 'holidays', 'hadiths']
# раздел assets → (раздел пакета, имя ресурса)
IN_PACK = {
    'dua': ('dua', '{c}.json'),
    'azkar': ('azkar', 'azkar_{c}.json'),
    'names': ('names99', '{c}.json'),
    'holidays': ('holidays', '{c}.json'),
    'hadiths': ('azkar', 'hadiths_{c}.json'),
}


def pack_db(code):
    with open(os.path.join(ROOT, 'manifest.json'), encoding='utf-8') as f:
        rel = json.load(f)['languages'][code]['database']
    return os.path.join(ROOT, rel)


def from_pack(code, sec):
    section, name = IN_PACK[sec]
    con = sqlite3.connect(pack_db(code))
    try:
        row = con.execute('SELECT data FROM resources WHERE section=? AND resource_name=?',
                          (section, name.format(c=code))).fetchone()
    finally:
        con.close()
    return gzip.decompress(row[0]) if row else None


def main():
    if len(sys.argv) != 2:
        raise SystemExit('Укажите путь к проекту приложения: export_builtin.py <qurb>')
    out = os.path.join(sys.argv[1], 'assets', 'l10n')
    total = 0
    os.makedirs(os.path.join(out, 'system'), exist_ok=True)
    for code in LANGS:
        with open(os.path.join(ROOT, 'system', f'{code}.json'), encoding='utf-8') as f:
            data = json.load(f)
        raw = json.dumps(dict(sorted(data.items())), ensure_ascii=False,
                         separators=(',', ':')).encode('utf-8')
        dst = os.path.join(out, 'system', f'{code}.json.gz')
        with open(dst, 'wb') as f:
            f.write(gzip.compress(raw, compresslevel=9, mtime=0))
        total += os.path.getsize(dst)
    for sec in SECTIONS:
        os.makedirs(os.path.join(out, sec), exist_ok=True)
        for code in LANGS:
            raw = from_pack(code, sec)
            if raw is None:
                src = os.path.join(ROOT, sec, f'{code}.json.gz')
                if not os.path.exists(src):
                    continue
                raw = gzip.decompress(open(src, 'rb').read())
            json.loads(raw)  # проверка
            dst = os.path.join(out, sec, f'{code}.json.gz')
            with open(dst, 'wb') as f:
                f.write(gzip.compress(raw, compresslevel=9, mtime=0))
            total += os.path.getsize(dst)
    print(f'assets/l10n: {total // 1024} КБ')
    for sec in ['system'] + SECTIONS:
        files = sorted(os.listdir(os.path.join(out, sec)))
        print(f'  {sec}: {", ".join(x.split(".")[0] for x in files)}')


if __name__ == '__main__':
    main()
