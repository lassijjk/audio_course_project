# Lassi Kirvesmäki 275173
# Project on Topic 1
# Algorithm based on equations 24-30 in paper:
# Ono, N., Miyamoto, K., Le Roux, J., Kameoka, H., & Sagayama, S. (2008, August).
# Separation of a monaural audio signal into harmonic/percussive components by complementary diffusion on spectrogram.
# In 2008 16th European Signal Processing Conference (pp. 1-4). IEEE.

import numpy as np
import librosa as lb
import librosa.display as display
import matplotlib.pyplot as plt
import time
from scipy.io.wavfile import write


def query_variables():
    file = input('Enter variable filename including extension: ')
    k_max = int(input('Enter variable k_max (integer): '))
    variables = []
    for variable in ['alpha', 'gamma']:
        variables.append(float(input('Enter ' + variable + ': ')))
    return file, k_max, variables


def calculate_delta(h, p, alpha):
    h_next, h_prev = h.copy(), h.copy()
    p_up, p_down = p.copy(), p.copy()

    h_next = np.roll(h_next, -1, axis=0)
    h_prev = np.roll(h_prev, 1, axis=0)

    p_up = np.roll(p_up, -1, axis=1)
    p_down = np.roll(p_down, 1, axis=1)

    # Eq. 23 in the paper.
    delta = alpha * (h_prev - 2 * h + h_next) / 4 - (1 - alpha) * (p_down - 2 * p + p_up) / 4
    return delta


def steps4to6(h, p, w, alpha):
    # Update variables delta calculation. Step 4.
    delta = calculate_delta(h, p, alpha)

    # Harmonic and percussive part calculation. Eq. 26 and 27 in paper. Step 5.
    h = np.minimum(np.maximum(h + delta, 0), w)
    p = w-h
    return h, p


def binarize(h, p, w):
    for i in range(len(h)):
        for j in range(len(h[0])):
            h[i][j] = 0 if h[i][j] < p[i][j] else w[i][j]
            p[i][j] = w[i][j] - h[i][j]
    return h, p


def binary_to_waveform(h, p, stft, gamma, data_length, hop_length):
    args = [h, p]
    waveforms = []
    for value in args:
        exp = np.exp(np.angle(stft)*1j) * np.power(value, 1/(2*gamma))
        print(np.sum(np.sum(exp, axis=1)))
        istft = lb.istft(exp, hop_length=hop_length, length=data_length)
        waveforms.append(istft)
    return waveforms


def plot_spectrogram(n, spec, fs, refpoint, title):
    plt.subplot(3, 1, n)
    lb.display.specshow(lb.amplitude_to_db(np.abs(spec), ref=refpoint), sr=fs, y_axis='log', x_axis='time')
    plt.colorbar()
    plt.title(title)
    plt.tight_layout()


def main():
    n_fft = 1024
    hop_length = int(n_fft / 2)

    file, k_max, [alpha, gamma] = query_variables()

    data, fs = lb.load(file)

    # STFT of the input signal, Step 1 in the algorithm.
    stft = lb.stft(data, n_fft=n_fft, hop_length=hop_length)

    # Range-compressed version of the STFT, Step 2 in algorithm and eq. 24 in the paper.
    w = np.power(np.abs(stft), 2*gamma)

    # Initial values of harmonic and percussive parts, Step 3 in algorithm and eq. 25 in the paper.
    h, p = 0.5*w.copy(), 0.5*w.copy()

    start = time.time()
    # Iterating steps 4 to 6 in the paper k_max times.
    for i in range(k_max):
        print(i)
        h, p = steps4to6(h, p, w, alpha)
    print(f"Iterating {k_max} times took {time.time()-start} seconds.")

    # Saving spectrograms for later usage
    h_spec, p_spec = h.copy(), p.copy()

    # Step 7 in the paper.
    h, p = binarize(h, p, w)

    # Step 8 in the paper.
    h_wav, p_wav = binary_to_waveform(h, p, stft, gamma, len(data), hop_length)

    # SNR calculation for evaluation of algorithm
    snr = lb.power_to_db(np.sum(np.power(data, 2)), np.sum(np.power(data - p_wav - h_wav, 2)))
    print(f"SNR: {snr} dB")

    # Saving harmonic and percussive parts for further usage (and for fun)
    write(f'k({k_max})_alpha({alpha})_gamma({gamma})_harmonic_parts_of_{file}', fs, h_wav)
    write(f'k({k_max})_alpha({alpha})_gamma({gamma})_percussive_parts_of_{file}', fs, p_wav)

    # Plotting using an example from librosa available at https://pythontic.com/visualization/signals/spectrogram
    rp = np.max(np.abs(stft))
    plt.figure(figsize=(12, 8))
    plot_spectrogram(1, stft, fs, rp, 'Original spectrogram')
    plot_spectrogram(2, h_spec, fs, rp, 'Harmonic spectrogram')
    plot_spectrogram(3, p_spec, fs, rp, 'Percussive spectrogram')
    plt.show()


if __name__ == '__main__':
    main()

