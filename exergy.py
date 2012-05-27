######
## Should be loaded in the pylab environment: ipython -pylab
## Call: execfile("streams.py")

import os,sys,subprocess,string
from collections import OrderedDict
import openpyxl as xl                 # For writing/reading excel files

from copy import deepcopy


def load_reference(filename="ReferenceTables.xlsx"):
    '''
    Load the reference data from the excel tables.
    '''

    # Load the workbook from existing file
    book = xl.load_workbook(filename)
    
    # Get all existing sheetnames
    sheetnames = book.get_sheet_names()
    
    # Load the reference table sheet - the first sheet
    sheet1 = book.get_sheet_by_name("SubstanceRefTables")
    
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
            refs[nm]['T0']      = T0
            refs[nm]['p0']      = p0
            refs[nm]['MW']      = sheet1.cell(row=j,column=3).value
            refs[nm]['e_ch_0a'] = sheet1.cell(row=j,column=4).value    # Ahrends
            refs[nm]['e_ch_0b'] = sheet1.cell(row=j,column=5).value    # Szargut
            refs[nm]['cp_0']    = sheet1.cell(row=j,column=7).value
            refs[nm]['h_0']     = sheet1.cell(row=j,column=8).value
            refs[nm]['s_0']     = sheet1.cell(row=j,column=9).value
            
            refs[nm]['H+']      = sheet1.cell(row=j,column=12).value
            refs[nm]['S+']      = sheet1.cell(row=j,column=13).value
            refs[nm]['a']       = sheet1.cell(row=j,column=14).value
            refs[nm]['b']       = sheet1.cell(row=j,column=15).value
            refs[nm]['c']       = sheet1.cell(row=j,column=16).value
            refs[nm]['d']       = sheet1.cell(row=j,column=17).value
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
    This class manages calculations for a given substance.
    '''

    def __init__(self,name,T,p,mdot,x,T0=298.15,p0=1.013):
        
        # Define some constants
        R = 8.314       # kJ/kmol-K, ideal gas constant
        
        # Make sure x is valid
        if x < 0 or x > 1:
            err = '''
Error:: substance:: Molar fraction must be between 0 and 1!
                    Stopping calculations.
'''
            sys.exit(err)

        # Generate the initial state of this substance in the stream
        state = OrderedDict(T=T,p=p,mdot=mdot*x,x=x)

        # Now check that we can actually model this substance
        if not name in refs.keys():
            err = '''
Error:: substance:: Substance {} not found!
                    Stopping calculations.
'''.format(name)
            sys.exit(err)
        
        # Since we know the substance exists,
        # load up the reference values here
        ref = refs[name].copy()
        #ref = deepcopy(refs[name])  # Shallow copy should be good enough since we don't modify refs!

        # Check to make sure we are using the same reference state (T0,p0)
        if not (T0 == ref['T0'] and p0 == ref['p0']):
            err = '''
Error:: substance:: Reference state for stream is different than for substance: {}
                    (T0,p0).stream    = ({:7.3f},{:7.3f})
                    (T0,p0).substance = ({:7.3f},{:7.3f})
