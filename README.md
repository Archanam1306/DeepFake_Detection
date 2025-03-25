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
  - Face2Face
  - FaceSwap
  - NeuralTextures
  - FaceShifter
  - DeepfakeDetection
- Performance:
  - Accuracy: **84%**
  - Macro Avg F1-Score: **0.85**
## Frontend 

cd frontEnd
npm install
npm run dev

 ## To-Do
 
 Improve detection speed for longer videos

 Add preview thumbnails or frame-level predictions

 Deploy backend to HuggingFace Spaces or Render



