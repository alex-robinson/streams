######
## Should be loaded in the pylab environment: ipython -pylab
## Call: execfile("streams.py")

import os,sys,subprocess,string
from collections import OrderedDict
import openpyxl as xl                 # For writing/reading excel files

import exergy as ex

from thermopy import iapws
from thermopy import nasa9polynomials as nasa9

#import exergy
#import streams

# First, define the central script directory and
# location of gatex.exe and the streams.py functions
# CHANGE THIS TO THE LOCATION ON YOUR COMPUTER:
SCRIPTDIR = "/Users/robinson/models/streams/"

# Now define locations of gatex and streams.py
#STREAMS   = os.path.join(SCRIPTDIR, "streams.py")
#EXERGY    = os.path.join(SCRIPTDIR, "exergy.py")

# And import the needed exergy calculating functions
#exec(open(STREAMS).read())
#exec(open(EXERGY).read())

# Load reference substance values
ref_file = SCRIPTDIR + "/" + "ReferenceTables.xlsx"
refs = ex.load_reference(ref_file)

filename_in  = "ExampleSimulation.xlsx"
filename_out = filename_in
sheetname    = "ExampleStreams1"
sheetname_out = "gatex"

# filename_in   = "h2_prod_exergy_v7.rep"
# filename_out  = "AspenSimulation_v7b.xlsx"
# sheetname     = "Streams"
# sheetname_out = "gatex"

########
## BELOW HERE, begin the
## individual calculations
########

## Test thermopy steamtables
x = iapws.Water(p=1013.0,T=298.15)
print("H2O: T = {}, P = {}, H = {}".format(x.T,x.p,x.enthalpy()))

ndb = nasa9.Database()
element = ndb.set_compound('C8H18,n-octane')
print("element {}: H_formation = {}, cp(T=298.15) = {}, Molecular weight = {}".format(element.inp_name,element.enthalpy_of_formation,element.heat_capacity(298.15),element.molecular_weight))

sys.exit()

## Test cases

if True:
    s1 = ex.stream(id=1,T=298.15,p=1.013,mdot=1,composition=[('CH4',1)],exergy_type="Ahrends")
    s2 = ex.stream(id=1,T=298.15,p=1.013,mdot=1,composition=[('CH4',1)],exergy_type="gatex")

    # s1.calc_exergy(exergy_type="Ahrends")
    # s2.calc_exergy_gatex(gatex_exec="../gatex_pc_if97_mj.exe")

    print(s1)
    print("\n ======= \n")
    print(s2)

if False:

    temps = arange(270,331)
    eph1  = []
    eph2  = []

    for temp in temps:

        ## Test cases
        s1 = ex.stream(id=1,T=temp,p=1.013,mdot=1,composition=[('CH4',1.0)])
        s2 = ex.stream(id=2,T=temp,p=1.013,mdot=1,composition=[('CH4',1.0)])

        s1.calc_exergy(exergy_type="Ahrends")
        s2.calc_exergy_gatex(gatex_exec="../gatex_pc_if97_mj.exe")

        eph1.append(s1.state['E_ph'])
        eph2.append(s2.state['E_ph'])

    for k,val in enumerate(temps):
        print(val,eph1[k],eph2[k])

#s2 = stream(id=2,T=473.15,p=10.0,mdot=1,composition=[('O2',0.21),('N2',0.79)])
#s3 = stream(id=2,T=1929.15,p=10.0,mdot=1,composition=[('O2',0.064),('N2',0.738),('CO2',0.066),('H2O',0.132)])

# s4 = stream(id=1,T=1520.0,p=9.412,mdot=92.92,
#        composition=[('N2',0.7507),('O2',0.1372),('CO2',0.0314),('H2O',0.0807)])
# s4.calc_exergy(exergy_type="Ahrends")

# s5 = stream(id='1',T=560.6371+273.15,p=124.0,mdot=65.2099,
#        composition=[('H2O',1.0)])
# sim5 = simulation(stream=s5,exergy_type="gatex")

# s5.calc_exergy(exergy_type="Ahrends")
# s5.calc_exergy_gatex(exergy_type="Ahrends")

# sim0 = simulation(filename="ExampleSimulation.xlsx",sheetname="H2Ostreams",
#                   exergy_method="gatex")

# ## Test loading a simulation and calculating exergies
# sim1 = simulation(filename=filename_in,sheetname=sheetname,
#                   exergy_method="gatex",exergy_type="ahrends",
#                   saturated_water=['65'],saturated_steam=['55'])
#
# ## Write results to Excel
# sim1.write_excel(filename=filename_out,sheetname=sheetname_out)



## Check stream 6
# comp = sim1.streams['6'].comp0
# tot = 0.0
# print "{:>12} {:>10} {:>12} {:>12}".format("Substance","x","h_0","x*h_0")
# for key,sub in comp.items():
#     tmp = sub.state['x']*sub.ref['h_0']
#     tot = tot + tmp
#     print "{:>12} {:10.5g} {:12.5g} {:12.5g}".format(key,sub.state['x'],sub.ref['h_0'],tmp)
# print "TOTAL = ",tot
