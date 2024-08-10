from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import io
from PIL import Image

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the trained model
model = load_model("./fruit_classifier.h5")

# Define the image size required by your model
IMG_HEIGHT, IMG_WIDTH = (
    100,
    100,
)  # Update these dimensions according to your model's requirements


def prepare_image(img):
    # Convert image to RGB if it's not
    if img.mode != "RGB":
        img = img.convert("RGB")
    img = img.resize((IMG_WIDTH, IMG_HEIGHT))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array


@app.route("/")
def serve_html():
    return send_file("./index.html")


@app.route("/upload", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        if file:
            img = Image.open(io.BytesIO(file.read()))
            img_array = prepare_image(img)
            predictions = model.predict(img_array)
            predicted_class = np.argmax(predictions, axis=1)

            # Replace this with your own class labels
            class_labels = [
                "apple",
                "banana",
                "beetroot",
                "bell pepper",
                "cabbage",
                "capsicum",
                "carrot",
                "cauliflower",
                "chilli pepper",
                "corn",
                "cucumber",
                "eggplant",
                "garlic",
                "ginger",
                "grapes",
                "jalepeno",
                "kiwi",
                "lemon",
                "lettuce",
                "mango",
                "onion",
                "orange",
                "paprika",
                "pear",
                "peas",
                "pineapple",
                "pomegranate",
                "potato",
                "raddish",
                "soy beans",
                "spinach",
                "sweetcorn",
                "sweetpotato",
                "tomato",
                "turnip",
                "watermelon",
            ]
            predicted_label = class_labels[predicted_class[0]]

            return jsonify({"fruit": predicted_label}), 200
    except Exception as e:
        print(f"Error processing image: {e}")
        return jsonify({"error": "Error processing image"}), 500

    return jsonify({"error": "Invalid file format"}), 400


if __name__ == "__main__":
    app.run(debug=True)
