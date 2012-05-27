######
## Should be loaded in the pylab environment: ipython -pylab
## Call: execfile("streams.py")

import os,sys,subprocess,string
from collections import OrderedDict
import openpyxl as xl                 # For writing/reading excel files

# First, define the central script directory and 
# location of gatex.exe and the streams.py functions
# CHANGE THIS TO THE LOCATION ON YOUR COMPUTER:
SCRIPTDIR = "/Users/robinson/Dropbox/zCalculators/streams.git/"
##SCRIPTDIR = "/Users/Fontina/Dropbox/z_Calculators/streams.git/"

filename = SCRIPTDIR + "/" + "ReferenceTables.xlsx"