
#
# This script converts transforms and normalizes data recorded at CLS into a single csv file for analysis
#
import numpy as np
import sys
import csv
import glob, os
from linecache import getline
#

############################################################################################################
####					 Definitions 							####
############################################################################################################

def transform(normfile):

    os.chdir("./")						# Place file names into lists
    datafiles = glob.glob("detsum*_K.txt") + glob.glob("detsum*_L.txt")
    xyfiles = glob.glob("*_pos.txt")
    ionfiles = glob.glob(normfile)

    ionlist = []
    xylist = []
    datalist = []
    counter = 0

    for i in ionfiles:						# Read ion chamber files and store each value in 
        ionlist.append([])                                      # separate line of array
        ionlist[counter].append(i)
        
        with open(i) as f:
             for line in f:
                 a = line.split()
                 for word in a:
                     ionlist[counter].append(word)

        f.close()
        counter = counter + 1
   
    counter = 0

    for i in xyfiles:						# Read xy position files and store each value in 
        xylist.append([])	                                # separate line of array
        xylist[counter].append(i)
        
        with open(i) as f:
             for line in f:
                 a = line.split()
                 for word in a:
                     xylist[counter].append(word)

        f.close()
        counter = counter + 1

    counter = 0

    for i in datafiles:						# Read detsum data files and store each value in 
        datalist.append([])	                                # separate line of array
        datalist[counter].append(i)
        
        with open(i) as f:
             for line in f:
                 a = line.split()
                 for word in a:
                     datalist[counter].append(word)

        f.close()
        counter = counter + 1

    normlist = []
  
    for i in range(0,len(datalist)):				# Normalize detsum data and place values in new array
        normlist.append([])
        j = "norm_" + datalist[i][0]
        normlist[i].append(j)

        for k in range(1,len(datalist[i])):
            a = float(datalist[i][k])
            b = float(ionlist[0][k])
            
            if b == 0.0:					# Overcomes division by 0 error when data glitches in 
               c = 0.0  					# miniion are present
            else:
               c = a / b

            d = str(c)
            normlist[i].append(d)   
   
    alllists = ionlist + xylist + datalist + normlist		# Concatenates all data into a single list
    formlists = zip(*alllists)            			# Transposes list: This is necessary in order
								# to properly format the data. E.g. the headers of
								# each column now becomes one column with each row a
     								# a header. CSV can only write row by row thus is required.

    with open("alldata.csv", "wb") as f:			# Write the data to a csv file.
        writer = csv.writer(f)
        writer.writerows(formlists)
 

    return ()

############################################################################################################
####					 Start of Script						####
############################################################################################################

os.chdir("./")
textfiles = glob.glob("*.txt")

CLSnormfile = 'MiniIon.txt'
CLSnormfile2 = 'currentminiion.txt'
NSLSnormfile = 'current_preamp_ch0.txt'
NSLSnormfileJul2017 = 'sclr_i0.txt'

if  CLSnormfile in textfiles:
    transform(CLSnormfile) 
elif  CLSnormfile2 in textfiles:
    transform(CLSnormfile2) 
elif  NSLSnormfile in textfiles:
    transform(NSLSnormfile) 
elif  NSLSnormfileJul2017 in textfiles:
    transform(NSLSnormfileJul2017) 
else:
    print("Cannot determine which synchrotron data was collected from and thus cannot continue - Sorry!")
    sys.exit()

 


