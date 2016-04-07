#!/usr/bin/env python2

import sys

from VirtualMachine import *


class Compiler:
    VARIABLES = {}

    def __init__(self):
        self.program = []
        self.vm = VM()

    def Compile(self, tree, indent=0):
        print('|   ' * indent + str(tree))
        indent += 1
        if(type(tree) == str):
            print "COMPILING " + tree
            return
        GOAL = tree.nonterminal
        if GOAL == 'Start':  # Program
            self.Compile(tree.children[0], indent)
        elif GOAL == 'Program':  # Cmd | { ListOfCmds }
            if len(tree.children) == 1:
                self.Compile(tree.children[0], indent)
            elif len(tree.children) == 3:
                self.Compile(tree.children[1], indent)
        elif GOAL == 'ListOfCmds':  # ListOfCmds;Cmd | Cmd
            self.Compile(tree.children[0], indent)
            if len(tree.children) == 3:
                self.Compile(tree.children[2], indent)
        elif GOAL == 'Cmd':  # Assignment | Loop | Condition | None
            self.Compile(tree.children[0], indent)
        elif GOAL == 'Assignment':  # Variable = Value
            self.program += [PUSH, tree.children[2], ASSIGN, tree.children[0]]
        elif GOAL == 'Loop':  # while ( cmd ) Program
            self.program += [PUSH, tree.children[2], PUSH, '0', EQ]
            self.program += [JMPIF, RESERVED]
            jmp_before_body = len(self.program)
            self.program += [JMP, jmp_before_body]
            self.Compile(tree.children[4])
            self.program[jmp_before_body - 1] = len(self.program)
        elif GOAL == 'Condition':  # if (Value) Program | if (Value) Program else Program
            if len(tree.children) == 5:  # if (Variable) Program
                self.program += [PUSH, tree.children[2], PUSH, '0', EQ]
                self.program += [JMPIF, RESERVED]
                jmp_before_if = len(self.program)
                self.Compile(tree.children[4], indent)
                self.program[jmp_before_if - 1] = len(self.program)
            if len(tree.children) == 7:  # if (Variable) Program else Program
                self.program += [PUSH, tree.children[2], PUSH, '0', EQ]
                self.program += [JMPIF, RESERVED]  # jump to after if
                jmp_before_if = len(self.program)
                self.Compile(tree.children[4], indent)
                self.program += [JMP, RESERVED]  # jump to after else
                self.program[jmp_before_if - 1] = len(self.program)
                jmp_before_else = len(self.program)
                self.Compile(tree.children[6])
                self.program[jmp_before_else - 1] = len(self.program)
