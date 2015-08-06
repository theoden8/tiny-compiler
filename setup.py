from distutils.cmd import Command
from distutils.errors import *

class open(Command):
	description = "Open all useful files of a project"
	def run(self):
		print "vim -p earley_parser.py source task"
