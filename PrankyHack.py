#!/usr/bin/python

import string
import sys


class PrankyHack:
	MATCH = {}
	c = 0
	for i in [	'for', 'while', 'until',
			'if', 'unless', 'elif', 'else',
			'switch', 'case',
			'{', '}',
			';', ',', '.',
			'=' ]:
		MATCH[i] = c
		c += 1

	def dark_deeds(self, text):
		return [self.MATCH[w] if w in self.MATCH else w for w in text]
