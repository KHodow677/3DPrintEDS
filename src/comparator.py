import cv2 as cv
import numpy as np
from skimage.metrics import structural_similarity as ssim
import sys, os

sys.path.append(os.getcwd())

from src.imageProcessor import ImageProcessor

class Comparator:
    def __init__(self, processor):
        self.processor = processor
    
    def compare_frames(self, frame1, frame2):
        try:
            gray_frame1 = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
            gray_frame2 = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
            similarity_index, _ = ssim(gray_frame1, gray_frame2, full=True)
        except: 
            return 1.0
        return similarity_index

    def get_frame_at_pixel_height(self, frame, height_from_bottom):
        height = frame.shape[0]
        if height_from_bottom < 0:
            return np.zeros_like(frame)
        elif height_from_bottom >= height:
            return frame
        else:
            modified_frame = frame[-height_from_bottom:, :, :]
            return modified_frame

    def compare_progressive_frames(self, frame1, frame2, samples):
        max_similarity = 0.0
        height = frame2.shape[0]
        for i in range(samples+1):
            current_height = int(i / 100 * height)
            frame2new = self.get_frame_at_pixel_height(frame2, current_height)
            frame1new, frame2new = self.processor.resize_frames(frame1, frame2new)
            similarity = self.compare_frames(frame1new, frame2new)
            max_similarity = max(max_similarity, similarity)
            if similarity == max_similarity:
                try:
                    cv.imwrite("res2.png", frame2new)
                    cv.imwrite("res1.png", frame1new)
                except:
                    pass
        return max_similarity

