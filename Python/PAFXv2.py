#!/usr/bin/env python

###################################################################
# Dependencies
###################################################################
# The file Dependencies.py includes will import all of
# modules, functions, and classes neccessary for the GUI to
# run properly.
from AudioDependencies import *


##################################################################

#################################################################
# Functions
#################################################################
# Declare function called by Read Button (readFrame)
def read():
    # Import required global variables
    global audio

    # Get filename string from readEntry Entry widget
    filename = readEntry.get()

    # Instantiate object of type Audio
    audio = Audio(filename)

    # Display sampling frequency and encoding type
    # in appropriate Label widgets
    Label(readFrame, text=str(audio.sampFreq)).grid(row=0, column=5, pady=1)
    Label(writeFrame, text=str(audio.sampFreq)).grid(row=0, column=5, pady=1)
    Label(readFrame, text=audio.format).grid(row=0, column=7, pady=1)
    Label(readFrame, text=audio.enctype).grid(row=0, column=9, pady=1)

    # Activate appropriate Buttons and Entry
    playOriginal.config(state=NORMAL)  # Input play button
    outputButton.config(state=NORMAL)  # Output play button
    plotOriginalButton.config(state=NORMAL)  # Plot input button
    outputEntry.config(state=NORMAL)  # Write Filename Entry
    delayButton.config(state=NORMAL)  # Perform Delay Button
    modButton.config(state=NORMAL)  # Perform Modulation Button
    reverbButton.config(state=NORMAL)  # Perform Reverb Button
    normButton.config(state=NORMAL)  # Perform Normalization Button


# Declare function called by Write Button (writeFrame)
def write():
    # Import required global variables
    global audio

    # Write file using Audio write method
    audio.write(outputEntry.get(), formatOpt.getvalue(), encOpt.getvalue())


# Declare function to perform delay (echo) effect
# called by Process Button (delayGroup)
def delay():
    # Import required global variables
    global audio

    # Activate Undo Button
    undoButton.config(state=NORMAL)
    # Activate plotOutputButton
    plotOutputButton.config(state=NORMAL)
    # Activate plotOverlayButton
    plotOverlayButton.config(state=NORMAL)
    # Activate playOutput button
    playOutput.config(state=NORMAL)

    # Apply delay using Audio delay method
    audio.delay(delayTimeScale.get(), gainScale.get())


# Declare function to perform modulation effect
# called by Process Button (modGroup)
def modulation():
    # Import required global variables
    global audio

    # Activate Undo Button
    undoButton.config(state=NORMAL)
    # Activate plotOutputButton
    plotOutputButton.config(state=NORMAL)
    # Activate plotOverlayButton
    plotOverlayButton.config(state=NORMAL)
    # Activate playOutput button
    playOutput.config(state=NORMAL)

    # Apply modulation using Audio modulation method
    audio.modulation(modDepthScale.get(), modFreqScale.get())


# Declare function to perform reverb effect
# called by Process Button (reverbGroup)
def reverb():
    # Import required global variables
    global audio

    # Activate Undo Button
    undoButton.config(state=NORMAL)
    # Activate plotOutputButton
    plotOutputButton.config(state=NORMAL)
    # Activate plotOverlayButton
    plotOverlayButton.config(state=NORMAL)
    # Activate playOutput button
    playOutput.config(state=NORMAL)

    # Apply reverb using Audio reverb method
    audio.reverb()


# Declare function to perform normalization
# called by Process Button (normGroup)
def normalize():
    # Import required global variables
    global audio

    # Activate Undo Button
    undoButton.config(state=NORMAL)
    # Activate plotOutputButton
    plotOutputButton.config(state=NORMAL)
    # Activate plotOverlayButton
    plotOverlayButton.config(state=NORMAL)
    # Activate playOutput button
    playOutput.config(state=NORMAL)

    # Apply normalization using Audio normalize method
    audio.normalize()


# Declare function called by Play Button (readFrame)
# Function plays original file
def originalPlayer():
    # Import required global variables
    global audio

    # Play original data using Audio playOriginal method
    audio.playOriginal()


