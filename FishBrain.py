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
        self.user_responses = user_response_dict
        self.split_str = split_str
        self.warning = None

        self.battery_info = None # class
        self.run_info = None # class
        self.analyzed_info = None # class
        self.secondary_info = None # class 

        if self.user_responses['analysis_machine'] == 'sauron':
            self.sauron_pipeline()
        
        else:
            self.mcam_pipeline()


    def warning_reset(self):
        self.warning = None


    def visualize_information(self, user_response_dict):
        self.user_responses = user_response_dict
        if self.user_responses['analysis_type'] == 'battery':
            DataVisualization.Sauron_Text_Visualization(self.user_responses['run_number'], self.user_responses['analysis_type'], self.battery_info, 
                                                        self.user_responses['name_file'], self.user_responses['user_file'])
            
        elif self.user_responses['analysis_type'] == 'preview':
            DataVisualization.Sauron_Text_Visualization(self.user_responses['run_number'], self.user_responses['analysis_type'], self.battery_info, 
                                                        self.user_responses['name_file'], self.user_responses['user_file'], treatments=self.analyzed_info.treatments, 
                                                        concentration_dict=self.analyzed_info.concentration_dict)
            
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
            
        else:
            self.sauron_run_funct(self.user_responses['run_number'])
            
            if not self.warning or self.warning[0] == 'UNKNOWN_TREATMENT':
                self.sauron_battery_funct(self.run_info.battery_number, n_frm=self.run_info.n_frames)

            if not self.warning or self.warning[0] == 'UNKNOWN_TREATMENT':
                self.sauron_analysis_funct(self.user_responses['run_number'], self.user_responses['analysis_group'], 
                                        self.user_responses['user_group'], self.user_responses['analysis_calculations'], 
                                        self.run_info.csv_well_dict, self.battery_info.battery_info, self.battery_info.frame_rate)
            
            if not self.warning or self.warning[0] == 'UNKNOWN_TREATMENT':
                if self.user_responses['secondary_calculations'] != 'no':
                    self.sauron_secondary_analysis_funct()

 
    def sauron_battery_funct(self, battery_number, n_frm=None):
        self.battery_info = FileReader.Sauron_Battery_Reader(battery_number, n_frames=n_frm)
            
        if self.battery_info.warning:
            self.warning = self.battery_info.warning
            # DO SOMETHING HERE ? 


    def sauron_run_funct(self, run_number):
        self.run_info = FileReader.Sauron_Run_Reader(run_number)
        
        if self.run_info.warning:
            self.warning = self.run_info.warning
            # DO SOMETHING HERE ? 


    def sauron_analysis_funct(self, run_number, analysis_group, user_group, analysis_calc, csv_well_dict, battery_info, frame_rate):
        self.analyzed_info = DataAnalysis.Sauron_Primary_Analysis(run_number, analysis_group, user_group, analysis_calc, csv_well_dict, 
                                                                  battery_info, frame_rate)

        if self.analyzed_info.warning:
            self.warning = self.analyzed_info.warning
            # DO SOMETHING HERE ?


    def sauron_secondary_analysis_funct(self):
        self.secondary_info = DataAnalysis.Sauron_Secondary_Analysis(self.analyzed_info, self.split_str)
        
        if self.user_responses['secondary_calculations'] == 'habituation':
            self.sauron_habituation()

        if self.secondary_info.warning:
            self.warning = self.secondary_info.warning


    def sauron_habituation(self):
        self.secondary_info.technical_habituation()


    def no_run_csv_pipe(self):
        self.warning_reset()
        
        self.sauron_run_funct(self.user_responses['run_number'])
        
        if not self.warning:
            self.sauron_battery_funct(self.run_info.battery_number, n_frm=self.run_info.n_frames)

        if not self.warning:
            self.sauron_analysis_funct(self.user_responses['run_number'], self.user_responses['analysis_group'], 
                                        self.user_responses['user_group'], self.user_responses['analysis_calculations'], 
                                        self.run_info.csv_well_dict, self.battery_info.battery_info, self.battery_info.frame_rate)
        
        if not self.warning and self.user_responses['secondary_calculations'] != 'no':
                self.sauron_secondary_analysis_funct()


    def no_battery_stimf_pipe(self):
        self.warning_reset()

        if self.user_responses['analysis_type'] == 'battery':
            self.sauron_battery_funct(self.user_responses['battery_number'])
            
        else:
            self.sauron_battery_funct(self.run_info.battery_number, n_frm=self.run_info.n_frames)

            if not self.warning:
                self.sauron_analysis_funct(self.user_responses['run_number'], self.user_responses['analysis_group'], 
                                            self.user_responses['user_group'], self.user_responses['analysis_calculations'], 
                                            self.run_info.csv_well_dict, self.battery_info.battery_info, self.battery_info.frame_rate)

            if not self.warning and self.user_responses['secondary_calculations'] != 'no':
                self.sauron_secondary_analysis_funct()

    
    def unknwn_trt_pipe(self, user_name_dict=None):
        self.warning_reset()

        if user_name_dict:
            treatment_textbase = Information_Textbase('TreatmentNames')
            treatment_textbase.add_line_to_text(user_name_dict)

            self.sauron_run_funct(self.user_responses['run_number'])

            if not self.warning:
                self.sauron_analysis_funct(self.user_responses['run_number'], self.user_responses['analysis_group'], 
                                            self.user_responses['user_group'], self.user_responses['analysis_calculations'], 
                                            self.run_info.csv_well_dict, self.battery_info.battery_info, self.battery_info.frame_rate)
            
            if not self.warning and self.user_responses['secondary_calculations'] != 'no':
                self.sauron_secondary_analysis_funct()
        

    def no_stim_pipe(self):
        # call function to find index adjustment
        # update textbase for index adjustments
        # recall splitting analysis only, averaging should be fine (if poss)
        self.warning_reset()


    def filename_helper_pipe(self):
        # recall vis with new name 
        self.warning_reset()
    

    def mcam_pipeline(self):
        pass



