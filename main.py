import pandas as pd
from torch.utils.data import Dataset
import torchaudio
import torch


class Frame:
    def __init__(self, directory):
        self.genre = None
        self.path = None
        self.dir = directory

    # creates dictionary which points the genre to all its path files
    def _create_dic(self):
        # define dictionary which maps genre with all the file paths
        genres_dic = {
            'blues': [],
            'classical': [],
            'country': [],
            'disco': [],
            'hiphop': [],
            'jazz': [],
            'metal': [],
            'pop': [],
            'reggae': [],
            'rock': []
        }
        # get list of all genres to loop through in a list
        genre_list = list(genres_dic.keys())
        for i in range(len(genre_list)):
            for j in range(100):
                if j < 10:
                    genres_dic[f'{genre_list[i]}'].append(f'{self.dir}/{genre_list[i]}/{genre_list[i]}.0000{j}.wav')
                else:
                    genres_dic[f'{genre_list[i]}'].append(f'{self.dir}/{genre_list[i]}/{genre_list[i]}.000{j}.wav')
        self.path = genres_dic
        self.genre = genre_list
        # return genres_dic, genre_list

    # creates a dataframe from the given dictionaries
    def create_df(self):
        # self.path, self.genre = self._create_dic()
        self._create_dic()
        # loop to create a list of dictionaries, then concat into one dataframe with index reset
        dic_list = []
        for i in range(len(self.genre)):
            dic_list.append(
                pd.DataFrame.from_dict({'Path': self.path[f'{self.genre[i]}'], 'Genre': f'{self.genre[i]}'}))
        dataframe = pd.concat(dic_list, ignore_index=True)
        return dataframe


# class Test(Frame):
#     def __init__(self, directory):
#         super().__init__(directory)
#         self.cock = 'hi'
#         self.create_df()
#
#
# a = Test(DIR)
#
# print(a.path)


class SoundDataset(Dataset):
    # annotations file keep track of the fold/filename to classid mapping
    # audio dir is path to the wav file
    def __init__(self, dataframe, transformation, target_sample_rate):
        self.dataframe = dataframe
        self.transformation = transformation
        self.target_sample_rate = target_sample_rate

    # defines the length of the dataset, a.k.a the number of samples in the dataset
    def __len__(self):
        return len(self.dataframe)

    def __getitem__(self, index):
        # get audio sample path based on index
        audio_sample_path = self._get_audio_sample_path(index)
        # get label associated with audio file path based on index
        label = self._get_audio_sample_label(index)
        # get waveform and sample rate of wavefile
        signal, sr = torchaudio.load(audio_sample_path)
        # make signals have all the same sample rates
        signal = self._resample_if_necessary(signal, sr)
        # turn waveform from multichannel to mono
        signal = self._mix_down_if_necessary(signal)
        # transform signal as a waveform to a mel spectrogram
        signal = self.transformation(signal)
        return signal, label

    def _resample_if_necessary(self, signal, sr):
        if sr != self.target_sample_rate:
            resampler = torchaudio.transforms.Resample(sr, self.target_sample_rate)
            signal = resampler(signal)
        return signal

    def _mix_down_if_necessary(self, signal):
        if signal.shape[0] > 1:
            signal = torch.min(signal, dim=0, keepdim=True)
        return signal

    def _get_audio_sample_path(self, index):
        return self.dataframe.iloc[index][0]

    def _get_audio_sample_label(self, index):
        return self.dataframe.iloc[index][1]


if __name__ == "__main__":
    DIR = 'Data/genres_original'
    SAMPLE_RATE = 16000

    mel_spectrogram = torchaudio.transforms.MelSpectrogram(
        sample_rate=SAMPLE_RATE,
        n_fft=1024,
        hop_length=512,
        n_mels=64
    )

    data = Frame(DIR)
    df = data.create_df()
    music_ds = SoundDataset(df, mel_spectrogram, SAMPLE_RATE)
    print(f"There are {len(music_ds)} samples in the dataset.")
    signal, label = music_ds[0]

    a = 1
