import csv
import json
import sys
import typing


MUL_CHOICE_SPLITERATOR = '\u250b'
# mul_choice: list[str]
# choice: str
# fill_int: list[int]
# fill_float: list[float]


def to_json(filename: str | typing.TextIO) -> list[dict]:
    if isinstance(filename, str):
        with open(filename, encoding='utf8') as f:
            data = list(csv.reader(f))
    else:
        data = list(csv.reader(filename))

    data = [
        [s.replace('&gt;', '>') for s in x]
        for x in data if x[2].strip() != '否'
    ]
    flipped = tuple(zip(*data))[2:] # 0: ORDINAL; 1: DATE; 2: IS_TARGET

    if len(flipped) != 63:
        raise ValueError(f'len(flipped) == {len(flipped)}')

    # index sets
    index_fill_ints = {
        42, # BED_H [8-11 -> 20-23]
        43, # BED_M
        44, # SLEEP_MINS
        45, # WAKE_H
        46, # WAKE_M
    }
    index_fill_floats = {
        *range(11, 19), # HOURS_PER_DAY
        47, # ASLEEP_HRS
    }
    index_mul_choice = {61}

    res = []
    for index, question in enumerate(flipped):
        title, *answered = question
        title: str
        answered: typing.Iterable[str]
        has_choices = False
        choices: set[str] = set()

        if index in index_mul_choice:
            _type = 'mul_choice'
            def split_answers(s: str) -> list[str]:
                return [x.strip() for x in s.split(MUL_CHOICE_SPLITERATOR)]
            answers = list(map(split_answers, answered))
            has_choices = True
            choices.update(*answers)
        elif index in index_fill_ints:
            _type = 'fill_int'
            answers = list(map(int, answered))
        elif index in index_fill_floats:
            _type = 'fill_float'
            answers = list(map(float, answered))
        else:
            _type = 'choice'
            answers = list(answered)
            has_choices = True
            choices.update(answers)
        obj = {
            'type': _type,
            'answers': answers,
        }
        res.append(obj)
        if has_choices:
            obj['choices'] = list(choices)
    return res


def _main():
    if len(sys.argv) != 2:
        print('Usage:', sys.argv[0], '<csv_filename>')
        exit(1)
    filename = sys.argv[1]
    res = to_json(filename)
    json.dump(res, sys.stdout, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    _main()
