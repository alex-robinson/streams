######
## Should be loaded in the pylab environment: ipython -pylab
## Call: execfile("streams.py")

import os,sys,subprocess,string

from xlwt import Workbook                                           # From writing to an excel file

## !!! THE STREAM WITH THE REFERENCE PRESSURE AND TEMPERATURE IS STREAM NUMBER 1 !!! ##
  
#-------------------------------------------------------------------##



file_name      = "CombinedRes.txt"
file_name_out  = "write.txt"
file_name_out2 = "write2.txt"
fflows         = "flows.prn"
fcomposition   = "composition.prn"
# fexergies      = "exergies.txt"


def calc_exergy_gatex(streams,fldr="gatex"):
    '''
    Use this subroutine to calculate exergy from a set of stream data (array)

    streams : numpy array of dimensions n_streams X n_variables
    fldr    : folder containing gatex program and 
              where temp. gatex files will be written
    '''
    
    # Define important gatex filenames
    gatex_f1 = fldr + "/" + "gate.inp"
    gatex_f2 = fldr + "/" + "flows.prn"
    gatex_f3 = fldr + "/" + "composition.prn"
    gatex_f1 = "gate.inp"
    gatex_f2 = "flows.prn"
    gatex_f3 = "composition.prn"

    gatex_exec = fldr + "/" + 'gatex_pc_if97_mj.exe'

    # To help figure things out, create a header
    # that shows the variable of each column
    head = array(["STREAM","mdot","T","p","x","SE","Ar","CO2","CO","COS","H2O","XX","CH4","H2","H2S","N2","O2","SO2","H"])


    # How many streams and variables are we working with?
    n_streams = len(streams)
    n_var     = len(head)

    ### Create the gate.inp file with the reference values #################
    reference = open(gatex_f1,'w')                        
    t0 = float(streams[0,2])
    p0 = float(streams[0,3])
    reference.write('\n\n[system]\n\nt0 =\t')             
    reference.write(str(t0))
    reference.write(' ;\np0 =\t')
    reference.write(str(p0))
    reference.write(' ;\nnumber =\t')
    reference.write(str(n_streams))
    reference.write('. ;\nndiff =\t')
    reference.write(str(n_streams))
    reference.write('. ;\nkelvin =\t')
    reference.write('0. ;')  
    reference.close
    #----------------------------------------------------------------------#

    #-- Separate streams depending on their type --------------------------#
    ## AJR: Fontina, are you sure this works properly?
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

    # streams_flat = streams.flatten()                              # to flatten the matrix OR ravel()
    # savetxt("./write2.txt",streams_flat,fmt="%10.4f")

    #---------------------------------------------------------------------##

    ## Create files for saving the different data parts ####################
    
    # Extract flow data from the stream array (with duplicate stream number!)
    # Then flatten to one vector and output to the flows.prn file
    flow_names = array(["STREAM","mdot","T","p","x"])
    inds = in1d(head2,flow_names)
    flows = streams2[:,inds]
    flows = flows.flatten()
    savetxt(gatex_f2,flows,fmt="%10.4f")
    
    # Now extract element composition data (with duplicate stream number!)
    # Then flatten to one vector and output to the composition.prn file
    element_names = array(["STREAM","Ar","CO2","CO","COS","H2O","XX","CH4","H2","H2S","N2","O2","SO2","H"])
    inds = in1d(head2,element_names)
    elements = streams2[:,inds]
    elements = elements.flatten()
    savetxt(gatex_f3,elements,fmt="%10.4f")

    #---------------------------------------------------------------------##
    
    ## Now call gatex and cross fingers !!! ################################
    os.system(('wine '+gatex_exec))

    E = loadtxt('exergies.m', skiprows = (37),comments = ']')
    print E
    
    Ef   = E[7,7]
    Ep1  = E[4,7]-E[2,7]
    Ep2  = E[6,7]-E[1,7]
    ED1  = Ef - Ep1
    ED2  = Ef - Ep2
    eff1 = Ep1/Ef*1E02
    eff2 = Ep2/Ef*1E02
    
    print '\nEf  : ','%.2f' %Ef
    print '\nEp1 : ','%.2f' %Ep1,          '\t##### Streams: 5-3'
    print '\nED1 : ','%.2f' %ED1      
    print '\neff1: ','%.1f' %eff1     

    print '\nEp2 : ','%.2f' %Ep2,          '\t##### Streams: 7-2'
    print '\nED2 : ','%.2f' %ED2         
    print '\neff2: ','%.1f' %eff2        
    
    exergy = E

    return exergy 

streams = load_ebsilon(fldr="./",file_in="CombinedRes1.m")
calc_exergy_gatex(streams)


# for f_loop in range(1,4,1):

#     f_in =  'CombinedRes'+str(f_loop)+'.m' # format looks in { } and replaces it with var but formatted as a string, so var = 1, var = 2, etc

#     #streams = load_ebsilon(file_in=f_in)
#     #streams = load_ebsilon(fldr="files_aspen",file_in='simu1.m')
#     streams = load_aspen(fldr="files_aspen",file_in='simu1.rep')
    
# #--------------------------------------------------------------------##

#     print ('Working with CombinedRes',f_loop)

#     NO_STR=len(streams)                                            # Total number of streams NO_STR 


# #---------------------------------------------------------------------##

# ### Write the sorted data to the output file ###########################
#     savetxt(file_name_out,streams,fmt="%10.4f")
# #---------------------------------------------------------------------##

