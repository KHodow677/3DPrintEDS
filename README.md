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

**App Class Initialization**<br>
The App class initializes various attributes and components needed for the application, including:

- Configuration options (stringingEnabled, similarityEnabled, etc.)
- Instances of ImageProcessor, Modeler, Comparator, and Annotator classes
- RealSense pipeline configuration
- GUI creation

```python
class App:
    def __init__(self):
        # Attribute initialization
        # RealSense pipeline setup
        # GUI creation
        self.create_gui()
```

**GUI Components**<br>

The create_gui method sets up the graphical user interface using Dear PyGui. It creates several windows and widgets, such as:

- Video display window
- Image display window
- Controls window with checkboxes, sliders, color picker, dropdown menu, and buttons
- Error log window

```python
def create_gui(self):
    dpg.create_context()
    # GUI setup
    dpg.create_viewport(title='App', width=self.viewport_width, height=self.viewport_height, x_pos=0, y_pos=0)
    dpg.show_viewport()
```

**Callback Functions**<br>

Callback functions handle user interactions with the GUI elements, updating the application's state accordingly.

**Update Frame**<br>

The update_frame method captures a frame from the RealSense camera, processes it, and updates the texture displayed in the GUI.

```python
def update_frame(self):
    # Capture and process frame
    dpg.set_value(self.texture_id, texture_data.ravel())
    dpg.render_dearpygui_frame()
```

**Update Sliced Images**<br>

The update_sliced_images method loads and updates the displayed images corresponding to the selected view.

```python
def update_sliced_images(self):
    # Load and update images
```

**Save Function**<br>

The save_function method copies the error file to a new file with a timestamp in its name.

```python
def save_function(self):
    dest = 'src/error_file_' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")).replace(':','_')
    shutil.copy('src/error_file.txt', dest)
```

**Run Loop**<br>

The run method contains the main application loop, updating frames, checking for errors, and handling similarity and stringing detection.

```python
def run(self):
    while dpg.is_dearpygui_running():
        # Update and process frames
```

**Cleanup**<br>

The cleanup method stops the RealSense pipeline and destroys the Dear PyGui context when the application exits.

```python
def cleanup(self):
    self.pipeline.stop()
    dpg.destroy_context()
```

**Stringing Detection**<br>

The stringing_detection method captures a frame and annotates it if stringing is detected with a confidence above the threshold.

```python
def stringing_detection(self):
    # Detect stringing and update error log
```

**Frame Processing**<br>

Helper methods for frame processing, such as get_cropped_frame, get_sliced_frame, and get_darkened_frame, handle specific image manipulations.
Generate Slices

The generate_slices method triggers the modeler to run and updates the sliced images in the GUI.

```python
def generate_slices(self):
    self.modeler.run()
    self.update_sliced_images()
```

**Compare Frame Similarity**

The compare_frame_similarity method compares the current frame with a reference image to detect significant differences.

```python
def compare_frame_similarity(self):
    # Compare frames and update error log
```

**How to Extend the Application**<br>
**Adding New Features**<br>

To add new features to the application, follow these general steps:

- Update the GUI:
-   Modify the create_gui method to add new controls or windows.
        Create new callback functions to handle interactions with the new GUI elements.

    Implement New Functionalities:
        Add new methods to the App class to implement the desired functionality.
        Integrate these methods into the run loop if they need to be called periodically.

    Modify Existing Logic:
        Update existing methods to incorporate new behaviors or improve functionality.
        Ensure compatibility with existing features and maintain code readability.

Example: Adding a New Detection Feature

    Update the GUI:
        Add a new checkbox to enable/disable the feature.
        Create a slider or other controls if needed for configuration.

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
