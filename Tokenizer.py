#!/usr/bin/env python2
# coding: utf-8

import string
import sys

import KeywordSub


_BLANK, _LETTER, _DIGIT, _DOT = range(4)


def _char_type(char):
    if char.isspace():
        return _BLANK
    elif char.isalpha() or char == '_':
        return _LETTER
    elif char.isdigit():
        return _DIGIT
    else:
        return _DOT
    raise Exception("tokenizer::undefined _char_type")


def _tokenize(text):
    tokens = []
    token = ""
    p = ""
    for c in text:
        t = _char_type(c)
        if token == "" and t != _BLANK:
            token = c
        elif t == _BLANK:
            if token == "":
                tokens += [token]
                token = ""
        elif(
            t == _LETTER and p in [_LETTER, _DIGIT] or
            t == _DIGIT and p in [_DIGIT]
        ):
            token += c
        else:
            tokens += [token]
            token = c
        p = t
    if token != "":
        tokens += [token]
        token = ""
    return tokens


END = "END\n"


def get_list():
    text = ""
    for line in sys.stdin:
        if line == END:
            break
        text += line
    return _tokenize(text[:-1])


def get_rules():
    RULE_SET = {}
    for line in sys.stdin:
        if line == END:
            break

        rules = KeywordSub.keywords_substitution(_tokenize(line))
        if rules[0] not in RULE_SET:
            RULE_SET[rules[0]] = []
        RULE_SET[rules[0]].append(rules[1:])
    print_rules(RULE_SET)
    return RULE_SET


def print_rules(RULE_SET):
    for r in RULE_SET:
        print "\t\033[0;1;4;40;96m" + str(r) + "\033[0;1;35m" + " "*(11 - len(str(r))) + "-> " + "\033[0;1;40;91m" + str(RULE_SET[r]) + "\033[0m"
