#!/usr/bin/env python2

import string
import sys


_KEYWORDS = dict([ (j, i) for i, j in enumerate([
        'for', 'while', 'until',
        'if', 'unless', 'elif', 'else',
        'switch', 'case',
        '{', '}', '(', ')',
        ';', ',', '.', '='
    ]
)])


def keywords_substitution(tokens):
    """
    Transforms an array of tokens (str) into array of recognized tokens (str, int).
    """
    return [_KEYWORDS[t] if t in _KEYWORDS else t for t in tokens]
