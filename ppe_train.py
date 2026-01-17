from ultralytics import YOLO


model = YOLO("yolov8n.pt")

model.train(
    data="C:/Users/krish/MarketWise/PPE_SAFETY_APP/PPE_DATASET/final_merged/dataset/dataset.yaml",
    epochs=30,
    batch=8,
    imgsz=640,
    project="Helmet_Training",
    name="helmet_only",
    device="cpu" 
)

