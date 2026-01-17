from ultralytics import YOLO

try:
    model = YOLO("runs/detect/train2/weights/best.pt")
    print("ALL CLASSES:")
    for id, name in model.names.items():
        print(f"ID {id}: {name}")
except Exception as e:
    print(f"Error: {e}")
