#!/usr/bin/python

import sys
import string


class VM:
	def push(self):
		self.stack.append(self.progue[self.line + 1])
		self.line += 2

	def add(self):
		self.stack[-2] += self.stack[-1]
		self.stack.pop()
		self.line += 1

	def jump(self):
		self.line = self.progue[self.line + 1]

	def jumpif(self):
		if self.stack[-2]:
			self.line = self.progue[self.line + 1]
		else:
			self.line += 2

	def jumpunless(self):
		if self.stack[-2]:
			self.line += 2
		else:
			self.line = self.progue[self.line + 1]

	def eq(self):
		self.stack.append(self.stack.pop() == self.stack.pop())
		self.line += 1

	def ne(self):
		self.stack.append(self.stack.pop() != self.stack.pop())
		self.line += 1

	def exit(self):
		print self.stack
		exit(0)

	PUSH, ADD, JUMP, JUMPIF, JUMPUNL, EXIT = range(6)
	MATCH = {
		PUSH    : push,
		ADD     : add,
		JUMP    : jump,
		JUMPIF  : jumpif,
		JUMPUNL : jumpunless,
		EXIT    : exit,
	}

	def __init__(self):
		self.line = 0
		self.progue = []
		self.stack = []

	def Perform(self, progue):
		self.line = 0
		self.progue = progue
		while True:
			operation = self.progue[self.line]
			VM.MATCH[operation](self)


vm = VM()

# i = 0
# while i != 10:
#	++i

#p = [VM.PUSH, 2, VM.PUSH, 2, VM.ADD, VM.EXIT]
p = [
	VM.PUSH
	VM.PUSH
]
vm.Perform(p)
