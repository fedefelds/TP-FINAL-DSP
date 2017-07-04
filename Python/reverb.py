# Declare function to perform reverb effect
# called by Process Button (reverbGroup)
from numpy import append
from numpy import zeros
from numpy import array
from scipy.signal import lfilter


def reverb():
    # Import required global variables
    global input
    global inputHold
    global output
    global outputHold
    global sampFreq

    # # Activate Undo Button
    # undoButton.config(state=NORMAL)
    # # Activate plotOutputButton
    # plotOutputButton.config(state=NORMAL)
    # # Activate plotOverlayButton
    # plotOverlayButton.config(state=NORMAL)
    # # Activate playOutput button
    # playOutput.config(state=NORMAL)

    # Before implementing reverb, hold current input in
    # case of undo
    inputHold = input



    # Reset input for next effect
    input = output