'''.format(name,T0,p0,ref['T0'],ref['p0'])
            sys.exit(err)

        # Get a useful factor (ajr: what is this?)
        y = T/1e3

        ##### Calculations of enthalpy h 
        ##### (depends only on T, because we assume ideal gases)

        # If H+ not known for the element, then we
        # calculate it using cp_0, h_0 and T
        if ref['H+'] == None:
            state['h'] = ( (ref['cp_0']) * (T-ref['T0']) ) + ref['h_0']      # NO change in cp
        
        else:
            state['h'] = 1e3 * (  ref['H+'] + ref['a']*y 
                                + ref['b']/2 * y**2 
                                - ref['c']*y**(-1) 
                                + ref['d']/3 * y**3 )
            
            # Limit enthalpy errors
            if state['h'] > -5.0 and state['h'] < 0.0:
                print "Warning: small negative enthalpy set to zero for substance: {}".format(name)
                state['h'] = 0.0


        ##### Calculations of entropy
        ##### (depend both on T and p)

        # If H+ not known for the element, then we
        # calculate it using cp_0, h_0 and T and p
        if ref['S+'] == None:
            state['s'] = ( (ref['cp_0']/T)*(T-ref['T0']) - R*log(p/ref['p0']) ) + ref['s_0']
        
        else:
            state['s'] = (  ref['S+'] + ref['a']*log(T) + ref['b']*y 
                          - ref['c']/2 * y**(-2) 
                          + ref['d']/2 * y**2   )     - R * log(p/ref['p0'])

        ##### Calculations of specific heat cp
        ##### (depends on T)
        if ref['a'] == None:
            state['cp'] = ref['cp_0'] 
        
        else:
            state['cp'] = ( ref['a'] + ref['b']*y 
                          + ref['c'] * y**(-2) 
                          + ref['d'] * y**2 )


        # Store the output
        self.name  = name
        self.state = state
        self.ref   = ref

        return
        
    def __str__(self):
        '''Output the substance object to the screen in a human readable way.'''
        
        text = "Substance: " + self.name
         
        for key,value in self.state.items():
            text = text + "\n {:<12} = {:>12.7n}".format(key,float(value))
        
        text = text +  "\n====== reference values ======"
        for key,value in self.ref.items():
            text = text + "\n {:<12} = {:>12.7n}".format(key,float(value))

        return text 


class stream:
    '''
    This class manages all values concerning a
    given stream and calculation of it's exergy.
    '''

    def __init__(self,id,T,p,mdot,composition,T0=298.15,p0=1.013):
        '''
        Initialize a stream
          id = stream number/name
          T  = stream temperature
          p  = stream pressure
          mdot = stream total mass flow rate kg/hr ?
          composition = list of substances and molar fractions x 
                        ( a list of tuples: [ ('N2',0.5), ('O2',0.1) ] )
          T0, p0 = reference state values for temp (K) and pressure (bar)
        '''
        
        ### TO DO ###
        # Implement optional arguments of an array row containing
        # all stream info and an array row containing the header
        # Then extract the info as needed for this class.
        #############
        
        # First store the state
        state = OrderedDict(T=T,p=p,mdot=mdot,T0=T0,p0=p0)

        ## Loop over the substances and initialize each
        ## one for the current stream state
        comp = OrderedDict()
        for name,x in composition:
            comp[name] = substance(name,T=T,p=p,mdot=mdot,x=x,T0=T0,p0=p0)
        
        ## Determine what kind of stream we have (H2O or not, flue gas or not)
        isH2O = True 
        for key in comp.keys():
            if not key in ['H2O(l)','H2O(g)']:
                isH2O = False
                break
        
        ## Handling water ##
        ## Make sure that if a stream has H2O(l), it also has H2O(g) and vice-versa
        ## (This will facilitate calculations later involving liquid and gas)
        if 'H2O(l)' in comp.keys() and not 'H2O' in comp.keys():
            comp['H2O'] = substance('H2O',T=T,p=p,mdot=mdot,x=0.0,T0=T0,p0=p0)
        if 'H2O' in comp.keys() and not 'H2O(l)' in comp.keys():
            comp['H2O(l)'] = substance('H2O(l)',T=T,p=p,mdot=mdot,x=0.0,T0=T0,p0=p0)
        
        # Make a duplicate list of stream substances
        # that will be adjusted for calculating the standard (T0,p0) values
        comp0 = deepcopy(comp)
        
        ## If stream is flue gas, adjust water percentages
        ## (For now, always adjust since we don't know how to tell
        ##  if it's flue gas or not)
        # At 25C the pressure would be 0.0317bar, so:
        # x_H2O_new(g) = ( 0.0317 * ( 1- x_H2O ) ) / (1 - 0.0317)         # % mol
        # x_H2O(l) = x_H2O(l) + (x_H2O - x_H2O_new(g))
        if 'H2O(l)' in comp0.keys():
            x_l = comp0['H2O(l)'].state['x']
            x_g = comp0['H2O'].state['x']
            x       = x_l + x_g
            if x > 0.0:
                x_new_g = 0.0317*(1.0-x) / (1.0-0.0317)    # mol frac
                x_new_g = max(x_new_g,0.0)
                x_new_l = (x - x_new_g)                    # mol frac
                x_new_l = max(x_new_l,0.0)
                comp0['H2O(l)'].state['x'] = x_new_l
                comp0['H2O'].state['x']    = x_new_g

                print "(x_l,x_g).old = ({:5.3f},{:5.3f})".format(x_l,x_g)
                print "(x_l,x_g).new = ({:5.3f},{:5.3f})".format(x_new_l,x_new_g)
                
            if not (comp0['H2O(l)'].state['x'] + comp0['H2O'].state['x'] 
                ==  comp['H2O(l)'].state['x'] +  comp['H2O'].state['x']):
                err = '''
