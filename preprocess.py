import math
import numpy as np
import pandas as pd
import librosa as lb
import matplotlib.pyplot as plt

# CODE FROM https://github.com/meetshah1995/crnn-music-genre-classification/blob/master/src/read_data.py:
def get_melspectrograms(labels_dense, num_classes=10):
    spectrograms = np.asarray([log_scale_melspectrogram(i) for i in labels_dense['path']])
    spectrograms = spectrograms.reshape(spectrograms.shape[0], spectrograms.shape[1], spectrograms.shape[2], 1)
    return spectrograms

Fs         = 12000
N_FFT      = 512
N_MELS     = 96
N_OVERLAP  = 256
DURA       = 29.12

def log_scale_melspectrogram(path, plot=False):
    signal, sr = lb.load(path, sr=Fs)
    n_sample = signal.shape[0]
    n_sample_fit = int(DURA*Fs)

    if n_sample < n_sample_fit:
        signal = np.hstack((signal, np.zeros((int(DURA*Fs) - n_sample,))))
    elif n_sample > n_sample_fit:
        bottom = int(math.floor(n_sample-n_sample_fit)/2)
        top = int(math.floor(n_sample+n_sample_fit)/2)

        signal = signal[bottom:top]

    melspect = lb.amplitude_to_db(lb.feature.melspectrogram(y=signal, sr=Fs, hop_length=N_OVERLAP, n_fft=N_FFT, n_mels=N_MELS)**2, ref=1.0)

    if plot:
        melspect = melspect[np.newaxis, :]
        plt.imshow(melspect.reshape((melspect.shape[1], melspect.shape[2])))
        plt.show()
        print(melspect.shape)
    return melspect


#########################################
# OUR CODE BELOW HERE:
#########################################

def preprocess(labels):
    """Given the labels array, produce two arrays, the first is the labels and the second is the
    corresponding data. The index of the labels array matches the index of the data array."""
    train_labels = []
    train_data = []
    print("Starting Data Process: ")
    print("\t" + str(len(labels)), "labels found...",end="\n\t")
    for i in range(len(labels)):
        path = labels['path'][i]
        label = int(labels['label'][i])
        train_labels.append(label)
        data = log_scale_melspectrogram(path)
        train_data.append(data)
        percent_done = round((i/len(labels))*100,2)
        print(str(percent_done) + "% done" + "."*(i%4), end="\r\t")
    print()
    return np.array(train_labels), np.array(train_data)

if __name__ == '__main__':
    labels_file = 'labels.csv'
    tags = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']
    labels = pd.read_csv(labels_file, header=0)
    out = preprocess(labels)

    np.save("labels.npy", out[0])
    print("labels array saved to labels.npy")
    np.save("data.npy", out[1])
    print("data array saved to data.npy")


