
#
# This script converts data recorded at CLS to h5 format for analysis in PyXRF
#
import h5py
import numpy as np
import sys
from linecache import getline
#
############################################################################################################
####		Obtain file names to convert and abort if not provided					####
############################################################################################################

if len(sys.argv) < 3:
    print "Incorrect input provided. Too few file names provided." 
    print "Script is run as follows (excluding brackets): python h5convert.py [text file name] [Vortex file name]"
    sys.exit()

if len(sys.argv) >= 4:
    print "Incorrect input provided. Too many file names provided." 
    print "Script is run as follows (excluding brackets): python h5convert.py [text file name] [Vortex file name]"
    sys.exit()

textfile = sys.argv[1]
countfile = sys.argv[2]

############################################################################################################
####					 Definitions 							####
############################################################################################################

# Determining correct format of countfile
def validate_file(filename):

    with open(filename, 'r') as F:
        for i, l in enumerate(F):
            pass
    return i + 1

# Setting up empty h5 file structure
def h5init ( textfile ):

    if textfile.endswith('.dat'):
        h5name = textfile[:-4] + '.h5'
   
    h5file = h5py.File(h5name,'w')
    root = h5file.create_group("xrfmap")
    subroot4 = h5file.create_group("/xrfmap/detsum")
    subroot5 = h5file.create_group("/xrfmap/positions")
    subroot6 = h5file.create_group("/xrfmap/scalers")

    h5file.close()

    return ( h5name )

# Determine the number of x and y steps
def xyno ( textfile, countfile ):                                 

    with open(textfile) as f:
         for ind, line in enumerate(f,1):                         #Loop to find where numeric data starts
             if not line.strip():                                 # It looks for the first blank line and
                break                                             # it's line number is stored in "ind" 

    xlist = []
    ylist = []

    with open(textfile) as g:
         for ind2, line in enumerate(g,1):                        #Loop that skips all header lines and
            if ind2 > ind:                                        # stores x and y positions into variables
               b = line.split()
               if len(b) > 1:                                     #Prevents crash when line is empty (esp at end of document)
                  xpos = b[0]                                     #H column
                  ypos = b[1]                                     #V column
                  xlist.append(xpos)                              #Appends positions to temporary storage lists
                  ylist.append(ypos)

    xstart = float(xlist[0])                                      #X start position
    xend = float(xlist[-1])                                       #X end position
    xstep = float(xlist[1]) - float(xlist[0])                     #Step size interval (assumed to be the same for y)
    ystart = float(ylist[0])                                      #Y start position
    yend = float(ylist[-1])                                       #Y end position

    xno = round( (xend - xstart) / xstep ) + 1                    #Number of steps in the x direction
    yno = round( (yend - ystart) / xstep ) + 1                    #Number of steps in the y direction

    print "Number of steps in the x direction: %s" %(xno)
    print "Number of steps in the y direction: %s" %(yno)

    return (xno, yno)

# Create 3D array of x and y positions
def xypos ( textfile, xno, yno ):

    xlist = []                                                    #Temporary lists to store x positions
    ylist = []                                                    #Temporary lists to store y positions

    with open(textfile) as f:
         for ind, line in enumerate(f,1):                         #Loop to find where numeric data starts
             if not line.strip():                                 # It looks for the first blank line and
                break                                             # it's line number is stored in "ind" 

    with open(textfile) as g:
         for ind2, line in enumerate(g,1):                        #Loop that skips all header lines and
            if ind2 > ind:                                        # stores x and y positions into variables
               b = line.split()
               if len(b) > 1:                                     #Prevents crash when line is empty (esp at end of document)
                  xpos = b[2]                                     #SampleHFeedback column
                  ypos = b[3]                                     #SampleVFeedback column
                  xlist.append(xpos)                              #Appends positions to temporary storage lists
                  ylist.append(ypos) 

    positions = np.empty((2,yno,xno))                             #Create empty 3D array to fill with positions  
               							  #Dimensions are based on the number of x and y steps
    for i in range(0,xno,1):                                      #Creates tables in h5 file
         n = i
         for j in range(0,yno,1):                                 #Creates rows and columns in h5 file
             positions[0,j,i] = float(xlist[n])                   #Populate with unvarying x-values
             positions[1,j,i] = float(ylist[n])                   #Populate with varying y-values
             n = n + xno                                          #Necessary to skip to rows in text file with fixed x-values
                                                                  # Text file is formatted with sequential y-values, hence necessary to skip by xno
    return positions 

