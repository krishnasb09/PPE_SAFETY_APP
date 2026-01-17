from ultralytics import YOLO
import sys

try:
    model = YOLO("runs/detect/train2/weights/best.pt")
    print("Model Classes:", model.names)
except Exception as e:
    print("Error loading model:", e)
    
    try:
        model = YOLO("yolov8n.pt")
        print("Standard Model Classes:", model.names)
    except:
        pass
