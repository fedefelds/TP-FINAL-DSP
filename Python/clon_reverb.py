from numpy import append
from numpy import zeros
from numpy import array
from scipy.signal import lfilter
import librosa

# Ensure correct input size
input.shape = original.shape
# Get input length in samples
inputLength = len(input)
# Initialize output array
output = zeros(input.shape)

carpeta='/Users/Fede/Desktop/The Turn of a Friendly Card 1979 (GPF)/Canciones del trabajo/'
filename='10'
formato='.mp3'
filename=carpeta+filename+formato
# cargar audio
y, sr = librosa.load(filename)

# Initialize filter coefficients
a = array([0.6, 0.4, 0.2, 0.1, 0.7, 0.6, 0.8])
R = array([700, 900, 600, 400, 450, 390])

# Implement reverb algorithm
num1 = append(0, zeros(R[0] - 1)); # parece que agrega un delay
num1 = append(num1, 1);
den1 = append(1, zeros(R[0] - 1));
den1 = append(den1, -a[0]);
d1 = lfilter(num1, den1, input)
num2 = append(0, zeros(R[1] - 1));
num2 = append(num2, 1);
den2 = append(1, zeros(R[1] - 1));
den2 = append(den2, -a[1]);
d2 = lfilter(num2, den2, input)
num3 = append(0, zeros(R[2] - 1));
num3 = append(num3, 1);
den3 = append(1, zeros(R[2] - 1));
den3 = append(den3, -a[2]);
d3 = lfilter(num3, den3, input)
num4 = append(0, zeros(R[3] - 1));
num4 = append(num4, 1);
den4 = append(1, zeros(R[3] - 1));
den4 = append(den4, -a[3]);
d4 = lfilter(num4, den4, input)
d = d1 + d2 + d3 + d4
num5 = append(a[4], zeros(R[4] - 1));
num5 = append(num5, 1);
den5 = append(1, zeros(R[4] - 1));
den5 = append(den5, a[4]);
d = lfilter(num5, den5, d)
num6 = append(a[5], zeros(R[5] - 1));
num6 = append(num6, 1);
den6 = append(1, zeros(R[5] - 1));
den6 = append(den6, a[5]);
d = lfilter(num6, den6, d)
output = input + a[6] * d;
# Clip amplitude to minimize distortion
output *= 0.45

# Ensure correct output array size
output.shape = original.shape

# Hold current output in case of undo
outputHold = output
