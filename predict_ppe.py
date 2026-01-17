from ultralytics import YOLO

model = YOLO("runs/detect/ppe_train/weights/best.pt")

model.predict(
    source="PPE_DATASET/ppe_dataset/test/images",
    show=True,
    save=True
)
