
# Import the exergy calculating functions
scriptdir = "../"
execfile(scriptdir+"streams.py")


## First, make a new empty workbook object
book = Workbook()

# Add a sheet called "Results" to the workbook
sheet_cur = book.add_sheet('Results')

# Write some headings to the sheet
sheet_cur.write(0,0,'Ef')    # zeroth line first  column
sheet_cur.write(0,1,'Ep1')   # zeroth line second column
sheet_cur.write(0,2,'ED1')   # zeroth line third  column
sheet_cur.write(0,3,'Eff1')
sheet_cur.write(0,5,'Ep2')
sheet_cur.write(0,6,'ED2')
sheet_cur.write(0,7,'eff2')

## Now perform calculations that we will save inside the workbook
## Loop over the CombinedRes files and output exergy tables
for f_loop in range(1,6,1):
    
    # Generate the current filename
    f_in =  'CombinedRes'+str(f_loop)+'.m'
    
    # Load the stream data from the input file
    streams = load_ebsilon(file_in=f_in)

    # Calculate exergies using GATEX
    E = calc_exergy_gatex(streams,gatex_exec=scriptdir+"gatex_pc_if97_mj.exe")

    # Generate an ouput filename and save exergy array
    f_out = 'exergies'+str(f_loop)+'.txt'
    savetxt(f_out,E,fmt="%10.5f")


    # Calculate some interesting results and output to Excel ############################

    Ef   = E[7,7]
    Ep1  = E[4,7]-E[2,7]
    Ep2  = E[6,7]-E[1,7]
    ED1  = Ef - Ep1
    ED2  = Ef - Ep2
    eff1 = Ep1/Ef*1E02
    eff2 = Ep2/Ef*1E02
    
    # Write the results of the current analysis to 
    # a row corresponding to the value of f_loop
    sheet_cur.write(f_loop,0,Ef)
    sheet_cur.write(f_loop,1,Ep1)
    sheet_cur.write(f_loop,2,ED1)
    sheet_cur.write(f_loop,3,eff1)
    sheet_cur.write(f_loop,5,Ep2)
    sheet_cur.write(f_loop,6,ED2)
    sheet_cur.write(f_loop,7,eff2)

# Save the book to the actual excel file
book.save('results.xls')

