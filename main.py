# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Fi76JcYwumtP7FNKgzZJoSUGUr8kxSBa
"""

pip install torch torchvision torchaudio opencv-python numpy pillow

# Install required libraries
!pip install torch torchvision numpy opencv-python pillow tqdm

# ✅ Import necessary libraries
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.models as models
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, Dataset
from PIL import Image
import os
import cv2
import numpy as np
from tqdm import tqdm  # For progress tracking

# ✅ Define CNN Model for Deepfake Detection
class DeepfakeCNN(nn.Module):
    def __init__(self, num_classes=2):
        super(DeepfakeCNN, self).__init__()
        self.resnet = models.resnet18(pretrained=True)
        self.resnet.fc = nn.Linear(self.resnet.fc.in_features, num_classes)  # Modify last layer for binary classification

    def forward(self, x):
        return self.resnet(x)

# ✅ Set device (GPU if available)
device = "cuda" if torch.cuda.is_available() else "cpu"
model = DeepfakeCNN().to(device)

# ✅ Define loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# ✅ Define Dataset Class for Deepfake Detection (Extracts Frames from Videos)
class DeepfakeVideoDataset(Dataset):
    def __init__(self, data_dir, transform=None, frame_interval=5):
        self.data_dir = data_dir
        self.transform = transform
        self.video_paths = []
        self.labels = []
        self.frame_interval = frame_interval  # Extract frames every 'frame_interval' frames

        # Load all videos from "real" and "fake" folders
        for label, folder in enumerate(["real", "fake"]):
            folder_path = os.path.join(data_dir, folder)
            for video in os.listdir(folder_path):
                if video.endswith(".mp4"):
                    self.video_paths.append(os.path.join(folder_path, video))
                    self.labels.append(label)

    def __len__(self):
        return len(self.video_paths)

    def __getitem__(self, idx):
        video_path = self.video_paths[idx]
        label = self.labels[idx]

        # ✅ Extract a random frame from the video
        cap = cv2.VideoCapture(video_path)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if frame_count == 0:
            cap.release()
            return None  # Skip if video is corrupt

        frame_idx = np.random.randint(0, frame_count, 1)[0]  # Select a random frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)

        ret, frame = cap.read()
        cap.release()

        if not ret:
            return None  # Skip corrupted frames

        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))  # Convert OpenCV BGR to PIL RGB

        if self.transform:
            image = self.transform(image)

        return image, label

# ✅ Define Data Transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# ✅ Load Dataset and DataLoader
dataset_path = "/content/drive/MyDrive/FF++"
train_dataset = DeepfakeVideoDataset(dataset_path, transform=transform)
train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)

# ✅ Train the Model
num_epochs = 7
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0

    for images, labels in tqdm(train_loader, desc=f"Epoch {epoch+1}/{num_epochs}"):
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()

        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(train_loader):.4f}")

# ✅ Save Trained Model
torch.save(model.state_dict(), "model.pt")
print("✅ Model saved as model.pt")

# ✅ Load Model for Inference
model = DeepfakeCNN()
model.load_state_dict(torch.load("model.pt", map_location=device))
model.to(device)
model.eval()
print("✅ Model loaded successfully.")

# ✅ Function to Extract Frames from a Video for Testing
def extract_frames(video_path, output_folder, frame_interval=5):
    os.makedirs(output_folder, exist_ok=True)
    cap = cv2.VideoCapture(video_path)

    frame_count, saved_count = 0, 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            frame_path = os.path.join(output_folder, f"frame_{saved_count}.jpg")
            cv2.imwrite(frame_path, frame)
            saved_count += 1

        frame_count += 1

    cap.release()
    print(f"✅ Extracted {saved_count} frames from {video_path} into {output_folder}")

# ✅ Define Function for Predicting a Single Frame
def predict_frame(frame_path, model, device="cuda"):
    image = Image.open(frame_path).convert("RGB")
    image = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output, 1)

    return predicted.item()  # 0 = Real, 1 = Fake

# ✅ Function to Predict if a Video is Fake or Real
import numpy as np

def predict_video(video_path, model, device="cuda"):
    # 1️⃣ Extract frames from the video
    video_frames_folder = "video_test_frames"
    extract_frames(video_path, video_frames_folder, frame_interval=10)

    # 2️⃣ Predict each frame
    frame_predictions = []

    for frame in sorted(os.listdir(video_frames_folder)):
        if frame.endswith(".jpg"):
            frame_path = os.path.join(video_frames_folder, frame)
            pred = predict_frame(frame_path, model, device)
            frame_predictions.append(pred)

    # 3️⃣ Use majority voting to decide final result
    final_prediction = np.bincount(frame_predictions).argmax()
    label = "Fake" if final_prediction == 1 else "Real"
    print(f"🎯 Final Prediction for Video '{video_path}': {label}")

# ✅ Run Prediction on a Single Test Video
test_video_path = "/content/drive/MyDrive/FF++/fake/02_27__walk_down_hall_angry__78M8S6M6.mp4"
predict_video(test_video_path, model)

video_path = "/content/drive/MyDrive/deepfaketest.mp4"
predict_video(video_path, model, device="cuda")  # Use "cpu" if no GPU
