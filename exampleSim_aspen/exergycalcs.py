
# Import the exergy calculating functions
scriptdir = "../"
execfile(scriptdir+"streams.py")






# Load the streams from an aspen file
streams = load_aspen(fldr="./",file_in='simu1.rep')

# Calculate exergies using GATEX
E = calc_exergy_gatex(streams,gatex_exec=scriptdir+"gatex_pc_if97_mj.exe")

# Generate an ouput filename and save exergy array
savetxt('exergies.txt',E,fmt="%10.5f")



    Ef   = E[7,7]
    Ep1  = E[4,7]-E[2,7]
    Ep2  = E[6,7]-E[1,7]
    ED1  = Ef - Ep1
    ED2  = Ef - Ep2
    eff1 = Ep1/Ef*1E02
    eff2 = Ep2/Ef*1E02
    

