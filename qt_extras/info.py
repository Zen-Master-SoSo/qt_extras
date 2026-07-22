#  qt_extras/qt_extras/info.py
#
#  Copyright 2025 Leon Dionne <ldionne@dridesign.sh.cn>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
"""
Provides a command-line tool which accepts a PyQT class name and provides a
list of all class members or an import statement. By default, shows all public
members of the given class.
"""
import sys, argparse, importlib
from pkgutil import iter_modules
from os import get_terminal_size
from os.path import dirname
from column_soso import StringColumns
import PyQt5


QT_MODULES = list(f'PyQt5.{module.name}' for module in iter_modules([dirname(PyQt5.__file__)]))

class QtCls:
	"""
	Wrapper containing information on a Qt module and class.
	"""

	@classmethod
	def get_class(cls, class_name):
		class_name = class_name.lower()
		for qtmodule in QT_MODULES:
			module = importlib.import_module(qtmodule)
			for qtclass in dir(module):
				if qtclass.lower() == class_name:
					return QtCls(module, qtclass)
		return None

	def __init__(self, module, class_name):
		self.module = module
		self.class_name = class_name
		self.qtclass = getattr(module, class_name)

	def members(self, search_term):
		members = [ member for member in dir(self.qtclass) if member[0] != '_' ]
		if search_term:
			search_term = search_term.lower()
			return [ member for member in members if search_term in member.lower() ]
		return members

	def print_members(self, search_term):
		members = self.members(search_term)
		if members:
			print(f'{self.class_name} "{search_term}":'
				if search_term
				else self.class_name)
			print('-' * 20)
			term_size = get_terminal_size()
			columns = StringColumns(members, term_size.columns, 2)
			columns.print()
		else:
			print('Nothing found')

	def print_import_statement(self):
		print(f'from {self.module.__name__} import {self.class_name}')

	def print_help(self, search_term):
		if search_term:
			for member in self.members(search_term):
				help(getattr(self.qtclass, member))
		else:
			help(self.qtclass)


def main():
	parser = argparse.ArgumentParser()
	parser.epilog = __doc__
	parser.add_argument('ClassName', type = str, help = 'Class to inspect')
	parser.add_argument('SearchTerm', type = str, nargs = '?',
		help = 'Search term to filter class members shown.')
	group = parser.add_mutually_exclusive_group()
	group.add_argument('--help-text', '-H', action = 'store_true',
		help = "Show help for the given class or method")
	group.add_argument('--import-statement', '-i', action='store_true',
		help="Show import statement")
	options = parser.parse_args()

	cls = QtCls.get_class(options.ClassName)
	if cls is None:
		sys.stderr.write(f'Class not found: "{options.ClassName}"\n')
		return 1
	if options.import_statement:
		cls.print_import_statement()
	elif options.help_text:
		cls.print_help(options.SearchTerm)
	else:
		cls.print_members(options.SearchTerm)
	return 0


if __name__ == "__main__":
	sys.exit(main())


#  end qt_extras/qt_extras/info.py
