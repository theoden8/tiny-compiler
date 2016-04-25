#!/usr/bin/env python2

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
        root = tree.nonterminal
        branches = tree.children
        if root == 'Start':  # Program
            self.Compile(branches[0], indent)
        elif root == 'Program':  # Cmd | { ListOfCmds }
            if len(branches) == 1:
                self.Compile(branches[0], indent)
            elif len(branches) == 3:
                self.Compile(branches[1], indent)
        elif root == 'ListOfCmds':  # ListOfCmds;Cmd | Cmd
            self.Compile(branches[0], indent)
            if len(branches) == 3:
                self.Compile(branches[2], indent)
        elif root == 'Cmd':  # Assignment | Loop | Condition | None
            self.Compile(branches[0], indent)
        elif root == 'Assignment':  # Variable = Eval
            self.Compile(branches[2])
            self.program += [ASSIGN, branches[0]]
        elif root == 'Loop':  # while ( Eval ) Program
            jmp_before_loop = len(self.program)
            self.Compile(branches[2])
            self.program += [PUSH, '0', EQ, JMPIF, RESERVED]
            jmp_before_body = len(self.program)
            self.Compile(branches[4])
            self.program += [JMP, jmp_before_loop]
            self.program[jmp_before_body - 1] = len(self.program)
        elif root == 'Condition':  # if (Eval) Program | if (Eval) Program else Program
            if len(branches) == 5:  # if (Variable) Program
                self.Compile(branches[2])
                self.program += [PUSH, '0', EQ, JMPIF, RESERVED]
                jmp_before_if = len(self.program)
                self.Compile(branches[4], indent)
                self.program[jmp_before_if - 1] = len(self.program)
            if len(branches) == 7:  # if (Variable) Program else Program
                self.Compile(branches[2])
                self.program += [PUSH, '0', EQ, JMPIF, RESERVED]  # jump to after if
                jmp_before_if = len(self.program)
                self.Compile(branches[4], indent)
                self.program += [JMP, RESERVED]  # jump to after else
                self.program[jmp_before_if - 1] = len(self.program)
                jmp_before_else = len(self.program)
                self.Compile(branches[6])
                self.program[jmp_before_else - 1] = len(self.program)
        elif root == 'Eval':
            EVAL = branches[0]
            if EVAL.isdigit(): # Value
                self.program += [PUSH, branches[0]]
            elif EVAL.isalnum(): # Variable
                self.program += [VALUE, branches[0]]
