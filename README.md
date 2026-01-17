<<<<<<< HEAD
# 🦺 PPE Safety Monitoring System

An intelligent video surveillance system for detecting Personal Protective Equipment (PPE) compliance in industrial environments using computer vision and machine learning.

## 🚀 Features

- **Real-time PPE Detection**: Upload videos or connect RTSP cameras for live monitoring
- **Green/Red Compliance Boxes**: Visual indicators showing compliant (green) and non-compliant (red) workers
- **Violation Logging**: Automatic logging of safety violations to database
- **Admin Dashboard**: Web-based dashboard for viewing violation reports and analytics
- **Multi-camera Support**: Support for both recorded videos and live RTSP streams

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd PPE_SAFETY_APP
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize database**:
   ```bash
   python database.py
   ```

4. **Create admin user** (optional):
   ```python
   from auth import register_admin
   register_admin('admin', 'admin123')
   ```

## 🎯 Usage

### Video Detection App
```bash
streamlit run app.py
```
- Upload video files or enter RTSP URLs
- Adjust confidence thresholds in the sidebar
- View real-time detection with colored bounding boxes

### Admin Dashboard
```bash
streamlit run pages/3_Dashboard.py
```
- Login with admin credentials
- View violation statistics and reports
- Monitor compliance trends

## 📊 Detection Logic

- **Green Box (SAFE ✓)**: Workers with detected objects nearby (considered PPE compliant)
- **Red Box (VIOLATION)**: Workers without nearby objects (safety violation logged)
- **Demo Mode**: Uses general object detection as PPE compliance proxy

## 🏗️ Architecture

- **Frontend**: Streamlit web applications
- **Backend**: Python with computer vision
- **Model**: YOLOv5/YOLOv8 for object detection
- **Database**: SQLite for violation logging
- **Tracking**: ByteTrack for person tracking across frames

## 📁 Project Structure

```
PPE_SAFETY_APP/
├── app.py                 # Main video detection application
├── pages/                 # Admin dashboard pages
│   ├── 1_Register.py
│   ├── 2_Login.py
│   └── 3_Dashboard.py
├── database.py           # Database initialization
├── auth.py              # Authentication system
├── violation_manager.py # Violation tracking logic
├── ppe_detector.py     # PPE detection (legacy)
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🔧 Configuration

- **Person Confidence**: Minimum confidence for person detection (default: 0.35)
- **PPE Confidence**: Minimum confidence for object detection (default: 0.30)
- **Violation Cooldown**: Time between logging same violation (default: 3 seconds)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This system uses general object detection as a proxy for PPE compliance. For production use, train custom models with actual PPE classes (helmets, vests, boots, etc.) for accurate safety monitoring.
=======
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
>>>>>>> a018294e45018a29dd66ece6ae29f0602911cdeb
