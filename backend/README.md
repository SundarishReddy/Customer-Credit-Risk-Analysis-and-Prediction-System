A small README for the backend service.

1. Install dependencies
   pip install -r backend/requirements.txt

2. Train model
   python train.py --data data/default_of_credit_card_clients.xls --out backend/model.joblib

3. Run server
   uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

API
- GET /health
- POST /predict  -> { "data": { <feature>: value, ... } }
