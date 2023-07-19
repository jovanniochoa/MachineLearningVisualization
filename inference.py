import torch
import torchaudio

from cnn import CNNNetwork
from main import SoundDataset, Frame
from train import SAMPLE_RATE, NUM_SAMPLES, DIR


class_mapping = [
    "blues",
    "classical",
    "country",
    "disco",
    "hiphop",
    "jazz",
    "metal",
    "pop",
    "reggae",
    "rock"
]


def predict(model, input, target, class_mapping):
    model.eval()
    with torch.no_grad():
        predictions = model(input)
        # Tensor (1, 10) -> [ [0.1, 0.01, ..., 0.6] ]
        predicted_index = predictions[0].argmax(0)
        predicted = class_mapping[predicted_index]
        expected = class_mapping[target]
    return predicted, expected


if __name__ == "__main__":
    # load back the model
    cnn = CNNNetwork()
    state_dict = torch.load("feedforwardnet.pth")
    cnn.load_state_dict(state_dict)

    # load urban sound dataset dataset
    mel_spectrogram = torchaudio.transforms.MelSpectrogram(
        sample_rate=SAMPLE_RATE,
        n_fft=1024,
        hop_length=512,
        n_mels=64
    )

    data = Frame(DIR)
    df = data.create_df()
    music_ds = SoundDataset(df, mel_spectrogram, SAMPLE_RATE, NUM_SAMPLES, "cpu")


    # get a sample from the urban sound dataset for inference
    # wrong = 0
    # for i in range(len(music_ds)):
    #     input, target = music_ds[i][0], music_ds[i][1]
    #     input.unsqueeze_(0)
    #     predicted, expected = predict(cnn, input, target,
    #                                   class_mapping)
    #     if predicted != expected:
    #         wrong = wrong + 1
    # print((1000 - wrong)/len(music_ds))

    input, target = music_ds[324][0], music_ds[324][1] # [batch size, num_channels, fr, time]
    input.unsqueeze_(0)

    # make an inference
    predicted, expected = predict(cnn, input, target,
                                  class_mapping)
    print(f"Predicted: '{predicted}', expected: '{expected}'")

    a = 1