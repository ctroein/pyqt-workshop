# pyqt-workshop
GUI programming tutorial for InfraVis days in Lund 2024

You will create a small graphical user interface for starting your webcam and plotting data from the camera.
We'll use [Qt](https://www.qt.io/) for the GUI, but for simplicity we'll borrow some high-level camera/image functionality from OpenCV.

1. Install PyQt to use the Qt GUI system from Python, plus OpenCV and matplotlib:

    - If using pip: `pip install pyqt5 pyqt5-tools opencv-python matplotlib`
    - If using conda: `conda install pyqt opencv matplotlib`

2. Run Qt Designer

    - with pip and pyqt5-tools: `pyqt5-tools designer`
    - with conda: `designer`

3. Draw a GUI with:

    - SpinBoxes called cameraNum, videoWidth and videoHeight (with suitable defaults)
    - PushButtons called startButton and stopButton for starting/stopping video capture
    - Widget called imagePlot with room for a histogram plot
    - Optionally:
        - ComboBox or other selector for red/green/blue histogram
        - PushButton called saveButton for saving the image

4. Save GUI and generate Python code for it:

    - `pyuic5 your_gui_file.ui -o your_gui_file.py`

5. Start from `gui-framework.py` and edit to make a working application. Search for "TODO".
    - Load the UI-generating code, e.g. from your_gui_file.py.
    - Connect the buttons you have drawn to the corresponding functions for starting/stopping the video capture.
    - Enable plotting of the histogram of pixel values, possibly with additional input controls etc.
    - Add saving of the plotted file.