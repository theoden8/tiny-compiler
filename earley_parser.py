#!/usr/bin/python

import string
import sys
import re

INITIAL_NONTERMINAL = 'Start'


class Tokenizer:
	BLANK, LETTER, DIGIT, DOT = range(4)

	def __init__(self):
		pass

	def char_type(self, char):
		if(char.isspace()):
			return self.BLANK
		elif(char.isalpha() or char == '_'):
			return self.LETTER
		elif(char.isdigit()):
			return self.DIGIT
		else:
			return self.DOT
		raise Exception("Tokenizer::undefined char_type")

	def tokenize(self, text):
		tokens = []
		token = ""
		p = ""
		for c in text:
			t = self.char_type(c)
			if(not token and t != self.BLANK):
				token = c
			elif(t == self.BLANK):
				if(not token):
					tokens += [token]
					token = ""
			elif(
				t == self.LETTER and (
					p == self.LETTER or p == self.DIGIT
				)
				or
				t == self.DIGIT and (
					p == self.DIGIT
				)
			):
				token += c
			else:
				tokens += [token]
				token = c
			p = t
		if(token):
			tokens += [token]
			token = ""
		return tokens


class PrankyHack:
	FOR, WHILE, IF, ELIF, ELSE, UNTIL, SWITCH, CASE, C_BR_Open, C_BR_Close, SEMICOLUMN, COMMA, DOT, ASSIGNMENT = range(14)
	MATCH = {
		'for'        : FOR,
		'while'      : WHILE,
		'if'         : IF,
		'elif'       : ELIF,
		'else'       : ELSE,
		'until'      : UNTIL,
		'switch'     : SWITCH,
		'case'       : CASE,
		'{'          : C_BR_Open,
		'}'          : C_BR_Close,
		';'          : SEMICOLUMN,
		','          : COMMA,
		'.'          : DOT,
		'='          : ASSIGNMENT,
	}
	def dark_deeds(self, text):
		return [ self.MATCH[w] if w in self.MATCH else w for w in text ]

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
			self.parsed + [self.remains[0]],
			self.remains[1:],
			self.children + [child]
		)


class EarleyParser:
	def __init__(self, rules):
		self.rules = rules

	def match_token(self, template, token):
		if type(token) == int and type(template) == int:
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
			self.push(cursor + 1, state.step(None))

	def parse(self, text):
		self.states = [
			[
				State(0, INITIAL_NONTERMINAL, [], r, [])
				for r in self.rules[INITIAL_NONTERMINAL]
			]
			if not i else [] for i in range(len(text) + 1)
		]
		for i in range(len(text) + 1):
			print "\033[1;92m" + str(text[:i]) + "\033[35m █ \033[93m" + str(text[i:]) + "\033[0m"
			for s in self.states[i]:
				print s
				if not s.remains:
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
	if(not s):
		return
	print('\t' * indent + str(s))
	for c in s.children:
		PrintTree(c, indent + 1)

def get_text():
	END = "END\n"
	text = ""
	for line in sys.stdin:
		if(line == END):
			break
		text += line
	return text[:-1]

if __name__ == "__main__":
	t = Tokenizer()
	p = PrankyHack()

	MEGASOURCE = get_text()

	RULE_SET = {}
	for line in sys.stdin:
		if(line == "END\n"):
			break
		rules = p.dark_deeds(t.tokenize(line))
		if rules[0] not in RULE_SET:
			RULE_SET[rules[0]] = []
		RULE_SET[rules[0]].append(rules[1:])
	for r in RULE_SET:
		print(r, RULE_SET[r])

	ep = EarleyParser(RULE_SET)
	s = ep.parse(p.dark_deeds(t.tokenize(MEGASOURCE)))
	print MEGASOURCE
	print Tokenizer().tokenize(MEGASOURCE)
	print "="*100
	print s
	if s is not None:
		PrintTree(s)
