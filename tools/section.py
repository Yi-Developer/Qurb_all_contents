#!/usr/bin/env python3
"""Распаковать или упаковать файл раздела (<раздел>/<код>.json.gz).

    python3 tools/section.py unpack dua kk     # -> dua/kk.json (обычный текст)
    ... правите dua/kk.json в редакторе ...
    python3 tools/section.py pack dua kk       # -> dua/kk.json.gz, .json удаляется
    python3 tools/build_packs.py kk            # пересобрать пакет языка

Разделы: dua, azkar, dhikr, hadiths, names, holidays.
"""
import gzip
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    if len(sys.argv) != 4 or sys.argv[1] not in ('unpack', 'pack'):
        raise SystemExit(__doc__)
    mode, folder, code = sys.argv[1:]
    plain = os.path.join(ROOT, folder, f'{code}.json')
    packed = plain + '.gz'
    if mode == 'unpack':
        with open(packed, 'rb') as f:
            data = json.loads(gzip.decompress(f.read()))
        with open(plain, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
            f.write('\n')
        print('Распаковано:', plain)
    else:
        with open(plain, encoding='utf-8') as f:
            data = json.load(f)
        raw = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
        with open(packed, 'wb') as f:
            f.write(gzip.compress(raw, compresslevel=9, mtime=0))
        os.remove(plain)
        print('Упаковано:', packed)


if __name__ == '__main__':
    main()
