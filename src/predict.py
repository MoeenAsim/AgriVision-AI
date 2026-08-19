from pathlib import Path

import numpy as np
import tensorflow as tf
from PIL import Image


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "best_cnn.keras"

# Model configuration
IMG_SIZE = (128, 128)

CLASS_NAMES = [
    "brown_rust",
    "healthy",
    "yellow_rust",
]


# Load model once when the module starts
model = tf.keras.models.load_model(MODEL_PATH)


def predict_image(image_path):
    """
    Predict the wheat leaf class from an image.
    """

    image = Image.open(image_path).convert("RGB")
    image = image.resize(IMG_SIZE)

    image_array = np.asarray(
    image,
    dtype=np.float32
)
    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    probabilities = model.predict(
        image_array,
        verbose=0
    )[0]

    predicted_index = int(np.argmax(probabilities))

    return {
        "disease": CLASS_NAMES[predicted_index],
        "confidence": float(probabilities[predicted_index]),
    }
if __name__ == "__main__":
    image_path = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "test"
        / "brown_rust"
        / "Brown_rust008.jpg"
    )

    result = predict_image(image_path)

    print(result)