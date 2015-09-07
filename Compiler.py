#!/usr/bin/python

import sys

from Earley_Parser import *
from VirtualMachine import *


class Compiler:
	VARIABLES = {}

	def __init__(self):
		self.progue = []
		self.vm = VM()

	def Compile(self, tree, indent = 0):
		print('< > ' * indent + str(tree))
		indent += 1
		GOAL = tree.nonterminal
		if GOAL == 'Start':
			self.Compile(tree.children[0], indent)
		elif GOAL == 'Program':
			if len(tree.children) == 1:
				self.Compile(tree.children[0], indent)
			elif len(tree.children) == 3:
				self.Compile(tree.children[1], indent)
		elif GOAL == 'ListOfCmd':
			self.Compile(tree.children[0], indent)
			if len(tree.children) == 3:
				self.Compile(tree.children[2], indent)
		elif GOAL == 'Cmd':
			self.Compile(tree.children[0], indent)
		elif GOAL == 'Assignment':
			self.progue += [self.vm.PUSH, tree.children[2], self.vm.ASSIGN, tree.children[0]]
#		elif GOAL == 'Loop': # while ( cmd ) Program
#			self.progue += [self.PUSH]
#			self.Compile(tree.children[3], indend)
#			self.Compile(tree.children[5], indend)
#		elif GOAL == 'Condition':
#			if len(tree.children) == 2:
#				self.Compile(tree.children[1], indent)
#				self.progue += [vm.PUSH, tree.children[2], vm.ASSIGN, tree.children[0]]
#				Cmd JumpUnless ... Cmd
#			if len(tree.children) == 4:
#				self.Compile(tree.children[-1], indent)
#				self.progue += [vm.PUSH, tree.children[2], vm.ASSIGN, tree.children[0]]
#				Cmd JumpUnless ... Cmd

if __name__ == "__main__":
	t = Tokenizer()
	p = PrankyHack()
	vm = VM()
	source = t.get_list()
	rules = t.get_rules(p)
	ep = EarleyParser(rules)
	s = ep.parse(p.dark_deeds(source))
	print "="*100
	if s is not None:
		PrintTree(s)
	print "="*100
	c = Compiler()
	c.Compile(s)
	c.progue += [vm.EXIT]
	print c.progue
	print 'Perform : ' + str(vm.Perform(c.progue))
	print 'Values : ' + str(vm.var_values)
