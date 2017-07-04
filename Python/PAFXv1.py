
#!/usr/bin/env python

###################################################################
# Modules
###################################################################
# GUI Modules
from tkinter import *
# import tkFont
# import Pmw
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
# Declare function called by Read Button (readFrame)
def read():
  # Import required global variables
  global sampFreq
  global enctype
  global form
  global original
  global origLen
  global input
  global output

  # Get filename string from inputEntry Entry widget
  filename = inputEntry.get()

  # Perform read operation based on file extension
  # Read data, sampling frequency, encoding type
  # using Scikits Audiolab methods
  # .aiff specific
  if filename[-4:] == 'aiff':
    original, sampFreq, enctype = aiffread(filename)
    bottomLabel.config(text= filename + ' successfully read!',
                       anchor=CENTER, fg = 'black')
  # .flac specific
  elif filename[-4:] == 'flac':
    original, sampFreq, enctype = flacread(filename)
    bottomLabel.config(text= filename + ' successfully read!',
                       anchor=CENTER, fg='black')
  # .wav specific
  elif filename[-3:] == 'wav':
    original, sampFreq, enctype = wavread(filename)
    bottomLabel.config(text= filename + ' successfully read!',
                       anchor=CENTER, fg='black')
  # If none of the above hold true, display error on bottom line
  else:
    bottomLabel.config(text='Invalid filename!', fg='red',
                       anchor=CENTER)

  # Extract file format from read file
  f = Sndfile(inputEntry.get(), 'r')
  form = f.file_format

  # Make copy of read data to be used as input
  input = original.copy()
  # Set current output equal to input
  output = input
  # Determine file format

  # Get length of read data
  origLen = len(original)

  # Display sampling frequency and encoding type
  # in appropriate Label widgets
  Label(readFrame, text=str(sampFreq)).grid(row=0,column=5,pady=1)
  Label(writeFrame, text=str(sampFreq)).grid(row=0,column=5,pady=1)
  Label(readFrame, text=form).grid(row=0,column=7,pady=1)
  Label(readFrame,text=enctype).grid(row=0,column=9,pady=1)

  # Activate appropriate Buttons and Entry
  playInput.config(state=NORMAL)      # Input play button
  outputButton.config(state=NORMAL)   # Output play button
  plotInputButton.config(state=NORMAL)# Plot input button
  outputEntry.config(state=NORMAL)    # Write Filename Entry
  delayButton.config(state=NORMAL)    # Perform Delay Button
  modButton.config(state=NORMAL)      # Perform Modulation Button
  reverbButton.config(state=NORMAL)   # Perform Reverb Button
  normButton.config(state=NORMAL)     # Perform Normalization Button

# Declare function called by Write Button (writeFrame)
def write():
  # Import required global variables
  global encOpt
  global sampFreq
  global output

  # Get filename from Write Filename Entry in writeFrame
  filename = outputEntry.get()
  # Get file format and encoding from Pmw option widgets in writeFrame
  fmt = Format(formatOpt.getvalue(), encOpt.getvalue())

  # Write file using scikits audiolab methods
  outfile = Sndfile(filename, 'w', fmt, 1, sampFreq)
  outfile.write_frames(output)

# Declare function to perform delay (echo) effect
# called by Process Button (delayGroup)
def delay():
  # Import required global variables
  global input
  global inputHold
  global output
  global outputHold
  global sampFreq

  # Activate Undo Button
  undoButton.config(state=NORMAL)
  # Activate plotOutputButton
  plotOutputButton.config(state=NORMAL)
  # Activate plotOverlayButton
  plotOverlayButton.config(state=NORMAL)
  # Activate playOutput button
  playOutput.config(state=NORMAL)

  # Before implementing delay, hold current input in case of undo
  inputHold = input

  # Get required parameters from Scale widgets
  delayinsec = delayTimeScale.get();
  gain = gainScale.get();

  # Ensure correct input size
  input.shape=original.shape
  # Get input length in samples
  inputLength = len(input)
  # Initialize output array
  output = zeros(input.shape)

  # Convert delay time in seconds to samples
  # Type-cast as int (value used for array indexing)
  R = int(round(delayinsec*sampFreq))

  # Implement delay algorithm
  output[0:R+1] = input[0:R+1]
  output[R+1:inputLength] = input[R+1:inputLength]  + gain*input[1:inputLength-R]

  # Ensure correct output array size
  output.shape = original.shape

  # Hold output in case of undo
  outputHold = output

  # Reset input for next effect
  input = output

