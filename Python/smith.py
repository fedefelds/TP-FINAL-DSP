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
# filtros viejos (smith)

# Parametros para smith
g=array([0.805,0.827,0.783,0.764,0.7,0.7,0.7])
d=array([901,778,1011,1123,125,42,12])

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
########################Empieza el filtrado#####################################

# # filtrado en paralelo x4:
y_1=fbcf(g[0],d[0],y)
y_2=fbcf(g[1],d[1],y)
y_3=fbcf(g[2],d[2],y)
y_4=fbcf(g[3],d[3],y)

# #sumador
y_rev=y_1+y_2+y_3+y_4

# filtrado en serie x3:
y_rev=ap(g[4],d[4],y_rev)
y_rev=ap(g[5],d[5],y_rev)
y_rev=ap(g[6],d[6],y_rev)

# sumador
y_rev=0.5*y_rev+y
y_rev=0.2*y_rev
librosa.output.write_wav('raw.wav', y, sr)
# librosa.output.write_wav('y_1.wav', y_1, sr)
# librosa.output.write_wav('y_2.wav', y_2, sr)
# librosa.output.write_wav('y_3.wav', y_3, sr)
# librosa.output.write_wav('y_4.wav', y_4, sr)
librosa.output.write_wav('smith_opera_rev.wav', y_rev, sr)
