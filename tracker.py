import cv2
import sys
from pathlib import Path

# Add the current directory to Python path if needed
sys.path.insert(0, str(Path(__file__).parent))

from PPE_SAFETY_APP.detection import Detector

cap = cv2.VideoCapture("demo2_marketwise.mp4")
detector = Detector()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    detections = detector.detect(frame)

    for det in detections:
        person_id = det["person_id"]
        x1, y1, x2, y2 = det["bbox"]

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            frame,
            f"ID:{person_id}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    cv2.imshow("Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
