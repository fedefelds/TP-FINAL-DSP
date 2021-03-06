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
filename='/Users/Fede/Documents/Github/TP-FINAL-DSP/Python/raw.mp3'
# cargar audio
y, sr = librosa.load(filename)

#filtros nuevos (reiss)
# parametros para Reiss
g=array([0.7,0.7,0.7,0.7,0.7,0.7,0.7])
tau=array([0.1,0.03,0.01,0.003,0.001,0.0004,0.0001])
d=tau*sr
d=d.astype(int)

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
librosa.output.write_wav('reiss_punch_rev.wav', y_rev, sr)

f, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=True)
ax1.plot(y)
ax2.plot(y_rev)
f.subplots_adjust(hspace=0)
ax1.set_ylabel('Amplitud')
ax2.set_ylabel('Amplitud')
ax2.set_xlabel('Muestras')
plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
plt.savefig('/Users/Fede/Documents/Github/TP-FINAL-DSP/Informe/imagenes/reiss_opera',dpi=300)
