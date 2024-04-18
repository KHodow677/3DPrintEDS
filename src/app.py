import dearpygui.dearpygui as dpg
import cv2 as cv
import numpy as np
import pyrealsense2 as rs

dpg.create_context()
dpg.create_viewport(title='Video Feed', width=1920, height=1080)
dpg.setup_dearpygui()

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)
pipeline.start(config)

frames = pipeline.wait_for_frames()
frame = np.asanyarray(frames.get_color_frame().get_data())
frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

frame_width = 640
frame_height = 480
video_fps = 30

data = np.flip(frame, 2)  
data = data.ravel() 
data = np.asfarray(data, dtype='f')
texture_data = np.true_divide(data, 255.0)

with dpg.texture_registry(show=False):
    dpg.add_raw_texture(frame.shape[1], frame.shape[0], texture_data, tag="texture_tag", format=dpg.mvFormat_Float_rgb)

with dpg.window(label="Video Window"):
    dpg.add_image("texture_tag")

dpg.show_viewport()
while dpg.is_dearpygui_running():
    frames = pipeline.wait_for_frames()
    frame = np.asanyarray(frames.get_color_frame().get_data())
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    data = np.flip(frame, 2)
    data = data.ravel()
    data = np.asfarray(data, dtype='f')
    texture_data = np.true_divide(data, 255.0)
    dpg.set_value("texture_tag", texture_data)

    dpg.render_dearpygui_frame()

pipeline.stop()
dpg.destroy_context()
