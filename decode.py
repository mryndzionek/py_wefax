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


ANALYSIS_WIN_START_SEC = 0
ANALYSIS_WIN_LEN_SEC = 29


def find_carrier(data, sr, plot=False):
    f, t, fft = sig.stft(data, fs=sr)
    Y = np.max(np.abs(fft), axis=-1)

    pk = sig.find_peaks(
        Y, height=np.min(Y) + 0.2 * (np.max(Y) - np.min(Y)), distance=5
    )[0]
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


def find_phase(data, sr, plot=False):
    k = np.concatenate(
        (
            np.zeros(round(sr * 0.475)),
            np.ones(round(sr * 0.025)),
            np.zeros(round(sr * 0.475)),
        )
    )
    sync_sig = sig.correlate(sig.medfilt(data, 201), k / len(k))
    per = round(sr / 2)
    pk = sig.find_peaks(sync_sig, height=1, distance=per)[0]

    pk_diffs = pk[1:] - pk[:-1]
    pk_bincount = np.bincount(pk_diffs)
    period_peak = pk_bincount.argmax()

    period_flt = []
    b_count = 0
    i = period_peak
    while pk_bincount[i] > 0:
        period_flt.append(i)
        b_count += pk_bincount[i]
        i += 1
    i = period_peak - 1
    while pk_bincount[i] > 0:
        period_flt.append(i)
        b_count += pk_bincount[i]
        i -= 1

    slant = (np.max(period_flt) - np.min(period_flt)) / b_count
    period = np.mean(period_flt)

    idx = np.where(pk_diffs == round(period))[0][-1]
    phase = pk[idx]
    phase_min = phase % per

    if plot:
        plt.plot(sync_sig)
        plt.plot(
            pk, sync_sig[pk], marker="x", linestyle="None", color="blue", linewidth=5
        )
        plt.plot(
            [phase_min, phase],
            [sync_sig[phase_min], sync_sig[phase]],
            marker="o",
            mfc="none",
            linestyle="None",
            color="red",
            linewidth=8,
        )
        plt.grid(True)
        plt.show()

    return phase_min, period, slant


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


def decode(input_fn, output_fn, aggressive_filt=False):
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

    if aggressive_filt:
        ff1 = sig.iirpeak(f1, 1.5, fs=sr)
        ff2 = sig.iirpeak(f2, 1.5, fs=sr)
        samples = sig.filtfilt(*ff1, samples) + sig.filtfilt(*ff2, samples)

    analytic_sig = sig.hilbert(samples)
    ref = 1.0 / (2 * math.pi * 0.99)
    r_prime = np.concatenate((np.zeros(1), analytic_sig[:-1]))
    fm_demod = (np.angle(np.conj(r_prime) * analytic_sig)) * ref * sr

    taps = sig.firwin(300, sr * 0.1, fs=sr)
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

    phase, period, slant = find_phase(head, sr)
    print(f"Sync pulse phase: {1000 * phase/sr:.2f}ms")
    print(f"Sync pulse period: {1000 * period/sr:.2f}ms")
    print(f"Slant: {slant}")

    img_data = deslant(bytestream, (sr / 2) + slant, phase)

    im = Image.fromarray(img_data)
    im = im.resize((img_data.shape[0], img_data.shape[0]), Image.Resampling.LANCZOS)
    im.save(output_fn)
    # im.show()


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
