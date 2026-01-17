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