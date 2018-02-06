# XRF
Scripts used to process XRF data collected at synchrotrons

-----------------------------------------------------------------------------------------------------------------------------------------------
Contents:
-----------------------------------------------------------------------------------------------------------------------------------------------

1. Convert_to_h5


-----------------------------------------------------------------------------------------------------------------------------------------------
Descriptions
-----------------------------------------------------------------------------------------------------------------------------------------------

1. Convert_to_h5
This folder contains scripts used to convert XRF data recorded at the Canadian Light Source VESPERS beamline to an H5 file format such that it can be read by the data analysis program pyXRF. Two versions are included. The first is the original python script implemented via command line as follows: 
python h5conversion_0.1.py datafile1 datafile2

Here datafile1 is the ROI file that contains information regarding the step sizes used in the collection and datafile2 is the file containing the raw data. Sample data cannot be uploaded due to size restrictions. This script has been convert to a more user-friendly gui whereby the two files are selected and loaded via a browser window. The script is also implemented via the command line (python h5convert_gui.py). This has been converted into a windows x64 distributable but it is too large to upload here. 
