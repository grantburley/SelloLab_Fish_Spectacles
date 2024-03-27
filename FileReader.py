import os
import csv
import re

import HardInformation
from FishLog import Fish_Log


# % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % 
# HELLO, this is FileReader                       #
# # the file contains classes for reading the     #
# # different output files necessary for analysis #
# # For the sauron pipeline, this currently       #
# # involves two different classes for the three  #
# # types of files needed. The run csv has its    # 
# # own class Sauron_Run_Reader while the two     #
# # csvs containing information about the         #
# # battery, battery_info & stim_frames are read  #
# # and information appended together in the      #
# # class Sauron_Battery_Reader.                  #
# % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ %


fish_logger = Fish_Log()




class Sauron_Run_Reader():
    # % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ %
    # HELLO, this is the class Sauron_Run_Reader          #
    # # my main purpose is to read the run csv file       #
    # # # and perform minor adjustments before            # 
    # # # finalizing the class attributes                 #
    # # this class is structured such that instantiating  #
    # # # this class directs flow through several         #
    # # # functions, the init function initializes all    #
    # # # the future attributes as none and directs the   #
    # # # script flow through serval functions with       #
    # # # functions they call. init calls load_treatments #
    # # # and read_run_csv which calls                    #
    # # # treatment_interpreter which calls               #
    # # # concentration_equalizer                         #
    # # the input to this class is only the run number    #
    # # # the filepaths are made from this number         #
    # # # using a standard formatting                     #
    # # the main final attribute of this class is         #
    # # # csv_well_dict                                   #
    # # this class is used in FishBrain to get            #
    # # # information from the run csv file               #
    # % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ^ %


    final_units = 'uM'
    
    relative_concentrations = {
            'pM' : 1,
            'nM' : 1000,
            'µM' : 1000000,
            'uM' : 1000000,
            'ÂµM' : 1000000,
            'mM' : 1000000000,
            'M' :  1000000000000
        }
    

    def __init__(self, run_number):
        self.run_number = run_number # int
        self.battery_number = None # int
        self.csv_well_dict = None # dict
        self.n_frames = None # int
        self.treatments = None

        self.load_directory = 'SauronResources/SauronRuns'

        self.replaced_treatment_names = []
        self.unknown_treatments = []
        self.warning = None

        self.load_treatment_names()

        self.read_run_csv()

        fish_logger.log(Fish_Log.INFO, f"Treatment Name Replacements {', '.join(f'{well_name} replaced {old_name} : {new_name}' for well_name, old_name, new_name in self.replaced_treatment_names)}")
        
        if self.unknown_treatments:
            if not self.warning:
                self.warning = ('UNKNOWN_TREATMENT', self.unknown_treatments)
            
            #fish_logger.log(Fish_Log.WARNING, f"Could Not Find Treatment(s) {', '.join([unknwn for unknwn in self.unknown_treatments])}")
        

    def read_run_csv(self):
        run_path = f'{self.load_directory}/{self.run_number}.csv'

        if os.path.isfile(run_path):
            treatment_title = 'treatments'
            well_title = 'well_label'
            mi_start_title = '0'
            battery_id_title = 'battery_id'

            with open(run_path, 'r', encoding='latin-1') as run_csv:
                run_csv_readr = csv.reader(run_csv)
                run_titles = next(run_csv_readr)

                index = {
                treatment_title: run_titles.index(treatment_title),
                well_title: run_titles.index(well_title),
                mi_start_title: run_titles.index(mi_start_title),
                battery_id_title: run_titles.index(battery_id_title)
                }

                self.n_frames = len(run_titles) - index[mi_start_title]

                self.battery_number = next(run_csv_readr)[index[battery_id_title]]

                run_csv.seek(0)
                next(run_csv_readr)

                self.csv_well_dict = {well[index[well_title]]: ([float(val) for val in well[index[mi_start_title]:]], self.treatment_interpreter(well[index[well_title]], well[index[treatment_title]])) for well in run_csv_readr}

                fish_logger.log(Fish_Log.INFO, f'Run Path {run_path}, Number Frames {self.n_frames}, Battery Number {self.battery_number}, Run Csv Dict Made {True if self.csv_well_dict else False}')

        else:
            fish_logger.log(Fish_Log.WARNING, f'UNABLE TO FIND RUN CSV FOR {self.run_number} AT PATH {run_path}')

            self.warning = ('NO_RUN_CSV', self.run_number, self.load_directory, run_path)


    def load_treatment_names(self):
        textbase = HardInformation.Information_Textbase('TreatmentNames')
        self.treatment_dict = textbase.read_text_to_dict()
        # too large to log 


    def treatment_interpreter(self, well, treatment_str):
        treatments = []

        matches = re.findall(r'([a-zA-Z0-9_]+)\s*\(([\d.]+)([a-zA-ZÂµ]*)\)', treatment_str)
        
        for match in matches:
            treatment, concentration, units = match

            if treatment in self.treatment_dict.keys():
                self.replaced_treatment_names.append((well, treatment, self.treatment_dict[treatment]))
                treatment = self.treatment_dict[treatment]
            
            else:
                self.unknown_treatments.append((well, treatment, self.concentration_equalizer(concentration, units)))

            treatments.append((treatment, self.concentration_equalizer(concentration, units)))

        if not treatments:
            return [('solvent', 0.0)]
        else:
            return treatments

    
    @classmethod
    def concentration_equalizer(cls, concentration, units):
        return float(concentration) * cls.relative_concentrations[units] / cls.relative_concentrations[cls.final_units]




