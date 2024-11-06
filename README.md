# pyqt-workshop
GUI programming tutorial for InfraVis days in Lund 2024

You will create a small graphical user interface for starting your webcam
and plotting data from the camera.

We'll use [Qt](https://www.qt.io/) for the GUI, but for simplicity we'll
borrow some high-level camera/image functionality from OpenCV. Python
bindings for Qt are available in two competing packages, PyQt and PySide,
which are nearly identical (and closely based on the Qt C++ API). Here we'll
use PyQt5.

Qt interfaces basically consist of a lot of widgets (from many different
classes that inherit QWidget) arranged by means of layouts (from several
different that inherit QLayout). Widgets often contain other widgets, as we
will see.

Widgets and other components are connected by [signals and
slots](https://doc.qt.io/qt-6/signalsandslots.html). A widget such as a
QPushButton or QLineEdit generates a specific set of signals when it is
pressed, edited etc, and we can *connect* signals to functions in our
program. A slot is a essentially a function. (Signals/slots are often used
for input events, such as when a widget receives information about mouse
movement.)

A matplotlib plot is integrated in one of the widgets in this tutorial to
show how data can be displayed in a user interface.

1. Install PyQt to use the Qt GUI system from Python, plus OpenCV and matplotlib:

    - If using pip: `pip install pyqt5 pyqt5-tools opencv-python matplotlib`
    - If using conda: `conda install pyqt opencv matplotlib`

2. Run Qt Designer

    - with pip and pyqt5-tools: `pyqt5-tools designer`
    - with conda: `designer`

3. Draw a GUI with:

    - [QSpinBoxes](https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QSpinBox.html)
      called cameraNum, videoWidth and videoHeight (with suitable defaults)
    - [QPushButtons](https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QPushButton.html)
      called startButton and stopButton for starting/stopping video capture
    - QWidget called imagePlot with room for a histogram plot
    - Optionally:
        - [QComboBox](https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QComboBox.html)
          or other selector for red/green/blue histogram
        - QPushButton called saveButton for saving the image

4. Save GUI and generate Python code for it:

    - `pyuic5 your_gui_file.ui -o your_gui_file.py`

5. Start from `gui-framework.py` and edit to make a working application. Search for "TODO".
    - Load you UI-generating code, e.g. from your_gui_file.py
    - Connect the buttons you have drawn to the corresponding functions for starting/stopping the video capture
    - Enable plotting of the histogram of pixel values, possibly with additional input controls etc.
    - Add saving of the plotted file, e.g. using
      [QFileDialog.getSaveFileName](https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QFileDialog.html#PySide2.QtWidgets.PySide2.QtWidgets.QFileDialog.getSaveFileName)
