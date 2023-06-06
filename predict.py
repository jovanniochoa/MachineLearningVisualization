import pandas as pd
import torch
import torchaudio

from cnn import CNNNetwork
from main import SoundDataset, Frame
from train import SAMPLE_RATE, NUM_SAMPLES, DIR
from inference import class_mapping


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


if __name__ == "__main__":
    cnn = CNNNetwork()
    state_dict = torch.load("feedforwardnet.pth")
    cnn.load_state_dict(state_dict)
    mel_spectrogram = torchaudio.transforms.MelSpectrogram(
        sample_rate=SAMPLE_RATE,
        n_fft=1024,
        hop_length=512,
        n_mels=64
    )
    path = 'uploads/SongJuan.wav'
    predictor = Prediction(cnn, class_mapping, mel_spectrogram)
    prediction = predictor.predict(path)
    print(prediction)
