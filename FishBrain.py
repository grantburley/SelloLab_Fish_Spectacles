import FileReader
import DataAnalysis
import DataVisualization
from HardInformation import Information_Textbase


# % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % 
# HELLO, this is FishBrain                        #
# # the main purpose of this file is to use the   #
# # user responses from FishHead to direct flow   #
# # through the code. The dictionary of user      #
# # responses is unpacked and fed into other      #
# # files/classes as needed                       #
# % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ %




class Fish_Analysis():
    # % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ %
    # HELLO, this is the class Fish_Analysis          #
    # # the main purpose of this class is to          #
    # # # determine what functions to call and        #
    # # # classes to instantiate depending on the     #
    # # # user input from FishHead                    #
    # # this class is structured such that when it    #
    # # # is instantiated, it determines the logic of #
    # # # which functions to call for file reading    #
    # # # and data analysis. There is a function,     #
    # # # visualize_information, which works          #
    # # # independently and is used to call the       #
    # # # correct class in DataVisualization          #
    # # the inputs to this class are the              #
    # # # user_response_dict and the split_str which  #
    # # # is used to separate the user reponses of    #
    # # # treatment and concentration in a single     #
    # # # string                                      #
    # # the only minor output of this class is        #
    # # # transfer some information about availibily  #
    # # # of graphs to make. There is no real output  #
    # # # from this class                             #
    # # this class is used to direct logic throught   #
    # # # the rest of the script                      #
    # % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ %
    

    def __init__(self, user_response_dict, split_str):
        self.subconscious_warnings = ["NO_STIM"]
        self.no_stim_i = 0  
        self.no_stim_search_status = True

        self.user_responses = user_response_dict
        self.split_str = split_str
        self.warning = {}

        self.battery_info = None # class
        self.run_info = None # class
        self.analyzed_info = None # class
        self.secondary_info = None # class 
        self.biological_analysis = None # class

        if self.user_responses['analysis_machine'] == 'sauron':
            self.sauron_pipeline()
        
        else:
            self.mcam_pipeline()

        if self.warning: 
            warning_list = list(self.warning.keys())
            for warning_name in warning_list:
                if warning_name in self.subconscious_warnings:
                    if warning_name == 'NO_STIM':
                        self.no_stim_pipe()
                    # other "subconscious" (FishBrain not FishHead) warning handling here


    def warning_reset(self, warning_name):
        del self.warning[warning_name]


    def visualize_information(self, user_response_dict):
        self.user_responses = user_response_dict
        if self.user_responses['analysis_type'] == 'battery':
            DataVisualization.Sauron_Text_Visualization(self.user_responses['run_number'], self.user_responses['analysis_type'], self.battery_info, 
                                                        self.user_responses['name_file'], self.user_responses['user_file'])
            
        elif self.user_responses['analysis_type'] == 'preview':
            DataVisualization.Sauron_Text_Visualization(self.user_responses['run_number'], self.user_responses['analysis_type'], self.battery_info, 
                                                        self.user_responses['name_file'], self.user_responses['user_file'], treatments=self.analyzed_info.treatments, 
                                                        concentration_dict=self.analyzed_info.concentration_dict)
            
        elif self.user_responses['visualize_secondary'] == 'yes' and self.user_responses['analysis_type'] == 'biological':
            DataVisualization.Sauron_Plot_Visualization(self.user_responses['analysis_type'], self.user_responses['run_numbers'], 
                                                                                  self.user_responses['battery_plot'], self.user_responses['analysis_group'], 
                                                                                  self.user_responses['analysis_calculations'], self.user_responses['specific_treatment'], 
                                                                                  self.user_responses['user_treatment'], self.user_responses['specific_assay'], 
                                                                                  self.user_responses['user_assay'], self.user_responses['isolate_stimuli'], 
                                                                                  self.user_responses['name_title'], self.user_responses['user_title'], 
                                                                                  self.user_responses['name_file'], self.user_responses['user_file'],
                                                                                  self.user_responses['visualize_secondary'], self.user_responses['user_habituation'],
                                                                                  self.battery_info[0], self.biological_info, self.split_str) 
            
        elif self.user_responses['visualize_secondary'] == 'yes':
            DataVisualization.Sauron_Plot_Visualization(self.user_responses['analysis_type'], self.user_responses['run_number'], 
                                                                                  self.user_responses['battery_plot'], self.user_responses['analysis_group'], 
                                                                                  self.user_responses['analysis_calculations'], self.user_responses['specific_treatment'], 
                                                                                  self.user_responses['user_treatment'], self.user_responses['specific_assay'], 
                                                                                  self.user_responses['user_assay'], self.user_responses['isolate_stimuli'], 
                                                                                  self.user_responses['name_title'], self.user_responses['user_title'], 
                                                                                  self.user_responses['name_file'], self.user_responses['user_file'],
                                                                                  self.user_responses['visualize_secondary'], self.user_responses['user_habituation'],
                                                                                  self.battery_info, self.secondary_info, self.split_str)
        
        elif self.user_responses['analysis_type'] == 'biological':
            DataVisualization.Sauron_Plot_Visualization(self.user_responses['analysis_type'], self.user_responses['run_numbers'], 
                                                                                  self.user_responses['battery_plot'], self.user_responses['analysis_group'], 
                                                                                  self.user_responses['analysis_calculations'], self.user_responses['specific_treatment'], 
                                                                                  self.user_responses['user_treatment'], self.user_responses['specific_assay'], 
                                                                                  self.user_responses['user_assay'], self.user_responses['isolate_stimuli'], 
                                                                                  self.user_responses['name_title'], self.user_responses['user_title'], 
                                                                                  self.user_responses['name_file'], self.user_responses['user_file'],
                                                                                  self.user_responses['visualize_secondary'], self.user_responses['user_habituation'],
                                                                                  self.battery_info[0], self.biological_info, self.split_str)

        else:
            DataVisualization.Sauron_Plot_Visualization(self.user_responses['analysis_type'], self.user_responses['run_number'], 
                                                                                  self.user_responses['battery_plot'], self.user_responses['analysis_group'], 
                                                                                  self.user_responses['analysis_calculations'], self.user_responses['specific_treatment'], 
                                                                                  self.user_responses['user_treatment'], self.user_responses['specific_assay'], 
                                                                                  self.user_responses['user_assay'], self.user_responses['isolate_stimuli'], 
                                                                                  self.user_responses['name_title'], self.user_responses['user_title'], 
                                                                                  self.user_responses['name_file'], self.user_responses['user_file'],
                                                                                  self.user_responses['visualize_secondary'], self.user_responses['user_habituation'],
                                                                                  self.battery_info, self.analyzed_info, self.split_str)


    def sauron_pipeline(self):
        if self.user_responses['analysis_type'] == 'battery':
            self.sauron_battery_funct(self.user_responses['battery_number'])
            
        elif  self.user_responses['analysis_type'] == 'preview' or self.user_responses['analysis_type'] == 'technical':
            self.sauron_run_funct(self.user_responses['run_number'])
            
            if not self.warning or len(self.warning) == 1 and 'UNKNOWN_TREATMENT' in self.warning:
                self.sauron_battery_funct(self.run_info.battery_number, n_frm=self.run_info.n_frames)

            if not self.warning or len(self.warning) == 1 and 'UNKNOWN_TREATMENT' in self.warning:
                self.sauron_analysis_funct(self.user_responses['analysis_type'], self.user_responses['run_number'], self.user_responses['analysis_group'], 
                                        self.user_responses['user_group'], self.user_responses['analysis_calculations'], 
                                        self.run_info.csv_well_dict, self.battery_info.battery_info, self.battery_info.frame_rate)
            
            if not self.warning or len(self.warning) == 1 and 'UNKNOWN_TREATMENT' in self.warning:
                if self.user_responses['secondary_calculations'] != 'no':
                    self.sauron_secondary_analysis_funct()

        elif self.user_responses['analysis_type'] == 'biological':
            self.sauron_bio_run_funct(self.user_responses['run_numbers'])

            if not self.warning or len(self.warning) == 1 and 'UNKNOWN_TREATMENT' in self.warning:
                btry_nm_lst = [run.battery_number for run in self.run_info]
                n_frms_lst = [run.n_frames for run in self.run_info]
                self.sauron_bio_battery_funct(btry_nm_lst, n_frms_lst)

            if not self.warning or len(self.warning) == 1 and 'UNKNOWN_TREATMENT' in self.warning:
                csv_well_dict_lst = [run.csv_well_dict for run in self.run_info]
                battery_info_lst = [btry.battery_info for btry in self.battery_info]
                frame_rate_lst = [btry.frame_rate for btry in self.battery_info]

                self.sauron_bio_analysis_funct(self.user_responses['analysis_type'], self.user_responses['run_numbers'], self.user_responses['analysis_group'], 
                                        self.user_responses['user_group'], self.user_responses['analysis_calculations'], 
                                        csv_well_dict_lst, battery_info_lst, frame_rate_lst)

            if not self.warning or len(self.warning) == 1 and 'UNKNOWN_TREATMENT' in self.warning:
                self.biological_info = DataAnalysis.Sauron_Primary_Analysis.average_primary_analysis(self.analyzed_info)
                self.biological_info.finalize_bio_info()

            if not self.warning or len(self.warning) == 1 and 'UNKNOWN_TREATMENT' in self.warning:
                if self.user_responses['secondary_calculations'] != 'no':
                    self.sauron_bio_secondary_analysis_funct()

 
    def sauron_battery_funct(self, battery_number, n_frm=None):
        self.battery_info = FileReader.Sauron_Battery_Reader(battery_number, n_frames=n_frm)
            
        if self.battery_info.warning:
            for warning in self.battery_info.warning:
                self.warning[warning] = self.battery_info.warning[warning]


    def sauron_run_funct(self, run_number):
        self.run_info = FileReader.Sauron_Run_Reader(run_number)
        
        if self.run_info.warning:
            for warning in self.run_info.warning:
                self.warning[warning] = self.run_info.warning[warning]


    def sauron_analysis_funct(self, analysis_type, run_number, analysis_group, user_group, analysis_calc, csv_well_dict, battery_info, frame_rate):
        self.analyzed_info = DataAnalysis.Sauron_Primary_Analysis(analysis_type, run_number, analysis_group, user_group, analysis_calc, csv_well_dict, 
                                                                  battery_info, frame_rate, self.no_stim_search_status)

        if self.analyzed_info.warning:
            for warning in self.analyzed_info.warning:
                self.warning[warning] = self.analyzed_info.warning[warning]


    def sauron_bio_run_funct(self, run_numbers):
        self.run_info = [FileReader.Sauron_Run_Reader(rn_nmb) for rn_nmb in run_numbers]

        for run in self.run_info:
            if run.warning:
                for warning in run.warning:
                    self.warning[warning] = run.warning[warning]


    def sauron_bio_battery_funct(self, battery_numbers, n_frms):
        self.battery_info = [FileReader.Sauron_Battery_Reader(battery_numbers[nm], n_frames=n_frms[nm]) for nm in range(0, len(battery_numbers))]
            
        for btry in self.battery_info:
            if btry.warning:
                for warning in btry.warning:
                    self.warning[warning] = btry.warning[warning]

    
    def sauron_bio_analysis_funct(self, analysis_type, run_numbers, analysis_group, user_group, analysis_calc, csv_well_dict, battery_info, frame_rate):
        self.analyzed_info = [DataAnalysis.Sauron_Primary_Analysis(analysis_type, run_numbers[nmbr], analysis_group, user_group, analysis_calc, csv_well_dict[nmbr], 
                                                                  battery_info[nmbr], frame_rate[nmbr], self.no_stim_search_status) for nmbr in range(0, len(run_numbers))]

        for analyzed in self.analyzed_info:
            if analyzed.warning:
                for warning in analyzed.warning:
                    self.warning[warning] = analyzed.warning[warning]


    def sauron_secondary_analysis_funct(self):
        self.secondary_info = DataAnalysis.Sauron_Secondary_Analysis(self.analyzed_info, self.split_str)
        
        if self.user_responses['secondary_calculations'] == 'habituation':
            self.secondary_info.habituation()

        if self.secondary_info.warning:
            for warning in self.secondary_info.warning:
                self.warning[warning] = self.secondary_info.warning[warning]

    
    def sauron_bio_secondary_analysis_funct(self):
        self.secondary_info = DataAnalysis.Sauron_Secondary_Analysis(self.biological_info, self.split_str)

        if self.user_responses['secondary_calculations'] == 'habituation':
            self.secondary_info.habituation()

        if self.secondary_info.warning:
            for warning in self.secondary_info.warning:
                self.warning[warning] = self.secondary_info.warning[warning]


    def no_run_csv_pipe(self):
        self.warning_reset('NO_RUN_CSV')
        
        self.sauron_run_funct(self.user_responses['run_number'])
        
        if not self.warning or len(self.warning) == 1 and 'UNKNOWN_TREATMENT' in self.warning:
            self.sauron_battery_funct(self.run_info.battery_number, n_frm=self.run_info.n_frames)

        if not self.warning or len(self.warning) == 1 and 'UNKNOWN_TREATMENT' in self.warning:
            self.sauron_analysis_funct(self.user_responses['run_number'], self.user_responses['analysis_group'], 
                                        self.user_responses['user_group'], self.user_responses['analysis_calculations'], 
                                        self.run_info.csv_well_dict, self.battery_info.battery_info, self.battery_info.frame_rate)
        
        if not self.warning or len(self.warning) == 1 and 'UNKNOWN_TREATMENT' in self.warning and self.user_responses['secondary_calculations'] != 'no':
            self.sauron_secondary_analysis_funct()


    def no_battery_stimf_pipe(self):
        self.warning_reset('NO_BATTERY_CSV')

        if self.user_responses['analysis_type'] == 'battery':
            self.sauron_battery_funct(self.user_responses['battery_number'])
            
        else:
            self.sauron_battery_funct(self.run_info.battery_number, n_frm=self.run_info.n_frames)

            if not self.warning or len(self.warning) == 1 and 'UNKNOWN_TREATMENT' in self.warning:
                self.sauron_analysis_funct(self.user_responses['run_number'], self.user_responses['analysis_group'], 
                                            self.user_responses['user_group'], self.user_responses['analysis_calculations'], 
                                            self.run_info.csv_well_dict, self.battery_info.battery_info, self.battery_info.frame_rate)

            if not self.warning or len(self.warning) == 1 and 'UNKNOWN_TREATMENT' in self.warning and self.user_responses['secondary_calculations'] != 'no':
                self.sauron_secondary_analysis_funct()

    
    def unknwn_trt_pipe(self, user_name_dict=None):
        self.warning_reset('UNKNOWN_TREATMENT')

        if user_name_dict:
            treatment_textbase = Information_Textbase('TreatmentNames')
            treatment_textbase.add_line_to_text(user_name_dict)

            self.sauron_run_funct(self.user_responses['run_number'])

            if not self.warning or len(self.warning) == 1 and 'UNKNOWN_TREATMENT' in self.warning:
                self.sauron_analysis_funct(self.user_responses['run_number'], self.user_responses['analysis_group'], 
                                            self.user_responses['user_group'], self.user_responses['analysis_calculations'], 
                                            self.run_info.csv_well_dict, self.battery_info.battery_info, self.battery_info.frame_rate)
            
            if not self.warning or len(self.warning) == 1 and 'UNKNOWN_TREATMENT' in self.warning and self.user_responses['secondary_calculations'] != 'no':
                self.sauron_secondary_analysis_funct()
        

    def no_stim_pipe(self):
        self.warning_reset('NO_STIM')
        
        if self.no_stim_search_status:

            shift_fix = self.analyzed_info.stim_finder()

            if shift_fix and shift_fix[1]:
                frame_shift_textbase = Information_Textbase('FrameAdjustments')

                frame_shift = {self.user_responses['run_number'] : shift_fix[1]}

                frame_shift_textbase.add_line_to_text(frame_shift)

                self.sauron_analysis_funct(self.user_responses['run_number'], self.user_responses['analysis_group'], 
                                        self.user_responses['user_group'], self.user_responses['analysis_calculations'], 
                                        self.run_info.csv_well_dict, self.battery_info.battery_info, self.battery_info.frame_rate)
                
                if not self.warning or len(self.warning) == 1 and 'UNKNOWN_TREATMENT' in self.warning and self.user_responses['secondary_calculations'] != 'no':
                    self.sauron_secondary_analysis_funct()

            else:
                self.no_stim_search_status = False
                # print this error to the user !
                # run alternative code ? 
            

    def filename_helper_pipe(self):
        # recall vis with new name 
        self.warning_reset('FILENAME_HELPER')
    

    def mcam_pipeline(self):
        pass



