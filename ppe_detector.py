from ultralytics import YOLO

class PPEDetector:
    def __init__(self):
        self.model = YOLO(
                    "runs/detect/runs/train/ppe_retrain/weights/best.pt")

        self.required_ppe = {
            "helmet",
            "vest",
            "shoes",
            "goggles",
            "mask"
        }

    def detect(self, person_crop):
        results = self.model(person_crop, conf=0.2, verbose=False)


        detected_items = set()

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                label = self.model.names[cls_id].lower()
                detected_items.add(label)

        missing_items = sorted(list(self.required_ppe - detected_items))

        return detected_items, missing_items
