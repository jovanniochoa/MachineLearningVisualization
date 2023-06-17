import os
import pickle
import importlib.util
import logging
import librosa
import numpy as np
from flask import Flask, jsonify, render_template, redirect, url_for, request

# Check if scikit-misc package is installed, and install it if not
package_name = 'scikit-misc'
spec = importlib.util.find_spec(package_name)
if spec is None:
    os.system(f"pip install scikit-misc")

app = Flask(__name__)

# Load the machine learning model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/uploads', methods=['POST'])
def upload():
    try:
        file = request.files['file']  # Access the uploaded file
        
        # Save the file to a designated location on the server
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        
        # Process the uploaded file with the machine learning model
        result = process_file(file_path)
        
        return jsonify({'message': 'File uploaded successfully', 'result': result})
    except Exception as e:
        app.logger.error(str(e))
        return jsonify({'message': 'Error occurred while uploading file'})

def process_file(file_path):
    # Preprocess the audio file
    signal, sr = librosa.load(file_path, sr=22050)
    
    # Extract features
    # Placeholder code, replace with your feature extraction code
    feature = extract_features(signal, sr)
    
    # Reshape the feature for model prediction
    feature = feature.reshape(1, -1)
    
    # Perform model prediction
    predicted_class = model.predict(feature)[0]
    
    return predicted_class


def extract_features(signal, sr):
    # Placeholder code for feature extraction
    # Replace with your actual feature extraction code
    # Here's an example using Mel-Frequency Cepstral Coefficients (MFCC)
    mfccs = librosa.feature.mfcc(signal, sr=sr, n_mfcc=13)
    feature = np.mean(mfccs.T, axis=0)  # Take the mean along the time axis
    
    return feature

@app.route('/')
def index():
    return render_template('MusicClassification.html')

if __name__ == '__main__':
    app.logger.setLevel(logging.ERROR)
    handler = logging.StreamHandler()
    app.logger.addHandler(handler)
    app.run(debug=True)
