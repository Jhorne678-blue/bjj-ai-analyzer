import os
import json
import numpy as np
from datetime import datetime

DATA_DIR = 'data'
MODEL_DIR = 'models'

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

def save_pose_sequence(video_id, pose_sequence):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    path = os.path.join(DATA_DIR, f'{video_id}_{timestamp}.json')
    with open(path, 'w') as f:
        json.dump(pose_sequence, f)
    print(f"Saved pose sequence to {path}")
    return path

def load_all_pose_sequences():
    sequences = []
    for file in os.listdir(DATA_DIR):
        if file.endswith('.json'):
            with open(os.path.join(DATA_DIR, file), 'r') as f:
                sequences.append(json.load(f))
    return sequences

def basic_train_model():
    sequences = load_all_pose_sequences()
    if not sequences:
        print("No data available to train.")
        return

    averages = []
    for seq in sequences:
        flat = [point for frame in seq for point in frame]
        averages.append(np.mean(flat))

    model = {
        "trained_on": len(sequences),
        "average_pose_value": float(np.mean(averages))
    }

    model_path = os.path.join(MODEL_DIR, 'model.json')
    with open(model_path, 'w') as f:
        json.dump(model, f)

    print(f"Model saved to {model_path}")
    return model
