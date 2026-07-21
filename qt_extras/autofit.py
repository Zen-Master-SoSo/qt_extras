#  qt_extras/qt_extras/autofit.py
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
Functions used for fitting text in a widget into a tight space.

First vowels and punctuation are removed, then other letters. Letters are
removed from the center to the ends, in keeping with the observation that:

  "aoccdrnig to a rscheearch at Cmabrigde Uinervtisy, it deosn’t mttaer in waht
  oredr the ltteers in a wrod are, the olny iprmoatnt tihng is taht the frist and
  lsat ltteer be in the rghit pclae."
"""
from functools import partial
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QStyle, QStyleOptionButton, \
							QPushButton, QCheckBox, QRadioButton, QLabel


__KEEPERS = list("bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ0123456789")
STYLE_OPTION = QStyleOptionButton()
ELIDE_CHARS = '...'


def available_width(widget):
	if isinstance(widget, QLabel):
		return widget.width() - 2
	if isinstance(widget, QPushButton):
		subelem = QStyle.SE_PushButtonContents
	elif isinstance(widget, QCheckBox):
		subelem = QStyle.SE_CheckBoxContents
	elif isinstance(widget, QRadioButton):
		subelem = QStyle.SE_RadioButtonContents
	return widget.width() + widget.style().subElementRect(subelem, STYLE_OPTION, widget).width()


# ----------------------
# AutoFit

def abbreviated_text(widget, text, *, fixed_width = None):
	"""
	Shortens text to fit buttons, labels, etc. by eliminating first spaces, then
	vowels, then consonants and numbers, starting from the beginning and ending and
	moving towards the center of the text.
	"""
	if len(text) == 1:
		return text
	available = fixed_width or available_width(widget)
	metrics = QFontMetrics(widget.font())
	remove_front = True
	while len(text) > 1 and metrics.boundingRect(text).width() > available:
		mid = len(text) // 2
		pop = None
		if remove_front:
			for i in range(mid, 0, -1):
				if not text[i] in __KEEPERS:
					pop = i
					break
		else:
			for i in range(mid, len(text)):
				if not text[i] in __KEEPERS:
					pop = i
					break
		if pop is None:
			pop = mid
		text = text[:pop] + text[pop + 1:]
		remove_front = not remove_front
	return text

def __set_abbreviated_text(widget, text):
	widget.qtxtra_autofit_text = text
	widget.qtxtra_autofit_set_text(abbreviated_text(widget, widget.qtxtra_autofit_text))

def __resize_abbreviated(widget, event):
	widget.qtxtra_autofit_resize_event(event)
	widget.qtxtra_autofit_set_text(abbreviated_text(widget, widget.qtxtra_autofit_text))

def autofit(widget):
	"""
	Applies the "autofit" effect on a QPushButton, QCheckBox, QRadioButton, or QLabel.

	Usage:

		label = QLabel(text, self)
		autofit(label)

	After applying the effect, when the widget's text is changed using
	"setText", or when the widget is resized, the text will be abrreviated if
	necessary to fit inside the available space.

	You should apply this effect in you form's constructor. Applying the effect
	after the form is shown can cause an endless recursion!
	"""
	if not isinstance(widget, (QPushButton, QCheckBox, QRadioButton, QLabel)):
		raise AttributeError('Cannot apply autofit effect to this widget')
	widget.qtxtra_autofit_text = ""
	widget.qtxtra_autofit_set_text = widget.setText
	widget.qtxtra_autofit_resize_event = widget.resizeEvent
	widget.setText = partial(__set_abbreviated_text, widget)
	widget.resizeEvent = partial(__resize_abbreviated, widget)


# ----------------------
# AutoElide

def elided_text(widget, text, *, fixed_width = None):
	"""
	Shortens the text to fit buttons, labels, etc. by adding an elide mark "..."
	"""
	if len(text) == 1:
		return text
	available = fixed_width or available_width(widget)
	metrics = QFontMetrics(widget.font())
	elide_width = metrics.boundingRect(ELIDE_CHARS).width()
	elide = ''
	while len(text) > 1 and (metrics.boundingRect(text).width() + elide_width) > available:
		text = text[:-1]
		elide = ELIDE_CHARS
	return text + elide

def __set_elided_text(widget, text):
	widget.qtxtra_elide_text = text
	widget.qtxtra_elide_set_text(elided_text(widget, widget.qtxtra_elide_text))

def __resize_elided(widget, event):
	widget.qtxtra_elide_resize_event(event)
	widget.qtxtra_elide_set_text(elided_text(widget, widget.qtxtra_elide_text))

def elide(widget):
	"""
	Applies the "elide" effect on a QPushButton, QCheckBox, QRadioButton, or QLabel.

	Usage:

		label = QLabel(text, self)
		elide(label)

	After applying the effect, when the widget's text is changed using
	"setText", or when the widget is resized, the text will be abrreviated if
	necessary to fit inside the available space.

	You should apply this effect in you form's constructor. Applying the effect
	after the form is shown can cause an endless recursion!
	"""
	if not isinstance(widget, (QPushButton, QCheckBox, QRadioButton, QLabel)):
		raise AttributeError('Cannot apply elide effect to this widget')
	widget.qtxtra_elide_text = ""
	widget.qtxtra_elide_set_text = widget.setText
	widget.qtxtra_elide_resize_event = widget.resizeEvent
	widget.setText = partial(__set_elided_text, widget)
	widget.resizeEvent = partial(__resize_elided, widget)


#  end qt_extras/qt_extras/autofit.py
