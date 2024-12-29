import tensorflow as tf
import tensorflow_hub as hub
import pkg_resources
import numpy as np
import cv2
import tf_keras
import warnings
import os

# Step 1: Suppress TensorFlow logs by setting the environment variable
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress INFO and WARNING logs from TensorFlow

# Step 2: Use the warnings module to filter out specific TensorFlow warnings
# Ignore deprecation warnings as well
warnings.simplefilter(action='ignore', category=DeprecationWarning)

# Load the model with the custom layer registered
def load_model(model_path):
    return tf_keras.models.load_model(
        model_path,
        custom_objects={'KerasLayer': hub.KerasLayer}  # Register the KerasLayer from tensorflow_hub
    )

# Fetch the model path from the installed package using pkg_resources
def get_model_path():
    return pkg_resources.resource_filename('dogcat_classifier', 'model.h5')

# Load the model using the path from pkg_resources
model_path = get_model_path()
model = load_model(model_path)

# Define the prediction function
def predict_image(image_path):
    # Read and preprocess the image
    image = cv2.imread(image_path)
    image_resized = cv2.resize(image, (224, 224))
    image_scaled = image_resized / 255.0
    image_reshaped = np.reshape(image_scaled, [1, 224, 224, 3])

    # Make a prediction
    prediction = model.predict(image_reshaped)
    pred_label = np.argmax(prediction)

    # Interpret the prediction
    if pred_label == 0:
        return 'Cat'
    else:
        return 'Dog'
