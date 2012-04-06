######
## Should be loaded in the pylab environment: ipython -pylab
## Call: execfile("streams.py")

import os,sys,subprocess,string
from xlwt import Workbook                             # For writing to an excel file

## !!! THE STREAM WITH THE REFERENCE PRESSURE AND TEMPERATURE IS STREAM NUMBER 1 !!! ##
  
#-------------------------------------------------------------------##

def load_ebsilon(fldr="./",file_in="CombinedRes1.m"):
    '''
    Load an ebsilon output array of stream data.
    Store data in an 'nparray'.
    If the file doesn't load, exit
    '''
    
    ### Try loading the values into an 'nparray' (numpy array) from the file #####
    ### If the file does not exist and an IOError occurs, exit               #####
    
    # Generate necessary filename
    file_input = fldr + "/" + file_in 

    try:
        out = loadtxt(file_input, skiprows = (1),comments = ']')
    except IOError as e:
        print('Unable to locate the file:', f_in, 'Ending Program.''\n', e)
        input("\nPress any key to exit.")
        sys.exit()
    
    ### Sort the list by row (using the first column to decide the order) ##
    order = out[:,0].argsort()
    out = out[order,:]

    return out

def write_ebsilon(out,file_output):
    '''
    Write an array of stream data to the ebsilon .m output format.
    '''
    
    nstreams = out.shape[0]

    outf = open(file_output,'w')
    outf.write("data{1} = [\n")
    for s in arange(0,nstreams):
        line = ["{0:12.6f}".format(v) for v in out[s,:]]
        line[0] = "{0:3g}".format(out[s,0])   # Correct the stream number to be an integer!
        line = " ".join(line)+"\n"
        outf.write(line)
    outf.write("];\n\n")
    
    print "Stream data written to: " + file_output

    return 

