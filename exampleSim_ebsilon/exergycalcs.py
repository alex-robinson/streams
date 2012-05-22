######
## exergycalcs.py
## This script should be run from a directory that 
## contains results of a simulation with ebsilon or aspen
## This should be loaded in the pylab environment: ipython -pylab
## Call: execfile("exergycalcs.py")
######

# Import some handy modules
import os,sys,subprocess,string
from collections import OrderedDict

# First, define the central script directory and 
# location of gatex.exe and the streams.py functions
# CHANGE THIS TO THE LOCATION ON YOUR COMPUTER:
##SCRIPTDIR = "/Users/robinson/Dropbox/zCalculators/streams.git/"
SCRIPTDIR = "/Users/admin/Dropbox/z_Calculators/streams.git/"

# Now define locations of gatex and streams.py
GATEX     = os.path.join(SCRIPTDIR, "gatex_pc_if97_mj.exe")
STREAMS   = os.path.join(SCRIPTDIR, "streams.py")

# And import the needed exergy calculating functions
execfile(STREAMS)


########
## BELOW HERE, begin the
## individual calculations
########

# Make a list of all simulation filenames that we will be 
# calculating exergies for.
filenames =  [ 'CombinedRes'+str(f_loop)+'.m' for f_loop in range(1,6,1) ] 


## Now perform calculations that we will save inside the workbook
## Loop over the filenames and output exergy tables

f_loop = 0  # Counter

for f_in in filenames:

    f_loop = f_loop + 1   # Increment the counter
    
    # Load the stream data from the input file
    streams = load_streams(file_in=f_in)

    # Calculate exergies using GATEX
    E = calc_exergy_gatex(streams,gatex_exec=GATEX)

    # Generate an ouput filename and save exergy array
    f_out = 'exergies'+str(f_loop)+'.txt'
    f_out = f_in.replace(".m",".txt")
    savetxt(f_out,E,fmt="%10.5f")

    ### Calculate some interesting results ########################################
    # Define the exergy of the fuel 'Ef' and the physical exergy 'Ep'
    # for each component (and any other interesting quantities)
    # Then calculate general quantities for each component
    

    ## COMPONENT DEFINTIONS ##############

    ## COMPONENT 1 ##
    comp1 = OrderedDict()
    comp1['name'] = "Component 1"
    comp1['Ef']   = E[8,8]
    comp1['Ep']   = E[5,8] - E[3,8]
    
    ## COMPONENT 2 ##
    comp2 = OrderedDict()
    comp2['name'] = "Component 2"
    comp2['Ef']  = E[8,8]
    comp2['Ep']  = E[7,8] - E[2,8]
    
    ######################################

    ## Now make a list containing the results of all components
    components = [comp1,comp2]
    
    # Calculate variables for each component,
    # like the exergy destruction 'ED' and
    # the exergetic efficiency 'eff'
    for comp in components:
        comp['ED']  = comp['Ef'] - comp['Ep']
        comp['eff'] = comp['Ep']/comp['Ef'] *1E02

    ###############################################################################

    # Write the results for each component to Excel file
    # If f_loop is 1, then it should be a new book!
    newBook = False
    if f_loop == 1: newBook = True
    exergy_to_excel(components=components,exergytable=E,
                     filename="results.xlsx",sheetname=f_out,newBook=newBook)




