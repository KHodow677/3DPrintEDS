import cv2 as cv
import numpy as np

class ImageProcessor:
    def __init__(self, rgb_color, threshold):
        self.rgb_color = rgb_color
        self.threshold = threshold

    def isolate_color(self, frame, rgb_color, threshold):
        bgr_color = np.array(rgb_color[::-1], dtype=np.uint8).reshape(1, 1, 3)
        hsv_color = cv.cvtColor(bgr_color, cv.COLOR_BGR2HSV)
        hue = hsv_color[0, 0, 0]
        lower_hue = np.array([hue - threshold, 175, 70])
        upper_hue = np.array([hue + threshold, 255, 255])
        hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv_frame, lower_hue, upper_hue)
        result = cv.bitwise_and(frame, frame, mask=mask)
        result = cv.cvtColor(result, cv.COLOR_BGR2GRAY)
        result = cv.cvtColor(result, cv.COLOR_GRAY2BGR)
        return result

    def get_filtered_frame(self, frame):
        isolated_color = self.isolate_color(frame, self.rgb_color, self.threshold)
        return isolated_color

    def get_cropped_frame(self, frame):
        x, y, w, h = self.get_crop_dimensions(frame)
        if x > x + w or y > y + h:
            print("No black pixels found")
            return None
        cropped_image = frame[y:y+h, x:x+w]
        return cropped_image

    def get_crop_dimensions(self, frame):
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        _, thresh = cv.threshold(gray, 1, 255, cv.THRESH_BINARY)

        width = thresh.shape[1]
        for x in range(width):
            if np.any(thresh[:, x] != 0):
                start_width = x
                break
        else:
            return 0, 0, frame.shape[1], frame.shape[0]  

        for x in range(width - 1, -1, -1):
            if np.any(thresh[:, x] != 0):
                end_width = x
                break

        height = thresh.shape[0]
        for y in range(height):
            if np.any(thresh[y, start_width:end_width + 1] != 0):
                start_height = y
                break

        for y in range(height - 1, -1, -1):
            if np.any(thresh[y, start_width:end_width + 1] != 0):
                end_height = y
                break

        return start_width, start_height, end_width - start_width, end_height - start_height
