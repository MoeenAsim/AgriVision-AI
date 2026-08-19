from pathlib import Path
import shutil
import tempfile
import requests

from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles

from src.predict import predict_image


app = FastAPI(
    title="AgriVision AI",
    description="Wheat disease classification API",
    version="1.0.0",
)


# n8n Production Webhook URL
N8N_WEBHOOK_URL = "http://localhost:5678/webhook/agri-vision-prediction"


# Serve frontend
app.mount(
    "/frontend",
    StaticFiles(directory="frontend", html=True),
    name="frontend"
)


@app.get("/")
def root():
    return {
        "message": "AgriVision AI API is running",
        "frontend": "/frontend/"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    suffix = Path(file.filename).suffix

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    ) as temp_file:

        shutil.copyfileobj(file.file, temp_file)
        temp_path = Path(temp_file.name)

    try:
        # 1. CNN prediction
        result = predict_image(temp_path)

        # 2. Send prediction to n8n
        n8n_data = {
            "filename": file.filename,
            "disease": result["disease"],
            "confidence": result["confidence"]
        }

        n8n_response = requests.post(
            N8N_WEBHOOK_URL,
            json=n8n_data,
            timeout=30
        )

        n8n_response.raise_for_status()

        # 3. Get processed data from n8n
        n8n_result = n8n_response.json()

        # n8n may return a list containing the final item
        if isinstance(n8n_result, list) and len(n8n_result) > 0:
            n8n_result = n8n_result[0]

        # 4. Return complete result
        return {
            "filename": file.filename,
            "disease": result["disease"],
            "confidence": result["confidence"],
            "confidence_percentage": n8n_result.get(
                "confidence_percentage",
                round(result["confidence"] * 100, 2)
            ),
            "explanation": n8n_result.get(
                "explanation",
                "Explanation unavailable."
            ),
            "symptoms": n8n_result.get(
                "symptoms",
                "Symptoms unavailable."
            ),
            "management": n8n_result.get(
                "management",
                "Management information unavailable."
            )
        }

    finally:
        temp_path.unlink(missing_ok=True)