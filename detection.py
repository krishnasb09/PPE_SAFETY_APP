from ultralytics import YOLO
import cv2

class Detector:
    def __init__(self):
        
        self.model = YOLO("yolov8n.pt")

    def detect(self, frame):
        """
        Detect & track persons in a frame using ByteTrack
        Returns list of persons with stable IDs
        """
        results = self.model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml",
            conf=0.35,
            iou=0.5,
            classes=[0]  
        )

        detections = []

        if not results or results[0].boxes is None:
            return detections

        boxes = results[0].boxes

        if boxes.id is None:
            return detections

        for box in boxes:
            person_id = int(box.id.item())
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])

            detections.append({
                "person_id": person_id,
                "bbox": (x1, y1, x2, y2),
                "confidence": conf
            })

        return detections
