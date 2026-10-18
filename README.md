# Customer Credit Risk - Full Stack

This branch adds a complete full-stack application around the existing CREDIT_CARD_CLIENTS.ipynb analysis. It includes:

- Backend: FastAPI service that loads a trained sklearn/XGBoost pipeline and exposes a /predict endpoint.
- Training script: train.py to preprocess data, train a pipeline, and save model artifacts to backend/model.joblib.
- Frontend: React + Vite single-page app with a form to enter customer features and call the prediction API.
- Docker + docker-compose setup to run frontend and backend together.

Quickstart
1. Copy the dataset into `data/default_of_credit_card_clients.xls` (or point to your path). The original notebook used the Excel file with header=1.
2. Create a Python venv and install train requirements: `pip install -r backend/requirements.txt`
3. Train the model: `python train.py --data data/default_of_credit_card_clients.xls --out backend/model.joblib`
4. Start backend: `uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000`
5. Start frontend:
   - `cd frontend`
   - `npm install`
   - `npm run dev`

Or use Docker Compose: `docker-compose up --build`

See backend/README.md and frontend/README.md for more details.
