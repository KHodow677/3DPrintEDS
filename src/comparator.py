import cv2
from skimage.metrics import structural_similarity as ssim

class Comparator:
    def __init__(self):
        pass
    
    def compare_frames(self, frame1, frame2):
        gray_frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray_frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        
        similarity_index, _ = ssim(gray_frame1, gray_frame2, full=True)
        return similarity_index