Error:: stream:: Corrected H2O molar fractions do not sum to original total!
'''
                sys.exit(err)
        
        ## Calculate MW of the stream
        state['MW'] = 0.0
        for key,sub in comp.items():
            state['MW'] = state['MW'] + ( sub.ref['MW']*sub.state['x'] )

        ## Calculate enthalpy (h) and entropy (s) depending on type of stream
        if not isH2O:
            
            # Enthalpy and entropy
            state['h']    = 0.0    # Enthalpy at T for mixture 
            state['h_0']  = 0.0    # Enthalpy at T0 for mixture
            state['s']    = 0.0    # Entropy at T for mixture
            state['s_0']  = 0.0    # Entropy at T0 for mixture
        
            # Loop over elements and get stream variables
            for key,sub in comp.items():
                state['h']   = state['h']   + ( sub.state['h']*sub.state['x'] )
                state['s']   = state['s']   + ( sub.state['s']*sub.state['x'] )
            
            # Loop over standard (T0,p0) elements and get stream variables
            for key,sub in comp0.items(): 
                state['h_0'] = state['h_0'] + ( sub.ref['h_0']*sub.state['x'] )    
                state['s_0'] = state['s_0'] + ( sub.ref['s_0']*sub.state['x'] )             

            
        else:   # Case 2: water stream, H2O(l) and/or H2O(g)
            
            #!!!! CHECK IF WE HAVE SATURATED WATER OR STEAM  !!!!!
            isSaturated = False
            ## ADD TEST HERE

            if isSaturated:
                # Calculate enthalpy from the IAPWS IF97 steam tables for saturated streams
                ## TO BE IMPLEMENTED !!!
                pass

            else:  # Not saturated, calculate here...
                
                # Copy enthalpy and entropy from the IAPWS IF97 steam tables for non-saturated streams
                # h_T_str  = ( (cp_T_el - cp_T0_el) * (T_str-T0) ) + h_T0_el        # here el: H2O
                # s_Tp_str = ( (cp_T_el - cp_T0_el) * ln(T_str/T0) + s_Tp0_el
                pass

        ####

        self.id    = id
        self.state = state
        self.comp  = comp 
        self.comp0 = comp0

        return

    def calc_exergy(self,exergy_type="Ahrends"):
        '''
        Calculation of exergies given the state of 
        a stream.
        '''
        
        # Define some constants
        R = 8.314       # kJ/kmol-K, ideal gas constant
        
        # Decide which chemical exergy value to use (Ahrends or Szargut)
        if exergy_type == "Ahrends":
            name_ch = 'e_ch_0a'
        elif exergy_type == "Szargut":
            name_ch = 'e_ch_0b'
        else:
            err = '''
Error:: substance:: Incorrect exergy type given: {}
                    Only "Ahrends" or "Szargut" are allowed.
