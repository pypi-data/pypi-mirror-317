#!/usr/bin/env python3
# coding: utf-8
from __future__ import annotations

import os
from typing import Iterable

__version__ = "0.4.2"

b32_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
b64_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/'

b64_urlsafe_chars = \
    'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-'


def random_hex(length: int = 24):
    size = sum(divmod(length, 2))
    bs = os.urandom(size)
    try:
        return bs.hex()[:length]
    except AttributeError:
        import base64
        return base64.b16encode(bs).decode('ascii')


def random_string(length: int, chars: str = None):
    import random
    chars = chars or b32_chars
    return ''.join(random.choice(chars) for _ in range(length))


def remove_chars(text: str, chars: str):
    """
    :param text: (str)
    :param chars: (str or list) characters to be removed
    :return: (str)
    """
    table = str.maketrans(dict.fromkeys(chars))
    return text.translate(table)


def remove_control_chars(text: str):
    return text.translate(dict.fromkeys(range(32)))


def remove_whitespaces(text: str):
    return ''.join(text.split())


def remove_newlines(text: str):
    # similar to VIM line join
    return ' '.join(text.splitlines())


def remove_emptylines(text: str):
    lines = text.splitlines(keepends=True)
    return ''.join(x for x in lines if x.strip())


def replace_newlines(text: str, nl='\n'):
    text = text.replace('\n\r', nl)
    text = text.replace('\r', nl)
    if nl != '\n':
        text = text.replace('\n', nl)
    return text


def dedup_spaces(text: str):
    import re
    return re.sub(r" {2,}", " ", text)


def proper_join(parts: Iterable[str]):
    import re
    regex = re.compile(r'\s$')
    _parts = []
    space = chr(32)
    for p in parts:
        if not p:
            continue
        if regex.search(p):
            _parts.append(p)
        else:
            _parts.append(p + space)
    return ''.join(_parts)


if __name__ == '__main__':
    print(__version__)
