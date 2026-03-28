import csv
import math
import os
from datetime import datetime


def euclidean_distance(p1, p2):
    return math.dist(p1, p2)


def eye_aspect_ratio(eye_points):
    """
    eye_points order:
    [left_corner, upper_left, upper_right, right_corner, lower_right, lower_left]
    """
    vertical_1 = euclidean_distance(eye_points[1], eye_points[5])
    vertical_2 = euclidean_distance(eye_points[2], eye_points[4])
    horizontal = euclidean_distance(eye_points[0], eye_points[3])

    if horizontal == 0:
        return 0.0

    return (vertical_1 + vertical_2) / (2.0 * horizontal)


def mouth_aspect_ratio(mouth_points):
    """
    mouth_points order:
    [left_corner, upper_lip, right_corner, lower_lip]
    """
    horizontal = euclidean_distance(mouth_points[0], mouth_points[2])
    vertical = euclidean_distance(mouth_points[1], mouth_points[3])

    if horizontal == 0:
        return 0.0

    return vertical / horizontal


def ensure_csv(csv_path):
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    if not os.path.exists(csv_path):
        with open(csv_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "event_type", "ear", "mar"])


def append_event(csv_path, event_type, ear, mar):
    ensure_csv(csv_path)
    with open(csv_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            event_type,
            f"{ear:.4f}",
            f"{mar:.4f}",
        ])


def alert_beep():
    """
    Cross-platform low-dependency alert:
    - Windows: winsound
    - Other platforms: terminal bell fallback
    """
    try:
        import winsound
        winsound.Beep(1200, 350)
    except Exception:
        print("\a", end="", flush=True)
