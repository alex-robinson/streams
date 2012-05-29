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



# Now define locations of gatex and streams.py
STREAMS   = os.path.join(SCRIPTDIR, "streams.py")
EXERGY    = os.path.join(SCRIPTDIR, "exergy.py")

# And import the needed exergy calculating functions
execfile(STREAMS)
execfile(EXERGY)

# Load reference substance values
ref_file = SCRIPTDIR + "/" + "ReferenceTables.xlsx"
refs = load_reference(ref_file)

# filename_in  = "ExampleSimulation.xlsx"
# filename_out = filename_in
# sheetname    = "ExampleStreams1"

filename_in   = "h2_prod_exergy_v4.rep"
filename_out  = "AspenSimulation1.xlsx"
sheetname     = "Sim1"

########
## BELOW HERE, begin the
## individual calculations
########



## Test cases
#s1 = stream(id=1,T=298.15,p=20.0,mdot=1,composition=[('CH4',1)])
#s2 = stream(id=2,T=473.15,p=10.0,mdot=1,composition=[('O2',0.21),('N2',0.79)])
#s3 = stream(id=2,T=1929.15,p=10.0,mdot=1,composition=[('O2',0.064),('N2',0.738),('CO2',0.066),('H2O',0.132)])


## Test loading a simulation and calculating exergies
sim1 = simulation(filename=filename_in,sheetname=sheetname,exergy_method="default")

## Write results to Excel
sim1.write_excel(filename=filename_out,sheetname=sheetname)



## Check stream 6
# comp = sim1.streams['6'].comp0
# tot = 0.0
# print "{:>12} {:>10} {:>12} {:>12}".format("Substance","x","h_0","x*h_0")
# for key,sub in comp.items():
#     tmp = sub.state['x']*sub.ref['h_0']
#     tot = tot + tmp
#     print "{:>12} {:10.5g} {:12.5g} {:12.5g}".format(key,sub.state['x'],sub.ref['h_0'],tmp)
# print "TOTAL = ",tot

