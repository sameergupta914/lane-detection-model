# Lane Detection App

This repo now contains:

- the original training notebook: `lanenet_model_mp.ipynb`
- the trained model: `best_model.keras`
- a FastAPI inference backend: `backend/`
- a React frontend: `frontend/`

## Backend

Backend entrypoint:

- `backend/app/main.py`

Run from repo root:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload
```

Backend URLs:

- Health: `http://localhost:8000/health`
- Predict: `http://localhost:8000/api/predict`
- Generated output images: `http://localhost:8000/outputs/...`

## Frontend

Frontend workspace:

- `frontend/`

Run:

```powershell
cd frontend
npm run dev
```

Frontend URL:

- `http://localhost:5173`

## Current Inference Flow

1. Upload a road image in the React UI.
2. Frontend sends it to the FastAPI backend as `multipart/form-data`.
3. Backend:
   - loads `best_model.keras`
   - resizes input to `224 x 224`
   - normalizes to `[0, 1]`
   - runs prediction
   - rounds the predicted mask
   - resizes mask back to original image size
   - creates an overlay image
4. Frontend displays:
   - original image preview
   - predicted mask
   - overlay image

## Notes

- Backend dependencies were installed into `.venv`.
- Frontend dependencies were installed in `frontend/node_modules`.
- The React app builds successfully with `npm run build`.
- The backend inference code was tested successfully on a real sample image from `train_set/clips/.../20.jpg`.
