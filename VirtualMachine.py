#!/usr/bin/env python2

import sys
import string
import operator


PUSH, JMP, JMPIF, JMPUNL, EXIT, NOT, NEG, \
POS, ABS, LT, LE, EQ, NE, GE, GT, GT, OR, \
AND, XOR, LSHIFT, RSHIFT, MOD, ADD, SUB, \
MUL, DIV, POW, VALUE, ASSIGN, RESERVED = \
    range(30)


class VM:
    """
    This is a stack machine built on top of python.
    Its task is to execute the given array of instructions.
    """

    _SIGEXIT = KeyboardInterrupt

    def __init__(self):
        self.line = 0
        self.program = []
        self.stack = []
        self.var_values = {}

    def _push(self):
        """
        Push a number into the stack.
        """
        self.stack.append(self.program[self.line + 1])
        self.line += 2

    def _jmp(self):
        """
        Virtual machine jump (like goto). JMP + absolute_line.
        """
        self.line = self.program[self.line + 1]

    def _jmpif(self):
        """
        Jump if the element above is true.
        """
        if self.stack.pop():
            self.line = self.program[self.line + 1]
        else:
            self.line += 2

    def _jmpunl(self):
        """
        Jump if the element above is false.
        """
        if self.stack.pop():
            self.line += 2
        else:
            self.line = self.program[self.line + 1]

    def _unary_op(func):
        """
        Returns decorator for unary operation.
        """
        def opn(self):
            self.stack.append(func(self.stack.pop()))
            self.line += 1
        return opn

    def _binary_op(func):
        """
        Returns decorator for binary operation.
        """
        def opn(self):
            self.stack.append(func(self.stack.pop(), self.stack.pop()))
            self.line += 1
        return opn

    def _value(self):
        """
        Retreive value from the previous variable.
        """
        self.stack.append(self.var_values[self.program[self.line + 1]])
        self.line += 2

    def _assign(self):
        """
        Assign variable to a value.
        """
        self.var_values[self.program[self.line + 1]] = self.stack.pop()
        self.line += 2

    def _exit(self):
        """
        Stop executing the code.
        """
        raise self._SIGEXIT

    """
    The following constants are numbers which are matched with instructions.
    """
    MATCH = {
        PUSH:    _push,
        JMP:     _jmp,
        JMPIF:   _jmpif,
        JMPUNL:  _jmpunl,
        EXIT:    _exit,
        # UNARY
        NOT:     _unary_op(lambda x: int(not x)),
        NEG:     _unary_op(lambda x: int(neg(x))),
        POS:     _unary_op(lambda x: int(pos(x))),
        ABS:     _unary_op(operator.__abs__),
        # BINARY
        LT:      _binary_op(lambda x, y: int(x < y)),
        LE:      _binary_op(lambda x, y: int(x <= y)),
        EQ:      _binary_op(lambda x, y: int(x == y)),
        NE:      _binary_op(lambda x, y: int(x != y)),
        GE:      _binary_op(lambda x, y: int(x >= y)),
        GT:      _binary_op(lambda x, y: int(x > y)),

        OR:      _binary_op(lambda x, y: int(x or y)),
        AND:     _binary_op(lambda x, y: int(x and y)),
        XOR:     _binary_op(lambda x, y: int(x ^ y)),

        LSHIFT:  _binary_op(operator.__lshift__),
        RSHIFT:  _binary_op(operator.__rshift__),
        MOD:     _binary_op(operator.__mod__),
        ADD:     _binary_op(operator.__add__),
        SUB:     _binary_op(operator.__sub__),
        MUL:     _binary_op(operator.__mul__),
        DIV:     _binary_op(operator.__div__),
        POW:     _binary_op(operator.__pow__),
        #
        VALUE:   _value,
        ASSIGN:  _assign,
        RESERVED: _exit
    }

    def Execute(self, program):
        """
        Executes the operations stack.
        """
        self.line = 0
        self.program = program
        OPERATIONS = [
            "PUSH", "JMP", "JMPIF", "JMPUNL", "EXIT", "NOT", "NEG", "POS",
            "ABS", "LT", "LE", "EQ", "NE", "GE", "GT", "GT", "OR", "AND",
            "XOR", "LSHIFT", "RSHIFT", "MOD", "ADD", "SUB", "MUL", "DIV",
            "POW", "VALUE", "ASSIGN", "RESERVED"
        ]
        print [OPERATIONS[step] if type(step) == int and step < len(OPERATIONS) else step for step in self.program]
        while True:
            operation = self.program[self.line]
            try:
                step = self.program[self.line]
                print "(" + str(self.line) + ":" + (OPERATIONS[step] if type(step) == int and step < len(OPERATIONS) else step) + ")\t" + str(self.stack)
                if self.MATCH[operation](self) == EXIT:
                    raise self._SIGEXIT
            except self._SIGEXIT:
                break
        return self.stack
