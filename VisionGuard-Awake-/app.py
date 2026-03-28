import cv2

import config
from detector import DrowsinessDetector


def main():
    cap = cv2.VideoCapture(config.CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)

    if not cap.isOpened():
        raise RuntimeError("Could not access webcam. Check camera permissions or CAMERA_INDEX in config.py.")

    detector = DrowsinessDetector()

    print("Starting VisionGuard Awake...")
    print("Press Q to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame from webcam.")
            break

        processed_frame, _ = detector.process_frame(frame)
        cv2.imshow(config.WINDOW_NAME, processed_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
