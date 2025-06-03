from flask import Flask, request, render_template, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np
import os
import uuid

app = Flask(__name__)

# Directory to save uploaded images
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load the trained model
model = load_model("skin_disease_model.keras")

# Class labels
class_names = [
    "Cellulitis", "Impetigo", "Athlete-Foot", "Nail-Fungus",
    "Ringworm", "Cutaneous-larva-migrans", "Chickenpox", "Shingles", "no disease"
]

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Check if file type is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Preprocess image for prediction
def preprocess_image(img, target_size=(150, 150)):
    img = img.resize(target_size)
    img = img.convert("RGB")
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = img / 255.0
    return img

@app.route("/", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        file = request.files.get("file")

        # ✅ If no file is uploaded, return "no disease"
        if not file or file.filename == "":
            return render_template("index.html", prediction="no disease", image_url=None)

        # ✅ Check file type
        if not allowed_file(file.filename):
            return render_template("index.html", prediction="Unsupported file type!", image_url=None)

        try:
            # Save the uploaded file
            filename = f"{uuid.uuid4().hex}_{file.filename}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            # Open and preprocess the image
            image = Image.open(filepath)
            processed = preprocess_image(image)

            # Predict
            prediction = model.predict(processed)
            predicted_class = class_names[np.argmax(prediction)]
            confidence = np.max(prediction)

            # Use this if you want to display confidence too
            result = f"{predicted_class} ({confidence * 100:.2f}% confidence)"

            # Display image
            image_url = url_for('static', filename=f"uploads/{filename}")
            return render_template("index.html", prediction=result, image_url=image_url)

        except Exception as e:
            print("Error during prediction:", e)
            return render_template("index.html", prediction="Error during prediction", image_url=None)

    # GET method
    return render_template("index.html", prediction=None, image_url=None)

if __name__ == "__main__":
    app.run(debug=True)