# Declare function to perform modulation effect
# called by Process Button (modGroup)
def modulation():
  # Import required global variables
  global input
  global inputHold
  global output
  global outputHold
  global sampFreq

  # Activate Undo Button
  undoButton.config(state=NORMAL)
  # Activate plotOutputButton
  plotOutputButton.config(state=NORMAL)
  # Activate plotOverlayButton
  plotOverlayButton.config(state=NORMAL)
  # Activate playOutput button
  playOutput.config(state=NORMAL)

  # Before implementing modulation, hold current input in
  # case of undo
  inputHold = input

  # Get required parameters from Scale widgets
  modDepth = modDepthScale.get();
  modFreq = modFreqScale.get();

  # Resize input
  input.shape=original.shape
  # Basic delay of input sample in seconds
  delay = modDepth
  # Basic delay converted from samples to seconds
  delay = round(delay*sampFreq)
  # Modulation modDepth in samples
  modDepth = round(modDepth*sampFreq)
  # Modulation frequency in samples
  modFreq = modFreq/sampFreq
  # Length of input in samples
  inputLength = len(input);
  # Length of entire delay in samples
  dLen = 2 + delay + modDepth * 2
  # Initialize delay line array
  delayLine = zeros(input.shape)
  # Initialize output array
  output = zeros(input.shape)

  # Implement modulation algorithm
  for n in range(inputLength):
      m = modFreq;
      mod = sin(m*2*pi*n)
      tap = 1+delay+modDepth*mod
      i = floor(tap)
      frac = tap - i
      delayLine = append(input[n], delayLine[0:dLen])
      output[n] = delayLine[i+1]*frac + delayLine[i] * (1-frac)

  # Ensure correct output array size
  output.shape=original.shape

  # Hold current output in case of undo
  outputHold = output

  # Reset input for next effect
  input = output

# Declare function to perform reverb effect
# called by Process Button (reverbGroup)
def reverb():
  # Import required global variables
  global input
  global inputHold
  global output
  global outputHold
  global sampFreq

  # Activate Undo Button
  undoButton.config(state=NORMAL)
  # Activate plotOutputButton
  plotOutputButton.config(state=NORMAL)
  # Activate plotOverlayButton
  plotOverlayButton.config(state=NORMAL)
  # Activate playOutput button
  playOutput.config(state=NORMAL)

  # Before implementing reverb, hold current input in
  # case of undo
  inputHold = input

  # Ensure correct input size
  input.shape=original.shape
  # Get input length in samples
  inputLength = len(input)
  # Initialize output array
  output = zeros(input.shape)

  # Initialize filter coefficients
  a = array([0.6, 0.4, 0.2, 0.1, 0.7, 0.6, 0.8])
  R = array([700, 900, 600, 400, 450, 390])

  # Implement reverb algorithm
  num1 = append(0, zeros(R[0]-1)); num1 = append(num1, 1);
  den1 = append(1, zeros(R[0]-1)); den1 = append(den1, -a[0]);
  d1 = lfilter(num1, den1, input)
  num2 = append(0, zeros(R[1]-1)); num2 = append(num2, 1);
  den2 = append(1, zeros(R[1]-1)); den2 = append(den2, -a[1]);
  d2 = lfilter(num2, den2, input)
  num3 = append(0, zeros(R[2]-1)); num3 = append(num3, 1);
  den3 = append(1, zeros(R[2]-1)); den3 = append(den3, -a[2]);
  d3 = lfilter(num3, den3, input)
  num4 = append(0, zeros(R[3]-1)); num4 = append(num4, 1);
  den4 = append(1, zeros(R[3]-1)); den4 = append(den4, -a[3]);
  d4 = lfilter(num4, den4, input)
  d = d1 + d2 + d3 + d4
  num5 = append(a[4], zeros(R[4]-1)); num5 = append(num5, 1);
  den5 = append(1, zeros(R[4]-1)); den5 = append(den5, a[4]);
  d = lfilter(num5, den5, d)
  num6 = append(a[5], zeros(R[5]-1)); num6 = append(num6, 1);
  den6 = append(1, zeros(R[5]-1)); den6 = append(den6, a[5]);
  d = lfilter(num6, den6, d)
  output = input + a[6]*d;
  # Clip amplitude to minimize distortion
  output *= 0.45

  # Ensure correct output array size
  output.shape=original.shape

  # Hold current output in case of undo
  outputHold = output

  # Reset input for next effect
  input = output