# ### Create the gate.inp file with the reference values #################
#     for i in range(1,3,1): 
#         reference = open('gate.inp','w')                        
#         t0 = float(streams[0,2])
#         p0 = float(streams[0,3])
#         reference.write('\n\n[system]\n\nt0 =\t')             
#         reference.write(str(t0))
#         reference.write(' ;\np0 =\t')
#         reference.write(str(p0))
#         reference.write(' ;\nnumber =\t')
#         reference.write(str(NO_STR))
#         reference.write('. ;\nndiff =\t')
#         reference.write(str(NO_STR))
#         reference.write('. ;\nkelvin =\t')
#         reference.write('0. ;')  
#         reference.close
# #----------------------------------------------------------------------##

# #-- Separate streams depending on their type --------------------------#
#     sat_water = [0]                                               # Write the numbers of saturated water streams
#     sat_steam = [0]                                               # Write the numbers of saturated steam streams
#     for i in sat_water:
#         streams[i,4] = 0                                          # x=0 when it is saturated water
#     for i in sat_steam: 
#         streams[i,4] = 1                                          # x=1 when it is saturated vapor
# #----------------------------------------------------------------------#

#     streams_flat = streams.flatten()                              # to flatten the matrix OR ravel()
#     savetxt(file_name_out2,streams_flat,fmt="%10.4f")

#     streams_flat = streams                                        # for gatex to read the file correctly I need to have the 
#     j=1                                                           # the stream number twice. So here, I add them.
#     for i in range(0,152,20):
#         streams_flat = np.insert(streams_flat,i,j)
#         j = j+1
# #---------------------------------------------------------------------##

# ## Create files for saving the different data ##########################
#     flows = []
#     NO_LIN = 6 * NO_STR
#     for i in range(0,152,20):
#         start  = i
#         finish = i+6
#         flows2 = streams_flat[start:finish]
#         flows.append(flows2)                                      # append because it is a list. Arrays do not have append
#         flows2 = resize(flows,(NO_LIN,1))
#     savetxt(fflows,flows2,fmt="%10.4f")                           # Create flows.txt

#                                                                   #        flows = ['Name', 'Mass', 'Temperature', 'Pressure', 'Quality']  
#     NO_LIN = 13 * NO_STR                                          # 14 because it's 12 + 2xNumberOfStream = 14                                                                                        
#     j=1
#     composition = []
#     for i in range(7,152,20):
#         start  = i
#         finish = i+11
#         composition.append(j)                                     # Adding the number of the stream
#         composition.append(j)                                     # twice
#         j = j+1
#         for i in streams_flat[start:finish]:
#             composition.append(i)
#         composition2 = resize(composition,(NO_LIN,1))
#     savetxt(fcomposition,composition2,fmt="%10.4f")               # Create composition.txt
#                                                                   #        composition = ('??', 'Ar', 'CO2', 'CO', 'COS', 'H2O', '??', 'CH4', 'H2', 'H2S', 'N2', 'O2', 'SO2')  
# #---------------------------------------------------------------------##

#     os.system(('wine '+exergy_calcs))

#     E = loadtxt('exergies.m', skiprows = (37),comments = ']')
#     print E
    
#     Ef   = E[7,7]
#     Ep1  = E[4,7]-E[2,7]
#     Ep2  = E[6,7]-E[1,7]
#     ED1  = Ef - Ep1
#     ED2  = Ef - Ep2
#     eff1 = Ep1/Ef*1E02
#     eff2 = Ep2/Ef*1E02
    
#     print '\nEf  : ','%.2f' %Ef
#     print '\nEp1 : ','%.2f' %Ep1,          '\t##### Streams: 5-3'
#     print '\nED1 : ','%.2f' %ED1      
#     print '\neff1: ','%.1f' %eff1     

#     print '\nEp2 : ','%.2f' %Ep2,          '\t##### Streams: 7-2'
#     print '\nED2 : ','%.2f' %ED2         
#     print '\neff2: ','%.1f' %eff2        
    

#     book = Workbook()
#     sheet_cur = book.add_sheet('Results')
#     ##sheet_cur = book.get_sheet('Results') 
#     # ajr: you don't need the above line because "sheet_cur" is already defined 
#     #      when you use the function 'add_sheet'. The function 'get_sheet' requires
#     #      the number of the sheet not the name, so
#     #      book.get_sheet(1), not book.get_sheet('Results')
    
# ##    sheet_cur = book.add_sheet('Sheet'+str(f_loop))  
#     sheet_cur.write(0,0,'Ef')   # zeroth line first column
#     sheet_cur.write(0,1,'Ep1')   # zeroth line first column
#     sheet_cur.write(0,2,'ED1')   # zeroth line first column
#     sheet_cur.write(0,3,'Eff1')
#     sheet_cur.write(0,5,'Ep2')
#     sheet_cur.write(0,6,'ED2')
#     sheet_cur.write(0,7,'eff2')


   
#     sheet_cur.write(f_loop,0,Ef)
#     sheet_cur.write(f_loop,1,Ep1)
#     sheet_cur.write(f_loop,2,ED1)
#     sheet_cur.write(f_loop,3,eff1)
#     sheet_cur.write(f_loop,5,Ep2)
#     sheet_cur.write(f_loop,6,ED2)
#     sheet_cur.write(f_loop,7,eff2)


#     book.save('results.xls')
    
#     ##    ##    savetxt(fexergies+str('f_loop'),exergies,fmt="%10.4f")
#     ##        
#     ##    ##def ex_anal(flows.prn, composition.prn, exergies.txt):
#     ## Exergy balances for the components
#     ## Fuel exergy
#     ##    Ef = 


#     ##    ex_anal()
        

        


