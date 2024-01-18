import FileReader
import DataAnalysis
import DataVisualization
#from FishLog import Fish_Log


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
            self.battery_info = FileReader.Sauron_Battery_Reader(self.user_responses['battery_number'])
            
            if self.battery_info.warning:
                self.warning = self.battery_info.warning
                return
            
        elif self.user_responses['analysis_type'] == 'preview' or self.user_responses['analysis_type'] == 'technical':
            self.run_info = FileReader.Sauron_Run_Reader(self.user_responses['run_number'])
        
            if self.run_info.warning:
                self.warning = self.run_info.warning
                return
            
            self.battery_info = FileReader.Sauron_Battery_Reader(self.run_info.battery_number, n_frames=self.run_info.n_frames)

            if self.battery_info.warning:
                self.warning = self.battery_info.warning
                return

            self.analyzed_info = DataAnalysis.Sauron_Primary_Analysis(self.user_responses['run_number'], self.user_responses['analysis_group'], 
                                    self.user_responses['user_group'], self.user_responses['analysis_calculations'], 
                                    self.run_info.csv_well_dict, self.battery_info.battery_info, self.battery_info.frame_rate)
        
        if self.user_responses['secondary_calculations'] == 'habituation':
            self.secondary_info = DataAnalysis.Sauron_Secondary_Analysis(self.analyzed_info, self.split_str)
            self.secondary_info.technical_habituation()
                
            
    def mcam_pipeline(self):
        pass



