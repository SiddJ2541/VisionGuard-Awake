import os
import time
from collections import deque
from dataclasses import dataclass

import cv2
import mediapipe as mp

import config
from utils import eye_aspect_ratio, mouth_aspect_ratio, append_event, alert_beep


@dataclass
class DetectionState:
    ear: float = 0.0
    mar: float = 0.0
    face_detected: bool = False
    eye_closed_frames: int = 0
    mouth_open_frames: int = 0
    yawn_count_recent: int = 0
    status: str = "Monitoring"
    alert_triggered: bool = False


class DrowsinessDetector:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

        # MediaPipe FaceMesh landmark indices
        self.left_eye_idx = [33, 160, 158, 133, 153, 144]
        self.right_eye_idx = [362, 385, 387, 263, 373, 380]
        self.mouth_idx = [78, 13, 308, 14]  # left, top, right, bottom

        self.eye_closed_counter = 0
        self.mouth_open_counter = 0
        self.yawn_timestamps = deque()
        self.last_alert_time = 0.0

        self.csv_path = os.path.join(config.LOG_DIR, config.LOG_FILE)
        os.makedirs(config.SNAPSHOT_DIR, exist_ok=True)
        os.makedirs(config.LOG_DIR, exist_ok=True)

    def _landmark_points(self, face_landmarks, image_shape, indices):
        h, w = image_shape[:2]
        points = []
        for idx in indices:
            lm = face_landmarks.landmark[idx]
            points.append((int(lm.x * w), int(lm.y * h)))
        return points

    def _save_snapshot(self, frame, label):
        if not config.SAVE_SNAPSHOTS:
            return
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{label.lower()}_{timestamp}.jpg"
        path = os.path.join(config.SNAPSHOT_DIR, filename)
        cv2.imwrite(path, frame)

    def _should_alert(self):
        return (time.time() - self.last_alert_time) >= config.ALERT_COOLDOWN_SECONDS

    def _trigger_alert(self, event_type, frame, ear, mar):
        if self._should_alert():
            alert_beep()
            append_event(self.csv_path, event_type, ear, mar)
            self._save_snapshot(frame, event_type)
            self.last_alert_time = time.time()

    def process_frame(self, frame):
        state = DetectionState()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb)

        if not results.multi_face_landmarks:
            state.status = "No face detected"
            return frame, state

        face_landmarks = results.multi_face_landmarks[0]
        state.face_detected = True

        left_eye = self._landmark_points(face_landmarks, frame.shape, self.left_eye_idx)
        right_eye = self._landmark_points(face_landmarks, frame.shape, self.right_eye_idx)
        mouth = self._landmark_points(face_landmarks, frame.shape, self.mouth_idx)

        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)
        ear = (left_ear + right_ear) / 2.0
        mar = mouth_aspect_ratio(mouth)

        state.ear = ear
        state.mar = mar

        # Draw eye and mouth points
        for point in left_eye + right_eye + mouth:
            cv2.circle(frame, point, 2, (0, 255, 0), -1)

        # Eye closure logic
        if ear < config.EAR_THRESHOLD:
            self.eye_closed_counter += 1
        else:
            self.eye_closed_counter = 0

        # Yawn logic
        yawn_registered = False
        if mar > config.MAR_THRESHOLD:
            self.mouth_open_counter += 1
        else:
            if self.mouth_open_counter >= config.MAR_CONSEC_FRAMES:
                self.yawn_timestamps.append(time.time())
                yawn_registered = True
            self.mouth_open_counter = 0

        current_time = time.time()
        while self.yawn_timestamps and current_time - self.yawn_timestamps[0] > config.YAWN_WINDOW_SECONDS:
            self.yawn_timestamps.popleft()

        state.eye_closed_frames = self.eye_closed_counter
        state.mouth_open_frames = self.mouth_open_counter
        state.yawn_count_recent = len(self.yawn_timestamps)

        is_drowsy_by_eye = self.eye_closed_counter >= config.EAR_CONSEC_FRAMES
        is_drowsy_by_yawn = len(self.yawn_timestamps) >= config.YAWN_ALERT_COUNT

        if is_drowsy_by_eye:
            state.status = "DROWSY: Eyes closed too long"
            state.alert_triggered = True
            self._trigger_alert("DROWSINESS", frame, ear, mar)
        elif is_drowsy_by_yawn:
            state.status = "WARNING: Frequent yawning"
            state.alert_triggered = True
            self._trigger_alert("YAWN_WARNING", frame, ear, mar)
        elif yawn_registered:
            state.status = "Yawn detected"
            append_event(self.csv_path, "YAWN_EVENT", ear, mar)
        else:
            state.status = "Monitoring"

        self._draw_overlay(frame, state)
        return frame, state

    def _draw_overlay(self, frame, state):
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (450, 185), (20, 20, 20), -1)
        cv2.addWeighted(overlay, 0.55, frame, 0.45, 0, frame)

        info_lines = [
            f"Status: {state.status}",
            f"EAR (Eye Aspect Ratio): {state.ear:.3f}",
            f"MAR (Mouth Aspect Ratio): {state.mar:.3f}",
            f"Eye closed frames: {state.eye_closed_frames}",
            f"Recent yawns (last {config.YAWN_WINDOW_SECONDS}s): {state.yawn_count_recent}",
            "Press Q to quit",
        ]

        y = 40
        for i, text in enumerate(info_lines):
            color = (0, 255, 0)
            if i == 0 and state.alert_triggered:
                color = (0, 0, 255)
            cv2.putText(
                frame,
                text,
                (20, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.62,
                color,
                2,
                cv2.LINE_AA,
            )
            y += 25
