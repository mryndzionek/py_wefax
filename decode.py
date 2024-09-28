import os
import math
import glob

import numpy as np
import scipy.signal as sig
import scipy.io.wavfile as wv
from scipy.fft import fft
from scipy import ndimage

import matplotlib.pyplot as plt
from PIL import Image


ANALYSIS_WIN_START_SEC = 7
ANALYSIS_WIN_LEN_SEC = 29


def find_carrier(data, sr, plot=False):
    f, t, fft = sig.stft(data, fs=sr)
    Y = np.max(np.abs(fft), axis=-1)

    pk = sig.find_peaks(Y, height=0.5, distance=10)[0]
    Yi = Y[pk]
    Xi = f[pk]

    si = np.flip(np.argsort(Yi))[:2]

    if plot:
        plt.plot(f, Y)
        plt.plot(
            Xi,
            Yi,
            marker="x",
            linestyle="None",
            color="red",
            linewidth=5,
            label="peaks (modes)",
        )
        plt.plot(
            Xi[si],
            Yi[si],
            marker="o",
            linestyle="None",
            mfc="none",
            color="red",
            linewidth=5,
            label="peaks (modes)",
        )
        plt.grid(True)
        plt.show()

    return sorted(Xi[si])


def find_phase_and_period(data, sr, plot=False):
    k = np.concatenate(
        (
            np.zeros(round(sr * 0.475)),
            np.ones(round(sr * 0.025)),
            np.zeros(round(sr * 0.475)),
        )
    )
    sync_sig = sig.correlate(sig.medfilt(data, 201), k / len(k))

    pk = sig.find_peaks(sync_sig, height=5, distance=round(sr * 0.475) // 2)[0]
    avgpk = np.average(sync_sig[pk])

    A = np.vstack([np.arange(len(pk)), np.ones(len(pk))]).T
    per, phase = np.linalg.lstsq(A, pk, rcond=None)[0]

    if phase > per:
        phase -= per

    print(f"Sync pulse period: {100 * per/sr:.2f}ms")
    print(f"Sync pulse phase: {100 * phase/sr:.2f}ms")

    if plot:
        plt.plot(sync_sig)
        plt.plot(
            pk, sync_sig[pk], marker="x", linestyle="None", color="red", linewidth=5
        )
        plt.plot(
            per * (np.arange(len(pk))) + phase,
            len(pk) * [avgpk],
            marker="o",
            mfc="none",
            linestyle="None",
            color="red",
            linewidth=5,
        )
        plt.grid(True)
        plt.show()

    return per, phase


def deslant(data, line_len, offset):
    img_data = []
    index = offset
    line_len_round = int(line_len)

    while True:
        i = round(index)
        l = data[i : i + line_len_round]
        if len(l) < line_len_round:
            break
        index += line_len
        img_data.append(l)

    return np.asarray(img_data)


def decode(input_fn, output_fn):
    sr, samples = wv.read(input_fn)
    samples = samples.astype(np.float32) / np.iinfo(type(samples[0])).max
    samples = 4 * samples[0 : sr * (len(samples) // sr)]

    taps = sig.firwin(300, sr * 0.4, fs=sr)
    samples = sig.filtfilt(taps, 1.0, samples)

    f1, f2 = find_carrier(
        samples[
            ANALYSIS_WIN_START_SEC
            * sr : (ANALYSIS_WIN_START_SEC + ANALYSIS_WIN_LEN_SEC)
            * sr
        ],
        sr,
    )

    print(f"Samplerate: {sr}Hz")
    print(f"Carrier freqs: {f1:.2f}Hz - {f2:.2f}Hz")
    print(f"Freq offset: {f2 - f1:.2f}Hz")

    analytic_sig = sig.hilbert(samples)
    ref = 1.0 / (2 * math.pi * 0.99)
    r_prime = np.concatenate((np.zeros(1), analytic_sig[:-1]))
    fm_demod = (np.angle(np.conj(r_prime) * analytic_sig)) * ref * sr

    taps = sig.firwin(300, sr * 0.06, fs=sr)
    fm_demod = sig.filtfilt(taps, 1.0, fm_demod)

    def tres_f(x):
        if abs(x - f1) > abs(x - f2):
            return 255
        else:
            return 0

    fm_demod = np.array(list(map(tres_f, fm_demod)))
    bytestream = np.round(fm_demod).astype(np.uint8)

    head = bytestream[
        ANALYSIS_WIN_START_SEC
        * sr : (ANALYSIS_WIN_START_SEC + ANALYSIS_WIN_LEN_SEC)
        * sr
    ].astype(np.float32)

    _, phase = find_phase_and_period(head, sr)
    offset = round(phase)

    img_data = deslant(bytestream, (sr / 2), offset)

    im = Image.fromarray(img_data)
    im = im.resize((img_data.shape[0], img_data.shape[0]), Image.Resampling.LANCZOS)
    im.save(output_fn)


file_names = glob.glob("recordings/*")

for fn in sorted(file_names):
    out_name = os.path.join(
        "images", os.path.splitext(os.path.basename(fn))[0] + ".png"
    ).replace(" ", "_")

    if not os.path.exists(out_name):
        print("Decoding file: {}".format(fn))
        decode(fn, out_name)

file_names = glob.glob("images/*")

for i, fn in enumerate(sorted(file_names)):
    if not "websdr.png" in fn:
        print("![img_{}]({})".format(i + 1, fn))
        print("")
