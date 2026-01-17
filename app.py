import streamlit as st
import cv2
from ultralytics import YOLO
import tempfile
import time
from datetime import datetime
import os


from violation_logic import log_violation
from video_utils import format_video_time
from violation_manager import ViolationManager


st.set_page_config(page_title="PPE Safety System", layout="wide", page_icon="🦺")
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    h1 { color: #00d4ff; }
    .stButton > button { background: #ff4b4b; color: white; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🦺 Industrial Safety Monitoring System")


DEFAULT_PERSON_CONF = 0.35
DEFAULT_PPE_CONF = 0.30
CONSECUTIVE_FRAMES_THRESHOLD = 3  
violation_manager = ViolationManager(cooldown_seconds=3, log_once_per_session=True)


def get_model():
    # Try multiple possible model paths in order of preference
    possible_paths = [
        "yolov5su.pt",           # Recommended YOLOv5 small updated model
        "yolov8n_ppe.pt",        # Pre-trained PPE model (if downloaded)
        "yolov5s.pt",            # Downloaded YOLOv5 small
        "runs/detect/train2/weights/best.pt",
        "runs/detect/train11/weights/best.pt",
        "runs/detect/train10/weights/best.pt",
        "runs/detect/train9/weights/best.pt",
        "yolov8n.pt"  # fallback
    ]

    for path in possible_paths:
        if os.path.exists(path):
            print(f"Loading model: {path}")
            try:
                return YOLO(path)
            except Exception as e:
                print(f"Failed to load {path}: {e}")
                continue

    print("No model found, using default YOLOv8n")
    return YOLO("yolov8n.pt")

model = get_model()


# Class mappings for PPE detection using default YOLOv8 classes as proxies
PERSON = 0
BACKPACK = 24    # Proxy for safety vest
UMBRELLA = 25    # Proxy for helmet
HANDBAG = 26     # Proxy for other PPE
HAT = 27         # Could be helmet
SUITCASE = 28    # Could be PPE bag

# Use proxy classes that exist in default YOLOv8
HELMET_PROXY = UMBRELLA  # Umbrella shape similar to helmet
VEST_PROXY = BACKPACK    # Backpack similar to safety vest
BOOTS_PROXY = HANDBAG    # Handbag as proxy for boots/PPE


with st.sidebar:
    st.header("⚙️ Configuration")
    
    st.subheader("Detection Thresholds")
    PERSON_CONF = st.slider(
        "Person Confidence",
        min_value=0.1,
        max_value=0.9,
        value=DEFAULT_PERSON_CONF,
        step=0.05,
        help="Minimum confidence to detect a person"
    )
    
    PPE_CONF = st.slider(
        "PPE Confidence",
        min_value=0.1,
        max_value=0.9,
        value=DEFAULT_PPE_CONF,
        step=0.05,
        help="Minimum confidence to detect PPE items (helmet, shoes)"
    )
    
    st.info(f"💡 Higher values = fewer false positives\n📊 Lower values = detect more items\n\n🎯 DEMO MODE:\n   • Any detected object = PPE compliance\n   • Green boxes = Safe workers\n   • Red boxes = Need PPE")


col1, col2 = st.columns([1, 2])
with col1:
    source = st.radio("Source", ["Recorded Video", "Live CCTV"])
    video_file = st.file_uploader("Video", type=["mp4", "avi", "mov", "mkv"]) if source == "Recorded Video" else None
    rtsp_url = st.text_input("RTSP URL") if source == "Live CCTV" else None
    start = st.button("🚀 Start Detection")

with col2:
    st.subheader("Live Feed")
    frame_window = st.empty()


if start:
    if source == "Recorded Video" and not video_file:
        st.warning("Please upload a video")
        st.stop()

    cap = None
    is_live = False
    source_name = "Unknown"

    if source == "Recorded Video":
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(video_file.read())
        cap = cv2.VideoCapture(tfile.name)
        source_name = video_file.name
    else:
        cap = cv2.VideoCapture(rtsp_url)
        source_name = "Live CCTV"
        is_live = True

    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    frame_count = 0
    
    
    violation_manager.reset_session()
    
    
    st.info("🔄 Detection in progress... Processing video frame by frame.")

    
    person_frames = {}
    
    
    violation_frames = {}

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.success("✅ Detection completed. Check dashboard for updated logs.")
            break

        frame_count += 1

         
        if frame_count % 3 != 0:
            continue

        video_time = (
            datetime.now().strftime("%H:%M:%S")
            if is_live else format_video_time(frame_count / fps)
        )

        results = model.track(
            frame,
            persist=True,
            conf=PPE_CONF,
            imgsz=640,
            tracker="bytetrack.yaml",
            classes=[PERSON, BACKPACK, UMBRELLA, HANDBAG, HAT, SUITCASE],  # Use available classes
            verbose=False
        )[0]

        # Debug: Show what classes the model actually has
        if not hasattr(model, '_class_names_shown'):
            if hasattr(model, 'names'):
                st.info(f"🔍 Model classes: {list(model.names.values())}")
            model._class_names_shown = True

        annotated = frame.copy()

        
        if results.boxes is None or results.boxes.id is None:
            cv2.putText(
                annotated,
                f"Time: {video_time} | Frame: {frame_count} | No detections",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 0),
                2
            )
            frame_window.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB))
            continue

        boxes = results.boxes.xyxy.cpu().tolist()
        classes = results.boxes.cls.cpu().tolist()
        ids = results.boxes.id.cpu().tolist()
        confs = results.boxes.conf.cpu().tolist()

        persons = {}
        ppe_items = []

        
        for pid, cls, box, conf in zip(ids, classes, boxes, confs):
            pid = int(pid)
            cls = int(cls)
            x1, y1, x2, y2 = map(int, box)

            if cls == PERSON and conf >= PERSON_CONF:
                h = y2 - y1
                persons[pid] = {
                    "bbox": (x1, y1, x2, y2),
                    "head": (x1, y1, x2, y1 + int(0.35 * h)),
                    "foot": (x1, y1 + int(0.75 * h), x2, y2),
                    "helmet": False,  # Will be detected as umbrella
                    "vest": False,    # Will be detected as backpack
                    "boots": False    # Will be detected as handbag
                }
                person_frames[pid] = person_frames.get(pid, 0) + 1

            elif conf >= PPE_CONF:
                ppe_items.append((cls, (x1, y1, x2, y2)))

        
        def center_inside(r1, r2):
            cx = (r1[0] + r1[2]) // 2
            cy = (r1[1] + r1[3]) // 2
            return r2[0] <= cx <= r2[2] and r2[1] <= cy <= r2[3]

        for cls, rect in ppe_items:
            for pid, p in persons.items():
                # Use proxy classes for PPE detection
                if cls == HELMET_PROXY and center_inside(rect, p["head"]):  # Umbrella as helmet
                    p["helmet"] = True
                elif cls == VEST_PROXY and center_inside(rect, p["bbox"]):  # Backpack as vest
                    p["vest"] = True
                elif cls == BOOTS_PROXY and center_inside(rect, p["foot"]):  # Handbag as boots
                    p["boots"] = True
                # For demo: If any object is detected near a person, consider them compliant
                elif center_inside(rect, p["bbox"]):
                    p["helmet"] = True  # Mark as having PPE for demonstration
            
            if person_frames.get(pid, 0) < 15:
                continue

            
            missing = []
            if not p["helmet"]:
                missing.append("Helmet")
            if not p["vest"]:
                missing.append("Vest")
            # Make boots optional for demonstration
            # if not p["boots"]:
            #     missing.append("PPE Bag")

            x1, y1, x2, y2 = p["bbox"]

            
            if missing:
                
                missing_key = tuple(sorted(missing))
                
                if pid not in violation_frames:
                    violation_frames[pid] = {}
                
                if missing_key not in violation_frames[pid]:
                    violation_frames[pid][missing_key] = 1
                else:
                    violation_frames[pid][missing_key] += 1
                
                
                if violation_frames[pid][missing_key] >= CONSECUTIVE_FRAMES_THRESHOLD:
                    
                    if violation_manager.should_log(pid, missing):
                        log_violation(pid, missing, video_time, source_name)
                        st.toast(f"⚠️ Violation logged: Person {pid} - Missing {', '.join(missing)}", icon="⚠️")
                
                color = (0, 0, 255)  # Red for violations
                label = f"ID:{pid} MISSING: {','.join(missing)}"
            else:
                
                if pid in violation_frames:
                    violation_frames[pid] = {}
                
                color = (0, 255, 0)  # Green for compliant
                label = f"ID:{pid} SAFE ✓"

            
            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
            cv2.putText(
                annotated,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2
            )

        cv2.putText(
            annotated,
            f"Time: {video_time} | Frame: {frame_count}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2
        )

        frame_window.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB))

    cap.release()
