######
## exergycalcs.py
## This script should be run from a directory that 
## contains results of a simulation with ebsilon or aspen
## This should be loaded in the pylab environment: ipython -pylab
## Call: execfile("exergycalcs.py")
######

# Import some handy modules
import os,sys,subprocess,string

# First, define the central script directory and 
# location of gatex.exe and the streams.py functions
# CHANGE THIS TO THE LOCATION ON YOUR COMPUTER:
SCRIPTDIR = "/Users/robinson/Dropbox/zCalculators/streams.git/"

# Now define locations of gatex and streams.py
GATEX     = os.path.join(SCRIPTDIR, "gatex_pc_if97_mj.exe")
STREAMS   = os.path.join(SCRIPTDIR, "streams.py")

# And import the needed exergy calculating functions
execfile(STREAMS)


########
## BELOW HERE, begin the
## individual calculations
########

## Now perform calculations that we will save inside the workbook
## Loop over the CombinedRes files and output exergy tables
for f_loop in range(1,6,1):
    
    # Generate the current filename
    f_in =  'CombinedRes'+str(f_loop)+'.m'
    
    # Load the stream data from the input file
    streams = load_ebsilon(file_in=f_in)

    # Calculate exergies using GATEX
    E = calc_exergy_gatex(streams,gatex_exec=GATEX)

    # Generate an ouput filename and save exergy array
    f_out = 'exergies'+str(f_loop)+'.txt'
    savetxt(f_out,E,fmt="%10.5f")


    ### Calculate some interesting results ########################################
    
    Ef   = E[7,8]
    Ep1  = E[4,8]-E[2,8]
    Ep2  = E[6,8]-E[1,8]
    ED1  = Ef - Ep1
    ED2  = Ef - Ep2
    eff1 = Ep1/Ef*1E02
    eff2 = Ep2/Ef*1E02

    # Save the results inside of a dictionary for writing easily.
    # Save them here in the order they should appear in excel!
    results = dict( 
        Ef = Ef, Ep1 = Ep1, Ep2 = Ep2,
        ED1 = ED1, ED2 = ED2,
        eff1 = eff1, eff2 = eff2
    )

    ###############################################################################
    

    # Write the results to Excel file
    # If f_loop is 1, then it should be a new book!
    newBook = False
    if f_loop == 1: newBook = True
    exergy_to_excel(exergy=E,results=results,filename="results.xls",newBook=newBook,line=f_loop)




