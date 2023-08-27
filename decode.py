import os
import math
import glob

import numpy as np
import scipy.signal as sig
import scipy.io.wavfile as wv
from scipy.fft import fft

import matplotlib.pyplot as plt
from PIL import Image


PULSES_OFFSET = 2


def find_carrier(data, sr):
    offset = PULSES_OFFSET * sr
    f, t, fft = sig.stft(data[offset:offset + (10 * sr)], fs=sr)
    Y = np.max(np.abs(fft), axis=-1)

    pk = sig.find_peaks(Y, height=0.2, distance=10)[0]
    Yi = Y[pk]
    Xi = f[pk]

    # plt.plot(f, Y)
    # plt.plot(Xi, Yi, marker="x",
    #          linestyle='None', color="red", linewidth=5, label="peaks (modes)")
    # plt.grid(True)
    # plt.show()

    if(len(pk) != 2):
        raise ValueError('Unable to detect the carrier frequency')

    # print(Xi[0], Xi[1])

    return Xi[0], Xi[1]


def deslant(data, line_len):
    img_data = []
    index = 0.0
    line_len_round = int(line_len)

    while True:
        i = round(index)
        l = data[i: i + line_len_round]
        if len(l) < line_len_round:
            break
        index += line_len
        img_data.append(l)

    return np.asarray(img_data)


def decode(input_fn, output_fn):
    sr, samples = wv.read(input_fn)
    samples = samples.astype(np.float32) / np.iinfo(type(samples[0])).max
    samples = 4 * samples[0:sr * (len(samples) // sr)]

    taps = sig.firwin(300, sr * 0.4, fs=sr)
    samples = sig.filtfilt(taps, 1.0, samples)

    f1, f2 = find_carrier(samples, sr)

    print("Samplerate: {}Hz".format(sr))
    print("Carrier freqs: {}Hz - {}Hz".format(f1, f2))
    print("Freq offset: {}Hz".format(f2 - f1))

    analytic_sig = sig.hilbert(samples)
    ref = 1.0 / (2*math.pi*0.99)
    r_prime = np.concatenate((np.zeros(1), analytic_sig[:-1]))
    fm_demod = (np.angle(np.conj(r_prime) * analytic_sig)) * ref * sr
    fm_demod = sig.medfilt(fm_demod, 3)

    def tres_f(x): return 255 * (x - f1) / (f2 - f1)

    bytestream = np.round(np.clip(tres_f(fm_demod), 0, 255)).astype(np.uint8)

    head = bytestream[PULSES_OFFSET *
                      sr:(PULSES_OFFSET + 10)*sr].astype(np.float32)
    sync_sig = sig.correlate(head, np.concatenate(
        (np.ones(100), np.zeros(200))) / 100)

    def tres_f(x): return x > 220

    matches = tres_f(sync_sig).astype(np.float32)
    edges = np.subtract(matches[1:], matches[:-1])
    falling = np.nonzero(edges < 0.0)[0]

    # plt.plot(matches)
    # plt.show()

    offset = falling[0] - 300
    bytestream = bytestream[(PULSES_OFFSET + 10)*sr + offset:]
    img_data = deslant(bytestream, (sr / 2) + 0.06)

    im = Image.fromarray(img_data)
    im = im.resize(
        (img_data.shape[0], img_data.shape[0]), Image.Resampling.LANCZOS)
    im.save(output_fn)


file_names = glob.glob('recordings/*')

for fn in sorted(file_names):
    out_name = os.path.join("images", os.path.splitext(
        os.path.basename(fn))[0] + ".png").replace(' ', '_')

    if not os.path.exists(out_name):
        print('Decoding file: {}'.format(fn))
        decode(fn, out_name)

file_names = glob.glob('images/*')

for i, fn in enumerate(sorted(file_names)):
    if not 'websdr.png' in fn:
        print("![img_{}]({})".format(i+1, fn))
        print('')