# Declare function to perform normalization
# called by Process Button (normGroup)
def normalize():
  # Import required global variables
  global input
  global inputHold
  global output
  global outputHold

  # Activate Undo Button
  undoButton.config(state=NORMAL)
  # Activate plotOutputButton
  plotOutputButton.config(state=NORMAL)
  # Activate plotOverlayButton
  plotOverlayButton.config(state=NORMAL)
  # Activate playOutput button
  playOutput.config(state=NORMAL)

  # Before implementing reverb, hold current input in
  # case of undo
  inputHold = input

  # Ensure correct input size
  input.shape=original.shape
  # Get input length in samples
  inputLength = len(input)

  # Implement normalization
  output = input/abs(input).max()

  # Ensure correct output array size
  output.shape=original.shape

  # Hold current output in case of undo
  outputHold = output

  # Reset input for next effect
  input = output

# Declare function called by Play Button (readFrame)
# Function plays original file
def inputPlayer():
  # Import required global variables
  global original
  global sampFreq

  # Play data using Scikits Audiolab method
  play(original, sampFreq)

# Declare function called by Play Button (writeFrame)
# Function plays current output file
def outputPlayer():
  # Import required global variables
  global output
  global sampFreq

  # Play output data using Scikits Audiolab method
  play(output, sampFreq)

# Declareunction called by Undo Button (writeFrame)
# Function undoes last effect processed
def undo():
  # Import required global variables
  global input
  global inputHold
  global output
  global outputHold

  # Reset input to help input
  input = inputHold
  # Reset output to new input
  output = input
  output.shape = original.shape

# Function called in fftPlot
# Calculates number equal to next power of 2 of input
# Analogous to MATLAB function of same name
def nextpow2(i):
  n = 2
  while n < i: n = n*2
  return n

# Function that calculates the NFFT-length FFT
# of the input data, NFFT is equal to the next power
# of 2 of the length of the input data,
# also returns frequency data (x-axis) to be used for plotting
def fftPlot(x, fs):
  # Get length of data
  L = len(x)
  # Calculate optimal length of FFT using nextpow2
  NFFT = 2^nextpow2(L)
  # Calculate fft using Numpy FFT method
  INPUT = numpy.fft.fft(x, NFFT)/L
  # Create frequency (x) axis data for plotting
  fAxis = fs/2 * linspace(0, 1, NFFT/2 + 1)
  # Calculate magnitude response from FFT data
  mAxis = 2*abs(INPUT[0:NFFT/2 + 1])
  # Return frequency axis data, magnitude response, and FFT length
  return fAxis, mAxis, NFFT

