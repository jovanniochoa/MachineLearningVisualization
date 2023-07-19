import os
from flask import Flask, render_template, request
import pandas as pd
import torch
import torchaudio

from cnn import CNNNetwork
from main import SoundDataset, Frame
from train import SAMPLE_RATE, NUM_SAMPLES, DIR
from inference import class_mapping
from pydub import AudioSegment

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class Prediction:
    def __init__(self, model, class_mapping, transformation):
        self.model = model
        self.class_mapping = class_mapping
        self.mel_spectrogram = transformation

    def predict(self, path):
        self.model.eval()
        with torch.no_grad():
            input = self._get_input(path)
            predictions = self.model(input)
            predicted_index = predictions[0].argmax(0)
            predicted = self.class_mapping[predicted_index]
        return predicted

    def _get_input(self, path):
        data = [[f'{path}', 0]]
        df = pd.DataFrame(data, columns=['Path', 'Genre'])
        music_ds = SoundDataset(df, self.mel_spectrogram, SAMPLE_RATE, NUM_SAMPLES, "cpu")
        input, _ = music_ds[0]  # Get both signal and label
        input = input.unsqueeze(0)  # Add a batch dimension
        return input


@app.route('/')
def index():
    return render_template('project1.html')

@app.route('/project1')
def project1():
    return render_template('project1.html')

@app.route('/uploads', methods=['POST'])
def uploads():
    file = request.files['file']
    if file:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        prediction = get_prediction(filepath)
        return render_template('result.html', prediction=prediction)
    return "No file uploaded."


def get_prediction(filepath):
    cnn = CNNNetwork()
    state_dict = torch.load("feedforwardnet.pth")
    cnn.load_state_dict(state_dict)
    mel_spectrogram = torchaudio.transforms.MelSpectrogram(
        sample_rate=SAMPLE_RATE,
        n_fft=1024,
        hop_length=512,
        n_mels=64
    )
    predictor = Prediction(cnn, class_mapping, mel_spectrogram)
    prediction = predictor.predict(filepath)
    return prediction


if __name__ == '__main__':
    app.run()
