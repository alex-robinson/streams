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
SCRIPTDIR = "/Users/robinson/models/streams/"
#SCRIPTDIR = "D:/FONTINA/Dropbox/z_Calculators/streams.git/"

# And import the needed exergy calculating functions
sys.path.insert(0, SCRIPTDIR)
from streams import * 

# Now define locations of gatex and streams.py
GATEX     = os.path.join(SCRIPTDIR, "gatex_pc_if97_mj.exe")


########
## BELOW HERE, begin the
## individual calculations
########

# Make a list of all simulation filenames that we will be 
# calculating exergies for.
##filenames =  [ 'CombinedRes'+str(f_loop)+'.m' for f_loop in range(0,10,1) ] 
filenames = [ 'CombinedRes0.m' ]

n_streams = 27

## Now perform calculations that we will save inside the workbook
## Loop over the filenames and output exergy tables

f_loop = 0  # Counter

for f_in in filenames:

    f_loop = f_loop + 1   # Increment the counter
    
    # Load the stream data from the input file
    streams = load_streams(file_in=f_in)
    
	# Limit calculations to number of streams
    streams = streams[0:n_streams,:]
	
    # Calculate exergies using GATEX
    E = calc_exergy_gatex(streams,gatex_exec=GATEX)

    # Generate an ouput filename and save exergy array
    #f_out = 'exergies'+str(f_loop)+'.txt'
    f_out = f_in.rsplit(".",1)[0] + '.txt'
	
    if f_out == f_in:
        sys.exit("Error: output filename would overwrite input!")
    savetxt(f_out,E,fmt="%10.5f")

    ### Calculate some interesting results ########################################
    # Define the exergy of the fuel 'Ef' and the physical exergy 'Ep'
    # for each component (and any other interesting quantities)
    # Then calculate general quantities for each component
    

    ## COMPONENT DEFINTIONS ##############

    ## COMPONENT 1 ##
    comp1 = OrderedDict()
    comp1['name'] = "Compressor"
    comp1['Ef']   = (E[2,4]-E[1,4])/0.99
    comp1['Ep']   = E[2,8]-E[1,8]
    
    ## COMPONENT 2 ##
    comp2 = OrderedDict()
    comp2['name'] = "CC"
    comp2['Ef']  = E[3,8]
    comp2['Ep']  = E[4,8]-E[2,8]

    ## COMPONENT 3 ##
    comp3 = OrderedDict()
    comp3['name'] = "GT"
    comp3['Ef']  = E[4,8]-E[5,8]
    comp3['Ep']  = ((E[4,4]-E[5,4])-(E[2,4]-E[1,4]))*0.99*0.985 + (E[2,4]-E[1,4])/0.99   

    ## COMPONENT 4 ##
    comp4 = OrderedDict()
    comp4['name'] = "RH"
    comp4['Ef']  = E[6,8]-E[7,8]
    comp4['Ep']  = E[29,8]-E[28,8]
	
	## COMPONENT 5 ##
    comp5 = OrderedDict()
    comp5['name'] = "HPSH"
    comp5['Ef']  = E[8,8]-E[9,8]
    comp5['Ep']  = E[41,8]-E[40,8]
	
	## COMPONENT 6 ##
    comp6 = OrderedDict()
    comp6['name'] = "HPEV"
    comp6['Ef']  = E[10,8]-E[11,8]
    comp6['Ep']  = E[40,8]-E[39,8]
	
	## COMPONENT 7 ##
    comp7 = OrderedDict()
    comp7['name'] = "HPEC"
    comp7['Ef']  = E[11,8]-E[12,8]
    comp7['Ep']  = E[39,8]-E[38,8]
	
	## COMPONENT 8 ##
    comp8 = OrderedDict()
    comp8['name'] = "IPSH"
    comp8['Ef']  = E[12,8]-E[13,8]
    comp8['Ep']  = E[27,8]-E[26,8]
	
	## COMPONENT 9 ##
    comp9 = OrderedDict()
    comp9['name'] = "IPEV"
    comp9['Ef']  = E[13,8]-E[14,8]
    comp9['Ep']  = E[26,8]-E[25,8]
	
	## COMPONENT 10 ##
    comp10 = OrderedDict()
    comp10['name'] = "IPEC"
    comp10['Ef']  = E[14,8]-E[15,8]
    comp10['Ep']  = E[25,8]-E[24,8]
	
	## COMPONENT 11 ##
    comp11 = OrderedDict()
    comp11['name'] = "LPSH"
    comp11['Ef']  = E[15,8]-E[16,8]
    comp11['Ep']  = E[31,8]-E[32,8]
	
	## COMPONENT 12 ##
    comp12 = OrderedDict()
    comp12['name'] = "LPEV"
    comp12['Ef']  = E[16,8]-E[17,8]
    comp12['Ep']  = E[36,8]-E[35,8]
	
	## COMPONENT 13 ##
    comp13 = OrderedDict()
    comp13['name'] = "LPEC"
    comp13['Ef']  = E[17,8]-E[18,8]
    comp13['Ep']  = E[20,8]-E[19,8]
	
	## COMPONENT 14 ##
    comp14 = OrderedDict()
    comp14['name'] = "HPST"
    comp14['Ef']  = E[41,8]-E[42,8]
    comp14['Ep']  = (E[41,4]-E[42,4])*0.99*0.985
	
	## COMPONENT 15 ##
    comp15 = OrderedDict()
    comp15['name'] = "IPST"
    comp15['Ef']  = E[29,8]-E[30,8]
    comp15['Ep']  = (E[29,4]-E[30,4])*0.99*0.985
	
	## COMPONENT 16 ##
    comp16 = OrderedDict()
    comp16['name'] = "LPST"
    comp16['Ef']  = E[43,8]-E[44,8]
    comp16['Ep']  = (E[43,4]-E[44,4])*0.99*0.985
	
	## COMPONENT 17 ##
    comp17 = OrderedDict()
    comp17['name'] = "Mixer1"
    comp17['Ef']  = E[30,1]*(E[30,8]/E[30,1]-E[43,8]/E[43,1])
    comp17['Ep']  = E[31,1]*(E[43,8]/E[43,1]-E[31,8]/E[31,1])
	
	## COMPONENT 18 ##
    comp18 = OrderedDict()
    comp18['name'] = "Mixer2"
    comp18['Ef']  = E[42,1]*(E[42,8]/E[42,1]-E[28,8]/E[28,1])
    comp18['Ep']  = E[27,1]*(E[28,8]/E[28,1]-E[27,8]/E[27,1])
	
	## COMPONENT 19 ##
    comp19 = OrderedDict()
    comp19['name'] = "COND_P"
    comp19['Ef']  = (E[19,4]-E[45,4])/(0.980*0.872)
    comp19['Ep']  = E[19,8]-E[45,8]
	
	## COMPONENT 20 ##
    comp20 = OrderedDict()
    comp20['name'] = "LPP"
    comp20['Ef']  = (E[35,4]-E[34,4])/(0.98*0.807)
    comp20['Ep']  = E[35,8]-E[34,8]
	
	## COMPONENT 21 ##
    comp21 = OrderedDict()
    comp21['name'] = "HPP"
    comp21['Ef']  = (E[38,4]-E[37,4])/(0.98*0.948)
    comp21['Ep']  = E[38,8]-E[37,8]
	
	## COMPONENT 22 ##
    comp22 = OrderedDict()
    comp22['name'] = "IPP"
    comp22['Ef']  = (E[24,4]-E[23,4])/(0.98*0.862)
    comp22['Ep']  = E[24,8]-E[23,8]
	
	## COMPONENT 23 ##
    comp23 = OrderedDict()
    comp23['name'] = "CT"
    comp23['Ef']  = 1.0
    comp23['Ep']  = 1.0
	
	## COMPONENT 24 ##
    comp24 = OrderedDict()
    comp24['name'] = "Deaerator"
    comp24['Ef']  = E[33,1]*(E[33,8]/E[33,1]-E[21,8]/E[21,1])
    comp24['Ep']  = (E[20,1]*(E[21,8]/E[21,1]-E[20,8]/E[20,1]))
	
	## COMPONENT 25 ##
    comp25 = OrderedDict()
    comp25['name'] = "Mixer_fg"
    comp25['Ef']  = E[9,1]*(E[9,8]/E[9,1]-E[10,8]/E[10,1])
    comp25['Ep']  = E[7,1]*(E[10,8]/E[10,1]-E[7,8]/E[7,1])
	
	## COMPONENT 26 ##
    comp26 = OrderedDict()
    comp26['name'] = "COND"
    comp26['Ef']  = E[44,8]-E[45,8]
    comp26['Ep']  = 1.0

	## COMPONENT TOTAL ##
    comp27 = OrderedDict()
    comp27['name'] = "TOTAL"
    comp27['Ef']  = E[1,8]+E[3,8]
    comp27['Ep']  = ((E[4,4]-E[5,4])-(E[2,4]-E[1,4]))*0.99*0.985+(E[41,4]-E[42,4])*0.99*0.985+(E[29,4]-E[30,4])*0.99*0.985+(E[43,4]-E[44,4])*0.99*0.985-(E[19,8]-E[45,8])-(E[35,8]-E[34,8])-(E[38,8]-E[37,8])-(E[24,8]-E[23,8])
	

    ######################################

    ## Now make a list containing the results of all components
    components = [comp1,comp2,comp3,comp4,comp5,comp6,comp7,comp8,comp9,comp10,comp11,comp12,comp13,comp14,comp15,comp16,comp17,comp18,comp19,comp20,comp21,comp22,comp23,comp24,comp25,comp26,comp27]
    
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