# Function that adds Save Figure options and Close Button to
# TopLevel widget created by any of 3 plot buttons
def saveFigure():
  # Import required global variables
  global plotWin
  global plotFig

  # Create Pmw Group To Hold Options
  printOptions = Pmw.Group(plotWin, tag_text='Print Options',
                           tag_font=Font)
  # Add Group to plotWin grid
  printOptions.grid(row=1, column=0, pady = 3)

  # Create figure Filename Label Widget
  # Add to printOptions grid
  Label(printOptions.interior(), text=' Filename: ', font=Font).grid(
    row=0,column=0,pady=1)

  # Create figure Filename Entry Widget
  printEntry = Entry(printOptions.interior())
  # Add to printOptions grid
  printEntry.grid(row=0, column=1,pady=1)

  # Create File Format Label Widget
  # Add to printOptions grid
  Label(printOptions.interior(), text='   Format: ', font=Font).grid(
    row=0,column=2,pady=1)

  # Create File Format Option Menu (Pmw mega)widget
  saveOpt = Pmw.OptionMenu(printOptions.interior(),
                             items = ['png', 'pdf', 'ps', 'eps', 'svg'],
                             menubutton_width=8)
  # Add to printOptions grid
  saveOpt.grid(row=0,column=3,pady=1)

  # Declare function called by Save Button (printOptions.interior)
  # Calls matplotlib save figure method, gets file format from
  # File Format Option Menu widget, saveOpt
  def saveFig():
    plotFig.savefig(printEntry.get(), dpi=None, facecolor='w', edgecolor='w',
            orientation='portrait', papertype=None,
            format=saveOpt.getvalue(), transparent=False,
            bbox_inches=None, pad_inches=0.1)

  # Create Save Button Widget
  saveButton = Button(printOptions.interior(),text = 'Save',font=Font,
                      width=8, command=saveFig)
  # Add to printOptions grid
  saveButton.grid(row=0,column=4,pady=1)

  # Create spacing Label Widget (aesthetic)
  Label(printOptions.interior(), text=' ').grid(row=0,column=5)

  # Create button that closes plotWin
  # Add to plotWin grid below Print Options group
  Button(plotWin, text='Close', font=Font,
         command = plotWin.destroy, width = 20
        ).grid(row=2,column=0,pady=2)

# Declare function called by Plot Input Button (bottomFrame)
# Function plots original audio data time series,
# FFT magnitude, and spectrogram using matplotlib
def plotInput():
  # Import required global variables
  global original
  global origLen
  global sampFreq
  global plotWin
  global plotFig

  # Create new TopLevel window to display plots & print options
  # Set TopLevel title to be displayed
  # Declare font to be consistent with GUI theme
  plotWin = Toplevel()
  plotWin.title('Python Audio Effects - Plot Window')
  Font = tkFont.Font(size=8, weight=tkFont.BOLD)

  # Calculate original data length in seconds
  seconds = arange(0,float(origLen)/sampFreq, 1.0/sampFreq)
  # Calculate FFT magnitude of original data
  freq, inputFFT, nfft = fftPlot(original, sampFreq)

  # Create plots using matplotlib
  # Create figure, add suptitle with description
  plotFig = Figure(figsize=(12,7))
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

  # Create TK Figure Canvas to display on plotWin TopLevel window
  # Show it
  # Add to plotWin grid
  plot = FigureCanvasTkAgg(plotFig, master=plotWin)
  plot.show()
  plot.get_tk_widget().grid(row=0, column=0)

  # Call saveFigure function to add print options and close button
  saveFigure()

