streams
=======

Exergy calculations for streams

Currently there are two versions of the code. The first version is a set of functions 
that allow the calculation of exergies from Ebsilon or Aspen model output (streams.py). 
The second version is an object-oriented framework for working with streams and exergies 
that can calculate exergy internally without using Gatex (exergy.py). streams.py has
been tested using various simulations and seems to work robustly. exergy.py still shows
some flaws and needs to be thoroughly debugged and tested before it can be used.

In the long run, it is desirable to switch to the exergy.py code and abandon the more
simplistic streams.py implementation. 

After downloading the repository, the streams repository should be stored in a central
path on the computer. This path is referred to as the `SCRIPTDIR`. 

Using streams.py
================

To use streams.py to calculate exergies for a given simulation (or set of simulations), copy 
exergycalcs.py from exampleSim_ebsilon/ to your output directory. 

Edit the file to make sure that the `SCRIPTDIR` is correct for your machine, that the 
simulation output filenames are correct (e.g., CombinedRes1.m), that the number of streams
is properly defined (e.g., `n_streams = 33`) and that any specific component calculations
make sense for this simulation. 

Once exergycalcs.py has been updated, in the simulation output directory open ipython in pylab mode
and execute the script:

    ipython --pylab 
    execfile("exergycalcs.py")
  
This should generate the exergy calculations in an output Excel file "Results.xlsx".

Using exergy.py
===============

To do !
