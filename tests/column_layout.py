#  qt_extras/tests/column_layout.py
#
#  Copyright 2026 Leon Dionne <ldionne@dridesign.sh.cn>
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
import logging
from random import randint
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QSpinBox, QLabel, \
							QShortcut, QVBoxLayout, QLayout, QFrame
from qt_extras.list_layout import ColumnListLayout, HORIZONTAL_FLOW


class MainWindow(QMainWindow):

	def __init__(self):
		super().__init__()
		shortcut = QShortcut(QKeySequence('Ctrl+Q'), self)
		shortcut.activated.connect(self.close)
		shortcut = QShortcut(QKeySequence('ESC'), self)
		shortcut.activated.connect(self.close)
		self.resize(450, 200)

		frame = QFrame(self)
		self.setCentralWidget(frame)
		lo = QVBoxLayout()
		lo.setSpacing(6)
		frame.setLayout(lo)

		button = QPushButton('Add widget', self)
		button.clicked.connect(self.slot_add_widget)
		lo.addWidget(button)

		lo.addWidget(QLabel('Index to add/remove:', self))

		self.spinbox = QSpinBox(self)
		self.spinbox.setMinimum(-1)
		self.spinbox.setMaximum(-1)
		lo.addWidget(self.spinbox)

		button = QPushButton('Insert widget', self)
		button.clicked.connect(self.slot_insert_widget)
		lo.addWidget(button)

		button = QPushButton('Remove widget', self)
		button.clicked.connect(self.slot_remove_widget)
		lo.addWidget(button)

		button = QPushButton('Clear list', self)
		button.clicked.connect(self.slot_clear_list)
		lo.addWidget(button)

		frm = QFrame(self)
		self.list = ColumnListLayout(HORIZONTAL_FLOW, end_space = True)
		self.list.setSpacing(0)
		frm.setLayout(self.list)
		lo.addWidget(frm)

		lo.addStretch()


	def resizeEvent(self, event):
		self.list.reflow(width = self.width())

	@pyqtSlot()
	def slot_add_widget(self):
		self.list.append(Thing(self))
		self.spinbox.setMaximum(len(self.list) - 1)

	@pyqtSlot()
	def slot_insert_widget(self):
		if self.spinbox.value() > -1:
			self.list.insert(self.spinbox.value(), Thing(self))
		self.spinbox.setMaximum(len(self.list) - 1)

	@pyqtSlot()
	def slot_remove_widget(self):
		if self.spinbox.value() > -1:
			widget = self.list[self.spinbox.value()]
			self.list.remove(widget)
			widget.deleteLater()

	@pyqtSlot()
	def slot_clear_list(self):
		self.list.clear()
		self.spinbox.setMaximum(-1)


class Thing(QWidget):

	ord = 1

	def __init__(self, parent):
		super().__init__(parent)
		lo = QVBoxLayout()
		lo.setContentsMargins(2,2,2,2)
		self.setLayout(lo)
		self.label = QLabel(f'Thing {Thing.ord} ' + ('X' * randint(1, 14)), self)
		self.layout().addWidget(self.label)
		Thing.ord += 1

	def __str__(self):
		return self.label.text()


if __name__ == "__main__":
	logging.basicConfig(
		level = logging.DEBUG,
		format = "[%(filename)24s:%(lineno)-4d] %(message)s"
	)
	app = QApplication([])
	window = MainWindow()
	window.show()
	app.exec()


#  end qt_extras/tests/column_layout.py
