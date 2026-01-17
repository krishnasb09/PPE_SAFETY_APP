# PPE_SAFETY_APP
aPPE Safety App is a computer vision–based application that detects the presence and absence of Personal Protective Equipment (PPE) such as helmets, gloves, safety shoes, and welding glasses using deep learning (YOLOv8). The system helps improve workplace safety by automatically monitoring compliance in real time.

🦺 PPE Safety App – AI-Based Workplace Safety Monitoring
📌 Overview

The PPE Safety App is a deep learning–based computer vision system designed to detect the presence and absence of Personal Protective Equipment (PPE) in industrial and construction environments.
Using YOLOv8, the system automatically identifies whether workers are wearing essential safety gear such as helmets, gloves, safety shoes, and welding glasses.

This application helps organizations improve workplace safety, reduce accidents, and monitor compliance in real time.

🎯 Objectives

Detect PPE compliance automatically using computer vision

Identify missing safety equipment in real-time

Reduce manual supervision and human error

Provide a scalable AI-based safety monitoring solution

🧠 Features

✅ Real-time PPE detection using YOLOv8

✅ Supports multiple PPE categories

✅ Custom-trained model on PPE datasets

✅ Image, video, and webcam inference

✅ Easy to extend with alerts or dashboards

🛠 Tech Stack

Programming Language: Python 3.9+

Deep Learning Framework: PyTorch

Object Detection Model: YOLOv8 (Ultralytics)

Computer Vision: OpenCV

Dataset Format: YOLO format

Environment: Virtual Environment (venv)




🧾 PPE Classes

Example classes used in the project:

- no-safety-glove
- no-safety-helmet
- no-safety-shoes
- no-welding-glass
- safety-glove
- safety-helmet
- safety-shoes
- welding-glass

📊 Dataset

Dataset follows YOLO format

Images and labels are organized into train / valid / test

data.yaml defines class names and paths

Example data.yaml:

train: train/images
val: valid/images
test: test/images

nc: 8
names:
  - no-safety-glove
  - no-safety-helmet
  - no-safety-shoes
  - no-welding-glass
  - safety-glove
  - safety-helmet
  - safety-shoes
  - welding-glass

⚙️ Installation & Setup

2️⃣ Create Virtual Environment
python -m venv venv


Activate it:

Windows

venv\Scripts\activate


Linux / Mac

source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt


If requirements.txt is not present:

pip install ultralytics opencv-python torch torchvision

🏋️ Model Training

To train the YOLOv8 model on the PPE dataset:

yolo train model=yolov8m.pt data=dataset/data.yaml epochs=100 imgsz=640 batch=16


Training results will be saved in:

runs/detect/train/

🔍 Model Evaluation

After training, evaluate using the validation or test set:

yolo val model=runs/detect/train/weights/best.pt data=dataset/data.yaml

🎥 Inference / Detection
Detect on Image
yolo detect model=models/best.pt source=path/to/image.jpg

Detect on Video
yolo detect model=models/best.pt source=path/to/video.mp4

Detect using Webcam
yolo detect model=models/best.pt source=0


Detected outputs are saved in:

runs/detect/

🧪 Example Use Cases

Industrial safety monitoring
Construction site compliance
Factory floor supervision
PPE violation detection
Smart surveillance systems

⚠️ Limitations

Performance depends on dataset quality
Occluded or low-light PPE may reduce accuracy
Model needs retraining for new PPE types

🚀 Future Enhancements
🔔 Real-time alerts for PPE violations
📱 Mobile app deployment
☁️ Cloud-based inference