class Sauron_Battery_Reader():


    # % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ %
    # HELLO, this is the class Sauron Battery Reader  #
    # # the main purpose of this class is to read the #
    # # # two csv files with informtion about the     #
    # # # battery/asssays played to the fish,         #
    # # # battery_info and stim_frames, and to append #
    # # # the information from these two files        #
    # # # together                                    #
    # # this class is structured such that when it is #
    # # # instiated, it calls several functions. the  # 
    # # # init functions initialiazes all of the      #
    # # # final attributes of the class as None while #
    # # # calling load_assay_names, read_battery_csv, #
    # # # read_stimulus_frames_csv,                   #
    # # # battery_interpreter and finalize_info       #
    # # inputs to this class are the battery number   #
    # # # and the number of frames from the run       #
    # # # if Sauron_Run_Reader.n_frames has been set  #
    # # the main final attribute is battery_info      #
    # # # which has the "interpreted" info from both  #
    # # # csv files, the assays that were played, the #
    # # # stimuli that were played during the assay,  #
    # # # and the start and stop indexes of both of   #
    # # # these things. assays is a list of assay     #
    # # # from this attibute and is useful in         #
    # # # simplifying the code in FishHead when       #
    # # # checking user input                         #
    # # this class is used by FishBrain and the       #
    # # # attibutes are fed into many other places    #
    # % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ %


    def __init__(self, battery_number, n_frames=None):
        self.battery_number = battery_number # int
        self.n_frames = n_frames 

        self.assay_dict = None # dict

        self.raw_battery = None # list
        self.raw_stim_list = None # list
        self.battery_info = None # list
        self.assay_name_counter = {} # 
        self.battery_lines = None # list
        self.frame_rate = None # int
        self.assays = None #

        self.load_directory = 'SauronResources/SauronBatteryInfo'

        self.replaced_assay_names = []
        self.warning = None


        self.load_assay_names()

        self.read_battery_csv()

        self.read_stimuli_frames_csv()

        self.battery_interpreter()

        fish_logger.log(Fish_Log.INFO, f"Treatment Name Replacements {', '.join(f'replaced {old_name} : {new_name}' for old_name, new_name in self.replaced_assay_names)}")

        self.finalize_info()


    def is_warning_check(function_name):
        def warning_check(self, *args, **kwargs):
            if not self.warning:
                return function_name(self, *args, **kwargs)
        
        return warning_check


    @is_warning_check
    def read_battery_csv(self):
        battery_path = f'{self.load_directory}/{self.battery_number}_battery.csv'

        if os.path.isfile(battery_path):
            with open(battery_path, 'r') as battery_csv:
                battery_info = csv.reader(battery_csv)
                
                asy_nm_ttl = 'simplified_name'
                asy_st_ttl = 'start_ms'
                asy_end_ttl = 'end_ms'

                battery_titles = next(battery_info)

                btry_indx = {
                    asy_nm_ttl: battery_titles.index(asy_nm_ttl),
                    asy_st_ttl: battery_titles.index(asy_st_ttl),
                    asy_end_ttl: battery_titles.index(asy_end_ttl)
                }

                self.raw_battery = [(assay[btry_indx[asy_nm_ttl]], (int(float(assay[btry_indx[asy_st_ttl]])), int(float(assay[btry_indx[asy_end_ttl]]))) ) for assay in battery_info]

                fish_logger.log(Fish_Log.INFO, f"Battery Csv Path {battery_path}, Battery Titles {battery_titles}, Battery Csv Dict Made {True if self.raw_battery else False}")

        else:
            fish_logger.log(Fish_Log.WARNING, f"UNABLE TO FIND BATTERY CSV FOR {self.battery_number} AT PATH {battery_path}")
            self.warning = ('NO_BATTERY_CSV', self.battery_number, self.load_directory, battery_path)
            

    @is_warning_check
    def read_stimuli_frames_csv(self):
        stimuli_frames_path = f'{self.load_directory}/{self.battery_number}_stim_frames.csv'

        if os.path.isfile(stimuli_frames_path):
            with open(stimuli_frames_path, 'r') as stim_frame_csv:
                stim_frame_info = csv.reader(stim_frame_csv)
                stim_frame_titles = next(stim_frame_info)

                stim_names = [title for title in stim_frame_titles]
                stim_names.pop(0) # time units - (ms)
                
                stim_v_lst = [(int(t[0]), stim_names[i-1].replace(' ', '_')) for t in stim_frame_info for i in range(1, len(t)) if int(t[i]) > 0]

                f_stim_nms = []
                for s in stim_v_lst:
                    if s[1] not in f_stim_nms:
                        f_stim_nms.append(s[1])

                stim_dict = {}
                for key in f_stim_nms:
                    stim_dict[key] = []
                for v in stim_v_lst:
                    stim_dict[v[1]].append(v[0])

                f_stim_lst = []

                for stim in stim_dict.keys():
                    st_end = []
                    st = False
                    c = 0
                    
                    for v in stim_dict[stim]:
                        if not st:
                            st = v
                            c = v

                        if v > c + 1:
                            st_end.append(st)
                            st_end.append(c)
                            st = v
                        
                        c = v

                    st_end_tups = [(st_end[2*n], st_end[2*n+1]) for n in range(0, int(len(st_end)/2))]
                    f_stim_lst.append([stim, st_end_tups])

            self.raw_stim_list = f_stim_lst
            
            fish_logger.log(Fish_Log.INFO, f'Stim Frames Csv Path {stimuli_frames_path}, Made Raw Stim List {True if self.raw_stim_list else False}')

        else:
            fish_logger.log(Fish_Log.WARNING, f'UNABLE TO FIND STIM FRAMES CSV FOR {self.battery_number} AT PATH {stimuli_frames_path}')
            self.warning = ('NO_STIM_FRAME_CSV', self.battery_number, self.load_directory, stimuli_frames_path)


    def load_assay_names(self):
        textbase = HardInformation.Information_Textbase('AssayNames')
        self.assay_dict = textbase.read_text_to_dict()
        fish_logger.log(Fish_Log.INFO, f'AssayNames Textbase {{{", ".join(f"{key}: {value}" for key, value in self.assay_dict.items())}}}')


    @is_warning_check
    def battery_interpreter(self):
        interpretation = []

        for assay in self.raw_battery:
            assay_lst = []

            for stim in self.raw_stim_list:
                stim_lst =  [(stim[0], (ts[0], ts[1])) for ts in stim[1] if ts[0] >= assay[1][0] and ts[1] <= assay[1][1]]
                
                if not assay_lst:
                    assay_lst = stim_lst
                else:
                    assay_lst += stim_lst
                    
            assay_lst = sorted(assay_lst, key=lambda x: x[1][0])

            interpretation.append((self.assay_name_interpreter(assay[0]), assay[1], assay_lst))

        self.battery_info = interpretation

        end_ms = interpretation[-1][1][1]

        if self.n_frames:
            self.frame_rate = int(end_ms / self.n_frames)
            
            self.battery_lines = [(stim_nm, (stm_st / self.frame_rate, stm_ed / self.frame_rate)) for asy in self.battery_info 
                          if len(asy[2]) > 0 for stim_nm, (stm_st, stm_ed) in asy[2]]

        fish_logger.log(Fish_Log.INFO, f"Interpreted Battery {True if self.battery_info else False}, N Frames {self.n_frames}, Frame Rate {self.frame_rate}, Battery Lines {True if self.battery_lines else False}")


    @is_warning_check
    def finalize_info(self):
        self.assays = [f"{assay[0]}" for assay in self.battery_info]


    def assay_name_interpreter(self, raw_assay_name):
        replaced = False
        name = raw_assay_name
        if name in self.assay_dict.keys():
            replaced = True
            name = self.assay_dict[name]

        if name not in self.assay_name_counter.keys():
            self.assay_name_counter[name] = 0
            fname = name
        else:
            replaced = True
            self.assay_name_counter[name] += 1
            fname = f"{name}_{self.assay_name_counter[name]:02d}"
        
        if replaced:
            self.replaced_assay_names.append((raw_assay_name, fname))    
        
        return fname
    



class Mcam_Reader():

    # % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ %
    # HELLO, name and type 
    # # the main purpose
    # # the structure of the class
    # # inputs to the class
    # # outputs of the class
    # # uses of the class
    # % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ %


    pass