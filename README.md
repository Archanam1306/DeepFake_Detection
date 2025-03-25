# AlgoSmash  
A DeepFake Video Detection Web Application powered by AI.

AlgoSmash is an end-to-end web solution designed to detect deepfake **videos** using a lightweight PyTorch model. The frontend is built with **Next.js** and **Tailwind CSS**, while the backend is a **Flask API** serving predictions via a `.pt` model. It processes uploaded videos frame-by-frame and classifies them into real or deepfake categories.


## Features

 Accepts **video uploads** via frontend interface
- Frame-by-frame deepfake classification using PyTorch model
- Fast and scalable backend powered by Flask + Gunicorn
- Predicts from 6 classes: Real, FaceSwap, Face2Face, NeuralTextures, FaceShifter, DeepfakeDetection
- Displays per-class metrics, including Precision, Recall, and F1-Score
- Docker support for clean deployment

## Workflow

1. Users upload a video file.
2. Frontend sends a `POST` request to `http://localhost:3001/predict`.
3. Backend:
   - Extracts frames from the video using OpenCV.
   - Passes frames to the `.pt` model for prediction.
   - Aggregates predictions into a final label.
4. Frontend displays the classification result (`Real` or deepfake class) back to the user.

---

## Model Info

- Format: PyTorch `.pt` file
- Input: Frames extracted from uploaded video
- Classes:
  - Real
  - Fake
- Datasets Used
  - FakeFace++
- Performance:
  - Accuracy: **84%**
  - Macro Avg F1-Score: **0.85**
## Frontend 

- cd frontEnd
- npm install
- npm run dev


![image](https://github.com/user-attachments/assets/c079efbd-4fec-4a4f-8193-97baf04a5a75)

![image](https://github.com/user-attachments/assets/a1e7d038-0db4-4a85-8e50-e627fea9916d)

![image](https://github.com/user-attachments/assets/372a1d78-88de-4149-bd90-09f88b488843)

![image](https://github.com/user-attachments/assets/cd2b2342-50c7-4b38-a977-1ada4e21286c)

![image](https://github.com/user-attachments/assets/8afeb4af-3891-4383-9d9f-6e7d4a3cf6f6)


 ## To-Do
 
 Improve detection speed for longer videos

 Add preview thumbnails or frame-level predictions

 Deploy backend to HuggingFace Spaces or Render





