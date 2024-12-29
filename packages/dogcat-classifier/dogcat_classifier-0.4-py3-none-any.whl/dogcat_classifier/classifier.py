import tensorflow as tf
import tensorflow_hub as hub
import tf_keras
# Load the model with the custom layer registered
def load_model(model_path):
    return tf_keras.models.load_model(
        model_path,
        custom_objects={'KerasLayer': hub.KerasLayer}  # Register the KerasLayer from tensorflow_hub
    )

# Load the model
model = load_model('dogcat_classifier/model.h5')

# Define the prediction function
def predict_image(image_path):
    import cv2
    import numpy as np

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
