import os
import json
import joblib
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(title="Cosmetic Classifier API")

# Montar pasta de arquivos estáticos (HTML/CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

model_path = os.path.join("models", "classifier.joblib")
data_path = os.path.join("data", "cosmeticos.json")

class PredictRequest(BaseModel):
    texto: str

@app.get("/")
def serve_index():
    return FileResponse("static/index.html")

@app.get("/produtos")
def get_produtos():
    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@app.post("/classificar")
def predict_category(req: PredictRequest):
    if not os.path.exists(model_path):
        return {"error": "Modelo não encontrado. Execute o treinamento primeiro."}
    
    model = joblib.load(model_path)
    prediction = model.predict([req.texto])[0]
    return {"categoria_prevista": prediction}