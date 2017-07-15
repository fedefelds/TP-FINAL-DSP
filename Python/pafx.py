import numpy
import librosa
from numpy import array
from numpy import append
from numpy import zeros
from numpy import flipud
from scipy.signal import lfilter
import matplotlib.pyplot as plt
import scipy as sp
# filename='/Users/Fede/Documents/Github/TP-FINAL-DSP/Python/raw.mp3'
filename='/Users/Fede/Documents/Github/TP-FINAL-DSP/Python/raww.mp3'

# cargar audio
y, sr = librosa.load(filename)
# Initialize filter coefficients
a = array([0.6, 0.4, 0.2, 0.1, 0.7, 0.6, 0.8])
R = array([700, 900, 600, 400, 450, 390])
R=R*1.3

# Implement reverb algorithm
num1 = append(0, zeros(R[0]-1)); num1 = append(num1, 1);
den1 = append(1, zeros(R[0]-1)); den1 = append(den1, -a[0]);
d1 = lfilter(num1, den1, y)
num2 = append(0, zeros(R[1]-1)); num2 = append(num2, 1);
den2 = append(1, zeros(R[1]-1)); den2 = append(den2, -a[1]);
d2 = lfilter(num2, den2, y)
num3 = append(0, zeros(R[2]-1)); num3 = append(num3, 1);
den3 = append(1, zeros(R[2]-1)); den3 = append(den3, -a[2]);
d3 = lfilter(num3, den3, y)
num4 = append(0, zeros(R[3]-1)); num4 = append(num4, 1);
den4 = append(1, zeros(R[3]-1)); den4 = append(den4, -a[3]);
d4 = lfilter(num4, den4, y)
d = d1 + d2 + d3 + d4
num5 = append(a[4], zeros(R[4]-1)); num5 = append(num5, 1);
den5 = append(1, zeros(R[4]-1)); den5 = append(den5, a[4]);
d = lfilter(num5, den5, d)
num6 = append(a[5], zeros(R[5]-1)); num6 = append(num6, 1);
den6 = append(1, zeros(R[5]-1)); den6 = append(den6, a[5]);
d = lfilter(num6, den6, d)
output = y + a[6]*d;
# Clip amplitude to minimize distortion
output *= 0.45


librosa.output.write_wav('pafx.wav', output, sr)
