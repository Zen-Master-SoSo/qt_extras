#  qt_extras/info.py
#
#  Copyright 2024 liyang <liyang@veronica>
#
import importlib, argparse

def imports():
	for qtmodule in ['PyQt5', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets']:
		module = importlib.import_module(qtmodule)
		for qtclass in dir(module):
			if qtclass[0] == 'Q' or qtclass[0] == 'q':
				print(f'from {module.__name__} import {qtclass}')
		print()

def members():
	for class_name in options.ClassName:
		print_members_of(class_name.lower())

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
	p = argparse.ArgumentParser()
	p.epilog = """
	Routines to show info from Qt classes.
	By default, shows an import statement for every Qt class discovered.
	If ClassName is given, shows all public members of that class.
	"""
	p.add_argument('ClassName', type=str, nargs='*', help='Class to inspect')
	options = p.parse_args()
	if options.ClassName:
		members()
	else:
		imports()

#  end qt_extras/info.py
