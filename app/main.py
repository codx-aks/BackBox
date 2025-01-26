import os
import base64
from ultralytics import YOLO
import cv2
import numpy as np
from collections import defaultdict
from app.controllers.alert_controller import AlertController

def process_video(base64_video, video_name="uploaded_video.mp4"):
    """
    Processes a video for object detection, generates alerts, and deletes the video after processing.

    :param base64_video: Base64 encoded video string.
    :param video_name: Name to save the decoded video as .mp4.
    """
    video_path = f"./{video_name}"
    print("hy1")
    with open(video_path, "wb") as video_file:
        video_file.write(base64.b64decode(base64_video))

    model_path = "best.pt"
    model = YOLO(model_path)

    cap = cv2.VideoCapture(video_path)
    print("hy2")
    if not cap.isOpened():
        raise Exception(f"Failed to open video file: {video_path}")

    frame_count = 0
    class_counts = defaultdict(int)
    confidence_threshold = 0.25

    class_names = [
        'Hardhat', 'Mask', 'NO-Hardhat', 'NO-Mask', 'NO-Safety Vest',
        'Person', 'Safety Cone', 'Safety Vest', 'Machinery', 'Vehicle'
    ]
    risk_levels = {
        "NO-Hardhat": "medium",
        "NO-Mask": "low",
        "NO-Safety Vest": "low",
        "Machinery": "medium",
        "Vehicle": "medium",
        "Safety Cone": "low"
    }

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        results = model(frame)

        for result in results:
            boxes = result.boxes.xyxy.numpy()
            scores = result.boxes.conf.numpy()
            classes = result.boxes.cls.numpy().astype(int)

            for box, score, cls in zip(boxes, scores, classes):
                if score >= confidence_threshold:
                    class_name = model.names[cls]
                    if class_name in class_names:
                        class_counts[class_name] += 1

    cap.release()

    average_counts = {class_name: count / frame_count for class_name, count in class_counts.items()}
    print("\nAverage Detections per Frame (Confidence >= 0.25):")
    for class_name, avg_count in average_counts.items():
        if avg_count > 0.005 and class_name in risk_levels:
            risk = risk_levels[class_name]
            alert_data = {
                "alert_id": f"{frame_count}_{class_name}",
                "severity": risk,
                "watch_id": 5,
                "lat": 5.045,
                "long": 7.034,
                "alert_type": class_name
            }
            AlertController.add_alert(alert_data)
            print(f"Alert sent: {alert_data}")

    os.remove(video_path)
    print(f"Temporary video file {video_name} deleted after processing.")

