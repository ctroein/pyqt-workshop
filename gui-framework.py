#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 03:28:27 2019

@author: carl
"""

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer

import sys

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

    def updateImage(self, frame):
        "Use matplotlib functions to draw some graphics on self.axes"
        # TODO: Clear axes and draw a histogram or something
        ...
        # Don't forget to actually draw the stuff.
        self.draw()

class MyGUI(QtWidgets.QMainWindow, Ui_MainWindow):
    VIDEOTITLE = "Video stream"

    def __init__(self, parent=None):
        super().__init__(parent)
        # Build the GUI
        self.setupUi(self)

        # Add our matplotlib canvas to the empty imagePlot widget
        plotlayout = QtWidgets.QHBoxLayout(self.imagePlot)
        self._canvas = PlotCanvas()
        plotlayout.addWidget(self._canvas)

        # TODO: Connect button clicks and other input events
        # Example: connect the "clicked" event on self.startButton to
        # the startVideo function:
        # self.startButton.clicked.connect(self.startVideo)
        # ...

        # The cv2 capture device
        self._cap = None
        # Prepare a timer for polling the camera and updating the plot
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.processFrame)


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
        self._canvas.updateImage(frame)

    def startVideo(self):
        "Start the camera and start running the display timer"
        if self._cap is not None:
            return
        cap = cv2.VideoCapture(self.cameraNum.value())
        # Set camera frame size; this apparently only takes effect if the
        # size matches an existing camera mode.
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.videoWidth.value())
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.videoHeight.value())
        self._cap = cap
        # Make the timer fire every 10 ms
        self._timer.start(10)

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

    def saveImage(self):
        "Save the plotted image to a file"
        # TODO: Use QtWidgets.QFileDialog.getSaveFileName to get a file name
        file = "example.png"
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