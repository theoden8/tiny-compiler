#!/usr/bin/python

import re
import sys
import string

SOURCE	= 0
PRODUCT	= 1

def	recurse(startpos, string, rules):
	print string
	for i in xrange(startpos, len(string)):
#		print '[' + str(i) + ':' + str(startpos) + ']\t' + string
		for rule in rules:
			end = i + len(rule[SOURCE])
			if(rule[SOURCE] == string[i:end]):
				applied = string[:i] + rule[PRODUCT] + string[end:]
				recurse(i + 1, applied, rules)

RULES	= []
MEGA_SOURCE = raw_input()

while(1):
	string	= ""
	try:
		string = raw_input()
		splitter = re.split('\s+', string, 1)
		RULES.append([splitter[0], splitter[1]])
	except EOFError:
		print
		break

for rule in RULES:
	print "RULE:\t" + rule[SOURCE] + '\t->\t' + rule[PRODUCT]
print

recurse(0, MEGA_SOURCE, RULES)
