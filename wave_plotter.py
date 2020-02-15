import sys
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt


def clear():
    print('\n' * 100)


def file_info(sig, sr, filename):
    samples = len(sig)
    sec = round(samples / sr, 2)
    msec = round(sec / 1000, 0)
    print('File loaded. Its name is', filename)
    print('It has', samples, 'samples at', sr, 'Hz.')
    print('That is', msec, 'ms or about', sec, 'seconds.')


def wave_plot(x, y):
    title = plot_title()
    if title == '':
        title = 'Wave plot'
    plt.plot(x, y)
    plt.xlabel('Time (ms)')
    plt.title(title)


def amplitude_plot(y, sr):
    title = plot_title()
    if title == '':
        title = 'Amplitude plot'
    librosa.display.waveplot(y, sr)
    plt.title(title)


def plot_spectrogram(y, kind='linear'):
    title = plot_title()
    if title == '':
        title = 'Spectrogram'
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    librosa.display.specshow(D, x_axis='time', y_axis=kind)
    plt.title(title)


def plot_title():
    print('Enter a fancy title? (ENTER for default)')
    title = input()
    return title


clear()

filename = sys.argv[1]

sig, sr = librosa.load(filename)

# make x time axis (ms)
t = (np.arange(len(sig)) / sr) * 1000

# if successful
clear()
file_info(sig, sr, filename)


entire_file = None
while entire_file != 'y' and entire_file != 'n':
    entire_file = input("Wanna plot the entire file? (y/n)")

if entire_file == 'y':
    y = sig
    x = t

elif entire_file == 'n':
    start_ms = input('Where to start? (ms)')
    end_ms = input('Where to end? (ms)')
    start = int((int(start_ms) / 1000) * sr)
    end = int((int(end_ms) / 1000) * sr)
    # cut the file and timeline
    y = sig[start:end]
    x = t[start:end]

response = ''

while response != 'e':
    clear()
    file_info(sig, sr, filename)
    print()
    print('Select plot type:')
    print('Wave plot (w)')
    print('Amplitude (via librosa) (a)')
    print('Spectrogram (linear) (s)')
    print('Spectrogram (log) (l)')
    print('Exit (e)')
    response = input()

    clear()

    # make the actual plot
    if response == 'w':
        wave_plot(x, y)
    elif response == 'a':
        amplitude_plot(y, sr)
    elif response == 's':
        plot_spectrogram(y, kind='linear')
    elif response == 'l':
        plot_spectrogram(y, kind='log')

    plt.show()

print('Bye bye!')

