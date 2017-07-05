import numpy
from numpy import array
from numpy import append
from numpy import zeros
from numpy import flipud
from scipy.signal import lfilter
import matplotlib.pyplot as plt
import scipy as sp
# mean = 0
# std = 1
# num_samples = 66150
# samples = numpy.random.normal(mean, std, size=num_samples)


x=array([2,0,0,1])
c=flipud(x)
print(c)