# Create 3D array of counts from the detector
def deccount ( countfile, xno, yno, eno ):

    ecounts = np.empty((yno,xno,eno))                             #Creates empty 3D array. X values = cols, y values = rows, per energy value 
    n = 0                                                         #Initializing energy count

    with open(countfile) as g:                                    #Opens count file. Structure of count file is rows = energy,
         for line in g:                                           # columns = counts for each x,y position.
             z = 0                                                # Reads file line by line (i.e. reads counts for each energy value).
             a = line.split()                                     # Separates counts for a given x,y position.
             for i in range(0,yno,1):                             # Loops through counts and populates 3D array, filling each column of a row first
                 for j in range(0,xno,1):                         # then moves to next row and fills columns until all counts are assigned to the
                     ecounts[i,j,n] = float(a[z])                 # 2D matrix. The energy value is then changed and the next 2D matrix populated
                     z = z + 1
                     
             n = n + 1

    return ecounts

# Create 3D array of scalers
def scalarcount (textfile, xno, yno):
 
    scalarlist = []                                               #Temporary storage list

    with open(textfile) as f:
         for ind, line in enumerate(f,1):                         #Loop to find where numeric data starts
             if not line.strip():                                 # It looks for the first blank line and
                break                                             # it's line number is stored in "ind" 

    with open(textfile) as g:
         for ind2, line in enumerate(g,1):                        #Loop that skips all header lines and
             if ind2 > ind:                                       # stores scaler values into a list
                b = line.split()
                if len(b) > 1:                                    #Prevents crash when line is empty (esp at end of document)
                    scal = b[6]                                   #MiniIonChamber column
                    scalarlist.append(scal)                       #Appends values to temporary storage lists

    scalars = np.empty((yno,xno,1))                               #Create empty 3D array to fill with scaler values  
               							  #Dimensions are based on the number of x and y steps
    n = 0
    for i in range(0,yno,1):                                      #Places values in temporary list into array.
         for j in range(0,xno,1):                                 # List is read sequentially, array is populated by
             scalars[i,j,0] = float(scalarlist[n])                # placing values in columns of a given row and then
             n = n + 1                                            # incrementing the row and repeating until all values
                                                                  # are assigned.
    return scalars

############################################################################################################
####					 Start of Script						####
############################################################################################################

# Establishing valid data format
if validate_file(countfile) != 2048:
    print('The data in "%s" appears to be invalid. The number of rows should be 2048. Please reformat your data file by transposing the values.' % countfile)
    sys.exit()

# Determining number of x and y steps and number of energy values
#
xynoout = xyno ( textfile, countfile )                            #Determines number of steps and makes them global variables
xno = int(round(xynoout[0]))
yno = int(round(xynoout[1]))

with open(countfile) as f:                                        #Determines the number of energy values used
     eno = sum(1 for line in f)

# Extracting x,y positions, energy counts and scalers from CLS data
#
positions = xypos ( textfile, xno, yno )                          #Obtain 3D array filled with x and y positions from text file
ecounts = deccount ( countfile, xno, yno, eno )                   #Obtain 3D array filled with detector counts for x,y positions at each energy value
scalars = scalarcount ( textfile, xno, yno)                       #Obtain 3D array filled with scalers for x,y positions
nularray = np.empty((yno,xno,eno))                                #Create empty array to pad 2nd and 3rd detector counts in h5 file

# Setting up and populating H5 file
#
h5name = h5init ( textfile )					  #Sets up h5 file and returns its name as a global variable

h5file = h5py.File(h5name,'r+')                                   #Open h5 file and write new datasets with correct dimensions

dset1 = h5file.create_dataset("/xrfmap/positions/pos", (2,yno,xno), dtype = "f")
dset5 = h5file.create_dataset("/xrfmap/detsum/counts", (yno,xno,eno), dtype = "f")
dset6 = h5file.create_dataset("/xrfmap/scalers/val", (yno,xno,1), dtype = "f")

dset1[...] = positions                                            #Fill dataset with x,y-positions
dset5[...] = ecounts                                              #Fill dataset with counts from the detector
dset6[...] = scalars                                              #Fill dataset with x,y-positions

# Creating notes and attributes in H5 file
#                                                               
dset11 = h5file.create_dataset("/xrfmap/positions/name", (2,), dtype = "S20")		#Create new dataset with type string (20 characters)
dset16 = h5file.create_dataset("/xrfmap/scalers/name", (1,), dtype = "S20")             #Create new dataset with type string (20 characters)

scalarname = [] 									#Creating a list in which headings will go
scalarname.append("MiniIon")
dset16[...] = scalarname								#Populating the dataset with heading names

posname = []										#Creating a list in which headings will go
posname.append("x_pos")                                                                                                            
posname.append("y_pos")                                                                                                            
dset11[...] = posname                                                                   #Populating the dataset with heading names

dset25 = h5file["/xrfmap/detsum/counts"]                                                #Defining datasets which attributes will be added to
attr_string25 = "Experimental data from channel sum"                                    #Specifying attribute string
dset25.attrs["comments"] = attr_string25                                                #Adding attribute to datasets

h5file.close()


