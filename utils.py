from __future__ import annotations
import typing as t
import json

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

def _(name: str, format: str = 'html', join: bool = True) -> t.Union[str, list]:
    with open(f'{name}.{format}', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if join:
        return ''.join(lines)
    return lines


def get_admins(name: str, format: str = 'txt'):
    return list(map(lambda value: int(value), _(name, format).split(',')))


def get_token(name: str, format: str = 'txt'):
    return _(name, format)
