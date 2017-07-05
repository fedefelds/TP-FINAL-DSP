from numpy import append
from numpy import zeros
from numpy import array
from scipy.signal import lfilter
import matplotlib.pyplot as plt

def delay_line(m,y):
    b=zeros(m+1)
    b[m]=1
    n=1
    a=zeros(n+1)
    a[0]=1
    out=lfilter(b,a,raw)
    plt.plot(raw)
    plt.plot(out)
    plt.show()
# delay a simple impulse
raw=array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
delay_line(5,raw)
