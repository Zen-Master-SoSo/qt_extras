#  qt_extras/info.py
#
#  Copyright 2024 liyang <liyang@veronica>
#
import importlib, argparse

def print_members_of(class_name):
	for qtmodule in ['PyQt5', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets']:
		module = importlib.import_module(qtmodule)
		for qtclass in dir(module):
			if qtclass.lower() == class_name:
				for member in dir(getattr(module, qtclass)):
					if member[0] != '_':
						print(member)
				return

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.epilog = """
	Routines to show info from Qt classes.
	By default, shows an import statement for every Qt class discovered.
	If ClassName is given, shows all public members of that class.
	"""
	parser.add_argument('ClassName', type=str, nargs='+', help='Class to inspect')
	parser.add_argument('--import-statement', '-i', action='store_true', help="Show import statement")
	options = parser.parse_args()
	if options.import_statement:
		imports = {}
		for qtmodule in ['PyQt5', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets']:
			module = importlib.import_module(qtmodule)
			for qtclass in dir(module):
				if qtclass[0] != '_':
					imports[ str(qtclass).lower() ] = f'from {module.__name__} import {qtclass}'

	for class_name in options.ClassName:
		class_name = class_name.lower()
		if options.import_statement:
			if class_name in imports:
				print(imports[class_name])
		else:
			print_members_of(class_name)


#  end qt_extras/info.py
