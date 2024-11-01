#  qt_extras/__init__.py
#
#  Copyright 2024 liyang <liyang@veronica>
#

import os, sys, logging
sys.path.append(os.path.dirname(os.path.realpath(__file__)))


class SigBlock:
	"""
	A context manager that blocks pyqt signal generation.
	Pass one or more objects which extend QObject to the constructor,
	and while in this context, their signals are blocked. For example:

		with SigBlock(button):
			button.setChecked(True)

	"""

	def __init__(self, *qtcontrols):
		self.qtcontrols = qtcontrols

	def __enter__(self):
		for control in self.qtcontrols:
			control.blockSignals(True)

	def __exit__(self, *_):
		for control in self.qtcontrols:
			control.blockSignals(False)


class ShutUpQT(object):
	"""
	A context manager for temporarily supressing DEBUG level messages.
	Primarily used when loading a Qt graphical user interface using uic.
	"""

	def __init__(self, level=logging.ERROR):
		self.level = level

	def __enter__(self):
		self.root = logging.getLogger()
		self.previous_log_level = self.root.getEffectiveLevel()
		self.root.setLevel(self.level)

	def __exit__(self, *_):
		self.root.setLevel(self.previous_log_level)	# Carry on ...


# end qt_extras/__init__.py
