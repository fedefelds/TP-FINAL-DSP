import numpy
import librosa
from numpy import array
from numpy import append
from numpy import zeros
from numpy import flipud
from scipy.signal import lfilter
import matplotlib.pyplot as plt
import scipy as sp
filename='/Users/Fede/Documents/Github/TP-FINAL-DSP/Python/raw.mp3'
# cargar audio
y, sr = librosa.load(filename)
librosa.output.write_wav('y_2.wav', y, 22050)
