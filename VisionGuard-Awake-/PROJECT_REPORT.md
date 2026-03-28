# VisionGuard Awake  
## Bring Your Own Project (BYOP) - Computer Vision Course Report

**Student Name:** _Your Name_  
**Registration Number:** _Your Reg. No._  
**Course:** Computer Vision  
**University:** VIT Bhopal University  
**Project Title:** VisionGuard Awake - Real-Time Driver Drowsiness and Yawn Monitoring System

---

## 1. Abstract

Road safety is a serious real-world problem, and one major cause of accidents is driver fatigue. A tired driver may keep their eyes closed longer than normal, yawn repeatedly, or lose alertness for short periods. These signs are often visible before a dangerous event occurs. The goal of this project is to build a lightweight computer vision system that can monitor a driver's face through a webcam and detect early visual symptoms of drowsiness.

The developed system uses OpenCV and MediaPipe FaceMesh to track facial landmarks in real time. It computes geometric indicators from the detected landmarks: the Eye Aspect Ratio (EAR) for eye closure and the Mouth Aspect Ratio (MAR) for yawning. When the eyes remain closed for several consecutive frames or when repeated yawns are detected within a time window, the system produces an alert. It also logs events into a CSV file and stores snapshots for later review.

This project applies core computer vision ideas such as image acquisition, landmark-based facial analysis, geometric feature extraction, threshold-based decision making, and real-time monitoring. It is purposeful, practical, and clearly distinct from document enhancement or scanning projects.

---

## 2. Problem Statement

Drowsy driving is a frequent but preventable cause of traffic accidents. Human fatigue reduces reaction time, lowers concentration, and may cause microsleep episodes. In many cases, fatigue symptoms begin to appear on the face before the driver completely loses awareness. A vision-based system that can detect these facial cues in real time can act as an early warning mechanism.

The problem selected for this BYOP is:

**"Can a webcam-based computer vision system detect signs of driver drowsiness such as prolonged eye closure and repeated yawning in real time and alert the user?"**

This is a meaningful real-world problem because:
- it has direct safety relevance
- it can be approached using computer vision techniques taught in class
- it does not require expensive hardware
- it can be demonstrated clearly in a live environment

---

## 3. Motivation

I wanted to choose a project that is useful beyond the classroom and demonstrates a practical use of computer vision. Since many students and professionals travel long distances, driver safety is a relatable and important problem. At the same time, I wanted a project different from document-scanning systems, so I selected a facial behavior monitoring task instead.

This project attracted me for three reasons:
1. It addresses a real safety issue.
2. It can be implemented with standard tools such as Python, OpenCV, and a webcam.
3. It shows how simple geometric analysis can solve a useful problem without requiring a large training dataset.

---

## 4. Objectives

The main objectives of the project were:

- To build a real-time face-based drowsiness monitoring system
- To detect prolonged eye closure using facial landmarks
- To detect yawning using mouth landmarks
- To generate on-screen and sound alerts
- To log events and store snapshots for basic analysis
- To design the system in a clean, modular, and reusable way

---

## 5. Scope of the Project

This project is a **prototype** designed for educational and demonstration purposes. It focuses on a single visible face captured through a webcam. It does not attempt to replace industrial automotive monitoring systems. Instead, it demonstrates how computer vision can be used to solve a real-world problem using accessible techniques.

The scope includes:
- webcam-based real-time frame processing
- face landmark detection
- drowsiness logic based on eye closure
- yawn analysis based on mouth opening
- alerting and event logging

The scope does not include:
- hardware integration with a vehicle
- multi-person scene understanding
- certified safety deployment
- advanced deep learning training on large datasets

---

## 6. System Design

The system follows the pipeline below:

1. **Video Capture**  
   Frames are obtained continuously from the webcam.

2. **Face Landmark Detection**  
   MediaPipe FaceMesh identifies detailed facial landmarks.

3. **Feature Extraction**  
   Selected landmarks from the eyes and mouth are used to compute:
   - Eye Aspect Ratio (EAR)
   - Mouth Aspect Ratio (MAR)

4. **Temporal Decision Logic**  
   The system checks:
   - whether EAR remains below a threshold for multiple consecutive frames
   - whether yawns occur repeatedly within a recent time window

5. **Alert and Logging Layer**  
   When risk conditions are met, the system:
   - displays a warning
   - triggers a sound alert
   - stores the event in a CSV file
   - saves a snapshot image

---

## 7. Methodology

### 7.1 Face Landmark Detection

Instead of training a custom model from scratch, I used MediaPipe FaceMesh because it provides stable and fast facial landmark estimation in real time. This allowed the project to focus on vision logic and system behavior.

### 7.2 Eye Aspect Ratio (EAR)

EAR is a geometric feature used to estimate whether the eye is open or closed. It is computed using distances between selected eye landmarks. When the eyes close, the vertical distance decreases while the horizontal distance remains relatively stable. Therefore, the ratio becomes smaller.

A low EAR for just one or two frames may happen naturally during blinking. To avoid false alarms, the system checks whether EAR stays below a threshold for a sequence of consecutive frames.