# Declare function called by Play Button (writeFrame)
# Function plays current output file
def outputPlayer():
    # Import required global variables
    global audio

    # Play current output data using Audio playOutput method
    audio.playOutput()


# Declareunction called by Undo Button (writeFrame)
# Function undoes last effect processed
def undo():
    # Import required global variables
    global audio

    # Undo last process using Audio undo method
    audio.undo()


# Function that adds Save Figure options and Close Button to
# TopLevel widget created by any of 3 plot buttons
def saveFigure(whichPlot):
    # Import required global variables
    global plotWin
    global audio
    global Font

    if whichPlot == 'input':
        plotFig = audio.origFig
    elif whichPlot == 'output':
        plotFig = audio.outFig
    elif whichPlot == 'overlay':
        plotFig = audio.overlayFig

    # Create Pmw Group To Hold Options
    printOptions = Pmw.Group(plotWin, tag_text='Print Options',
                             tag_font=Font)
    # Add Group to plotWin grid
    printOptions.grid(row=1, column=0, pady=3)

    # Create figure Filename Label Widget
    # Add to printOptions grid
    Label(printOptions.interior(), text=' Filename: ', font=Font).grid(
        row=0, column=0, pady=1)

    # Create figure Filename Entry Widget
    printEntry = Entry(printOptions.interior())
    # Add to printOptions grid
    printEntry.grid(row=0, column=1, pady=1)

    # Create File Format Label Widget
    # Add to printOptions grid
    Label(printOptions.interior(), text='   Format: ', font=Font).grid(
        row=0, column=2, pady=1)

    # Create File Format Option Menu (Pmw mega)widget
    saveOpt = Pmw.OptionMenu(printOptions.interior(),
                             items=['png', 'pdf', 'ps', 'eps', 'svg'],
                             menubutton_width=8)
    # Add to printOptions grid
    saveOpt.grid(row=0, column=3, pady=1)

    # Declare function called by Save Button (printOptions.interior)
    # Calls matplotlib save figure method, gets file format from
    # File Format Option Menu widget, saveOpt
    def saveFig():
        plotFig.savefig(printEntry.get(), dpi=None, facecolor='w',
                        edgecolor='w', orientation='portrait',
                        papertype=None, format=saveOpt.getvalue(),
                        transparent=False, bbox_inches=None,
                        pad_inches=0.1)

    # Create Save Button Widget
    saveButton = Button(printOptions.interior(), text='Save', font=Font,
                        width=8, command=saveFig)
    # Add to printOptions grid
    saveButton.grid(row=0, column=4, pady=1)

    # Create spacing Label Widget (aesthetic)
    Label(printOptions.interior(), text=' ').grid(row=0, column=5)

    # Create button that closes plotWin
    # Add to plotWin grid below Print Options group
    Button(plotWin, text='Close', font=Font,
           command=plotWin.destroy, width=20
           ).grid(row=2, column=0, pady=2)


# Declare function called by Plot Input Button (bottomFrame)
# Function plots original audio data time series,
# FFT magnitude, and spectrogram using matplotlib
def plotInput():
    # Import required global variables
    global audio
    global plotWin
    global Font

    # Create new TopLevel window to display plots & print options
    # Set TopLevel title to be displayed
    # Declare font to be consistent with GUI theme
    plotWin = Toplevel()
    plotWin.title('PyFX - Plot Window')

    # Plot original data using Audio plotOriginal method
    audio.plotOriginal()

    # Create TK Figure Canvas to display on plotWin TopLevel window
    # Show it
    # Add to plotWin grid
    plot = FigureCanvasTkAgg(audio.origFig, master=plotWin)
    plot.show()
    plot.get_tk_widget().grid(row=0, column=0)

    # Call saveFigure function to add print options and close button
    saveFigure('input')


