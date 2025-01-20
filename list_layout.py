#  qt_extras/list_layout.py
#
#  Copyright 2024 liyang <liyang@veronica>
#
"""
"Collection" layouts which act like lists.
"""
from PyQt5.QtWidgets import QLayout, QBoxLayout, QHBoxLayout, QVBoxLayout, QGridLayout, QWidget


class _ListLayout(QLayout):
	"""
	Abstract class which is the base of the list layouts.
	"""

	def __iter__(self):
		return self.items.__iter__()

	def __reversed__(self):
		return self.items.__reversed__()

	def __contains__(self, item):
		return item in self.items

	def __len__(self):
		return len(self.items)

	def __getitem__(self, idx):
		return self.items[idx]

	def append(self, item):
		if self.end_space is None:
			self.addWidget(item)
		else:
			self.insertWidget(len(self.items), item)
		self.items.append(item)

	def insert(self, index, item):
		if not (0 <= index <= len(self.items)):
			raise IndexError()
		if index == len(self.items):
			self.append(item)
		else:
			self.items.insert(index, item)
			self.insertWidget(index, item)

	def remove(self, item):
		if item not in self.items:
			raise ValueError("Item not in list layout")
		index = self.items.index(item)
		del self.items[index]
		item.deleteLater()

	def clear(self):
		for iter_index in reversed(range(len(self.items))):
			item = self.takeAt(iter_index)
			item.widget().deleteLater()
		self.items = []

	def count(self):
		return len(self.items)

	def index(self, item):
		return self.items.index(item)


class _ListBoxLayout(QBoxLayout, _ListLayout):

	def __init__(self, end_space=None):
		"""
		"end_space" is optional spacing with the given minimal size (int)
		to append to the end of the list.
		"""
		super().__init__()
		self.items = []
		self.end_space = end_space
		if self.end_space is not None:
			self.addStretch(self.end_space)



class HListLayout(QHBoxLayout, _ListBoxLayout):

	pass


class VListLayout(QVBoxLayout, _ListBoxLayout):

	pass



class GListLayout(QGridLayout, _ListLayout):
	"""
	Extends QGridLayout.
	By default, adds items left-to-right, top-to-bottom.
	Change this using one of the direction constants.
	"""

	HORIZONTAL_FLOW = 0
	VERTICAL_FLOW = 1

	def __init__(self, columns_or_rows = 1, flow = 0):
		super().__init__()
		self.items = []
		self.columns_or_rows = columns_or_rows
		self.flow = flow

	def append(self, item):
		tup = self._place_widget(item, len(self.items))
		self.items.append(item)
		return tup

	def insert(self, index, item):
		if not (0 <= index <= len(self.items)):
			raise IndexError()
		if index == len(self.items):
			return self.append(item)
		else:
			self._take_all_from(index)
			tup = self._place_widget(item, index)
			self.items.insert(index, item)
			self._add_all_from(index + 1)
			return tup

	def remove(self, item):
		if item not in self.items:
			raise ValueError('Item not in list layout')
		index = self.items.index(item)
		self._take_all_from(index)
		del self.items[index]
		item.deleteLater()
		self._add_all_from(index)

	def set_columns(self, columns):
		if columns != self.columns_or_rows or self.flow != GListLayout.HORIZONTAL_FLOW:
			self._take_all_from(0)
			self.columns_or_rows = columns
			self.flow = GListLayout.HORIZONTAL_FLOW
			self._add_all_from(0)

	def set_rows(self, rows):
		if rows != self.columns_or_rows or self.flow != GListLayout.VERTICAL_FLOW:
			self._take_all_from(0)
			self.columns_or_rows = rows
			self.flow = GListLayout.VERTICAL_FLOW
			self._add_all_from(0)

	def _place_widget(self, item, index):
		"""
		Puts the given widget in the correct cell for the given index
		"""
		if self.flow == GListLayout.HORIZONTAL_FLOW:
			row = index // self.columns_or_rows
			column = index - row * self.columns_or_rows
		else:
			column = index // self.columns_or_rows
			row = index - column * self.columns_or_rows
		self.addWidget(item, row, column)
		return row, column

	def _add_all_from(self, index):
		"""
		Puts items in the list back into the layout after insert / other.
		"""
		for iter_index in range(index, len(self.items)):
			self._place_widget(self.items[iter_index], iter_index)

	def _take_all_from(self, index):
		"""
		Takes items from the layout but leaves them in the list.
		"""
		for iter_index in reversed(range(index, len(self.items))):
			self.takeAt(iter_index)


#  end qt_extras/list_layout.py
