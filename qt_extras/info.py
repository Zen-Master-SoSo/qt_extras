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


def print_columnar(items):
	term_size = get_terminal_size()
	columns = StringColumns(items, term_size.columns, 2)
	columns.print()


class AbstractEntity:
	"""
	Abstract base class of QtModule and QtClass
	"""

	def members(self, search_term):
		members = [ member for member in dir(self.actual_entity) if member[0] != '_' ]
		if search_term:
			search_term = search_term.lower()
			return [ member for member in members if search_term in member.lower() ]
		return members

	def print_members(self, search_term):
		members = self.members(search_term)
		if members:
			print(f'{self.name} "{search_term}":'
				if search_term
				else self.name)
			print('-' * 20)
			print_columnar(members)
		else:
			print('Nothing found')

	def print_help(self, search_term):
		if search_term:
			for member in self.members(search_term):
				help(getattr(self.actual_entity, member))
		else:
			help(self.actual_entity)


class QtModule(AbstractEntity):
	"""
	Wrapper providing information about a Qt module.
	"""

	@classmethod
	def get_module(cls, module_name):
		module_name = module_name.lower()
		for qtmodule in QT_MODULES:
			if module_name == qtmodule.lower():
				return QtModule(importlib.import_module(qtmodule))
		return None

	def __init__(self, module):
		self.actual_entity = module
		self.name = module.__name__

	def print_import_statement(self):
		print(f'import {self.name}')


class QtCls(AbstractEntity):
	"""
	Wrapper providing information about a Qt class.
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
		self.name = class_name
		self.actual_entity = getattr(module, class_name)

	def print_import_statement(self):
		print(f'from {self.module.__name__} import {self.name}')


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('EntityName', type = str, nargs = '?',
		help = 'Class or module to inspect')
	parser.add_argument('SearchTerm', type = str, nargs = '?',
		help = 'Search term to filter which members of the given Entity to show.')
	group = parser.add_mutually_exclusive_group()
	group.add_argument('--help-text', '-H', action = 'store_true',
		help = "Show pydoc help for the given module, class, or method")
	group.add_argument('--import-statement', '-i', action='store_true',
		help="Print the import statement for the given module or class.")
	parser.epilog = __doc__
	options = parser.parse_args()

	if options.EntityName:
		entity = QtModule.get_module(options.EntityName) \
			or QtModule.get_module('PyQt5.' + options.EntityName) \
			or QtCls.get_class(options.EntityName)
		if entity is None:
			sys.stderr.write(f'Module or class not found: "{options.EntityName}"\n')
			return 1
		if options.import_statement:
			entity.print_import_statement()
		elif options.help_text:
			entity.print_help(options.SearchTerm)
		else:
			entity.print_members(options.SearchTerm)
	else:
		print('PyQt modules available:')
		print('-' * 20)
		print_columnar(QT_MODULES)
	return 0


if __name__ == "__main__":
	sys.exit(main())


#  end qt_extras/qt_extras/info.py
