# 3D Print Error Detection System

This project is a deliverable prototype from the class ME266K at the University of Texas at Austin and was contributed by Kyle Hodowany, Rafiq Hamzeh, Manuel Salazar, and Travis Bouchard.

## Installation and Setup

### Hardware Setup
TODO
### Package Dependencies
This project requires prior installation of `Python` and the `pip` package manager. 

Run the command to install the dependencies for the project in the `requirements.txt` file under the `src` directory.
```
pip install -r src/requirements.txt
```
From there you have all the necessary libraries for the application.

### Starting the App
To run and launch the application, run the following command and an GUI window will pop up for your print session.
```
python3 src/app.py
```

## How to Use

This is where we talk about how a complete noob is going to use the application, with screenshots of what certain buttons do

After the software has been downloaded, all dependencies installed, and the phsical setup configured, the 3D Print Error Detection System (EDS) can be used. First connect an Intel RealSense camera to your device using an appropriate cable. Rename the .STL file as example.STL and place it in the src folder. Then run the app.py file to start the application and display the GUI. An example of the GUI display is shown below.

<p align="center">
  <img src="docRes/GUI Full Image.png" alt="GUI Full Image" width="500" height="auto"/>
</p>

The GUI is composed of several windows including the camera view window, the controls window, the sliced images window, and the error log window. The controls window is used to setup the parameters and slice the model, and is shown below.

<p align="center">
  <img src="docRes/Control Panel Image.png" alt="Control Panel Image" width="500" height="auto"/>
</p>

The first two chekcboxes can be used to disable and enable the stringing and image matching susbsystems. Below them, two sliders can be used to adjust the threshold values for the similarity score and stringing confidence. A color selector can be used to choose the filament color for the filter. The generate slices button will produce slices of the supplied model and populate the sliced images window. A drop down menu is used to match the sliced view to the orientation of the model with respect to the camera. The slices for x1, y1, x2, and y2 are shown in the images window for reference. Finally, a save error file button can be used to save the contents of the error log window.

### Connecting a Camera

### Loading a Model


## Technical Information

Our error detection currently has 2 subsystems in place for finding print defects from the camera feed: **2D Image Similarity** and **Stringing Machine Learning**. The main entry point for the application is located in `app.py`, however, various modules are located in the `src` directory for data processing.

### app.py

`app.py` is a Python script designed to interface with a 3D printer monitoring system. The application captures video frames, processes images, performs similarity comparisons, and detects stringing issues. It provides a graphical user interface (GUI) using Dear PyGui to display video feeds and control settings.

**App Class Initialization**
The App class initializes various attributes and components needed for the application, including:

- Configuration options (stringingEnabled, similarityEnabled, etc.)
- Instances of ImageProcessor, Modeler, Comparator, and Annotator classes
- RealSense pipeline configuration
- GUI creation

### annotator.py
TODO

### comparator.py
TODO

### imageProcessor.py
TODO

### modeler.py
TODO

## Future Work
TODO
