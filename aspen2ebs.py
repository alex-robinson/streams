######
## Should be loaded in the pylab environment: ipython -pylab
## Call: execfile("streams.py")

import os,sys,subprocess,string




file_name = "files_aspen/simu1.rep"


lines = open(file_name,'r').readlines()


# STEP 1: Filter file to relevant stream information
# Need to process each 'stream section' of the file that
# starts with " STREAM SECTION "
# and ends with " ASPEN PLUS "
lines1 = []
in_stream = False

skipchars = [" FROM"," TO"," SUBSTREAM"," PHASE"," COMPONENTS"," TOTAL FLOW",
             " STATE"," ENTHALPY","ENTROPY","DENSITY"]
addchars = [" STREAM ID","   CO2 ","   WATER ","   N2 ","   O2 ","   H2 ",
            "   CH4 ","   AR ","   KG/HR ", "   TEMP ","   PRES ","   KCAL/KG ","   CAL/GM-K "]
ncols = len(addchars)

for line in lines:
    
    if in_stream and " ASPEN PLUS " in line:
        in_stream = False

    elif in_stream and any([substring in line for substring in addchars]):
        line1 = line.strip()
        line1 = line1.replace(" BAR ","     ")
        line1 = line1.replace(" C ","   ")
        line1 = line1.replace("MISSING","9999.99")
        line1 = line1.replace("+","e")
        line1 = line1.replace("-","e-")
        line1 = line1.replace(" e-"," -")
        line1 = line1.replace("GMe-","GM-")
        line1 = line1.replace("STREAM ID","STREAM   ")
        line1 = line1.replace("WATER","H20  ")
        line1 = line1.replace("AR","Ar")
        line1 = line1.replace("KG/HR","mdot ")          # Mass flow rate
        line1 = line1.replace("KCAL/KG","H      ")      # Enthalpy
        line1 = line1.replace("CAL/GM-K","SE      ")    # Entropy
        lines1.append(line1)
        
    elif " STREAM SECTION " in line:
        in_stream = True


# Check that we have a multiple of ncols
print "ncols =",ncols
print "nlines =",len(lines1)
nrep = len(lines1)/ncols

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
outh = array(["STREAM","mdot","T","p","X","SE","Ar","CO2","CO","COS","H2O","CH4","H2","H2S","N2","O2","SO2","H"])
ncolsx = len(outh) 
out = zeros((nstreams,ncolsx))

# Populate a new array that is exactly the size and shape we need
# by matching the columns of input data with the right columns in the output arra
for j in arange(0,ncols):
    h0 = headings[j]
    
    if h0 in outh:
        out[:,outh==h0] = data[:,headings==h0]

## Make unit conversions
out[:,outh=="mdot"] = out[:,outh=="mdot"] * (1/3600)   # kg/h => kg/s
out[:,outh=="SE"] = out[:,outh=="SE"] * (1000)         # CAL/GM-K => CAL/kg-K


# Now convert the composition values to percentages
inds = [ h in ["CO2","H20","N2","O2","H2","CH4","Ar"] for h in headings]


