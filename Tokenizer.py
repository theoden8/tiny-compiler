#!/usr/bin/python

import string
import sys


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
					p == self.LETTER or
					p == self.DIGIT
				) or
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

	def get_list(self):
		END = "END\n"
		text = ""
		for line in sys.stdin:
			if(line == END):
				break
			text += line
		return self.tokenize(text[:-1])

	def print_rules(self, RULE_SET):
		for r in RULE_SET:
			print "\t\033[0;1;4;40;96m" + str(r) + "\033[0;1;35m" + " "*(11 - len(str(r))) + "-> " + "\033[0;1;40;91m" + str(RULE_SET[r]) + "\033[0m"

	def get_rules(self, p):
		END = "END\n"
		RULE_SET = {}
		for line in sys.stdin:
			if(line == END):
				break
			rules = p.dark_deeds(self.tokenize(line))
			if rules[0] not in RULE_SET:
				RULE_SET[rules[0]] = []
			RULE_SET[rules[0]].append(rules[1:])
		self.print_rules(RULE_SET)
		return RULE_SET