# Declare function called by Plot Output Button
# Function plots current output audio data time series,
# FFT magnitude, and spectrogram using matplotlib
def plotOutput():
    # Import required global variables
    global audio
    global plotWin
    global Font

    # Create new TopLevel window to display plots & print options
    # Set TopLevel title to be displayed
    # Declare font to be consistent with GUI theme
    plotWin = Toplevel()
    plotWin.title('PyFX - Plot Window')

    # Plot output data using Audio plotOutput method
    audio.plotOutput()

    # Create TK Figure Canvas to display on plotWin TopLevel window
    # Show it
    # Add to plotWin grid
    plot = FigureCanvasTkAgg(audio.outFig, master=plotWin)
    plot.show()
    plot.get_tk_widget().grid(row=0, column=0)

    # Call saveFigure function to add print options and close button
    saveFigure('output')


# Declare function called by Plot Overlay Button
# Function plots original audio data and current output data
# time series and FFT magnitudes atop one another for comparison
def plotOverlay():
    # Import required global variables
    global audio
    global plotWin
    global Font

    # Create new TopLevel window to display plots & print options
    # Set TopLevel title to be displayed
    # Declare font to be consistent with GUI theme
    plotWin = Toplevel()
    plotWin.title('PyFX - Plot Window')

    # Create overlay plot using Audio plotOverlay method
    audio.plotOverlay()

    # Create TK Figure Canvas to display on plotWin TopLevel window
    # Show it
    # Add to plotWin grid
    plot = FigureCanvasTkAgg(audio.overlayFig, master=plotWin)
    plot.show()
    plot.get_tk_widget().grid(row=0, column=0)

    # Call saveFigure function to add print options and close button
    saveFigure('overlay')


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
                            items=itemList,
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
readFrame.grid(row=0, column=0, sticky=W + E)
# Create Write File frame
writeFrame = Frame(root, bd=5, relief=GROOVE)
writeFrame.grid(row=1, column=0, sticky=W + E)
# Create Effects frame
effectsFrame = Frame(root)
effectsFrame.grid(row=2, column=0)
# Create Bottom frame
bottomFrame = Frame(root, bg='gray')
bottomFrame.grid(row=3, column=0, sticky=W + E)

# -----------------------------------------------------------------
# Populate Read File Frame (readFrame)
# Read File Frame functions:
# Get filename, read file, play read data,
# display read data sampling frequency, format, and encoding type
# All widgets will be placed on grid in a single row

# Create Filename Label widget
Label(readFrame, text="Filename: ", width=8,
      font=Font).grid(row=0, column=0, pady=1)

# Create Filename (To Be Read) Entry widget
readEntry = Entry(readFrame, width=24,
                  font=tkFont.Font(size=12),
                  justify='center')
readEntry.grid(row=0, column=1, padx=1, pady=1)

# Create File Read Button widget
readButton = Button(readFrame, text="Read", command=read,
                    width=8, font=Font)
readButton.grid(row=0, column=2, pady=1)

# Create Play Read Data Button widget
playOriginal = Button(readFrame, width=8, text='Play', state=DISABLED,
                      font=Font, command=originalPlayer)
playOriginal.grid(row=0, column=3, padx=1, pady=1)

# Create 1st Sampling Frequency Label widget
fsLabel = Label(readFrame, text="Fs (Hz): ", width=8,
                font=Font)
fsLabel.grid(row=0, column=4, pady=1)

# Create 2nd Sampling Frequency Label widget
# This label will display sampling frequency when data is read
# (after File Read Button (readButton) is pressed)
Label(readFrame, width=6).grid(row=0, column=5, padx=1, pady=1)

# Create 1st File Format Label widget
formLabel = Label(readFrame, text='Format: ', width=8,
                  font=Font)
formLabel.grid(row=0, column=6, pady=1)

# Create 2nd File Format Label widget
# This label will display file format when data is read
# (after File Read Button (readButton) is pressed)
Label(readFrame, width=8).grid(row=0, column=7, padx=1, pady=1)

# Create 1st Encoding Type Label widget
encLabel = Label(readFrame, text="Enc: ", width=8,
                 font=Font)
