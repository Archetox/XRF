# XRF
Scripts used to process XRF data collected at synchrotrons

--------------------------------------------------------------------------------------------------------------------------------------------
Contents:
--------------------------------------------------------------------------------------------------------------------------------------------

1. Convert_to_h5
2. Transformtxt
3. Matlab-scripts

--------------------------------------------------------------------------------------------------------------------------------------------
Descriptions:
--------------------------------------------------------------------------------------------------------------------------------------------
1. Convert_to_h5

This folder contains scripts used to convert XRF data recorded at the Canadian Light Source VESPERS beamline to an H5 file format such that it can be read by the data analysis program pyXRF. Two versions are included. The first is the original python script implemented via command line as follows: 

python h5conversion_0.2.py datafile1 datafile2

Here datafile1 is the ROI file that contains information regarding the step sizes used in the collection and datafile2 is the file containing the raw data. Sample data cannot be uploaded due to size restrictions. This script has been convert to a more user-friendly gui whereby the two files are selected and loaded via a browser window. The script is also implemented via the command line (python h5convert_gui.py). This has been converted into a windows x64 distributable but it is too large to upload here. NOTE: h5conversion_0.2.py is more updated than the gui in that it is able to determine if data is in the correct format.

2. Transformtxt

This folder contains scripts used to concatenate files output from pyXRF into a single csv file such that it can be plot in Origin. The script is implement from the command line and needs to be run in the folder containing the output data files. The script just needs to be run - no additional arguments are needed. The folder contains sample data obtained from pyXRF analysis on data obtained from the Canadian Light Sources VESPERS beamline and from the Brookhaven National Synchrotron Light Source SRX beamline. The script automatically determines which beamline the data has been obtained from by identifying the names of the normalization files which differ between the two.

3. Matlab-scripts

This folder contains two Matlab scripts which allow XRF data obtained from synchrotrons to be visualized using Matlab. The two scripts are run sequentially, first importxrfdata.m followed by plotxrfdata. The former prompts the user to select an element to visualize, following which it loads the data file (obtained after pyXRF deconvolution). It normalizes the data (using a filename that must be changed depending on whether CLS or NSLS was used to record the data) and then creates a frequency distribution of the values that are used to determine the upper and lower limits necessary for the plot. Once complete, the second script plots the normalized data using the upper and lower limits specficied from the user (which is obtained by looking at the frequency distribution). The number of contour levels is also specified for by the user.