# Declare function called by Plot Output Button
# Function plots current output audio data time series,
# FFT magnitude, and spectrogram using matplotlib
def plotOutput():
  # Import required global variables
  global original
  global output
  global sampFreq
  global plotWin
  global plotFig

  # Create new TopLevel window to display plots & print options
  # Set TopLevel title to be displayed
  # Declare font to be consistent with GUI theme
  plotWin = Toplevel()
  plotWin.title('PyFX - Plot Window')
  Font = tkFont.Font(size=8, weight=tkFont.BOLD)

  # Ensure data size is consistent to original data shape
  output.shape=original.shape
  # Calculate length of output data
  outLen = len(output)

  # Calculate output data length in seconds
  seconds = arange(0,float(outLen)/sampFreq, 1.0/sampFreq)
  # Calculate FFT magnitude of output
  freq, outputFFT, nfft = fftPlot(output, sampFreq)

  # Create plots using matplotlib
  # Create figure, add suptitle with description
  plotFig = Figure(figsize=(12,7))
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

  # Create TK Figure Canvas to display on plotWin TopLevel window
  # Show it
  # Add to plotWin grid
  plot = FigureCanvasTkAgg(plotFig, master=plotWin)
  plot.show()
  plot.get_tk_widget().grid(row=0, column=0)

  # Call saveFigure function to add print options and close button
  saveFigure()

# Declare function called by Plot Overlay Button
# Function plots original audio data and current output data
# time series and FFT magnitudes atop one another for comparison
def plotOverlay():
  # Import required global variables
  global original
  global origLen
  global output
  global sampFreq
  global plotWin
  global plotFig

  # Create new TopLevel window to display plots & print options
  # Set TopLevel title to be displayed
  # Declare font to be consistent with GUI theme
  plotWin = Toplevel()
  plotWin.title('PyFX - Plot Window')
  Font = tkFont.Font(size=8, weight=tkFont.BOLD)

  # Ensure data size is consistent to original data shape
  output.shape=original.shape
  # Calculate length of output data
  outLen = len(output)

  # Calculate signal length in seconds
  seconds = arange(0,float(origLen)/sampFreq, 1.0/sampFreq)
  # Calculate FFT magnitude of original data, output data
  freq, inputFFT, nfft = fftPlot(original,sampFreq)
  freq, outputFFT, nfft = fftPlot(output, sampFreq)

  # Create plots using matplotlib
  # Create figure, add suptitle with description
  plotFig = Figure(figsize=(12,7))
  plotFig.suptitle('Original/Processed Overlay - Time & FFT Magnitude Plots',
                   fontsize=12, fontweight='bold')

  # Add subplot to figure in top position
  tPlot = plotFig.add_subplot(211)
  # Create time series plots for original data and output data
  # on single subplot using matplotlib hold method
  tPlot.plot(seconds, output, 'b')  # Plot output in blue
  tPlot.hold('on')
  tPlot.plot(seconds, original, 'r')# Plot original in red
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
  fPlot.plot(freq, inputFFT, 'r') # Plot original in red
  # Set axes, x label & y label
  fPlot.axis('tight')
  fPlot.set_xlabel('Frequency (Hz)')
  fPlot.set_ylabel('Magnitude')
  fPlot.hold('off')
  # Add legend to bottom subplot
  fPlot.legend(('Processed', 'Original'), loc=0)

  # Create TK Figure Canvas to display on plotWin TopLevel window
  # Show it
  # Add to plotWin grid
  plot = FigureCanvasTkAgg(plotFig, master=plotWin)
  plot.show()
  plot.get_tk_widget().grid(row=0, column=0)

  # Call saveFigure function to add print options and close button
  saveFigure()

# Declare function called by Format Option Widget (writeFrame)
# Controls items in Encoding Option Widget based on chosen Format
def encOptionCreator(format):
  # Import required global variables
  global encOpt

  # Get format from Pmw Option Menu (formatOpt)
  format = formatOpt.getvalue()
  # Create blank list to hold items
  itemList = []
  # Populate item list from Scikits Audiolab
  # available_encodings attribute
  for enc in available_encodings(format):
    itemList.append(enc)

  # Create Pmw Option Menu with encoding types
  encOpt = Pmw.OptionMenu(writeFrame,
                          items = itemList,
                          menubutton_width=5)
  # Add to encOpt grid
  encOpt.grid(row=0, column=9, pady=1)

# Declare function called by Quit Button (bottomFrame)
# Function closes GUI window
def terminate():
  sys.exit(0)
####################################################################


