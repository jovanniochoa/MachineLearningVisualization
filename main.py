import pandas as pd
from torch.utils.data import Dataset

DIR = 'Data/genres_original'


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
                    genres_dic[f'{genre_list[i]}'].append(f'{self.dir}/{genre_list[i]}/{genre_list[i]}.000{j}.wav')
                else:
                    genres_dic[f'{genre_list[i]}'].append(f'{self.dir}/{genre_list[i]}/{genre_list[i]}.00{j}.wav')
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
    def __init__(self, dataframe):
        self.dataframe = df

    # defines the length of the dataset, a.k.a the number of samples in the dataset
    def __len__(self):
        return len(self.dataframe)

    def __getitem__(self, index):
        # get audio sample path based on index
        audio_sample_path = self._get_audio_sample_path(index)
        # get label associated with audio file path based on index
        label = self._get_audio_sample_label(index)


# create df from data
df = Frame(DIR).create_df()

a = SoundDataset(df)
print(a.__len__())
