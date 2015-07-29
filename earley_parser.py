#!/usr/bin/python

import string
import sys
import re

INITIAL_NONTERMINAL = 'S'
SOURCE, RESULT = range(2)


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
			"\033[1;102;30m" + self.parsed +
			"\033[1;103;30m" + self.remains +
			"\033[1;40;97m ]\033[0m"
		)

	def __eq__(self, other):
		return(
			self.begin == other.begin and
			self.nonterminal == other.nonterminal and
			self.parsed == other.parsed and
			self.remains == other.remains
		)

	def step(self, child):
		return State(
			self.begin,
			self.nonterminal,
			self.parsed + self.remains[0],
			self.remains[1:],
			self.children + [child]
		)


class EarleyParser:
	def __init__(self, rules):
		self.rules = rules

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
			self.push(i, State(i, state.remains[0], "", r, []))

	def scan(self, state, symbol, cursor):
		if state.remains[0] == symbol:
			self.push(cursor + 1, state.step(None))

	def parse(self, text):
		self.states = [
			[
				State(0, INITIAL_NONTERMINAL, "", r, [])
				for r in self.rules[INITIAL_NONTERMINAL]
			]
			if not i else [] for i in range(len(text) + 1)
		]

		for i in range(len(text) + 1):
			for s in self.states[i]:
				if len(s.remains) == 0:
					self.complete(s, i)
				elif s.remains[0] in self.rules:
					self.predict(s, i)
				elif i < len(text):
					self.scan(s, text[i], i)

		for s in self.states[-1]:
			if len(s.remains) == 0 and s.begin == 0 and s.nonterminal == INITIAL_NONTERMINAL:
				return s

		return None

def calcTree(s):
	rule = s.nonterminal + ":" + s.parsed
	if rule == "S:D":
		return calcTree(s.children[0])
	if rule == "D:D+P":
		return calcTree(s.children[0]) + calcTree(s.children[2])
	if rule == "D:D-P":
		return calcTree(s.children[0]) - calcTree(s.children[2])
	if rule == "D:P":
		return calcTree(s.children[0])
	if rule == "P:P*M":
		return calcTree(s.children[0]) * calcTree(s.children[2])
	if rule == "P:P/M":
		return calcTree(s.children[0]) / calcTree(s.children[2])
	if rule == "P:M":
		return calcTree(s.children[0])
	if rule == "M:(D)":
		return calcTree(s.children[1])
	if rule == "M:N":
		return calcTree(s.children[0])
	return float(s.parsed[0])

if __name__ == "__main__":
	MEGASOURCE = raw_input()
	RULE_SET = {}
	for line in sys.stdin:
		pair = line.split()
		source = pair[0]
		RULE_SET[source] = pair[1].split('|')
	for nonterminal in RULE_SET:
		for product in RULE_SET[nonterminal]:
			print(
				'\033[1;4;91mRule\033[0m :\t\033[93m[ ' + nonterminal +
				' ]\t\033[1;97m->\t\033[92m[ ' + product +
				' ]\033[0m'
			)
	print(MEGASOURCE)
	ep = EarleyParser(RULE_SET)
	s = ep.parse(MEGASOURCE)
	if s is not None:
		print(calcTree(s))
