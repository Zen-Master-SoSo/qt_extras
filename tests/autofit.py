#  qt_extras/tests/autofit.py
#
#  Copyright 2024 liyang <liyang@veronica>
#
import qt_extras.autofit
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QShortcut, \
							QPushButton, QCheckBox, QRadioButton, QLabel, \
							QLineEdit, QVBoxLayout, QSizePolicy
from PyQt5.QtGui import QKeySequence


class MainWindow(QMainWindow):

	def __init__(self):
		super().__init__()

		layout = QVBoxLayout()
		ed = QLineEdit()

		layout.addWidget(QLabel('QPushbutton:', self))
		w = QPushButton(self)
		w.autoFit()
		w.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
		ed.textChanged.connect(w.setText)
		layout.addWidget(w)

		layout.addWidget(QLabel('QPushbutton with padding:', self))
		w = QPushButton(self)
		w.autoFit()
		w.setStyleSheet('QPushButton { padding: 16px; }')
		w.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
		ed.textChanged.connect(w.setText)
		layout.addWidget(w)

		layout.addWidget(QLabel('QLabel:', self))
		w = QLabel(self)
		w.autoFit()
		w.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
		ed.textChanged.connect(w.setText)
		layout.addWidget(w)

		layout.addWidget(QLabel('QLabel with padding:', self))
		w = QLabel(self)
		w.autoFit()
		w.setStyleSheet('QLabel { padding: 16px; }')
		w.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
		ed.textChanged.connect(w.setText)
		layout.addWidget(w)

		layout.addWidget(QLabel('QCheckBox:', self))
		w = QCheckBox(self)
		w.autoFit()
		w.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
		ed.textChanged.connect(w.setText)
		layout.addWidget(w)

		layout.addWidget(QLabel('QCheckBox with padding:', self))
		w = QCheckBox(self)
		w.autoFit()
		w.setStyleSheet('QCheckBox { padding: 16px; }')
		w.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
		ed.textChanged.connect(w.setText)
		layout.addWidget(w)

		layout.addWidget(QLabel('QRadioButton:', self))
		w = QRadioButton(self)
		w.autoFit()
		w.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
		ed.textChanged.connect(w.setText)
		layout.addWidget(w)

		layout.addWidget(QLabel('QRadioButton with padding:', self))
		w = QRadioButton(self)
		w.autoFit()
		w.setStyleSheet('QRadioButton { padding: 16px; }')
		w.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
		ed.textChanged.connect(w.setText)
		layout.addWidget(w)

		layout.addWidget(ed)

		w = QWidget()
		w.setLayout(layout)
		self.setCentralWidget(w)

		self.quit_shortcut = QShortcut(QKeySequence('Ctrl+Q'), self)
		self.quit_shortcut.activated.connect(self.close)
		self.esc_shortcut = QShortcut(QKeySequence('Esc'), self)
		self.esc_shortcut.activated.connect(self.close)


if __name__ == "__main__":
	app = QApplication([])
	window = MainWindow()
	window.move(QPoint(300,300))
	window.show()
	app.exec()


#  end qt_extras/tests/autofit.py
