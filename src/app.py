import dearpygui.dearpygui as dpg
import cv2 as cv
import numpy as np
import pyrealsense2 as rs
import sys, os

sys.path.append(os.getcwd())

from src.imageProcessor import ImageProcessor
from src.modeler import Modeler

class App:
    def __init__(self):
        self.processor = ImageProcessor([255, 128, 0], 10)
        self.modeler = Modeler("example.STL")
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)
        self.pipeline.start(self.config)
        self.frame_width = 640
        self.frame_height = 480
        self.video_fps = 30
        self.create_gui()


    def create_gui(self):
        dpg.create_context()
        dpg.create_viewport(title='Video Feed', width=1920, height=1080)
        dpg.setup_dearpygui()

        self.texture_data = np.zeros((self.frame_height, self.frame_width, 3), dtype=np.float32)

        with dpg.texture_registry(show=False):
            self.texture_id = dpg.add_raw_texture(self.frame_width, self.frame_height, self.texture_data.ravel(), tag="texture_tag", format=dpg.mvFormat_Float_rgb)

        with dpg.window(label="Video Window"):
            self.image_item = dpg.add_image("texture_tag")

        with dpg.window(label="Controls"):
            dpg.add_button(label="Save Cropped Frame", callback=self.save_cropped_frame)
            dpg.add_button(label="Save Sliced Frame", callback=self.save_sliced_frame)
            dpg.add_button(label="Save Darkened Frame", callback=self.save_darkened_frame)

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

    def run(self):
        while dpg.is_dearpygui_running():
            self.update_frame()

    def cleanup(self):
        self.pipeline.stop()
        dpg.destroy_context()

    def save_cropped_frame(self):
        frames = self.pipeline.wait_for_frames()
        frame = np.asanyarray(frames.get_color_frame().get_data())
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame = self.processor.get_filtered_frame(frame)

        cropped_frame = self.processor.get_cropped_frame(frame)
        if cropped_frame is not None:
            cv.imwrite("frame.png", cropped_frame)


    def save_sliced_frame(self):
        image_path = "Image1.png"
        frame = cv.imread(image_path)

        cropped_frame = self.processor.get_cropped_frame(frame)

        if cropped_frame is not None:
            cv.imwrite("slicedFrame.png", cropped_frame)

    def save_darkened_frame(self):
        image_path = "Image1.png"
        frame = cv.imread(image_path)

        darkened_frame = self.processor.get_darkened_frame(frame, 0.625)

        if darkened_frame is not None:
            cv.imwrite("darkenedFrame.png", darkened_frame)

if __name__ == "__main__":
    app = App()
    app.run()
    app.cleanup()
