#!/usr/bin/env python2

import string
import sys


_KEYWORDS, c = {}, 0
for i in [
    'for', 'while', 'until',
        'if', 'unless', 'elif', 'else',
        'switch', 'case',
        '{', '}',
        '(', ')',
        ';', ',', '.',
        '=']:
    _KEYWORDS[i] = c
    c += 1


def keywords_substitution(tokens):
    """
    Transforms an array of tokens (str) into array of recognized tokens (str, int).
    """
    return [_KEYWORDS[t] if t in _KEYWORDS else t for t in tokens]
