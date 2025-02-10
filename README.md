# Hello and Welcome to Fish Spectacles !
*by Grant Burley, Sello Lab UCSF*


## General Overview
This python script is designed to work in tandum with the behavioral profiling machines, 
Sauron and MCAM, here in the Sello Lab at UCSF. It reads the data files from a set 
directory structure and returns either text files with text information or pdf files 
with graphs of the desired plots. 


## How it Works
The script was designed such that minimal or no understanding of the underlying python is 
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
deleted else the visualization questions are reprompted. 


## Required Python Modules not in Base Python
To use the script, these modules need to be installed if they have not already
been installed on the computer. This can be done easily with pip.
Modules (pip statement to run from terminal if needed)
- matplotlib ('pip install matplotlib')
- numpy ('pip install numpy')


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


## Using the Script
**Before Using the Script**
The user must already have the three csv files needed to analyze a run (at least for 
analyzing information from Sauron) which are the run.csv, battery_info.csv, and 
stim_frames.csv and they must be in the correct directories (see Directory Structure) 
All three of these files are available to download from the Valinor server. 

This script is designed to be called from the terminal. In the terminal, the user needs
to navigate to the Fish_Spectacles directory or start a terminal from inside the folder. 
Once in the correct location, call python to open the "Launch_Fish_Spectacles.py" file 
by typing in "python Launch_Fish_Spectacles.py" or if on a mac its better to explicity
call python3 with "python3 Launch_Fish_Spectacles.py".

Once the file is called, you, the user, should be presented with several prompts.
- Which analysis machine data to process
    This is referring two the currently two differnt behavorial profiling instruments 
    in the sello lab, multi camera array microscope (MCAM), or Sauron.  
    This question decides which pipeline to call in FishHead
- What type of analysis to perform
    This question is about what type of data the user wants to visualize. 
    Battery and preview return text information in text documents, while technical
    and biological returns plots in pdfs as the default with optionality of making text 
    files. Technical performs the analysis within a single run while biological performs
    the analysis over multiple runs, comparing and averaging the traces for biological
    replicates.   
    This question directs which classes to instantiate in FishHead
- What run or battery number to analyze
    This question is for the number of the run or battery as reffered to by the
    Sauron system / Valinor database which are subsequently used in the file names for 
    the csv files. The run numbers and battery numbers can be found by looking in either
    of the folders within SauronResources, SauronRuns or SauronBatteryInfo, with the 
    respective formatting (run_number).csv or (run_number)_battery_info.csv / 
    (run_number)_stim_frames.csv. 
    This is used by the script to find the files to read.
- How to group the data
    This question is for how the the data should be grouped or not grouped. At the base
    level, the data is sorted by wells, with a mi trace for each. The script has the 
    capability to read the treatment info (treatment_database_identifier, concentration),
    and use this to sort the data into treatments and concentrations. The 
    treatment_database_identifier can be replaced with the correct treament name if it is
    already in the TextBase. Currently these need to manually be input into the TextBase 
    files using the HardInformation file but funtionality is inprogress to do this from 
    the terminal prompts. The script also has the functionality to automatically group 
    data for looking at error analysis. This sorts the data for a plate into its rows 
    (A-H), columns (1-12), and halves (top, bottom, left, right). (WARNING: this can
    be intensive on the cpu and take longer than normal). Finally, the script can also
    accept custom grouping of wells input by the user. The name of the grouping along 
    with which wells to include in this group and input.
- What type of calculations to perform on the data
    This questions determines if the replicates should be averaged into a single trace
    and if the mi traces should be split into assay traces and stimulus responses. If
    the data is not averaged and there are multiple replicates for a conditon, the 
    replicates will be overlaid on mi traces or plotted side by side for bar graphs. 
    If the data is split, it becomes possible to make many graphs from the data, and 
    because of this, the user will be prompted will a secondary graphing prompt to 
    determine how to make graphs. If the data is not split, this is not necessary, and 
    the plots are made after the analysis. Also, to perform secondary analysis. The 
    data will need to be split at a minimum. It is recommended to use "full" when 
    performing secondary analysis. 
    - Which, if any, secondary calculations to perform
        This question is for if secondary analysis on the primary analysis should be
        perform. Right now, only the habituation analysis is working. Habitation looks
        for recognized assays within the battery and calculates the rates of habituation
        via the slope of responses from those assays.  
- How should the file be named
    This question is for directing the name of the file to be a default naming 
    convention or to input a custom name for the file. 
- How should the plots be named
    This question is for directing the title of the plots to be a default naming 
    convention or to input a custom title for the plots.
- Should the stimuli be plotted on the mi trace
    This question is asking if the indexes for the stimuli should be overlaid on the mi 
    traces as colored vertical lines. The colors for the stimuli are as follows
    - purple LED : purple
    - soft solenoid : magenta
    - blue LED : blue
    - red LED : red
    - solenoid : light blue
    - MP3 : light green
    - green LED : green
- Do you want to view specific treatments
    This questions is asking about how many of the graphs from the data should be made.
    By answering treatment or treatment concentration, only the specific treatment or 
    treatment - concentration graphs will be made. Also for this question, use "treatment"
    if only specific wells or specific groupings are desired. The names of the treatments 
    from the run are returned to the the user when answering yes.
- Do you want to view specific assays
    If the mi traces have been split, this question is asking if the user want to only \
    plot the mi traces of individual assays and if so which assays to make the graphs for.
    The names of the assays are returned to the user for selection when answering yes.
    These graphs will be made instead of the full mi trace graphs. 
- Do you want to isolate the stimuli
    If the mi traces have been split, this question is asking if only the responses within
    the stimuli indexes should be plotted as a bar graph for each stimuli in each assay. 
    These graphs will be made instead of the full mi trace graphs.
- Do you want to view the secondary analysis
    If the mi traces have been split and a secondary analysis has been performed, this 
    question asks if the graphs made by the secondary analysis should be made. These 
    graphs will be made instead of the full mi trace graphs.





# Questions or Help
Please contact Grant Burley in the Sello Lab


























