encLabel.grid(row=0, column=8, pady=1)

# Create 2nd Encoding Type Label widget
# This label will display encoding type when data is read
# (after File Read Button (readButton) is pressed)
Label(readFrame, width=8).grid(row=0, column=9, padx=1, pady=1)
# -----------------------------------------------------------------

# -----------------------------------------------------------------
# Populate Write File Frame (writeFrame)
# Write File Frame functions:
# Input filename to be written, write file, play current output,
# display current output sampling frequency, choose file's
# file format and encoding type
# All widgets will be placed on grid in a single row

# Create Filename Label widget
Label(writeFrame, text="Filename: ", width=8, \
      font=Font). \
    grid(row=0, column=0, padx=1, pady=1)

# Create Filename (To Be Written) Entry widget
outputEntry = Entry(writeFrame, width=24,
                    font=tkFont.Font(size=12),
                    justify='center', state=DISABLED)
outputEntry.grid(row=0, column=1, padx=1, pady=1)

# Create File Write Button widget
outputButton = Button(writeFrame, text="Write", command=write,
                      width=8, font=Font, state=DISABLED)
outputButton.grid(row=0, column=2, pady=1)

# Create Play Current Output Button widget
playOutput = Button(writeFrame, width=8, text='Play', state=DISABLED,
                    font=Font,
                    command=outputPlayer)
playOutput.grid(row=0, column=3, padx=1, pady=1)

# Create 1st Sampling Frequency Label widget
fsLabel2 = Label(writeFrame, text="Fs (Hz): ", width=8,
                 font=Font)
fsLabel2.grid(row=0, column=4, pady=1)

# Create 2nd Sampling Frequency Label widget
# This label will display sampling frequency when data is read
# (after File Read Button (readButton) is pressed)
Label(writeFrame, width=6).grid(row=0, column=5, padx=1, pady=1)

# Create File Format Label widget
Label(writeFrame, text='Format: ', font=Font).grid(row=0, column=6, pady=1)

# Create File Format Option Menu (Pmw Mega)Widget
# 3 Options: .aiff, .flac, .wav
formatOpt = Pmw.OptionMenu(writeFrame,
                           items=['aiff', 'flac', 'wav'],
                           command=encOptionCreator,
                           menubutton_width=5)
formatOpt.grid(row=0, column=7, pady=1)

# Create Encoding Type Label widget
Label(writeFrame, text='Enc: ', font=Font).grid(row=0, column=8, pady=1)

# Create Encoding Type Option Menu (Pmw Mega)Widget Holder
# To be replaced once File Format is chosen
# as encoding type options are dependent on file format
# (See function encOptionCreator above)
encOptHold = Pmw.OptionMenu(writeFrame,
                            menubutton_width=5)
encOptHold.grid(row=0, column=9, pady=1)
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
delayGroup.grid(row=0, column=0, padx=1, pady=1)

# Create Scale widget that contols delay time
delayTimeScale = Scale(delayGroup.interior(), from_=0.0, to_=2.0, resolution=0.01, \
                       orient=HORIZONTAL, label='Delay Time (sec)', \
                       tickinterval=0.5, length=200, font=Font)

# Create Scale widget that controls delay gain
gainScale = Scale(delayGroup.interior(), from_=0.0, to_=1.0, resolution=0.01, \
                  orient=HORIZONTAL, label='Gain', tickinterval=0.5, \
                  length=200, font=Font)

# Create Button widget that implements Delay effect
delayButton = Button(delayGroup.interior(), command=delay, text='Process', \
                     width=55, font=Font, state=DISABLED)

# Place widgets on grid within Delay Group
delayTimeScale.grid(row=0, column=0, padx=1, sticky=W)
gainScale.grid(row=0, column=1, padx=1, sticky=W)
delayButton.grid(row=1, column=0, columnspan=2, pady=1, padx=1)

