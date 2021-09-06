from __future__ import annotations
import typing as t
import sys, json
from os import path as p

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

def view_callback(path: str) -> t.Callable:
    def get_view(name: str) -> str:
        with open(p.join(path, f'{name}.html'), 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return ''.join(lines)
    return get_view