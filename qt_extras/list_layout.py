#  qt_extras/qt_extras/list_layout.py
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
"Collection" layouts which act like lists.
"""
import logging
from math import ceil
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout, QSpacerItem, QSizePolicy

HORIZONTAL_FLOW = 0
VERTICAL_FLOW = 1


class _ListLayout:
	"""
	Abstract class which is the base of the list layouts.
	"""

	sig_len_changed = pyqtSignal()

	def __init__(self):
		super().__init__()
		self.items = []

	def __iter__(self):
		return self.items.__iter__()

	def __reversed__(self):
		return self.items.__reversed__()

	def __contains__(self, item):
		return item in self.items

	def __len__(self):
		return len(self.items)

	def __bool__(self):
		return bool(self.items)

	def __getitem__(self, idx):
		return self.items[idx]

	def append(self, item):
		raise NotImplemented()

	def insert(self, index, item):
		raise NotImplemented()

	def remove(self, item):
		raise NotImplemented()

	def swap(self, item_a, item_b):
		if not item_a in self.items or not item_b in self.items:
			raise ValueError("Item not in list layout")
		index_a = self.items.index(item_a)
		index_b = self.items.index(item_b)
		if index_a < index_b:
			self.replaceWidget(item_a, item_b)
			self.insertWidget(index_b, item_a)
		else:
			self.replaceWidget(item_b, item_a)
			self.insertWidget(index_a, item_b)
		self.items[index_a] = item_b
		self.items[index_b] = item_a

	def clear(self):
		"""
		Clears (and deletes) all the widgets in this layout.
		"""
		while item := self.takeAt(0):
			if widget := item.widget():
				widget.deleteLater()
		self.items = []
		self.sig_len_changed.emit()

	def count(self):
		return len(self.items)

	def index(self, item):
		return self.items.index(item)


class _ListLinearLayout(_ListLayout):
	"""
	Abstract class which handles box (not grid) layouts.
	"""

	def remove(self, item):
		"""
		Removes the item from the layout, and calls "item.deleteLater()" to actually
		delete the widget.
		"""
		if item not in self.items:
			raise ValueError("Item not in list layout")
		index = self.items.index(item)
		del self.items[index]
		item.deleteLater()
		self.sig_len_changed.emit()

	def move_previous(self, item):
		if item not in self.items:
			raise ValueError("Item not in list layout")
		index = self.items.index(item)
		if index == 0:
			raise ValueError("Item is first in layout")
		self.swap(item, self.items[index - 1])

	def move_next(self, item):
		if item not in self.items:
			raise ValueError("Item not in list layout")
		index = self.items.index(item)
		if index == len(self.items) - 1:
			raise ValueError("Item is last in layout")
		self.swap(item, self.items[index + 1])


class _ListBoxLayout(_ListLinearLayout):
	"""
	Abstract class which handles box (not grid) layouts.
	"""

	def __init__(self, /, end_space = None):
		"""
		"end_space" is optional spacing with the given stretch factor
		to append to the end of the list.
		"""
		super().__init__()
		self.end_space = end_space
		if self.end_space is not None:
			self.addStretch(self.end_space)

	def append(self, item):
		if self.end_space is None:
			self.addWidget(item)
		else:
			self.insertWidget(len(self.items), item)
		self.items.append(item)
		self.sig_len_changed.emit()

	def insert(self, index, item):
		if not 0 <= index <= len(self.items):
			raise IndexError()
		if index == len(self.items):
			self.append(item)
		else:
			self.items.insert(index, item)
			self.insertWidget(index, item)
		self.sig_len_changed.emit()

	def clear(self):
		super().clear()
		if self.end_space is not None:
			self.addStretch(self.end_space)


class HListLayout(QHBoxLayout, _ListBoxLayout):
	"""
	A horizontal layout which behaves just like a python list.
	"""


class VListLayout(QVBoxLayout, _ListBoxLayout):
	"""
	A vertical layout which behaves just like a python list.
	"""


class GListLayout(_ListLayout, QGridLayout):
	"""
	Extends QGridLayout to create a layout with a fixed number of columns
	or rows, which increases the number of columns or rows in the non-fixed axis
	when needed.

	By default, adds items left-to-right, top-to-bottom. Change this using
	one of the direction constants.

	Create a GListLayout with two columns:

		lo = GListLayout(2, flow = VERTICAL_FLOW)

	Create a GListLayout with four rows:

		lo = GListLayout(4, flow = HORIZONTAL_FLOW)

	"""

	def __init__(self, columns_or_rows, flow = HORIZONTAL_FLOW):
		"""
		The meaning of columns_or_rows depends on "flow".
		If the flow is horizontal, items are added left to right, then top to bottom.
		If the flow is vertical, items are added top to bottom, then left to right.
		"""
		super().__init__()
		self.columns_or_rows = columns_or_rows
		self.flow = flow

	def append(self, item):
		tup = self._place_widget(item, len(self.items))
		self.items.append(item)
		self.sig_len_changed.emit()
		return tup

	def insert(self, index, item):
		if not 0 <= index <= len(self.items):
			raise IndexError()
		if index == len(self.items):
			tup = self.append(item)
		else:
			self._take_all_from(index)
			tup = self._place_widget(item, index)
			self.items.insert(index, item)
			self._add_all_from(index + 1)
		self.sig_len_changed.emit()
		return tup

	def remove(self, item):
		if item not in self.items:
			raise ValueError('Item not in list layout')
		index = self.items.index(item)
		self._take_all_from(index)
		del self.items[index]
		self._add_all_from(index)
		self.sig_len_changed.emit()

	def set_columns(self, columns):
		if columns != self.columns_or_rows or self.flow != HORIZONTAL_FLOW:
			self._take_all_from(0)
			self.columns_or_rows = columns
			self.flow = HORIZONTAL_FLOW
			self._add_all_from(0)
			self.sig_len_changed.emit()

	def set_rows(self, rows):
		if rows != self.columns_or_rows or self.flow != VERTICAL_FLOW:
			self._take_all_from(0)
			self.columns_or_rows = rows
			self.flow = VERTICAL_FLOW
			self._add_all_from(0)
			self.sig_len_changed.emit()

	def _place_widget(self, item, index):
		"""
		Puts the given widget in the correct cell for the given index
		"""
		if self.flow == HORIZONTAL_FLOW:
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


class ColumnListLayout(QGridLayout, _ListLinearLayout):
	"""
	Extends QGridLayout to allow for arranging items in columns which wrap
	automatically according to the item's sizeHint.

	You must call "reflow()" on your instance of this class if the container which
	uses this layout resizes, or else contained widgets may be squeezed.
	"""

	def __init__(self, flow = HORIZONTAL_FLOW, end_space = False):
		"""
		"flow" determines whether to add items left-to-right, or top-to-bottom. If you
		want to add items left-to-right, use HORIZONTAL_FLOW, If you want to add items
		top-to-bottom, use VERTICAL_FLOW,
		"""
		super().__init__()
		self.flow = flow
		self.end_space = end_space
		self.height = None
		self.width = None

	def reflow(self, *, height = None, width = None):
		"""
		Calculates number of columns or rows needed and reorders accordingly.
		"""
		if height:
			self.height = height
		if width:
			self.width = width
		if len(self.items) == 0:
			return
		if self.flow == HORIZONTAL_FLOW:
			if self.width is None:
				raise RuntimeError('Cannot reflow with unknown width')
			widget_widths = [ item.sizeHint().width() for item in self.items ]
			flow_scenario = best_flow_scenario(widget_widths, self.width, self.spacing())
			while item := self.takeAt(0):
				pass
			for row, items in enumerate(flow_scenario.partition(self.items)):
				for col, item in enumerate(items):
					self.addWidget(item, row, col)
			if self.end_space:
				self.addItem(QSpacerItem(0, 0, QSizePolicy.MinimumExpanding, QSizePolicy.Preferred),
					0, self.columnCount(), self.rowCount() - 1, 1)
		else:
			if self.height is None:
				raise RuntimeError('Cannot reflow with unknown height')
			widget_heights = [ item.sizeHint().height() for item in self.items ]
			flow_scenario = best_flow_scenario(widget_heights, self.height, self.spacing())
			while item := self.takeAt(0):
				pass
			for col, items in enumerate(flow_scenario.partition(self.items)):
				for row, item in enumerate(items):
					self.addWidget(item, row, col)
			if self.end_space:
				self.addItem(QSpacerItem(0, 0, QSizePolicy.Preferred, QSizePolicy.MinimumExpanding),
					self.rowCount(), 0, 1, self.columnCount() - 1)

	def append(self, item):
		self.items.append(item)
		self.reflow()
		self.sig_len_changed.emit()

	def insert(self, index, item):
		if not 0 <= index <= len(self.items):
			raise IndexError()
		if index == len(self.items):
			self.append(item)
		else:
			self.items.insert(index, item)
		self.reflow()
		self.sig_len_changed.emit()

	def remove(self, item):
		super().remove(item)
		self.reflow()

	def swap(self, item_a, item_b):
		if not item_a in self.items or not item_b in self.items:
			raise ValueError("Item not in list layout")
		index_a = self.items.index(item_a)
		index_b = self.items.index(item_b)
		self.items[index_a] = item_b
		self.items[index_b] = item_a
		self.reflow()


class FlowScenario:

	def __init__(self, widget_sizes, spacing, x_axis_count):
		self.spacing = spacing
		self.x_axis_len = x_axis_count
		self.y_axis_len = ceil(len(widget_sizes) / self.x_axis_len)
		self.y_axis_list = self.partition(widget_sizes)
		self.x_axis_sizes = [
			max(
				self.y_axis_list[i][x_axis] if x_axis < len(self.y_axis_list[i]) else 0
				for i in range(self.y_axis_len)
			)
			for x_axis in range(self.x_axis_len)
		]

	def space_needed(self):
		return sum(self.x_axis_sizes) + self.spacing * (len(self.x_axis_sizes) - 1)

	def partition(self, items):
		return [
			items[i * self.x_axis_len : i * self.x_axis_len + self.x_axis_len]
			for i in range(self.y_axis_len)
		]


def best_flow_scenario(widget_sizes, container_size, spacing):
	x_axis_count = 1
	cumulative_size = 0
	for widget_size in widget_sizes:
		cumulative_size += widget_size
		if cumulative_size >= container_size:
			break
		cumulative_size += spacing
		x_axis_count += 1
	flow_scenario = None
	while x_axis_count > 1:
		flow_scenario = FlowScenario(widget_sizes, spacing, x_axis_count)
		if flow_scenario.space_needed() <= container_size:
			break
		x_axis_count -= 1
	return flow_scenario or FlowScenario(widget_sizes, spacing, 1)


#  end qt_extras/qt_extras/list_layout.py