'''.format(exergy_type)
            sys.exit(err)


        # Open variables locally
        state = self.state
        comp  = self.comp 

        ## PHYSICAL EXERGY
        # Physical specific exergy of stream  ###
        state['e_ph']    = ( state['h']-state['h_0'] 
                           - state['T0']*(state['s']-state['s_0']) )    # kJ/kmol
        
        # Limit e_ph to postive values and/or give warnings
        if state['e_ph'] < -5.0:
            print "Warning: negative physical exergy for stream {}".format(self.id)
        elif state['e_ph'] < 0.0:
            state['e_ph'] = 0.0


        ## CHEMICAL EXERGY
        # Chemical specific exergy of stream ###
        sum1 = 0.0
        sum2 = 0.0
        for key,sub in comp.items():
            if not sub.state['x'] == 0.0:
                sum1 = sum1 + ( sub.ref[name_ch]*sub.state['x'] )
                sum2 = sum2 + ( sub.state['x']*log(sub.state['x']) )

        state['e_ch']    = sum1 + R*state['T0']*sum2           # kJ/kmol
        
        
        ## Convert exergies to per kg
        state['e_ph_kg'] = state['e_ph'] /state['MW']          # kJ/kg
        state['e_ch_kg'] = state['e_ch'] /state['MW']          # kJ/kg
        
        ## Get absolute exergies (in MW)
        state['E_ph'] = state['e_ph_kg'] *state['mdot']/1e3    # MW
        state['E_ch'] = state['e_ch_kg'] *state['mdot']/1e3    # MW

        ## TOTAL EXERGY

        # Specific
        state['e_tot_kg'] = state['e_ph_kg'] + state['e_ch_kg']   # KJ/kg
        
        # Absolute
        state['E_tot'] = state['E_ph'] + state['E_ch']            # MW
        
        E_tot_check = state['e_tot_kg'] * state['mdot'] /1e3      # MW
        
        ebs = 1e-5
        if not abs(state['E_tot']-E_tot_check) < ebs:
            err = '''
                  Warning:: calc_exergy::
                  Total exergy calculations do not match:
                  E_ph + E_ch != e_tot_kg * mdot
                  {:10.3f} + {:10.3f} != {:10.3f} * {:10.3f}
                  '''.format(state['E_ph'],state['E_ch'],state['e_tot_kg'],state['mdot']/1e3)
            

            #sys.exit(err)
            print err
        
        # Update the stream's state object
        self.state = state 

        return
    
    def __repr__(self):
        
        text = "Stream: {}".format(self.id)
         
        for key,value in self.state.items():
            text = text + "\n {:<12} = {:>12.7n}".format(key,float(value))

        return text

    def __str__(self):
        '''Output the stream object to the screen in a human readable way.'''
        
        text = "Stream: {}".format(self.id)
         
        for key,value in self.state.items():
            text = text + "\n {:<12} = {:>12.7n}".format(key,float(value))
        
        # text = text +  "\n====== reference values ======"
        # for key,value in self.ref.items():
        #     text = text + "\n {:<12} = {:>12.7n}".format(key,float(value))

        return text 


### SIMULATION CLASS ###
class simulation(stream):
    '''This class holds all simulation information in the
       proper format. This can be read in from an excel file 
       or original formats from aspen (not implemented) or ebsilon (not implemented)
       The simulation data is held in stream classes.
    '''
    
    def __init__(self,filename="../ReferenceTables.xlsx",sheetname="ExampleStreams1"):
        '''Initialize the simulation'''
        
        ## Check file extension to see which type of data to load

        self.streams = self.load_excel(filename=filename,sheetname=sheetname)

        return 
    
    def load_excel(self,filename="../ReferenceTables.xlsx",sheetname="ExampleStreams1"):
        '''Load the simulation data from an excel sheet.'''

        # Load the workbook from existing file
        book = xl.load_workbook(filename)
        
        # Get all existing sheetnames
        sheetnames = book.get_sheet_names()
        
        # Make sure the sheet exists!
        if not sheetname in sheetnames:
            err = '''
Error:: load_excel:: Desired sheetname {} does not exist in the workbook {}.
'''.format(filename,sheetname)
            sys.exit(err)

        # Load the simulation sheet
        sheet1 = book.get_sheet_by_name(sheetname)
        
        #### Begin loading simulation data

        streams = OrderedDict()

        for j in arange(1,1000):
            
            # First see if this row has a substance
            streamid = sheet1.cell(row=j,column=0).value

            # If an element was actually found in this row,
            # load all the data and generate a new stream object
            if not streamid == None:
                mdot      = sheet1.cell(row=j,column=7).value
                T         = sheet1.cell(row=j,column=8).value
                p         = sheet1.cell(row=j,column=9).value
                
                # Now loop over substances
                comp = []
                for i in arange(0,200):
                    
                    name = sheet1.cell(row=0,column=11+i).value
                    
                    if not name == None:
                        x = sheet1.cell(row=j,column=11+i).value
                        if x == None: x = 0
                        #print i,j,name,x
                        comp.append( (name,x) )
                    else:
                        break

                # Now we have loaded the state variables and 
                # the composition, so generate a stream object
                streamidstr = "{}".format(streamid)
                streams[streamidstr] = stream(id=streamid,T=T,p=p,mdot=mdot,composition=comp)
                streams[streamidstr].calc_exergy()

            else:
                break

        return streams
    
    def __str__(self):
        '''Print out the handy simulation.'''
        
        text = ""

        for key,stream in self.streams.items():
            text = text + "\n" + repr(stream)


        return text


