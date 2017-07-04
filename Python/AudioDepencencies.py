###################################################################
# Modules
###################################################################
# GUI Modules
from Tkinter import *
import tkFont
import Pmw
# Numpy, Scipy, and Scikits Audiolab modules
from numpy import *
from scipy.signal import *
from scikits.audiolab import *
from scikits.audiolab import available_file_formats, available_encodings
# Plotting Modules
from matplotlib import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


##################################################################

#################################################################
# Functions
#################################################################
# Declare function called in fftPlot
# Calculates number equal to next power of 2 of input
# Analogous to MATLAB function of same name
def nextpow2(i):
    n = 2
    while n < i: n = n * 2
    return n


# Declare function that calculates the NFFT-length FFT
# of the input data, NFFT is equal to the next power
# of 2 of the length of the input data,
# also returns frequency data (x-axis) to be used for plotting
def fftPlot(x, fs):
    # Get length of data
    L = len(x)
    # Calculate optimal length of FFT using nextpow2
    NFFT = 2 ^ nextpow2(L)
    # Calculate fft using Numpy FFT method
    INPUT = numpy.fft.fft(x, NFFT) / L
    # Create frequency (x) axis data for plotting
    fAxis = fs / 2 * linspace(0, 1, NFFT / 2 + 1)
    # Calculate magnitude response from FFT data
    mAxis = 2 * abs(INPUT[0:NFFT / 2 + 1])
    # Return frequency axis data, magnitude response, and FFT length
    return fAxis, mAxis, NFFT


#################################################################


#################################################################
# The 'Audio' Class
#################################################################


