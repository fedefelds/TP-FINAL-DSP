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


def ap(g,n,y):
    num=zeros(n+1)
    num[0]=-g
    num[len(num)-1]=1
    den=flipud(num)
    y1=lfilter(num,den,y)
    return y1

def fbcf(g,n,y):
    num=zeros(n+1)
    num[0]=1
    den=zeros(n+1)
    den[0]=1
    den[len(num)-1]=-g
    y1=lfilter(num,den,y)
    return y1

g_1=0.7
n_1=347
g_2=0.7
n_2=113
g_3=0.7
n_3=37

y_1=ap(g_1,n_1,y)
y_2=ap(g_2,n_2,y_1)
y_3=ap(g_3,n_3,y_2)

g_4=0.773
n_4=1687
g_5=0.802
n_5=1601
g_6=0.753
n_6=2053
g_7=0.733
n_7=2251

x_1=fbcf(g_4,n_4,y_3)
x_2=fbcf(g_5,n_5,y_3)
x_3=fbcf(g_6,n_6,y_3)
x_4=fbcf(g_7,n_7,y_3)

s_1=x_1+x_3
s_2=x_2+x_4

a=s_1+s_2
b=-a
d=s_1-s_2
c=-d

librosa.output.write_wav('a.wav', a, sr)
librosa.output.write_wav('b.wav', b, sr)
librosa.output.write_wav('c.wav', c, sr)
librosa.output.write_wav('d.wav', d, sr)