### 7.3 Mouth Aspect Ratio (MAR)

MAR estimates mouth openness by comparing vertical mouth opening with horizontal mouth width. A high MAR suggests the mouth is open widely. If the mouth stays open for several frames, the event is counted as a yawn candidate. If multiple yawns occur within a short interval, the system raises a fatigue warning.

### 7.4 Threshold-Based Logic

The project uses rule-based logic:

- If `EAR < threshold` for many consecutive frames -> drowsiness warning
- If several yawns occur in a rolling time window -> fatigue warning

I selected this approach because it is lightweight, explainable, and easy to tune.

---

## 8. Tools and Technologies Used

| Tool / Library | Purpose |
|---|---|
| Python | Main programming language |
| OpenCV | Video capture, frame processing, display |
| MediaPipe | Face landmark detection |
| NumPy | Numeric support |
| CSV logging | Record detected events |

---

## 9. File Structure

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

The code is modular so that each component has a clear responsibility:

- `app.py` handles webcam input and main execution
- `detector.py` contains face analysis and alert logic
- `utils.py` stores mathematical helpers and logging utilities
- `config.py` centralizes thresholds and runtime settings

---

## 10. Key Design Decisions

Several design decisions shaped the project:

### 10.1 Choosing Landmark Geometry Over Deep Model Training
I deliberately chose EAR and MAR based detection because:
- it is interpretable
- it runs in real time on standard laptops
- it avoids the need for a large labeled dataset
- it is suitable for a course-level prototype

### 10.2 Using Temporal Conditions
A single frame is not enough to conclude drowsiness. Natural blinking or speaking can look similar to fatigue for a moment. Therefore, I used temporal thresholds such as consecutive low-EAR frames and repeated yawns in a time window.

### 10.3 Adding Logging and Snapshots
I included CSV logs and saved frames because a real system should not only detect events, but also produce evidence or records for review. This also improves usability and makes the project more complete.

---

## 11. Challenges Faced

During the design and development of this project, the main challenges were:

### 11.1 Threshold Sensitivity
Different people have different facial structures and blinking behavior. A threshold that works for one user may not work perfectly for another. To solve this, I placed all key settings inside `config.py` so the system can be calibrated easily.

### 11.2 False Positives
Normal blinking, head movement, low light, or talking can create temporary patterns similar to drowsiness or yawning. This was reduced using consecutive-frame logic and rolling-window checks.

### 11.3 Real-Time Performance
A computer vision system must process frames quickly enough to remain useful. Choosing MediaPipe and geometric calculations helped keep the pipeline lightweight.

### 11.4 Environmental Limitations
Glasses, occlusion, weak lighting, and extreme face angles can affect landmark quality. This is a practical limitation of webcam-based monitoring and is acknowledged in the final system.

---

## 12. Results and Observations

The final prototype successfully demonstrates the full pipeline of webcam capture, face landmark detection, feature computation, warning logic, and event recording. The system is capable of:

- identifying when the user's eyes remain closed for too long
- detecting large mouth openings interpreted as yawns
- generating real-time warnings on the video frame
- recording events for later review

Since this project is a course prototype, evaluation was primarily **qualitative and functional** rather than benchmark-driven. The main success criterion was whether the system could respond meaningfully to visible signs of simulated fatigue during a live webcam session.

---

## 13. Limitations

Although the system works as a prototype, it still has limitations:

- It assumes that a single face is clearly visible.
- It may be affected by low light or camera quality.
- It uses manually chosen thresholds rather than learned personalization.
- It does not combine other fatigue cues such as head nodding or gaze deviation.
- It is not suitable for direct real-world deployment without further testing.

---

## 14. Future Improvements

This project can be extended in many useful directions:

- add head pose estimation for nodding detection
- combine eye, mouth, and gaze features into a unified fatigue score
- detect phone distraction or looking away from the road
- integrate with a mobile app or embedded device
- use deep learning for more robust fatigue classification
- build a dashboard for reviewing driver alert history

---

## 15. Learning Outcomes

This project helped me understand the practical side of computer vision beyond theory. Through this work, I learned:

- how to process a live video stream in real time
- how landmark-based facial analysis works
- how simple geometric features can be transformed into useful signals
- how thresholding and temporal logic influence detection quality
- how to organize a project into reusable modules
- how to think about limitations, usability, and real-world deployment

It also taught me that a strong project does not always require a large neural network. In some cases, a carefully designed classical pipeline can still solve a meaningful problem effectively.

---

## 16. Conclusion

VisionGuard Awake is a practical and well-scoped BYOP project that applies computer vision to a real problem: detecting signs of driver fatigue. By using webcam input, facial landmarks, EAR, MAR, and temporal alert logic, the system provides a simple but effective fatigue monitoring prototype. The project is relevant to course concepts, easy to demonstrate, and clearly different from image-to-document enhancement applications.

Overall, this project shows how computer vision can be used not only to analyze images, but also to create systems that support safety and awareness in everyday life.