#####################################################################
# Create root (main) window.
#####################################################################
root = Tk()
# Put title on window
root.title('Python Audio Effects - Main')
#####################################################################

#####################################################################
# Build GUI
#####################################################################
# Set default font for GUI
Font = tkFont.Font(size=8, weight=tkFont.BOLD)

# Create frames to be placed on root window
# and add to root window grid

# Create Read File frame
readFrame = Frame(root, bd=5, relief=GROOVE)
readFrame.grid(row=0,column=0,sticky=W+E)
# Create Write File frame
writeFrame = Frame(root, bd=5, relief=GROOVE)
writeFrame.grid(row=1,column=0,sticky=W+E)
# Create Effects frame
effectsFrame = Frame(root)
effectsFrame.grid(row=2,column=0)
# Create Bottom frame
bottomFrame = Frame(root, bg='gray')
bottomFrame.grid(row=3,column=0,sticky=W+E)

# -----------------------------------------------------------------
# Populate Read File Frame (readFrame)
# Read File Frame functions:
# Get filename, read file, play read data,
# display read data sampling frequency, format, and encoding type
# All widgets will be placed on grid in a single row

# Create Filename Label widget
Label(readFrame,text="Filename: ", width=8,
      font=Font).grid(row=0,column=0,pady=1)

# Create Filename (To Be Read) Entry widget
inputEntry = Entry(readFrame, width = 24,
                   font=tkFont.Font(size=12),
                   justify = 'center')
inputEntry.grid(row=0,column=1,padx=1,pady=1)

# Create File Read Button widget
inputButton = Button(readFrame, text="Read", command=read,
                     width = 8, font=Font)
inputButton.grid(row=0, column=2, pady=1)

# Create Play Read Data Button widget
playInput = Button(readFrame, width=8, text='Play', state=DISABLED,
                    font=Font, command=inputPlayer)
playInput.grid(row=0, column=3, padx=1, pady=1)

# Create 1st Sampling Frequency Label widget
fsLabel = Label(readFrame, text = "Fs (Hz): ", width=8,
                font=Font)
fsLabel.grid(row=0, column=4, pady = 1)

# Create 2nd Sampling Frequency Label widget
# This label will display sampling frequency when data is read
# (after File Read Button (inputButton) is pressed)
Label(readFrame, width=6).grid(row=0,column=5,padx=1,pady=1)

# Create 1st File Format Label widget
formLabel = Label(readFrame, text='Format: ', width=8,
                  font=Font)
formLabel.grid(row=0, column=6, pady = 1)

# Create 2nd File Format Label widget
# This label will display file format when data is read
# (after File Read Button (inputButton) is pressed)
Label(readFrame, width=8).grid(row=0,column=7,padx=1,pady=1)

# Create 1st Encoding Type Label widget
encLabel = Label(readFrame, text = "Enc: ", width=8,
                font=Font)
encLabel.grid(row=0, column=8, pady=1)

# Create 2nd Encoding Type Label widget
# This label will display encoding type when data is read
# (after File Read Button (inputButton) is pressed)
Label(readFrame, width=8).grid(row=0,column=9,padx=1,pady=1)
# -----------------------------------------------------------------

# -----------------------------------------------------------------
# Populate Write File Frame (writeFrame)
# Write File Frame functions:
# Input filename to be written, write file, play current output,
# display current output sampling frequency, choose file's
# file format and encoding type
# All widgets will be placed on grid in a single row

# Create Filename Label widget
Label(writeFrame,text="Filename: ", width=8,\
      font=Font).\
      grid(row=0,column=0,padx=1,pady=1)

# Create Filename (To Be Written) Entry widget
outputEntry = Entry(writeFrame, width = 24,
                   font=tkFont.Font(size=12),
                   justify = 'center', state=DISABLED)
outputEntry.grid(row=0,column=1,padx=1,pady=1)

# Create File Write Button widget
outputButton = Button(writeFrame, text="Write", command=write,
                     width = 8, font=Font, state=DISABLED)
