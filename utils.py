from __future__ import annotations
import typing as t


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
