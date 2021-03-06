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

################################################################################
#							filtros (smith) serie->paralelo
# 		https://ccrma.stanford.edu/~jos/pasp/Schroeder_Reverberators.html
################################################################################


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

g=array([0.7,0.7,0.7,0.773,0.802,0.753,0.733])
n=array([347,113,37,1687,1601,2053,2251])

y_1=ap(g[0],n[0],y)
y_2=ap(g[1],n[1],y_1)
y_3=ap(g[2],n[2],y_2)

x_1=fbcf(g[3],n[3],y_3)
x_2=fbcf(g[4],n[4],y_3)
x_3=fbcf(g[5],n[5],y_3)
x_4=fbcf(g[6],n[6],y_3)

s_1=x_1+x_3
s_2=x_2+x_4

a=s_1+s_2
# b=-a
# d=s_1-s_2
# c=-d


librosa.output.write_wav('smith_1_opera.wav',a, sr)

f, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=True)
ax1.plot(y)
ax2.plot(a)
f.subplots_adjust(hspace=0)
ax1.set_ylabel('Amplitud')
ax2.set_ylabel('Amplitud')
ax2.set_xlabel('Muestras')
plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
plt.savefig('/Users/Fede/Documents/Github/TP-FINAL-DSP/Informe/imagenes/smith_1_opera',dpi=300)
