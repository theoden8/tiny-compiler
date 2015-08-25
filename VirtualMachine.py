#!/usr/bin/python

import sys
import string
import operator


class VM:
	SIGEXIT = KeyboardInterrupt
	def push(self):
		self.stack.append(self.progue[self.line + 1])
		self.line += 2

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

	def unary_op(func):
		def opn(self):
			self.stack.append(func(self.stack.pop()))
			self.line += 1
		return opn

	def binary_op(func):
		def opn(self):
			self.stack.append(func(self.stack.pop(), self.stack.pop()))
			self.line += 1
		return opn

	def value(self):
		self.stack.append(self.var_values[self.progue[self.line + 1]])
		self.line += 2

	def assign(self):
		self.var_values[self.progue[self.line + 1]] = self.stack.pop()
		self.line += 2

	def exit(self):
		raise VM.SIGEXIT

	PUSH, JUMP, JUMPIF, JUMPUNL, EXIT, NOT, NEG, POS, ABS, LT, LE, EQ, NE, GE, GT, GT, OR, AND, XOR, LSHIFT, RSHIFT, MOD, ADD, SUB, MUL, DIV, POW, VALUE, ASSIGN = range(29)
	MATCH = {
		PUSH    : push,
		JUMP    : jump,
		JUMPIF  : jumpif,
		JUMPUNL : jumpunless,
		EXIT    : exit,
		# UNARY
		NOT     : unary_op(operator.__not__),
		NEG     : unary_op(operator.__neg__),
		POS     : unary_op(operator.__pos__),
		ABS     : unary_op(operator.__abs__),
		# BINARY
		LT      : binary_op(operator.__lt__),
		LE      : binary_op(operator.__le__),
		EQ      : binary_op(operator.__eq__),
		NE      : binary_op(operator.__ne__),
		GE      : binary_op(operator.__ge__),
		GT      : binary_op(operator.__gt__),
		GT      : binary_op(operator.__gt__),

		OR      : binary_op(operator.__or__),
		AND     : binary_op(operator.__and__),
		XOR     : binary_op(operator.__xor__),

		LSHIFT  : binary_op(operator.__lshift__),
		RSHIFT  : binary_op(operator.__rshift__),
		MOD     : binary_op(operator.__mod__),
		ADD     : binary_op(operator.__add__),
		SUB     : binary_op(operator.__sub__),
		MUL     : binary_op(operator.__mul__),
		DIV     : binary_op(operator.__div__),
		POW     : binary_op(operator.__pow__),
		#
		VALUE   : value,
		ASSIGN  : assign,
	}

	def __init__(self):
		self.line = 0
		self.progue = []
		self.stack = []
		self.var_values = {}

	def Perform(self, progue):
		self.line = 0
		self.progue = progue
		while True:
			operation = self.progue[self.line]
			try:
				VM.MATCH[operation](self) == ['exit']
			except VM.SIGEXIT:
				break
		print '='*100
		return self.stack
