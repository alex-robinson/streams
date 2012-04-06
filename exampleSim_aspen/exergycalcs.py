
# Import the exergy calculating functions
scriptdir = "../"
execfile(scriptdir+"streams.py")






# Load the streams from an aspen file
streams = load_aspen(fldr="./",file_in='simu1.rep')

# Calculate exergies using GATEX
E = calc_exergy_gatex(streams,gatex_exec=scriptdir+"gatex_pc_if97_mj.exe")

# Generate an ouput filename and save exergy array
savetxt('exergies.txt',E,fmt="%10.5f")
