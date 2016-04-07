#!/usr/bin/env python2

import string
import sys


"""
This file replaces keywords (strings) with a number corresponding to the keyword.
"""

_keywordsES = {}
c = 0
for i in [
    'for', 'while', 'until',
        'if', 'unless', 'elif', 'else',
        'switch', 'case',
        '{', '}',
        '(', ')',
        ';', ',', '.',
        '=']:
    _keywordsES[i] = c
    c += 1


def keywords_substitution(text):
    """
    Transforms an array of tokens into array of recognized tokens.
    What is recognized is now a number (int).
    """
    return [_keywordsES[w] if w in _keywordsES else w for w in text]
