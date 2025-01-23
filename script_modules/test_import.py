import importlib
import typing

import settings as bs

def test(file_list: typing.List[str]):
    print(bs.COMMON_PATH)

    new_list = []
    for path in file_list:
        new_list.append(path.replace('/', '.'))

    obj = {
        'm': 3,
        'n': [3, 4, 5]
    }
    for m in new_list:
        mo = importlib.import_module(m)
        print(mo.__name__, mo.handle(obj))
    print(obj)


def _init():
    pass


print(bs.COMMON_PATH)