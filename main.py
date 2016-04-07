#!/usr/bin/env python

from Compiler import *
from Earley_Parser import *
from VirtualMachine import *
import KeywordSub


def separate_a_section():
    print "="*100

if __name__ == "__main__":
    c, vm = Compiler(), VM()
    source, rules = Tokenizer.get_list(), Tokenizer.get_rules()
    s = EarleyParser(rules).parse(KeywordSub.keywords_substitution(source))
    if(s is None):
        print
        print "Syntax error."
        sys.exit(1)
    # separate_a_section()
    # PrintTree(s)
    # separate_a_section()
    c.Compile(s)
    c.program += [EXIT]
    separate_a_section()
    vm.Execute(c.program)
    separate_a_section()
    print 'Values : ' + str(vm.var_values)
