#  qt_extras/list_layout.py
#
#  Copyright 2024 liyang <liyang@veronica>
#
"""
"Collection" layouts which act like lists:
"""
from PyQt5.QtWidgets import QBoxLayout, QHBoxLayout, QVBoxLayout


class ListLayout(QBoxLayout):
	"""
	Exposes the widgets in a layout as a list, ignoring spacers.
	"""

	def __init__(self, end_space=None):
		"""
		end_space (int) is optional spacing with the given minimal size
		to append to the end of the list.
		"""
		super().__init__(QBoxLayout.LeftToRight if isinstance(self, QHBoxLayout) else QBoxLayout.TopToBottom)
		self.items = []
		self.end_space = end_space
		if self.end_space is not None:
			self.addStretch(self.end_space)

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
		self.items.append(item)
		if self.end_space is None:
			self.addWidget(item)
		else:
			self.insertWidget(super().count() - 1, item)

	def insert(self, index, item):
		if index < 0:
			raise ValueError("Index must be >= 0")
		if index < len(self.items):
			layout_index = self.indexOf(self.items[index])
			self.items.insert(index, item)
			self.insertWidget(layout_index, item)
		else:
			self.append(item)

	def count(self):
		return len(self.items)

	def index(self, item):
		return self.items.index(item)

	def remove(self, item):
		if item not in self.items:
			raise Exception("Item not in list")
		i = self.items.index(item)
		del self.items[i]
		i = self.indexOf(item)
		if i < 0:
			raise Exception("Item not in layout")
		self.removeWidget(item)
		item.deleteLater()


class HListLayout(ListLayout, QHBoxLayout):

	pass


class VListLayout(ListLayout, QVBoxLayout):

	pass


#  end qt_extras/list_layout.py
