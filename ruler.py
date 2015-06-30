#!/usr/bin/python

import re;
import sys;

class	Rule:
	source	= ""
	product	= ""
	def	__init__(self, source, product):
		self.source	= source
		self.product	= product

def	recurse(string, rules):
	for rule in rules:
		applied = string.replace(rule.source, rule.product)
		if(applied == string):
			continue
		else:
			print	applied
			recurse(applied, rules)
			continue

rules	= []
string	= ""
thesource = raw_input();
while(1):
	try:
		string = raw_input();
		splitter = re.split('\s+', string, 1)
		rules.append(Rule(splitter[0], splitter[1]))
	except EOFError:
		print
		break
for rule in rules:
	print "RULE:\t" + rule.source + '\t->\t' + rule.product
print

print	thesource
recurse(thesource, rules)