def load_aspen(fldr="files_aspen",file_in="simu1.rep",file_out="simu1.m",write_mfile=True):
    '''
    Given the aspen output file located at fldr/in,
    convert the format to the .m table for gatex at fldr/out 
    '''

    # Generate necessary filenames
    file_input   = fldr + "/" + file_in 
    file_output  = fldr + "/" + file_out 

    # Load lines of input file
    lines = open(file_input,'r').readlines()

    # STEP 1: Filter file to relevant stream information
    # Need to process each 'stream section' of the file that
    # starts with " STREAM SECTION "
    # and ends with " ASPEN PLUS "
    lines1 = []
    in_stream = False

    skipchars = [" FROM"," TO"," SUBSTREAM"," PHASE"," COMPONENTS"," TOTAL FLOW",
                 " STATE"," ENTHALPY","ENTROPY","DENSITY"]
    addchars = [" STREAM ID","   CO2 ","   WATER ","   N2 ","   O2 ","   H2 ",
                "   CH4 ","   AR ","   KG/HR ", "   TEMP ","   PRES ","   VFRAC ",
                "   KCAL/KG ","   CAL/GM-K "]
    ncols = len(addchars)
    
    # Loop over the lines and add those inside of the 'stream section'
    # Modify some strings to make a proper table
    for line in lines:
        
        if in_stream and " ASPEN PLUS " in line:
            in_stream = False

        elif in_stream and any([substring in line for substring in addchars]):
            line1 = line.strip()
            line1 = line1.replace(" BAR ","     ")
            line1 = line1.replace(" C ","   ")
            line1 = line1.replace("MISSING","nan")
            line1 = line1.replace("+","e")
            line1 = line1.replace("-","e-")
            line1 = line1.replace(" e-"," -")
            line1 = line1.replace("GMe-","GM-")
            line1 = line1.replace("STREAM ID","STREAM   ")
            line1 = line1.replace("TEMP","T   ")
            line1 = line1.replace("PRES","p   ")
            line1 = line1.replace("VFRAC","x    ")
            line1 = line1.replace("WATER","H20  ")
            line1 = line1.replace("AR","Ar")
            line1 = line1.replace("KG/HR","mdot ")          # Mass flow rate
            line1 = line1.replace("KCAL/KG","H      ")      # Enthalpy
            line1 = line1.replace("CAL/GM-K","SE      ")    # Entropy
            lines1.append(line1)
            
        elif " STREAM SECTION " in line:
            in_stream = True


    # Check that we have a multiple of ncols
    print "ncols =",ncols," nlines=",len(lines1)
    nrep = len(lines1)/ncols
    print "If this is a whole number, data was properly read: " + str(float(len(lines1))/float(ncols))

    # Now, generate a new table, by pasting the multiples
    # on as additional columns. In this way, each column
    # represents one stream 
    lines2 = lines1[0:ncols]

    for n in arange(1,nrep):
        for q in arange(0,ncols):
            now = n*ncols + q
            lines2[q] = lines2[q] + "  " + lines1[now]

    # Split the lines by white space and convert list into
    # a numpy array. Transpose so that each row is one stream
    table0 = asarray( [line.split() for line in lines2] )
    table0 = transpose(table0)

    # Extract the headings of each column and remove them from the data part
    headings = table0[0,:]
    inds = [ e == "STREAM" for e in table0[:,0] ]
    table1 = table0[logical_not(inds),:]

    # Convert the text table into a data array
    data = asarray( [[float(a) for a in row] for row in table1 ] )

    # Get the shape of the data
    nstreams = data.shape[0]
    ncols    = data.shape[1]

    # Make the output array and headings we want for each column
    outh = array(["STREAM","mdot","T","p","x","SE","Ar","CO2","CO","COS","H2O","XX","CH4","H2","H2S","N2","O2","SO2","H"])
    ncolsx = len(outh) 
    out = zeros((nstreams,ncolsx))

    # Populate a new array that is exactly the size and shape we need
    # by matching the columns of input data with the right columns in the output arra
    for j in arange(0,ncols):
        h0 = headings[j]
        
        if h0 in outh:
            #print "Writing " + h0 + " to column " + str(j)
            out[:,outh==h0] = data[:,headings==h0]

    ## Make unit conversions
    out[:,outh=="mdot"] = out[:,outh=="mdot"] * (1.0/3600.0)   # kg/h => kg/s
    out[:,outh=="SE"] = out[:,outh=="SE"] * (1e3)         # CAL/GM-K => CAL/kg-K

    # Now convert the composition values to fractions
    elements = array(["Ar","CO2","CO","COS","H2O","CH4","H2","H2S","N2","O2","SO2"])
    inds = in1d(outh,elements)

    for s in arange(0,nstreams):
        tot = sum( out[s,inds] )
        if tot > 0.0: out[s,inds] = out[s,inds] / tot
        #print sum(out[s,inds])  # check each row sums to 1!

        # Also eliminate nan values (fortran program can't read them)
        out[s,isnan(out[s,:])] = 0.0
    
    # Reorder the data by stream number
    ### Sort the list by row (using the first column to decide the order) ##
    order = out[:,0].argsort()
    out = out[order,:]

    ## FINAL STEP: if desired, also write the data to output file in ebsilon format
    if write_mfile: write_ebsilon(out,file_output)
    
    # Return the array of stream data in ebsilon format
    return out 

