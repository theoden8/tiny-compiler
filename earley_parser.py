#!/usr/bin/python

import string
import sys
import re

INITIAL_NONTERMINAL = 'Start'
SOURCE, RESULT = range(2)

def prespace(text):
	le = 0
	while(len(text) > le and text[le] in string.whitespace):
		le += 1
	return le

def left(text):
	if(not text):
		return ""
	w = prespace(text)

#	sys.stdout.write("\033[1;101;30m" + text[:w] + "\033[1;103;30m" + text[w:] + "\033[0m\n" + text[:w] + "\033[1;7m")
	tokentype = ""
	for it in [string.digits, string.ascii_letters + string.digits, string.punctuation, string.whitespace]:
		if(text[w] in it):
			tokentype = it
			break
	if(not tokentype):
#		print text[w:] + "\033[0m"
#		print
		return text[w:]
	for i in xrange(w, len(text)):
		if(text[i] not in tokentype):
#			print text[w:i] + "\033[0m"
#			print
			return text[w:i]
#	print text[w:] + "\033[0m"
#	print
	return text[w:]

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
			self.parsed + left(self.remains),
			self.remains[prespace(self.remains) + len(left(self.remains)):],
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
			if s.remains and left(s.remains) == completed.nonterminal:
				self.push(cursor, s.step(completed))

	def predict(self, state, cursor):
		for r in self.rules[left(state.remains)]:
			self.push(cursor, State(cursor, left(state.remains), "", r, []))

	def scan(self, state, token, cursor):
		if left(state.remains) == token:
			self.push(cursor, state.step(None))

	def parse(self, text):
		self.states = [
			[
				State(0, INITIAL_NONTERMINAL, "", r, [])
				for r in self.rules[INITIAL_NONTERMINAL]
			]
			if not i else [] for i in range(len(text) + 1)
		]

		i = 0
		while i <= len(text):
			print("\033[1;102;30m" + text[:i] + "\033[1;103;30m" + text[i:] + "\033[0m")
			cursor = i + prespace(text[i:])
			for s in self.states[i]:
				print s
				if not s.remains:
					self.complete(s, cursor)
				elif left(s.remains) in self.rules:
					self.predict(s, cursor)
				elif i < len(text):
					self.scan(s, left(text[i:]), cursor)
			i += max(1, cursor - i + len(left(text[i:])))

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
	MEGASOURCE = ""
	for line in sys.stdin:
		if(line == "END\n"):
			break
		MEGASOURCE += line
	MEGASOURCE = MEGASOURCE[:-1]
	RULE_SET = {}
	for line in sys.stdin:
		pair = re.split("\s+", line[:-1], 1)
		RULE_SET[pair[0]] = pair[1].split('|')
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
	print s
#	if s is not None:
#		print(calcTree(s))
