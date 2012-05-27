######
## Should be loaded in the pylab environment: ipython -pylab
## Call: execfile("streams.py")

import os,sys,subprocess,string
from collections import OrderedDict
import openpyxl as xl                 # For writing/reading excel files



def load_reference(filename="ReferenceTables.xlsx"):
    '''
    Load the reference data from the excel tables.
    '''

    # Load the workbook from existing file
    book = xl.load_workbook(filename)
    
    # Get all existing sheetnames
    sheetnames = book.get_sheet_names()
    
    # Load 'Sheet1' - the first sheet
    sheet1 = book.get_sheet_by_name("Sheet1")
    
    ## Now load some reference data

    # First get T0 and p0 used for these data
    T0 = sheet1.cell('B2').value
    p0 = sheet1.cell('A2').value 
    
    # Now get the names of all the substances we
    # have data for (in column C) and the 
    # relevant information
    
    refs = OrderedDict()

    for j in arange(2,1000):
        
        # First see if this row has a substance
        nm = sheet1.cell(row=j,column=2).value

        # If an element was actuall found in this row
        # store all the reference values in the OrderedDict!
        if not nm == None:
            refs[nm] = OrderedDict()
            refs[nm]['mw']     = sheet1.cell(row=j,column=3).value
            refs[nm]['ech_0a'] = sheet1.cell(row=j,column=4).value    # Ahrends
            refs[nm]['ech_0b'] = sheet1.cell(row=j,column=5).value    # Szargut
            refs[nm]['cp_0']   = sheet1.cell(row=j,column=7).value
            refs[nm]['h_0']    = sheet1.cell(row=j,column=8).value
            refs[nm]['s_0']    = sheet1.cell(row=j,column=9).value
            
            refs[nm]['H+']     = sheet1.cell(row=j,column=12).value
            refs[nm]['S+']     = sheet1.cell(row=j,column=13).value
            refs[nm]['a']      = sheet1.cell(row=j,column=14).value
            refs[nm]['b']      = sheet1.cell(row=j,column=15).value
            refs[nm]['c']      = sheet1.cell(row=j,column=16).value
            refs[nm]['d']      = sheet1.cell(row=j,column=17).value
        else:
            break

    print "The following substances are available:"
    print ", ".join(refs.keys())

    return refs

### THE FUNCTIONS BELOW ARE METHODS
### FOR THE 'ref' object,
### which is an OrderedDict of OrderedDicts
### Eventually these should be encapsulated nicely!!!

def ref_check(refs,nm='N2'):
    '''
    Nicely print the reference values for the desired substance.
    '''
    print "Substance: " + nm

    if nm in refs.keys():
        for key,value in refs[nm].items():
          print "    {:<10} = {}".format(key,value)

    else:
        print "Error: substance not found in reference values!"

    return

def ref_array(refs):
    
    # Get column/row headings
    tmp1,tmp2 = refs.items()[0]
    headings = tmp2.keys()
    names = refs.keys()

    # Determine length of output array
    ns = len(refs)
    nv = len(headings)
    
    # Generate array and fill it in
    table = zeros([ns,nv])
    i = -1
    for nm in names:
        i = i+1
        j = -1
        for key,val in refs[nm].items():
            j = j+1
            table[i,j] = val
    
    return(table)

def ref_print(refs):
    
    nms = refs
    for nm in refs.keys():
      print "Substance: " + nm
      for key,value in refs[nm].items():
          print " {:<10} = {}".format(key,value)
    
    return


### NOW STREAM CLASS ###

class substance:
    ''' 
    This class manages calculations for a given substance 
    '''

    def __init__(self):

    return

class stream:
    '''
    This class manages all values concerning a
    given stream and calculation of it's exergy.
    '''

    def __init__(self,id,mdot,T,p,composition):

        self.id = id
        self.mdot = mdot
        self.T    = T
        self.p    = p

        comp = OrderedDict()


        return