outputButton.grid(row=0,column=2, pady=1)

# Create Play Current Output Button widget
playOutput = Button(writeFrame, width=8, text='Play', state=DISABLED,
                    font=Font,
                    command=outputPlayer)
playOutput.grid(row=0,column=3, padx=1, pady=1)

# Create 1st Sampling Frequency Label widget
fsLabel2 = Label(writeFrame, text = "Fs (Hz): ", width=8,
                font=Font)
fsLabel2.grid(row=0, column=4, pady=1)

# Create 2nd Sampling Frequency Label widget
# This label will display sampling frequency when data is read
# (after File Read Button (inputButton) is pressed)
Label(writeFrame, width=6).grid(row=0,column=5,padx=1,pady=1)

# Create File Format Label widget
Label(writeFrame, text='Format: ', font=Font).grid(row=0,column=6,pady=1)

# Create File Format Option Menu (Pmw Mega)Widget
# 3 Options: .aiff, .flac, .wav
formatOpt = Pmw.OptionMenu(writeFrame,
                          items = ['aiff', 'flac', 'wav'],
                          command = encOptionCreator,
                          menubutton_width=5)
formatOpt.grid(row=0, column=7, pady=1)

# Create Encoding Type Label widget
Label(writeFrame, text='Enc: ', font=Font).grid(row=0,column=8,pady=1)

# Create Encoding Type Option Menu (Pmw Mega)Widget Holder
# To be replaced once File Format is chosen
# as encoding type options are dependent on file format
# (See function encOptionCreator above)
encOptHold = Pmw.OptionMenu(writeFrame,
                            menubutton_width=5)
encOptHold.grid(row=0,column=9,pady=1)
# -----------------------------------------------------------------

# -----------------------------------------------------------------
# Populate Effects Frame (effectsFrame)
# Effects Frame functions:
# Hold four Pmw Group widgets that implement the 4 available
# audio effects: delay, modulation, reverb, normalization
# The 4 Group widgets will be held in a 2x2 grid

################
# Create and populate Delay Group (delayGroup)
# Group consists of two Scale widgets and a 'Process' Button widget
delayGroup = Pmw.Group(effectsFrame, tag_text='Delay', tag_font=Font)
delayGroup.grid(row=0,column=0,padx=1,pady=1)

# Create Scale widget that contols delay time
delayTimeScale = Scale(delayGroup.interior(), from_=0.0, to_=2.0, resolution=0.01, \
                       orient=HORIZONTAL, label='Delay Time (sec)', \
                       tickinterval=0.5, length=200,font=Font)

# Create Scale widget that controls delay gain
gainScale = Scale(delayGroup.interior(), from_=0.0, to_=1.0, resolution=0.01, \
                  orient=HORIZONTAL, label='Gain', tickinterval=0.5, \
                  length=200,font=Font)

# Create Button widget that implements Delay effect
delayButton = Button(delayGroup.interior(), command=delay, text='Process', \
                    width=55,font=Font, state=DISABLED)

# Place widgets on grid within Delay Group
delayTimeScale.grid(row=0,column=0,padx=1,sticky=W)
gainScale.grid(row=0,column=1,padx=1,sticky=W)
delayButton.grid(row=1,column=0,columnspan=2, pady=1, padx=1)

################
# Create and populate Modulation Group (modGroup)
# Group consists of two Scale widgets and a 'Process' Button widget
modGroup = Pmw.Group(effectsFrame, tag_text='Modulation', tag_font=Font)
modGroup.grid(row=0,column=1,padx=1,pady=1)

# Create Scale widget that controls modulation depth
modDepthScale = Scale(modGroup.interior(), from_=0.0, to_=0.1, resolution=0.01, \
                       orient=HORIZONTAL, label='Modulation Depth', \
                       tickinterval=0.025, length=200,font=Font)

