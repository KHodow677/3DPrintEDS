import dearpygui.dearpygui as dpg
import cv2 as cv
import numpy as np
import pyrealsense2 as rs
import sys, os
import pyautogui
import shutil
from datetime import datetime

sys.path.append(os.getcwd())

from src.imageProcessor import ImageProcessor
from src.modeler import Modeler
from src. comparator import Comparator


#Opening and clearing error file
f = open('src/error_file.txt', "w")
f.write('')
f.close()

class App:
    def __init__(self):
        self.stringingEnabled = True
        self.similarityEnabled = True
        self.similarityThreshold = 0.75
        self.confidenceThreshold = 0.7
        self.RGBColor = [255, 128, 0]
        self.outputStr_sim = ""
        self.outputStr_str = ""
        self.view = "x1"
        self.processor = ImageProcessor(self.RGBColor, 10)
        self.modeler = Modeler("example.STL", self.processor)
        self.comparator = Comparator()
        self.modeler.run()

        width, height = pyautogui.size()[0], pyautogui.size()[1]
        self.viewport_width, self.viewport_height = int(0.75*width), int(0.9*height)
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.frame_width = 640
        self.frame_height = 480
        self.frame_ar = self.frame_height/self.frame_width
        self.video_fps = 30
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)
        self.pipeline.start(self.config)
        
        self.create_gui()

        self.view_map = {
            "x1": "Image1.png",
            "y1": "Image2.png",
            "x2": "Image3.png",
            "y2": "Image4.png" 
        }


    def create_gui(self):
        dpg.create_context()
        margin = 20
        offset = 45

        dpg.setup_dearpygui()
        dpg.set_global_font_scale(1.25)
        
        def stringing_checkbox_change(sender,app_data):
            self.stringingEnabled = app_data

        def similarity_checkbox_change(sender,app_data):
            self.similarityEnabled = app_data
        
        def sim_slide_change(sender,app_data):
            self.similarityThreshold = app_data

        def conf_slide_change(sender,app_data):
            self.confidenceThreshold = app_data

        def color_select_change(sender,app_data):
            modified_color = app_data[:3]
            for i in range(len(modified_color)):
                modified_color[i] *= 255
                modified_color[i] = int(modified_color[i])
            self.RGBColor = modified_color
            self.processor.rgb_color = self.RGBColor

        def view_dropdown_callback(sender, app_data):
            self.view = app_data

        self.texture_data = np.zeros((self.frame_height, self.frame_width, 3), dtype=np.float32)

        with dpg.texture_registry(show=False):
            self.texture_id = dpg.add_raw_texture(self.frame_width, self.frame_height, self.texture_data.ravel(), tag="texture_tag", format=dpg.mvFormat_Float_rgb)

        width_x1, height_x1, channels_x1, data_x1 = dpg.load_image('Image1.png')
        aspectratio_x1 = height_x1/width_x1

        width_y1, height_y1, channels_y1, data_y1 = dpg.load_image('Image2.png')
        aspectratio_y1 = height_y1/width_y1

        width_x2, height_x2, channels_x2, data_x2 = dpg.load_image('Image3.png')
        aspectratio_x2 = height_x2/width_x2

        width_y2, height_y2, channels_y2, data_y2 = dpg.load_image('Image4.png')
        aspectratio_y2 = height_y2/width_y2

        with dpg.texture_registry(show=False):
            self.x1texture = dpg.add_dynamic_texture(width=width_x1, height=height_x1, default_value=data_x1, tag="x1image")

        with dpg.texture_registry(show=False):
            self.y1texture = dpg.add_dynamic_texture(width=width_y1, height=height_y1, default_value=data_y1, tag="y1image")
        
        with dpg.texture_registry(show=False):
            self.x2texture = dpg.add_dynamic_texture(width=width_x2, height=height_x2, default_value=data_x2, tag="x2image")
        
        with dpg.texture_registry(show=False):
            self.y2texture = dpg.add_dynamic_texture(width=width_y2, height=height_y2, default_value=data_y2, tag="y2image")
        
        
        with dpg.window(label="Video Window", width = self.frame_width, height = self.frame_height + 40, no_close=True):
            self.image_item = dpg.add_image("texture_tag")

        with dpg.window(label="Images", width = int(0.4*(self.viewport_width-self.frame_width)), height = self.viewport_height-55, pos = [self.frame_width,0], no_resize = True, no_close= True):
            # image_window_width = int(self.viewport_width-(self.frame_width)-(0.25*self.viewport_width)-margin)
            image_window_width = int(0.4*(self.viewport_width-self.frame_width))
            dpg.add_text(default_value='x1')
            dpg.add_image('x1image',label= 'x1', width = int(0.9*image_window_width),height = int(aspectratio_x1*0.9*image_window_width))
            dpg.add_text(default_value='y1')
            dpg.add_image('y1image',label= 'y1', width = int(0.9*image_window_width),height = int(aspectratio_y1*0.9*image_window_width))
            dpg.add_text(default_value='x2')
            dpg.add_image('x2image',label= 'x2', width = int(0.9*image_window_width),height = int(aspectratio_x2*0.9*image_window_width))
            dpg.add_text(default_value='y2')
            dpg.add_image('y2image',label= 'x2', width = int(0.9*image_window_width),height = int(aspectratio_y2*0.9*image_window_width))

        with dpg.window(label="Controls", width = int(self.frame_width), height = self.viewport_height-self.frame_height+40-3*offset, pos = [0,self.frame_height+40], no_resize = True, no_close= True):
            stringing_checkbox = dpg.add_checkbox(label='Stringing',default_value=True)
            
            dpg.set_item_callback(stringing_checkbox,stringing_checkbox_change)

            dpg.add_spacer(height = 10)

            similarity_checkbox = dpg.add_checkbox(label='Image Matching',default_value=True)
            dpg.set_item_callback(similarity_checkbox,similarity_checkbox_change)

            dpg.add_spacer(height = 20)
            sim_slider = dpg.add_slider_float(label = 'Similarity Value', max_value=1.0,default_value=0.75)
            dpg.set_item_callback(sim_slider,sim_slide_change)

            dpg.add_spacer(height = 20)

            conf_slider = dpg.add_slider_float(label = 'Confidence Value', max_value=1.0,default_value=0.7)
            dpg.set_item_callback(conf_slider,conf_slide_change)

            dpg.add_spacer(height = 20)

            color_select = dpg.add_color_edit((255, 128, 0, 255), label="Filament RGB",no_alpha = True)
            dpg.set_item_callback(color_select,color_select_change)

            dpg.add_spacer(height = 20)

            dpg.add_combo(items=["x1", "x2", "y1", "y2"], label="View", default_value="x1", callback=view_dropdown_callback)

            dpg.add_button(label="Generate Slices", callback= self.generate_slices)

            dpg.add_spacer(height = 10)

            dpg.add_button(label="Save Error File", callback= self.save_function)
            
        with dpg.window(tag = 'log',label="Error Log", width = self.viewport_width-self.frame_width-int(0.4*(self.viewport_width-self.frame_width))-margin, height = self.viewport_height-55, pos = [self.frame_width+int(0.4*(self.viewport_width-self.frame_width)),0], no_resize = True, no_close= True):
            # user data and callback set when button is created
            with dpg.group() as self.log_group:
                pass

        #Creating viewport to fit screen
        dpg.create_viewport(title='App', width=self.viewport_width, height=self.viewport_height, x_pos=0,y_pos=0,min_width=self.viewport_width,max_width=self.viewport_width,min_height=self.viewport_height,max_height=self.viewport_height)
        dpg.show_viewport()

    def update_frame(self):
        frames = self.pipeline.wait_for_frames()
        frame = np.asanyarray(frames.get_color_frame().get_data())
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame = self.processor.get_filtered_frame(frame)
        data = np.flip(frame, 2)
        data = np.asfarray(data, dtype=np.float32)
        texture_data = np.true_divide(data, 255.0)
        dpg.set_value(self.texture_id, texture_data.ravel())
        dpg.render_dearpygui_frame()

    def update_sliced_images(self):
        _, _, _, data_x1 = dpg.load_image('Image1.png')

        _, _, _, data_y1 = dpg.load_image('Image2.png')

        _, _, _, data_x2 = dpg.load_image('Image3.png')

        _, _, _, data_y2 = dpg.load_image('Image4.png')

        dpg.set_value(self.x1texture, data_x1)
        dpg.set_value(self.y1texture, data_y1)
        dpg.set_value(self.x2texture, data_x2)
        dpg.set_value(self.y2texture, data_y2)

    
    def save_function(self):
        dest = 'src/' + 'error_file_' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")).replace(':','_')
        shutil.copy('src/error_file.txt',dest)

    def run(self):
        while dpg.is_dearpygui_running():
            if (not self.outputStr_sim == ""):
                f = open('src/error_file.txt', "a")
                f.write(self.outputStr_sim + '\n')
                f.close()
                dpg.add_text(self.outputStr_sim,parent=self.log_group)
                self.outputStr_sim = ""
            if (not self.outputStr_str == ""):
                f = open('src/error_file.txt', "a")
                f.write(self.outputStr_str + '\n')
                f.close()
                dpg.add_text(self.outputStr_str,parent=self.log_group)
                self.outputStr_str = ""
            self.update_frame()
            if self.similarityEnabled:
                self.compare_frame_similarity()
            if self.stringingEnabled:
                pass

    def cleanup(self):
        self.pipeline.stop()
        dpg.destroy_context()

    def get_cropped_frame(self):
        frames = self.pipeline.wait_for_frames()
        frame = np.asanyarray(frames.get_color_frame().get_data())
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame = self.processor.get_filtered_frame(frame)

        cropped_frame = self.processor.get_cropped_frame(frame)
        return cropped_frame

    def get_sliced_frame(self, frame):
        cropped_frame = self.processor.get_cropped_frame(frame)

        return cropped_frame

    def get_darkened_frame(self, frame):
        darkened_frame = self.processor.get_darkened_frame(frame, 0.625)

        return darkened_frame

    def generate_slices(self):
        self.modeler.run()
        self.update_sliced_images()

    def compare_frame_similarity(self):
        frame1 = self.get_cropped_frame()
        frame2 = self.get_sliced_frame(cv.imread(self.view_map[self.view]))
        frame2 = self.get_darkened_frame(frame2) 

        frame1new, frame2new = self.processor.resize_frames(frame1, frame2)
        # cv.imwrite("frame1.png", frame1new)
        # cv.imwrite("frame2.png", frame2new)

        sim = self.comparator.compare_progressive_frames(frame1new, frame2new, 100)

        if sim < self.similarityThreshold:
            self.outputStr_sim = "Error: [2D Similarity]\n\tReason: Similarity too low, similarity = " + str(sim)

if __name__ == "__main__":
    app = App()
    app.run()
    app.cleanup()
