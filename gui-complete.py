#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 03:28:27 2019

@author: carl
"""

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer

import sys
import numpy as np

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
matplotlib.use('QT5Agg')
import matplotlib.pyplot as plt

from guiexample import Ui_MainWindow
"Alternative way of importing UI, directly from .ui file"
# from PyQt5 import uic
# from pkg_resources import resource_filename
# Ui_MainWindow = uic.loadUiType(resource_filename(__name__, "guiexample.ui"))[0]

class PlotCanvas(FigureCanvas):
    "Canvas for drawing matplotlib figure in Qt widget"
    def __init__(self, parent=None):
        self.fig = plt.Figure()
        self.axes = self.fig.add_axes((0,0,1,1))
        self.axes.set_xlim(0, 256)

        super().__init__(self.fig)

    def updateImage(self, frame, rgb_index):
        "Draw a histogram in red, green or blue"
        color = [0., 0., 0.]
        color[rgb_index] = 1.
        self.axes.clear()
        rgb = frame.reshape((-1, 3))
        self.axes.hist(rgb[:, rgb_index], bins=np.arange(0, 256),
                       color=color)
        # Don't forget to actually draw the stuff.
        self.draw()

    def save(self, filename):
        self.fig.savefig(filename)


class MyGUI(QtWidgets.QMainWindow, Ui_MainWindow):
    VIDEOTITLE = "Video stream"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Make the About menu item work
        self.actionAbout.triggered.connect(
            lambda: QtWidgets.QMessageBox.information(
                self, "About", "This is fun. Lots of fun."))

        # TODO: Connect button clicks to functions
        self.startButton.clicked.connect(self.startVideo)
        self.stopButton.clicked.connect(self.stopVideo)
        self.saveButton.clicked.connect(self.saveImage)

        # Add our matplotlib canvas to the empty imagePlot widget
        self._canvas = PlotCanvas()
        plotlayout = QtWidgets.QHBoxLayout(self.imagePlot)
        plotlayout.addWidget(self._canvas)

        # The cv2 capture device
        self._cap = None
        # Prepare a timer for polling the camera and updating the plot
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.processFrame)
        # Enable/disable some buttons
        self.updateEnabled()


    def processFrame(self):
        "Pull a videoe fram from the camera and process it"
        if self._cap is None:
            print("Video not running")
            self._timer.stop()
            return
        ret, frame = self._cap.read()
        if not ret:
            print("Image read error; halting video stream")
            self.stopVideo()
            return
        # Open opencv HighGUI window and show the image
        cv2.imshow(self.VIDEOTITLE, frame)
        # Pass control to opencv to let it render the window
        cv2.waitKey(1)
        # Do something with the image in our plot widget
        self._canvas.updateImage(frame, self.plotType.currentIndex())

    def updateEnabled(self):
        "Enable/disable some GUI elements"
        playing = self._cap is not None
        self.startButton.setEnabled(not playing)
        self.stopButton.setEnabled(playing)
        self.saveButton.setEnabled(playing)

    def startVideo(self):
        "Start the camera and start running the display timer"
        if self._cap is not None:
            return
        cap = cv2.VideoCapture(self.cameraNum.value())
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.videoWidth.value())
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.videoHeight.value())
        self._cap = cap

        self._timer.start(10)
        # Enable/disable some buttons since the state changed
        self.updateEnabled()

    def stopVideo(self):
        "Shut down the camera and remove the camera image window"
        if self._cap is None:
            return
        self._cap.release()
        self._cap = None
        # There's no option to just close the window so we destroy it
        cv2.destroyWindow(self.VIDEOTITLE)
        # 1 ms opencv wait needed to make the window go away
        cv2.waitKey(1)
        self._timer.stop()
        # Enable/disable some buttons since the state changed
        self.updateEnabled()

    def saveImage(self):
        "Save the plotted image to a file"
        # Get a file name (or empty string). The second return value is the
        # selected filter which could be used to deduce a file format, but we
        # trust that matplotlib will deduce it from the filename.
        file, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save histogram", filter="PNG images (*.png)")
        if file:
            self._canvas.save(file)

if __name__ == '__main__':
    # Get the Qt system / application started
    app = QtWidgets.QApplication.instance()
    if not app:
        app = QtWidgets.QApplication(sys.argv)
    # OpenCV is imported here because of conflicts with Qt otherwise, at
    # least on my computer.
    import cv2
    window = MyGUI()
    window.show()
    app.lastWindowClosed.connect(app.quit);
    res = app.exec_()
