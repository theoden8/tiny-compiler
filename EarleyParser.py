#!/usr/bin/env python2
# coding: utf-8

import string
import sys
import re

import Tokenizer

INITIAL_NONTERMINAL = 'Start'


class State:
    def __init__(self, begin, nonterminal, parsed, remains, children):
        self.begin = begin
        self.nonterminal = nonterminal
        self.parsed = parsed
        self.remains = remains
        self.children = children

    def __str__(self):
        return(
            "\033[1;40;97m[ " +
            "\033[1;44;97m " + str(self.begin) + " \033[107;30m:"
            "\033[1;102;30m" + str(self.parsed) +
            "\033[1;103;30m" + str(self.remains) +
            "\033[1;40;97m ] > " + str(self.children) + "\033[0m"
        )

    def __eq__(self, other):
        return(
            self.begin == other.begin and
            self.nonterminal == other.nonterminal and
            self.parsed == other.parsed and
            self.remains == other.remains
        )

    def step(self, child):
        """
        Pushes one parsed step over state.
        """
        return State(
            self.begin,
            self.nonterminal,
            self.parsed + [self.remains[0]],
            self.remains[1:],
            self.children + [child]
        )


_TYPE_SUBST = int


class EarleyParser:
    def __init__(self, rules):
        self.rules = rules

    def match_token(self, template, token):
        if type(token) == _TYPE_SUBST and type(template) == _TYPE_SUBST:
            return template == token
        if type(token) == str and type(template) == str and template not in self.rules:
            return True
        return False

    def push(self, cursor, state):
        for s in self.states[cursor]:
            if s == state:
                return
        self.states[cursor].append(state)

    def complete(self, completed, cursor):
        for s in self.states[completed.begin]:
            if len(s.remains) > 0 and s.remains[0] == completed.nonterminal:
                self.push(cursor, s.step(completed))

    def predict(self, state, i):
        for r in self.rules[state.remains[0]]:
            self.push(i, State(i, state.remains[0], [], r, []))

    def scan(self, state, token, cursor):
        if self.match_token(state.remains[0], token):
            self.push(cursor + 1, state.step(token))

    def parse(self, text):
        self.states = [
            [
                State(0, INITIAL_NONTERMINAL, [], r, [])
                for r in self.rules[INITIAL_NONTERMINAL]
            ]
            if i == 0 else [] for i in range(len(text) + 1)
        ]

        for i in range(len(text) + 1):
            print "\033[1;92m" + str(text[:i]) + "\033[35m █ \033[93m" + str(text[i:]) + "\033[0m"
            for s in self.states[i]:
                print s
                if s.remains == []:
                    self.complete(s, i)
                elif s.remains[0] in self.rules:
                    self.predict(s, i)
                elif i < len(text):
                    self.scan(s, text[i], i)

        for s in self.states[-1]:
            if len(s.remains) == 0 and s.begin == 0 and s.nonterminal == INITIAL_NONTERMINAL:
                return s

        return None


def PrintTree(s, indent=0):
    if type(s) not in [type(None), str, _TYPE_SUBST]:
        print '\t' * indent + str(s)
        for c in s.children:
            PrintTree(c, indent + 1)
