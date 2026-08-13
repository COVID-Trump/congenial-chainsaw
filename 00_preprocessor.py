#!/usr/bin/env python3
import csv
import datetime
from typing import Iterable

COL_ORDINAL = 0
COL_TIMESTAMP = 1
COL_DURATION = 2
COL_SOURCE_TAG = 3
COL_SOURCE_DETAIL = 4
COL_SOURCE_IP = 5

COLS_EXCLUDED = (COL_DURATION, COL_SOURCE_TAG, COL_SOURCE_DETAIL, COL_SOURCE_IP)
COL_DATA_START = 6


def _filter_timestamp(timestamp: str) -> str:
    dt = datetime.datetime.strptime(timestamp, '%Y/%m/%d %H:%M:%S')
    return dt.date().isoformat()


def _filter_each_line(line: list[str]) -> list[str]:
    return [
        (s if i != COL_TIMESTAMP else _filter_timestamp(s))
        for i, s in enumerate(line) if i not in COLS_EXCLUDED
    ]


def preprocess(file: Iterable[str], output) -> Iterable[str]:
    reader = csv.reader(file)
    writer = csv.writer(output)

    title_line = next(reader, None)
    if not title_line:
        raise ValueError('Empty, invalid or malformed title line')
    questions = title_line[COL_DATA_START:]

    title_line_new = [s for i, s in enumerate(title_line) if i not in COLS_EXCLUDED]
    writer.writerow(title_line_new)

    writer.writerows(map(_filter_each_line, reader))
    return map(lambda p: '[%02d] %s' % p, enumerate(questions, start=0))


def preprocess_file(filename_in: str, filename_output: str) -> None:
    with (
        open(filename_in, encoding='utf8') as f,
        open(filename_output, 'w', encoding='utf8') as g,
    ):
        questions = preprocess(f, g)
        print('Questions:', *questions, sep='\n- ')


if __name__ == '__main__':
    import sys

    try:
        _, f_input, f_output = sys.argv
    except ValueError:
        print('Usage: ' + sys.argv[0] + ' <file_input> <file_output>')
        exit(1)

    preprocess_file(f_input, f_output)
