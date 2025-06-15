import cv2
import mediapipe as mp
import numpy as np
from trainer import save_pose_sequence

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

def run_fake_analysis(filename):
    cap = cv2.VideoCapture(f'uploads/{filename}')
    pose_sequence = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            pose_frame = [[lm.x, lm.y, lm.z] for lm in landmarks]
            pose_sequence.append(pose_frame)

    cap.release()

    # Save pose data for learning
    save_pose_sequence(filename, pose_sequence)

    return {
        'status': 'Analysis Complete',
        'frames_processed': len(pose_sequence),
        'sample_pose': pose_sequence[0] if pose_sequence else 'No poses found'
    }
