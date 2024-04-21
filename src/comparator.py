import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import sys, os

sys.path.append(os.getcwd())

class Comparator:
    def __init__(self):
        pass
    
    def compare_frames(self, frame1, frame2):
        gray_frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray_frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        
        similarity_index, _ = ssim(gray_frame1, gray_frame2, full=True)
        return similarity_index

    def get_frame_at_pixel_height(self, frame, height_from_bottom):
        height = frame.shape[0]
        if height_from_bottom < 0:
            return np.zeros_like(frame)
        elif height_from_bottom >= height:
            return frame
        else:
            height_from_top = height - height_from_bottom
            modified_frame = frame.copy()
            modified_frame[:height_from_top, :] = 0
            return modified_frame

    def compare_progressive_frames(self, frame1, frame2, samples):
        max_similarity = 0.0
        height = frame2.shape[0]
        for i in range(samples+1):
            current_height = int(i / 100 * height)
            similarity = self.compare_frames(frame1, self.get_frame_at_pixel_height(frame2, current_height))
            max_similarity = max(max_similarity, similarity)
        return max_similarity

if __name__ == "__main__":
    frame1 = cv2.imread("slicedFrame.png")
    frame2 = cv2.imread("slicedFrame.png")

    comparator = Comparator()
    max_sim = comparator.compare_progressive_frames(frame1, frame2, 100)

    print(max_sim)