# Create Scale widget that controls modulation frequency
modFreqScale = Scale(modGroup.interior(), from_=0.0, to_=1.0, resolution=0.01, \
                  orient=HORIZONTAL, label='Modulation Frequency', tickinterval=0.25, \
                  length=200,font=Font)

# Create Button widget that implements Modulation effect
modButton = Button(modGroup.interior(), command=modulation, text='Process', \
                    width=55,font=Font, state=DISABLED)

# Place widgets on grid within Modulation Group
modDepthScale.grid(row=0,column=0,padx=1,sticky=W)
modFreqScale.grid(row=0,column=1,padx=1,sticky=W)
modButton.grid(row=1,column=0,columnspan=2, pady=1, padx=1)

################
# Create and populate Reverb Group (reverbGroup)
# Group consists of a 'Process' Button widget only
reverbGroup = Pmw.Group(effectsFrame, tag_text='Reverb', tag_font=Font)
reverbGroup.grid(row=1,column=0,padx=1,pady=1)

# Create Button widget that implements Reverb effect
reverbButton = Button(reverbGroup.interior(), command=reverb, text='Process', \
                    width=55,font=Font, state=DISABLED)
reverbButton.grid(row=0,column=0,columnspan=2, pady=1, padx=1)

################
# Create and populate Normalization Group (normGroup)
# Group consists of a 'Process Button widget only
normGroup = Pmw.Group(effectsFrame, tag_text='Normalization', tag_font=Font)
normGroup.grid(row=1,column=1,padx=1,pady=1)

# Create Button widget that implements Reverb effect
normButton = Button(normGroup.interior(), command=normalize, text='Process', \
                    width=55,font=Font, state=DISABLED)
normButton.grid(row=0,column=0,columnspan=2, pady=1, padx=1)
# -----------------------------------------------------------------

# -----------------------------------------------------------------
# Populate Bottom Frame (bottomFrame)
# Bottom Frame functions:
# Display messages, undo last process, plot original data,
# plot current output data, plot overlay, and quit
# All widgets will be placed on a grid in a single row

# Create Message Label widget
# Will change based on certain actions throughout GUI
bottomLabel = Label(bottomFrame, text=' Python Audio Effects GUI by Leon D\'Angio',
      font=Font, width=60, anchor=CENTER, bg='gray')

# Create Undo Button widget
undoButton = Button(bottomFrame,text='Undo',width=8,font=Font,
                    state=DISABLED,command=undo)

# Create separator between Undo and Plot Input Buttons
separator1 = Frame(bottomFrame, bd=5, relief=SUNKEN)

# Creat Plot Input Button widget
plotInputButton = Button(bottomFrame,text='Plot Input',width=8,
                    font=Font,state=DISABLED, command=plotInput)

# Create Plot Output Button widget
plotOutputButton = Button(bottomFrame,text='Plot Output', width=8,
                          font=Font, state=DISABLED, command=plotOutput)

# Create Plot Overlay Button widget
plotOverlayButton = Button(bottomFrame,text='Plot Overlay', width=8, font=Font,
                          state=DISABLED, command=plotOverlay)

# Create seperator between Plot Overlay and Quit Buttons
separator2 = Frame(bottomFrame, bd=5, relief=SUNKEN)

# Create Quit Button
quitButton = Button(bottomFrame,text='Quit',command=terminate,
                font=Font, width=8)

# Arrange widgets on bottomFrame grid in single row
bottomLabel.grid(row=0,column=0)
undoButton.grid(row=0,column=1,pady=1,padx=1)
separator1.grid(row=0,column=2,pady=1,padx=2)
plotInputButton.grid(row=0,column=3,pady=1,padx=1)
plotOutputButton.grid(row=0,column=4,pady=1,padx=1)
plotOverlayButton.grid(row=0,column=5,pady=1,padx=1)
separator2.grid(row=0,column=6,pady=1,padx=2)
quitButton.grid(row=0,column=7, padx=1, pady=1)
# -----------------------------------------------------------------

# End of GUI
root.mainloop()
