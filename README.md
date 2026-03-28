# VisionGuard Awake

VisionGuard Awake is a real-time **driver drowsiness and yawn monitoring system** built using **Python, OpenCV, and MediaPipe**.  
It uses a webcam feed to track the driver's face, estimate **eye closure** and **mouth opening**, and trigger alerts when signs of fatigue appear.

---

## Why this project?

Drowsy driving is a real-world safety problem. Many accidents happen because drivers microsleep, lose focus, or continue driving while tired.

This project solves that problem using computer vision by:
- detecting **prolonged eye closure**
- detecting **frequent yawning**
- generating **visual + sound alerts**
- storing **event logs and snapshots**

This makes the project practical, relevant to computer vision, and clearly different from document-scanning systems like SmartDoc-Vision.

---

## Features

- Real-time webcam-based monitoring
- Face landmark detection using MediaPipe FaceMesh
- Eye Aspect Ratio (EAR) based drowsiness detection
- Mouth Aspect Ratio (MAR) based yawn detection
- Alert cooldown to avoid repeated alarm spam
- Snapshot saving during warning events
- CSV logging of important detections
- Easy threshold tuning from `config.py`

---

## Project structure

```text
VisionGuard-Awake/
├── app.py
├── detector.py
├── utils.py
├── config.py
├── requirements.txt
├── README.md
├── PROJECT_REPORT.md
├── logs/
├── snapshots/
└── assets/
```

---

## Tech stack

- **Python**
- **OpenCV**
- **MediaPipe FaceMesh**
- **NumPy**

---

## How it works

1. The webcam captures video frames.
2. Each frame is processed using MediaPipe FaceMesh.
3. Facial landmark points are extracted for:
   - both eyes
   - mouth
4. Two geometric features are computed:
   - **EAR (Eye Aspect Ratio)** → measures eye openness
   - **MAR (Mouth Aspect Ratio)** → measures mouth openness
5. If the eyes remain closed for too many consecutive frames, the system raises a drowsiness alert.
6. If large mouth opening is repeatedly detected within a short time window, the system raises a yawn warning.
7. Events are logged and snapshots are saved.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/VisionGuard-Awake.git
cd VisionGuard-Awake
```

### 2. Create a virtual environment

**Linux / macOS**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows**
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run the project

```bash
python app.py
```

Press **Q** to quit.

---

## Configuration

All thresholds are inside `config.py`.

Important parameters:

- `EAR_THRESHOLD` → lower value means eye is more closed
- `EAR_CONSEC_FRAMES` → how many continuous low-EAR frames count as drowsiness
- `MAR_THRESHOLD` → larger value means wider mouth opening
- `MAR_CONSEC_FRAMES` → how long mouth must stay open to count as a yawn
- `YAWN_ALERT_COUNT` → number of yawns in a rolling time window before warning
- `ALERT_COOLDOWN_SECONDS` → prevents repeated alarm triggering too quickly

You can tune these values depending on:
- webcam quality
- face distance from camera
- lighting conditions
- individual facial structure

---

## Output

The application shows:

- status on screen
- EAR value
- MAR value
- eye-closed frame count
- number of recent yawns

It also creates:

- `logs/drowsiness_events.csv`
- images inside `snapshots/`

---

## Example use cases

- driver fatigue monitoring
- transport safety prototype
- computer vision course project
- human attention monitoring prototype

---

## Limitations

- Works best when one clear face is visible
- Sensitive to poor lighting and very low-quality webcams
- Eyeglasses, head pose, or occlusion can affect detection quality
- This is a prototype and not a certified automotive safety product

---

## Future improvements

- Head pose estimation
- Phone distraction detection
- Seatbelt detection
- Mobile deployment
- Deep learning based fatigue classification
- Dashboard analytics for fleet monitoring

---

## Author

Replace this section with your name, course, university, and GitHub profile.