class Audio:
    """
    This Audio class includes a group of methods
    to read, write, visualize, and process audio.
    The class will specifically support 3 common
    audio file formats:
      .wav
      .aiff
      .flac
  
    Example usage:
    # Read in the file 'austin.wav'
    audio = Audio('austin.wav')
    """

    def __init__(self, filename):
        """
        The __init__ method is to be used to read the audio file,
        create the Audio object, and setup certain attributes
        to be accessed by the Audio methods (original data,
        current input data, current output data, input and
        output temp data (for Undo method), length of
        original data array), sampling frequency,
        format, and encoding type). The __init__ method
        takes as input a string that contains the filename of the
        audio file. This method also has some simple error checking
        built in to provide a more elegant error in the case that
        an incompatible filename is given as input.
    
        Input Parameter:
          filename
            Type: string
            Description: filename of the audio file to be read
        """

        # Perform read operation based on file extension
        # Read data, sampling frequency, encoding type
        # using Scikits Audiolab methods

        # .aiff specific
        # If last four characters of filename spell out aiff
        if filename[-4:] == 'aiff':
            try:
                # Read data; extract sampling frequency and encoding type
                self.original, self.sampFreq, self.enctype = aiffread(filename)

                # Get file format
                f = Sndfile(filename, 'r')
                self.format = f.file_format

                # Set up appropriate attributes
                self.origLen = len(self.original)
                self.input = self.original
                self.inputHold = self.input
                self.output = self.original
                self.outputHold = self.output
            except IOError:
                print
                '''
            I/O Error:
            Argument must meet following criteria:
            - Must be string.
            - Must be of format .wav, .aiff, or .flac.
            - Must include extension, ie. '.wav', '.aiff', '.flac'
            - Must be in current working directory.
              '''

        # .flac specific
        # If last four characters of filename spell out flac
        elif filename[-4:] == 'flac':
            try:
                # Read data; extract sampling frequency and encoding type
                self.original, self.sampFreq, self.enctype = flacread(filename)

                # Get file format
                f = Sndfile(filename, 'r')
                self.format = f.file_format

                # Set up appropriate attributes
                self.origLen = len(self.original)
                self.input = self.original
                self.inputHold = self.input
                self.output = self.original
                self.outputHold = self.output
            except IOError:
                print
                '''
            I/O Error:
            Argument must meet following criteria:
            - Must be string.
            - Must be of format .wav, .aiff, or .flac.
            - Must include extension, ie. '.wav', '.aiff', '.flac'
            - Must be in current working directory.
            '''

        # .wav specific
        # If last three characters of filename spell out wav
        elif filename[-3:] == 'wav':
            try:
                # Read data; extract sampling frequency and encoding type
                self.original, self.sampFreq, self.enctype = wavread(filename)

                # Get file format
                f = Sndfile(filename, 'r')
                self.format = f.file_format

                # Set up appropriate attributes
                self.origLen = len(self.original)
                self.input = self.original
                self.inputHold = self.input
                self.output = self.original
                self.outputHold = self.output
            except IOError:
                print
                '''
            I/O Error:
            Argument must meet following criteria:
            - Must be string.
            - Must be of format .wav, .aiff, or .flac.
            - Must include extension, ie. '.wav', '.aiff', '.flac'
            - Must be in current working directory.
              '''
        # If filename does not include any of the supported extensions
        else:
            try:
                raise IOError
            except IOError:
                print
                '''
            I/O Error:
            Argument must meet following criteria:
            - Must be string.
            - Must be of format .wav, .aiff, or .flac.
            - Must include extension, ie. '.wav', '.aiff', '.flac'
            - Must be in current working directory.
              '''

    def list(self):
        """
        The list method is simply a utility that lists the 3 supported
        fileformats supported by the class and the encoding types
        available for each. This method is meant to assist users with
        the input parameters of the write method detailed next.
        """
        # Create list of supported file formats
        format = ['wav', 'aiff', 'flac']
        # Loop through file format list
        for fmt in format:
            # Print file format to screen
            print("%s:\n" % fmt)
            # Loop through available encoding types
            # for current format
            for enc in available_encodings(fmt):
                # Print encoding types to screen
                print("\t%s\n" % enc)

            print
            "\n"

    def write(self, filename, format, enctype):
        """
        The writes the current output data to the current working
        working directory. The method takes three string inputs:
        the desired filename, file format, and desired encoding
        type for the audio file to be written.
    
        Input Parameters:
          filename
            Type: string
            Description: desired filename of written file
          format
            Type: string
            Description: desired file format of written file
          enctype
            Type: string
            Description: desired encoding type of written file
    
        Example usage:
        # Write current output data to a 8-bit WAV file names 'austin.wav'
        audio.write('austin.wav', 'wav', 'pcmu8')
        """

        # Assign attributes to variables for ease of use
        output = self.output
        sampFreq = self.sampFreq

        # Create format object to be used by Sndfile method
        fmt = Format(format, enctype)

        # Write output to file
        outfile = Sndfile(filename, 'w', fmt, 1, sampFreq)
        outfile.write_frames(output)

    def playOriginal(self):
        """
        The playOriginal method plays the original read data
        through the computer speakers.
        """
        # Play original data using Scikits Audiolab play method
        play(self.original, self.sampFreq)

    def playInput(self):
        """
        The playInput method plays the current input data through
        the computer speakers. The current input is the array
        generated immediately before the most recent effect has been
        processed. If no effects have been processed, the current
        input data is equal to the original data.
        """
        # Play current input data using Scikits Audiolab play method
        play(self.input, self.sampFreq)

    def playOutput(self):
        """
        The playOutput method plays the current output data through
        the computer speakers. The current output data is the array
        generated immediately after the most recent effect has been
        processed. 
        """
        # Play current output data using Scikits Audiolab play method
        play(self.input, self.sampFreq)

    def plotOriginal(self):
        """
        The plotOriginal method will generate a figure using
        matplotlib that contains 3 visualizations of the original
        data: data as function of time in seconds, FFT magnitude as
        function of frequency in hertz, and spectrogram.
    
        The figure is stored in an attribute called origFig.
        """

        # Assign attributes to variables for ease of use
        original = self.original
        origLen = self.origLen
        sampFreq = self.sampFreq

        # Calculate original data length in seconds
        seconds = arange(0, float(origLen) / sampFreq, 1.0 / sampFreq)
        # Calculate FFT magnitude of original data
        freq, inputFFT, nfft = fftPlot(original, sampFreq)

        # Create plots using matplotlib
        # Create figure, add suptitle with description
        plotFig = Figure(figsize=(12, 7))
        plotFig.suptitle('Original Signal - Time, FFT Magnitude, & Spectrogram Plots',
                         fontsize=12, fontweight='bold')

        # Add subplot to figure in top position
        tPlot = plotFig.add_subplot(211)
        # Create time series plot
        tPlot.plot(seconds, original, 'r')
        # Set axes, x label & y label
        tPlot.axis('tight')
        tPlot.set_xlabel('Time (sec)')
        tPlot.set_ylabel('Amplitude')

        # Add subplot to figure in lower left position
        fPlot = plotFig.add_subplot(223)
        # Plot FFT magnitude
        fPlot.plot(freq, inputFFT, 'r')
        # Set axes, x label & ylabel
        fPlot.axis('tight')
        fPlot.set_xlabel('Frequency (Hz)')
        fPlot.set_ylabel('Magnitude')

        # Add subplot to figure in lower right position
        specPlot = plotFig.add_subplot(224)
        # Plot spectrogram using matplotlib specgram method
        specPlot.specgram(original, NFFT=nfft, Fs=sampFreq)

        # Create new attribute containing generated figure
        self.origFig = plotFig

    def plotOutput(self):
        """
        The plotOutput method will generate a figure using
        matplotlib that contains 3 visualizations of the current output
        data: data as function of time in seconds, FFT magnitude as
        function of frequency in hertz, and spectrogram.
    
        The figure is stored in an attribute called outFig.
        """

        # Assign attributes to variables for ease of use
        output = self.output
        outLen = len(output)
        sampFreq = self.sampFreq

        # Calculate output data length in seconds
        seconds = arange(0, float(outLen) / sampFreq, 1.0 / sampFreq)
        # Calculate FFT magnitude of output
        freq, outputFFT, nfft = fftPlot(output, sampFreq)

        # Create plots using matplotlib
        # Create figure, add suptitle with description
        plotFig = Figure(figsize=(12, 7))
        plotFig.suptitle('Processed Signal - Time, FFT Magnitude, & Spectrogram Plots',
                         fontsize=12, fontweight='bold')

        # Add subplot to figure in top position
        tPlot = plotFig.add_subplot(211)
        # Create time series plot
        tPlot.plot(seconds, output, 'b')
        # Set axes, x label & y label
        tPlot.axis('tight')
        tPlot.set_xlabel('Time (sec)')
        tPlot.set_ylabel('Amplitude')

        # Add subplot to figure in lower left position
        fPlot = plotFig.add_subplot(223)
        # Plot FFT magnitude
        fPlot.plot(freq, outputFFT, 'b')
        # Set axes, x label & ylabel
        fPlot.axis('tight')
        fPlot.set_xlabel('Frequency (Hz)')
        fPlot.set_ylabel('Magnitude')

        # Add subplot to figure in lower right position
        specPlot = plotFig.add_subplot(224)
        # Plot spectrogram using matplotlib specgram method
        specPlot.specgram(output, NFFT=nfft, Fs=sampFreq)

        # Create new attribute containing generated figure
        self.outFig = plotFig

    def plotOverlay(self):
        """
        The plotOverlay method will generate a figure using
        matplotlib that contains 2 visualizations that compare
        the original data and the current output data.
    
        The figure is stored in an attribute called overlayFig.
        """

        # Assign attributes to variables for ease of use
        original = self.original
        origLen = self.origLen
        output = self.output
        sampFreq = self.sampFreq

        # Calculate signal length in seconds
        seconds = arange(0, float(origLen) / sampFreq, 1.0 / sampFreq)
        # Calculate FFT magnitude of original data, output data
        freq, inputFFT, nfft = fftPlot(original, sampFreq)
        freq, outputFFT, nfft = fftPlot(output, sampFreq)

        # Create plots using matplotlib
        # Create figure, add suptitle with description
        plotFig = Figure(figsize=(12, 7))
        plotFig.suptitle('Original/Processed Overlay - Time & FFT Magnitude Plots',
                         fontsize=12, fontweight='bold')

        # Add subplot to figure in top position
        tPlot = plotFig.add_subplot(211)
        # Create time series plots for original data and output data
        # on single subplot using matplotlib hold method
        tPlot.plot(seconds, output, 'b')  # Plot output in blue
        tPlot.hold('on')
        tPlot.plot(seconds, original, 'r')  # Plot original in red
        # Set axes, x label & y label
        tPlot.axis('tight')
        tPlot.set_xlabel('Time (sec)')
        tPlot.set_ylabel('Amplitude')
        tPlot.hold('off')

        # Add subplot to figure in bottom position
        fPlot = plotFig.add_subplot(212)
        # Create FFT magnitude plots for original data and output data
        # on single subplot using matplotlib hold method
        fPlot.plot(freq, outputFFT, 'b')  # Plot output in blue
        fPlot.hold('on')  # Create plots using matplotlib
        # Create figure, add suptitle with description
        fPlot.plot(freq, inputFFT, 'r')  # Plot original in red
        # Set axes, x label & y label
        fPlot.axis('tight')
        fPlot.set_xlabel('Frequency (Hz)')
        fPlot.set_ylabel('Magnitude')
        fPlot.hold('off')
        # Add legend to bottom subplot
        fPlot.legend(('Processed', 'Original'), loc=0)

        # Create new attribute containing generated figure
        self.overlayFig = plotFig

    def delay(self, delayinsec, gain):
        """
        The delay method implements a simple delay (echo) algorithm.
        The method takes two input parameters of type float: the delay
        time in seconds and the delay gain.
    
        Input parameters:
          delayinsec
            Type: float
            Description: the delay time in seconds
          gain
            Type: float
            Description: the delay gain
    
        Example usage:
        # Read 'austin.wav' and apply a delay effect
        # with 0.5 second delay and 0.75 delay gain
        audio = Audio('austin.wav')
        audio.delay(0.5, 0.75)
    
        """

        # Assign attributes to variables for ease of use
        input = self.input
        output = self.output
        original = self.original
        inputLength = self.origLen
        sampFreq = self.sampFreq

        # Ensure input array shape matches original array shape
        input.shape = original.shape

        # Hold current input in case of undo
        self.inputHold = input

        # Initialize output array
        output = zeros(input.shape)

        # Convert delay time in seconds to samples
        # Type-cast as int (value used for array indexing)
        R = int(round(delayinsec * sampFreq))

        # Implement delay algorithm
        output[0:R + 1] = input[0:R + 1]
        output[R + 1:inputLength] = input[R + 1:inputLength] + gain * input[1:inputLength - R]

        # Ensure correct output array size
        output.shape = original.shape

        # Reset output
        self.output = output

        # Hold output in case of undo
        self.outputHold = output

        # Reset input for next effect
        self.input = output

    def modulation(self, modDepth, modFreq):
        """
        The modulation method implements a simple modulation (vibrato)
        algorithm. The method takes two input parameters of type float:
        the modulation depth and the modulation frequency.
    
        Input parameters:
          modDepth
            Type: float
            Description: modulation depth
          modFreq
            Type: float
            Description: modulation frequency
    
        Example usage:
        # Read in 'austin.wav' and apply modulation
        # with 0.05 modulation depth and 0.1 Hz modulation frequency
        audio = Audio('austin.wav')
        audio.modulation(0.05, 0.1)
    
        """

        # Assign attributes to variables for ease of use
        input = self.input
        output = self.output
        original = self.original
        inputLength = self.origLen
        sampFreq = self.sampFreq

        # Hold current input in case of undo
        self.inputHold = input

        # Initialize output array
        output = zeros(input.shape)

        # Resize input
        input.shape = original.shape
        # Basic delay of input sample in seconds
        delay = modDepth
        # Basic delay converted from samples to seconds
        delay = round(delay * sampFreq)
        # Modulation modDepth in samples
        modDepth = round(modDepth * sampFreq)
        # Modulation frequency in samples
        modFreq = modFreq / sampFreq
        # Length of input in samples
        # inputLength = len(input);
        # Length of entire delay in samples
        dLen = 2 + delay + modDepth * 2
        # Initialize delay line array
        delayLine = zeros(input.shape)
        # Initialize output array
        output = zeros(input.shape)

        # Implement modulation algorithm
        for n in range(inputLength):
            m = modFreq;
            mod = sin(m * 2 * pi * n)
            tap = 1 + delay + modDepth * mod
            i = floor(tap)
            frac = tap - i
            delayLine = append(input[n], delayLine[0:dLen])
            output[n] = delayLine[i + 1] * frac + delayLine[i] * (1 - frac)

        # Ensure correct output array size
        output.shape = original.shape

        # Reset output
        self.output = output

        # Hold current output in case of undo
        self.outputHold = output

        # Reset input for next effect
        self.input = output

    def reverb(self):
        """
        The reverb method implements a simple Schroedinger reverberation
        algorithm.
    
        Example usage:
        # Read in 'austin.wav' and apply a reverb effect
        audio = Audio('austin.wav')
        audio.reverb()
        """
        # Assign attributes to variables for ease of use
        input = self.input
        output = self.output
        original = self.original
        inputLength = self.origLen
        sampFreq = self.sampFreq

        # Ensure input array shape matches original array shape
        input.shape = original.shape

        # Hold current input in case of undo
        self.inputHold = input

        # Initialize output array
        output = zeros(input.shape)

        # Initialize filter coefficients
        a = array([0.6, 0.4, 0.2, 0.1, 0.7, 0.6, 0.8])
        R = array([700, 900, 600, 400, 450, 390])

        # Implement reverb algorithm
        num1 = append(0, zeros(R[0] - 1));
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

        # Reset output
        self.output = output

        # Hold current output in case of undo
        outputHold = output

        # Reset input for next effect
        self.input = output

    def normalize(self):
        """
        The normalize method normalizes the current input data.
    
        Example usage:
        # Read in 'austin.flac' and normalize
        audio = Audio('austin.flac')
        audio.normalize()
    
        """
        # Assign attributes to variables for ease of use
        input = self.input
        output = self.output
        original = self.original
        inputLength = self.origLen
        sampFreq = self.sampFreq

        # Ensure input array shape matches original array shape
        input.shape = original.shape

        # Hold current input in case of undo
        self.inputHold = input

        # Initialize output array
        output = zeros(input.shape)

        # Implement normalization
        output = input / abs(input).max()

        # Ensure correct output array size
        output.shape = original.shape

        # Reset output
        self.output = output

        # Hold current output in case of undo
        self.outputHold = output

        # Reset input for next effect
        self.input = output

    def undo(self):
        """
        The undo method undoes the last effect processed and resets
        the current input and output data accordingly.
        """
        # Replace current input with temporary input
        self.input = self.inputHold
        # Replace current output with current input
        self.output = self.input
        # Ensure current output is correct size
        self.output.shape = self.original.shape
