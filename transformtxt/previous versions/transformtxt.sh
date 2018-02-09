#!/bin/bash
#
##################################################################################################################
# Formats data obtained from PyXRF into a single column (csv file) which can then be used to plot in Origin 
#
# Type ./transformtxt.sh in the folder with txt file. 
#
# Note all txt files will be read so make sure only data txt file are present  
##################################################################################################################

### Obtaining path informtion

#txtfiles=`ls *.txt | awk -F'.' '{print $1}'`

detsum=`ls detsum*.txt | awk -F'.' '{print $1}'`
current=`ls current*.txt | awk -F'.' '{print $1}'`
pos=`ls *pos.txt | awk -F'.' '{print $1}'`

txtfiles=`echo $detsum $current $pos`

for i in $txtfiles
  do
  
    echo $i > $i".tmp"
 
    while read line
     do

       for number in $line
        do
          
          echo $number >> $i".tmp"

        done
       

     done < $i".txt"

  done

### Combining all files into one

paste -d ',' *.tmp > alldata.csv

rm *.tmp