################
# Create and populate Modulation Group (modGroup)
# Group consists of two Scale widgets and a 'Process' Button widget
modGroup = Pmw.Group(effectsFrame, tag_text='Modulation', tag_font=Font)
modGroup.grid(row=0, column=1, padx=1, pady=1)

# Create Scale widget that controls modulation depth
modDepthScale = Scale(modGroup.interior(), from_=0.0, to_=0.1, resolution=0.01, \
                      orient=HORIZONTAL, label='Modulation Depth', \
                      tickinterval=0.025, length=200, font=Font)

# Create Scale widget that controls modulation frequency
modFreqScale = Scale(modGroup.interior(), from_=0.0, to_=1.0, resolution=0.01, \
                     orient=HORIZONTAL, label='Modulation Frequency', tickinterval=0.25, \
                     length=200, font=Font)

# Create Button widget that implements Modulation effect
modButton = Button(modGroup.interior(), command=modulation, text='Process', \
                   width=55, font=Font, state=DISABLED)

# Place widgets on grid within Modulation Group
modDepthScale.grid(row=0, column=0, padx=1, sticky=W)
modFreqScale.grid(row=0, column=1, padx=1, sticky=W)
modButton.grid(row=1, column=0, columnspan=2, pady=1, padx=1)

################
# Create and populate Reverb Group (reverbGroup)
# Group consists of a 'Process' Button widget only
reverbGroup = Pmw.Group(effectsFrame, tag_text='Reverb', tag_font=Font)
reverbGroup.grid(row=1, column=0, padx=1, pady=1)

# Create Button widget that implements Reverb effect
reverbButton = Button(reverbGroup.interior(), command=reverb, text='Process', \
                      width=55, font=Font, state=DISABLED)
reverbButton.grid(row=0, column=0, columnspan=2, pady=1, padx=1)

################
# Create and populate Normalization Group (normGroup)
# Group consists of a 'Process Button widget only
normGroup = Pmw.Group(effectsFrame, tag_text='Normalization', tag_font=Font)
normGroup.grid(row=1, column=1, padx=1, pady=1)

# Create Button widget that implements Reverb effect
normButton = Button(normGroup.interior(), command=normalize, text='Process', \
                    width=55, font=Font, state=DISABLED)
normButton.grid(row=0, column=0, columnspan=2, pady=1, padx=1)
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
undoButton = Button(bottomFrame, text='Undo', width=8, font=Font,
                    state=DISABLED, command=undo)

# Create separator between Undo and Plot Input Buttons
separator1 = Frame(bottomFrame, bd=5, relief=SUNKEN)

# Creat Plot Input Button widget
plotOriginalButton = Button(bottomFrame, text='Plot Input', width=8,
                            font=Font, state=DISABLED, command=plotInput)

# Create Plot Output Button widget
plotOutputButton = Button(bottomFrame, text='Plot Output', width=8,
                          font=Font, state=DISABLED, command=plotOutput)

# Create Plot Overlay Button widget
plotOverlayButton = Button(bottomFrame, text='Plot Overlay', width=8, font=Font,
                           state=DISABLED, command=plotOverlay)

# Create seperator between Plot Overlay and Quit Buttons
separator2 = Frame(bottomFrame, bd=5, relief=SUNKEN)

# Create Quit Button
quitButton = Button(bottomFrame, text='Quit', command=terminate,
                    font=Font, width=8)

# Arrange widgets on bottomFrame grid in single row
bottomLabel.grid(row=0, column=0)
undoButton.grid(row=0, column=1, pady=1, padx=1)
separator1.grid(row=0, column=2, pady=1, padx=2)
plotOriginalButton.grid(row=0, column=3, pady=1, padx=1)
plotOutputButton.grid(row=0, column=4, pady=1, padx=1)
plotOverlayButton.grid(row=0, column=5, pady=1, padx=1)
separator2.grid(row=0, column=6, pady=1, padx=2)
quitButton.grid(row=0, column=7, padx=1, pady=1)
# -----------------------------------------------------------------

# End of GUI
root.mainloop()