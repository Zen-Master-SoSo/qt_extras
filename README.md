# qt_extras

Provides various extras for PyQt, including menu_button, list_button,
list_layouts, autofit, SigBlock, ShutUpQT, WidgetDisabler and DevilBox


## Classes:

### SigBlock:

A context manager which blocks widgets from generating signals.

Use like:

```python
with SigBlock(b_open, b_close):
	b_open.setChecked(True)
	b_close.setChecked(False)
```

### ShutUpQT(object):

A context manager for temporarily supressing DEBUG level messages.
Primarily used when loading a Qt graphical user interface using uic.

```python
with ShutUpQT():
	uic.loadUi(join(dirname(__file__), 'dialog.ui'), self)
```

### WidgetDisabler:

A context manager that disables every widget in a window.

### DevilBox(QMessageBox):

Quick and dirty error message dialog.

```python
if error:
	DevilBox('Oh boy, this is gonna be bad...')
```

## Sub-modules:

### menu_button module

Provides a pushbutton with an integrated drop-down menu.

Usage (inside a dialog created by QtDesigner):

```python
menu_button = QtMenuButton(self)
self.layout().replaceWidget(self.menu_button_placeholder, menu_button)
self.menu_button_placeholder.deleteLater()
self.b_menu = menu_button

action = QAction('Do the first thing', self.b_menu)
action.triggered.connect(self.slot_first_thing)
self.b_menu.addAction(action)

action = QAction('Do the second thing', self.b_menu)
action.triggered.connect(self.slot_second_thing)
self.b_menu.addAction(action)
```

### list_button module

Pushbutton with an integrated drop-down list containing text and data.

### list_layouts module

"Collection" layouts which act like lists.

```python
frame = QFrame()
layout = VListLayout()
frame.setLayout(layout)
for string in strings:
	layout.append(QLabel(string, frame))
for widget in layout:
	# do something ...
for widget in reversed(layout):
	# do something ...
print(len(layout))
item1 = layout[1]
item2 = layout[2]
item3 = layout[3]
layout.swap(item1, item2)
layout.remove(item3)
```

### autofit module

Functions to abbreviate widget text to fit inside a widget's available space.

#### autofit

Applies the "autofit" effect on a QPushButton, QCheckBox, QRadioButton, or QLabel.

Usage:

	label = QLabel(text, self)
	autofit(label)

After applying the effect, when the widget's text is changed using
"setText", or when the widget is resized, the text will be abrreviated if
necessary to fit inside the available space.

Shortens the text to fit buttons, labels, etc. by eliminating first spaces, then
vowels, then consonants and numbers, starting from the beginning and ending and
moving towards the center of the text.

#### elide

Applies the "elide" effect on a QPushButton, QCheckBox, QRadioButton, or QLabel.

Usage:

	label = QLabel(text, self)
	elide(label)

After applying the effect, when the widget's text is changed using
"setText", or when the widget is resized, the text will be abrreviated if
necessary to fit inside the available space.

Shortens the text to fit buttons, labels, etc. by adding an elide mark "..."

### info module

Provides a command-line tool which accepts a PyQT class name and provides a
list of all class members or an import statement. By default, shows all public
members of the given class.

```
usage: qtinfo [-h] [--import-statement] ClassName [ClassName ...]

positional arguments:
  ClassName             Class to inspect

optional arguments:
  -h, --help            show this help message and exit
  --import-statement, -i
                        Show import statement

```
