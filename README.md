# Hello and Welcome to Fish Spectacles !
*by Grant Burley, Sello Lab UCSF*


## General Overview
This python script is designed to work in tandum with the behavioral profiling machines, 
Sauron and MCAM, here in the Sello Lab at UCSF. It reads the data files from a set 
directory structure and returns either text files with text information or pdf files 
with graphs of the desired plots. 


## How it Works
The script was designed such that minimal or no understanding of the underlying code is 
needed to use the script. Once it is called from the terminal, the user is guided 
through a prompt in which the user input is checked against known answers whenever 
possible, and if the answer is not correct, the user is prompted to reinput a response 
to the question. Once information on which files to analyze and how to analyze the 
files is gathered from the user, the files are read and primary and possibly secondary 
analysis is performed on the data. The information of these results is used to prompt 
the user on which graphs they want to make when necessary. If no further prompting is 
needed to understand what files no make, the txt or pdf file is made in their respective 
output directories. After the files are made, the user is prompted if they would like to
make more graphs from this data. If not, a new prompt is started with the old data 
deleted, else the visualization questions are reprompted. 


## Using the Script
**Before Using the Script : ** 
The user must already have the three csv files needed to analyze a run (at least for 
analyzing information from Sauron) which are the run.csv, battery_info.csv, and 
stim_frames.csv and they must be in the correct directories (see Directory Structure) 
All three of these files are available to download from the Valinor server. 

This script is designed to be called from the terminal. In the terminal, the user needs
to navigate to the Fish_Spectacles directory or start a terminal from inside the folder. 
Once in the correct location, call python to open the "Launch_Fish_Spectacles.py" file 
by typing in "python Launch_Fish_Spectacles.py" or if on a mac its better to explicity
call python3 with "python3 Launch_Fish_Spectacles.py".


## Directory Structure
The Fish_Spectacles directory should be structured as follows
Fish_Spectacles
- SauronResults 
    - PdfOutput
    - TextOutput
- SauronResources
    - LogFiles
    - SauronBatteryInfo
    - SauronRuns
    - TextBase
    - TextBaseBackup (optional)

The SauronResults directory does not need to be made, but the SauronResources
directory will need to be made if it does not exist along with its subdirectories
SauronBatteryInfo and SauronRuns. These two subdirectories will also need to be 
populated with the .csv files from the Valinor server. The SauronRuns folder 
needs the run csv which is formated as {run_number}.csv and the SauronBatteryInfo
fodler needs both the battery csv and stimulus frames csv which are fomatted as
{battery_number}_battery_info.csv and {battery_number}_stim_frames.csv respectively.

All the other directories / subdirectories will be made by the script  


## Required Python Modules not in Base Python
To use the script, these modules need to be installed if they have not already
been installed on the computer. This can be done easily with pip.
Modules (pip statement to run from terminal if needed)
- matplotlib ('pip install matplotlib')
- numpy ('pip install numpy')


## Questions or Help
Please contact Grant Burley in the Sello Lab


























































