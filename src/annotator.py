import supervision as sv  
from ultralytics import YOLO
import datetime as datetime

class Annotator:
    def __init__(self):
        self.model = YOLO("src/bestn_100.pt") 

    def annotate(self, frame, conf_val):
        box_annotator = sv.BoxAnnotator(
                thickness=2,
                text_thickness=2,
                text_scale=1
            )   #Appearance of Labels
        
        result = self.model(frame, conf=conf_val)[0] # Set confidence threshold
        detections = sv.Detections.from_ultralytics(result)     #Runs Detection
        labels = [
            f"{self.model.model.names[class_id]} {confidence:0.2f}"
            for _, _, confidence, class_id, _, _
            in detections
        ]   #Labels for confidence and failures

        conf_vals = []
        for confidence in detections:
            conf_vals.append(confidence[2])
            
        ann_image = box_annotator.annotate(
            scene=frame,
            detections=detections,
            labels=labels
        )   #Annotates the Frame

        return ann_image, conf_vals