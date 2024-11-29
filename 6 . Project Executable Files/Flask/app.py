from flask import Flask, render_template, request, url_for
from PIL import Image
import numpy as np
import tensorflow as tf
import os
import uuid

# Initialize the Flask app
app = Flask(__name__)

# Use the existing uploads folder in the static directory
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load the model at the start of the application
model_path = 'breastcancer.h5'
if os.path.exists(model_path):
    try:
        print("Loading model...")
        model = tf.keras.models.load_model(model_path)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        model = None
else:
    print(f"Model not found at {model_path}.")
    model = None

@app.route('/')
def index():
    """Render the home page."""
    return render_template('index.html', prediction=None, image_url=None)

@app.route('/predict', methods=['POST'])
def predict():
    """Handle image uploads, make predictions, and display the image."""
    try:
        # Check if an image file was uploaded
        if 'input_file' not in request.files or request.files['input_file'].filename == '':
            return render_template('index.html', prediction="No file selected. Please upload an image.", image_url=None)

        file = request.files['input_file']

        # Save the image to the upload folder with a unique name
        filename = f"{uuid.uuid4().hex}.jpg"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Open the image using PIL
        img = Image.open(filepath).convert('RGB')  # Ensure 3 channels (RGB)
        img = img.resize((128, 128))  # Resize to target size

        # Convert the image to a numpy array
        img_array = np.array(img) / 255.0  # Normalize to [0, 1]
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

        # Make prediction
        if model:
            prediction = model.predict(img_array)[0][0]
            if prediction > 0.5:
                result = "Malignant Tumor: Please consult your doctor."
            else:
                result = "Benign Tumor: No need to worry."
        else:
            result = "Error: Model not loaded."

        # Generate a relative URL for the uploaded image
        image_url = url_for('static', filename=f'uploads/{filename}')

        # Return the prediction and the uploaded image URL
        return render_template('index.html', prediction=result, image_url=image_url)

    except Exception as e:
        print(f"Error occurred during prediction: {e}")
        return render_template('index.html', prediction=f"Error: {str(e)}", image_url=None)

if __name__ == '__main__':
    app.run(debug=True)
