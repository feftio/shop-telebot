from __future__ import annotations
import typing as t
import sys
import json
from os import path as p, listdir

sys.path.append(p.abspath(p.join(p.dirname(__file__), '..')))


class Event:
    NAME_ALIAS: str = 'n'
    DATA_ALIAS: str = 'd'
    __slots__ = ('name', 'data')

    @classmethod
    def loads(cls, dumped: str) -> Event:
        event, loads = Event(), json.loads(dumped)
        event.name, event.data = loads[cls.NAME_ALIAS], loads[cls.DATA_ALIAS]
        return event

    @classmethod
    def dumps(cls, name: str, data: str) -> str:
        return json.dumps({cls.NAME_ALIAS: name, cls.DATA_ALIAS: data})


def content_callback(path: str) -> t.Callable:
    def get_content(name: str) -> str:
        with open(p.join(path, f'{name}.html'), 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return ''.join(lines)
    return get_content


def dictify(path: str) -> t.Dict[str, str]:
    _dict, content = dict(), content_callback(path)
    for filename in listdir(path):
        if not p.isfile(p.join(path, filename)):
            continue
        key = p.splitext(filename)[0]
        _dict[key] = content(key)
    return _dict