def calc_exergy_gatex(streams,fldr="./",gatex_exec="./gatex_pc_if97_mj.exe"):
    '''
    Use this subroutine to calculate exergy from a set of stream data (array)
    using GATEX.

    == INPUT ==
    streams : numpy array of dimensions n_streams X n_variables
    fldr    : folder containing gatex program and 
              where input and output data are stored
              (for now must be the current working directory, since gatex.exe looks there)
    
    == OUTPUT ==
    E       : table of exergy calculations obtained from GATEX 

    '''
    
    # Define important gatex filenames
    gatex_f1 = os.path.join(fldr,"gate.inp")
    gatex_f2 = os.path.join(fldr,"flows.prn")
    gatex_f3 = os.path.join(fldr,"composition.prn")

    # To help figure things out, create a header
    # that shows the variable of each column
    head = array(["STREAM","mdot","T","p","x","SE","Ar","CO2","CO","COS","H2O","XX","CH4","H2","H2S","N2","O2","SO2","H"])

    # How many streams and variables are we working with?
    n_streams = len(streams)
    n_var     = len(head)

    ### Create the gate.inp file with the reference values #################
    ref = open(gatex_f1,'w',buffering=0)                        
    t0 = float(streams[0,2])
    p0 = float(streams[0,3])
    ref.write('\n\n[system]\n\nt0 =\t')             
    ref.write(str(t0))
    ref.write(' ;\np0 =\t')
    ref.write(str(p0))
    ref.write(' ;\nnumber =\t')
    ref.write(str(n_streams))
    ref.write('. ;\nndiff =\t')
    ref.write(str(n_streams))
    ref.write('. ;\nkelvin =\t')
    ref.write('0. ;')  
    ref.close
    print "Wrote file for GATEX: " + gatex_f1

    #----------------------------------------------------------------------#

    #-- Separate streams depending on their type --------------------------#
    ## AJR: Fontina, are you sure this works properly? Is this general?
    sat_water = [0]                                               # Write the numbers of saturated water streams
    sat_steam = [0]                                               # Write the numbers of saturated steam streams
    for i in sat_water:
        streams[i,4] = 0                                          # x=0 when it is saturated water
    for i in sat_steam: 
        streams[i,4] = 1                                          # x=1 when it is saturated vapor
    #----------------------------------------------------------------------#
    
    # For gatex to read the file correctly, the
    # stream number should appear twice. Here we duplicate
    # the first column (which is the stream number)
    streams2 = insert(streams,1,streams[:,0],axis=1)
    head2    = insert(head,1,head[0])

    #---------------------------------------------------------------------##

    ## Create files for saving the different data parts ####################
    
    # Extract flow data from the stream array (with duplicate stream number!)
    # Then flatten to one vector and output to the flows.prn file
    flow_names = array(["STREAM","mdot","T","p","x"])
    inds = in1d(head2,flow_names)
    flows = streams2[:,inds]
    flows = flows.flatten()
    savetxt(gatex_f2,flows,fmt="%10.4f")
    print "Wrote file for GATEX: " + gatex_f2

    # Now extract element composition data (with duplicate stream number!)
    # Then flatten to one vector and output to the composition.prn file
    element_names = array(["STREAM","Ar","CO2","CO","COS","H2O","CH4","H2","H2S","N2","O2","SO2"])
    inds = in1d(head2,element_names)
    elements = streams2[:,inds]
    elements = elements.flatten()
    savetxt(gatex_f3,elements,fmt="%10.4f")
    print "Wrote file for GATEX: " + gatex_f3

    #---------------------------------------------------------------------##
    
    # Now call gatex #######################################################
    print "Calling GATEX..."
    
    # Determine whether to use wine or not
    # (If on linux or mac, use wine)
    uname = os.uname()    # Operating system info
    call_prefix = ""
    if ( uname[0] in ["Darwin"] ): call_prefix = "wine "

    ## Now call gatex and cross fingers !!! 
    os.system((call_prefix+gatex_exec))
    
    # If it worked, load the exergies
    E = loadtxt('exergies.m', skiprows = (37),comments = ']')
    
    # Do some calculations to check the output    
    Ef   = E[7,7]
    Ep1  = E[4,7]-E[2,7]
    Ep2  = E[6,7]-E[1,7]
    ED1  = Ef - Ep1
    ED2  = Ef - Ep2
    eff1 = Ep1/Ef*1E02
    eff2 = Ep2/Ef*1E02
    
    print 'Checking GATEX output:'
    # print E
    print 'Ef  : ', '%.2f'%(Ef)
    print 'Ep1 : ', '%.2f'%(Ep1), '\t##### Streams: 5-3'
    print 'ED1 : ', '%.2f'%(ED1)      
    print 'eff1: ', '%.2f'%(eff1)     

    print 'Ep2 : ', '%.2f'%(Ep2), '\t##### Streams: 7-2'
    print 'ED2 : ', '%.2f'%(ED2)         
    print 'eff2: ', '%.2f'%(eff2)        
    print '======================'
    #---------------------------------------------------------------------##

    # Done, return the table of exergies
    return E




