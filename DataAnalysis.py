from FishLog import Fish_Log
import HardInformation


# % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % 
# HELLO, this is DataAnalysis                     #
# # this file contains classes for processing     #
# # information read from files. These classes    #
# # do things such as sort into                   #
# # treatment:concentration or group depending    #
# # depending on user input, average between      #
# # replicates, and split traces into assays and  #
# # stimulus responses                            #
# % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ %


fish_logger = Fish_Log()




class Sauron_Primary_Analysis():


    # % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ %
    # HELLO, this is the class Sauron_Primary_Analysis #
    # # the main purpose of this class is to do a      #
    # # # first pass analysis over data such as        #
    # # # sorting averaging, and identifying stimulus  # 
    # # # responses                                    #
    # # this class is structured such that when it is  #
    # # # instantiated, the final attibutes are        #
    # # # initialized with None, and main functions    #
    # # # are called to determine if each step should  #
    # # # be performed depending on user input         #
    # # inputs to the class are the run_info,          #
    # # # battery_info, and user_responses values      #
    # # the main attributes of this class include      #
    # # # sorted_dictionary, averaged_dictionary, and  #
    # # # split_dictionary                             #
    # # this class is used by fish brain to determine  #
    # # # and perform necessary calculations on the    #
    # # # information from FileReader                  #
    # % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ %


    @classmethod
    def Average_Primary_Analysis(*cls):
        if cls[0].working_dictionary == 'sorted':
            pass
        elif cls[0].working_dictionary == 'averaged':
            pass
        elif cls[0].working_dictionary == 'split':
            pass


    dispersion_error = {
        'full_plate' : ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12',
        'B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B09', 'B10', 'B11', 'B12',
        'C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08', 'C09', 'C10', 'C11', 'C12',
        'D01', 'D02', 'D03', 'D04', 'D05', 'D06', 'D07', 'D08', 'D09', 'D10', 'D11', 'D12', 
        'H01', 'H02', 'H03', 'H04', 'H05', 'H06', 'H07', 'H08', 'H09', 'H10', 'H11', 'H12',
        'G01', 'G02', 'G03', 'G04', 'G05', 'G06', 'G07', 'G08', 'G09', 'G10', 'G11', 'G12',
        'F01', 'F02', 'F03', 'F04', 'F05', 'F06', 'F07', 'F08', 'F09', 'F10', 'F11', 'F12',
        'E01', 'E02', 'E03', 'E04', 'E05', 'E06', 'E07', 'E08', 'E09', 'E10', 'E11', 'E12'],

        'left_half' : ['A01', 'B01', 'C01', 'D01', 'E01', 'F01', 'G01', 'H01', 'A02', 'B02', 'C02', 'D02', 'E02', 'F02', 'G02', 'H02',
        'A03', 'B03', 'C03', 'D03', 'E03', 'F03', 'G03', 'H03', 'A04', 'B04', 'C04', 'D04', 'E04', 'F04', 'G04', 'H04',
        'A05', 'B05', 'C05', 'D05', 'E05', 'F05', 'G05', 'H05', 'A06', 'B06', 'C06', 'D06', 'E06', 'F06', 'G06', 'H06'],
  
        'right_half' : ['A12', 'B12', 'C12', 'D12', 'E12', 'F12', 'G12', 'H12', 'A11', 'B11', 'C11', 'D11', 'E11', 'F11', 'G11', 'H11',
        'A10', 'B10', 'C10', 'D10', 'E10', 'F10', 'G10', 'H10', 'A09', 'B09', 'C09', 'D09', 'E09', 'F09', 'G09', 'H09',
        'A08', 'B08', 'C08', 'D08', 'E08', 'F08', 'G08', 'H08', 'A07', 'B07', 'C07', 'D07', 'E07', 'F07', 'G07', 'H07'],
        
        'top_half' : ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12',
        'B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B09', 'B10', 'B11', 'B12',
        'C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08', 'C09', 'C10', 'C11', 'C12',
        'D01', 'D02', 'D03', 'D04', 'D05', 'D06', 'D07', 'D08', 'D09', 'D10', 'D11', 'D12'],

        'bottom_half' : ['H01', 'H02', 'H03', 'H04', 'H05', 'H06', 'H07', 'H08', 'H09', 'H10', 'H11', 'H12',
        'G01', 'G02', 'G03', 'G04', 'G05', 'G06', 'G07', 'G08', 'G09', 'G10', 'G11', 'G12',
        'F01', 'F02', 'F03', 'F04', 'F05', 'F06', 'F07', 'F08', 'F09', 'F10', 'F11', 'F12',
        'E01', 'E02', 'E03', 'E04', 'E05', 'E06', 'E07', 'E08', 'E09', 'E10', 'E11', 'E12'],
        
        'A' : ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12'],
        'B' : ['B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B09', 'B10', 'B11', 'B12'],
        'C' : ['C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08', 'C09', 'C10', 'C11', 'C12'],
        'D' : ['D01', 'D02', 'D03', 'D04', 'D05', 'D06', 'D07', 'D08', 'D09', 'D10', 'D11', 'D12'],
        'E' : ['E01', 'E02', 'E03', 'E04', 'E05', 'E06', 'E07', 'E08', 'E09', 'E10', 'E11', 'E12'],
        'F' : ['F01', 'F02', 'F03', 'F04', 'F05', 'F06', 'F07', 'F08', 'F09', 'F10', 'F11', 'F12'],
        'G' : ['G01', 'G02', 'G03', 'G04', 'G05', 'G06', 'G07', 'G08', 'G09', 'G10', 'G11', 'G12'],
        'H' : ['H01', 'H02', 'H03', 'H04', 'H05', 'H06', 'H07', 'H08', 'H09', 'H10', 'H11', 'H12'],
        '01' : ['A01', 'B01', 'C01', 'D01', 'E01', 'F01', 'G01', 'H01'],
        '02' : ['A02', 'B02', 'C02', 'D02', 'E02', 'F02', 'G02', 'H02'],
        '03' : ['A03', 'B03', 'C03', 'D03', 'E03', 'F03', 'G03', 'H03'],
        '04' : ['A04', 'B04', 'C04', 'D04', 'E04', 'F04', 'G04', 'H04'],
        '05' : ['A05', 'B05', 'C05', 'D05', 'E05', 'F05', 'G05', 'H05'],
        '06' : ['A06', 'B06', 'C06', 'D06', 'E06', 'F06', 'G06', 'H06'],
        '07' : ['A07', 'B07', 'C07', 'D07', 'E07', 'F07', 'G07', 'H07'],
        '08' : ['A08', 'B08', 'C08', 'D08', 'E08', 'F08', 'G08', 'H08'],
        '09' : ['A09', 'B09', 'C09', 'D09', 'E09', 'F09', 'G09', 'H09'],
        '10' : ['A10', 'B10', 'C10', 'D10', 'E10', 'F10', 'G10', 'H10'],
        '11' : ['A11', 'B11', 'C11', 'D11', 'E11', 'F11', 'G11', 'H11'],
        '12' : ['A12', 'B12', 'C12', 'D12', 'E12', 'F12', 'G12', 'H12']
}


    def __init__(self, run_number, user_analysis_group, user_group, user_analysis_calculations, raw_run_info, battery_info, frame_rate, no_stim_search):
        self.run_number = run_number
        self.user_analysis_group = user_analysis_group
        self.user_group = user_group
        self.user_analysis_calculations = user_analysis_calculations
        self.raw_run_info = raw_run_info
        self.battery_info = battery_info
        self.frame_rate = frame_rate
        self.no_stim_search = no_stim_search

        self.adjust_frame_index = 0                                                               
        self.working_dictionary = None
        self.sorted_dictionary = None
        self.averaged_dictionary = None
        self.split_dictionary = None

        self.treatments = None
        self.concentration_dict = None
        self.no_stim_assays = []

        self.warning = {}

        self.load_adjust_frames()

        self.sorting()
    
        self.averaging()
        
        self.splitting()
        
        self.finalize_info()

    
    def load_adjust_frames(self):
        textbase = HardInformation.Information_Textbase('FrameAdjustments')
        frame_adj_dict = textbase.read_text_to_dict()

        if str(self.run_number) in frame_adj_dict.keys():
            self.adjust_frame_index = int(frame_adj_dict[str(self.run_number)])

        fish_logger.log(Fish_Log.INFO, f'Adjusted Frames {True if str(self.run_number) in frame_adj_dict.keys() else False}, AssayNames Textbase {{{", ".join(f"{key}: {value}" for key, value in frame_adj_dict.items())}}}')


    def sorting(self):
        if self.user_analysis_group == 'treatment':
            self.sort_treatments()

        elif self.user_analysis_group == 'error':
            self.sort_dictionary(self.dispersion_error)

        elif self.user_analysis_group == 'custom':
            self.sort_dictionary(self.user_group)

        else: 
            # self.user_analysis_group == 'well' 
            self.restructure_dictionary()
    
    
    def sort_treatments(self):
        treatment_dictionary = {}

        for well, info_tuple in self.raw_run_info.items():
            if len(info_tuple[1]) == 1:
                # single treatment
                treatment = info_tuple[1][0][0]
                concentration = str(info_tuple[1][0][1])

                if treatment not in treatment_dictionary.keys():
                    treatment_dictionary[treatment] = {concentration : [info_tuple[0]]}
                elif concentration not in treatment_dictionary[treatment].keys():
                    treatment_dictionary[treatment][concentration] = [info_tuple[0]]
                else:
                    treatment_dictionary[treatment][concentration].append(info_tuple[0])
                
            else:
                # multiple treatment
                sorted_trt_cnc_tuple = sorted(info_tuple[1], key=lambda x: x[0])
                
                treatments = '::'.join(f'{trt_cnc_tup[0]}' for trt_cnc_tup in sorted_trt_cnc_tuple)
                concentrations = '::'.join(f'{trt_cnc_tup[1]}' for trt_cnc_tup in sorted_trt_cnc_tuple)


                if treatments not in treatment_dictionary.keys():
                    treatment_dictionary[treatments] = {concentrations : [info_tuple[0]]}
                elif concentrations not in treatment_dictionary[treatments].keys():
                    treatment_dictionary[treatments][concentrations] = [info_tuple[0]]
                else:
                    treatment_dictionary[treatments][concentrations].append(info_tuple[0])
            
        self.working_dictionary = 'sorted'
        self.sorted_dictionary = treatment_dictionary

        fish_logger.log(Fish_Log.INFO, f'Sorted Dictionary {{{", ".join(f"{key}: {value.keys()}" for key, value in self.sorted_dictionary.items())}}}')
        

    def sort_dictionary(self, sorting_dictionary):
        result_dictionary = {}
        for well, info_tuple in self.raw_run_info.items():
            for group_name, grouping in sorting_dictionary.items():
                if well in grouping:
                    if group_name not in result_dictionary.keys():
                        result_dictionary[group_name] = [info_tuple[0]]
                    else:
                        result_dictionary[group_name].append(info_tuple[0])

        self.working_dictionary = 'sorted'
        self.sorted_dictionary = result_dictionary

        fish_logger.log(Fish_Log.INFO, f'Sorted Dictionary {{{", ".join(f"{key}" for key in self.sorted_dictionary.keys())}}}')


    def restructure_dictionary(self):
        result_dictionary = {}
        for well, info_tuple in self.raw_run_info.items():
            result_dictionary[well] = [info_tuple[0]]

        self.working_dictionary = 'sorted'
        self.sorted_dictionary = result_dictionary

        fish_logger.log(Fish_Log.INFO, f'Sorted Dictionary {{{", ".join(f"{key}" for key in self.sorted_dictionary.keys())}}}')


    def averaging(self):
        if self.user_analysis_calculations == 'average' or self.user_analysis_calculations == 'full' and self.user_analysis_group != 'well':
            if self.user_analysis_group == 'treatment':
                self.average_treatments()
            else:
                self.average_grouping()
        else:
            pass


    def average_treatments(self):
        average_dict = {}
        for treatment in self.sorted_dictionary.keys():
            for concentration in self.sorted_dictionary[treatment].keys():
                mi_avg_list = []
                mi_st_dev_list = []
                mi_med_list = []

                if len(self.sorted_dictionary[treatment][concentration]) > 1:
                    for mi in range(0, len(self.sorted_dictionary[treatment][concentration][0])):
                        mi_repl = [self.sorted_dictionary[treatment][concentration][repl][mi] for repl in range(0, len(self.sorted_dictionary[treatment][concentration]))]
                        mi_avg = sum(mi_repl) / len(mi_repl)
                        
                        squared_diff = [(x - mi_avg) ** 2 for x in mi_repl]
                        variance = sum(squared_diff) / len(mi_repl)
                        st_dev = variance ** 0.5
                        if st_dev == 0:
                            st_dev = 0.01
                        
                        sorted_mi_repl = sorted(mi_repl)
                        n = len(sorted_mi_repl)
                        if n % 2 == 0:
                            mi_med = (sorted_mi_repl[n // 2 - 1] + sorted_mi_repl[n // 2]) / 2
                        else:
                            mi_med = sorted_mi_repl[n // 2]

                        mi_avg_list.append(mi_avg)
                        mi_st_dev_list.append(st_dev)
                        mi_med_list.append(mi_med)
                
                else:
                    mi_avg_list = self.sorted_dictionary[treatment][concentration][0][0] # no actual average
                    mi_st_dev_list = [0 for i in range(0, len(mi_avg_list))]
                    mi_med_list = self.sorted_dictionary[treatment][concentration][0][0] # no actual median

                if treatment not in average_dict.keys():
                    average_dict[treatment] = {concentration : (mi_avg_list, mi_med_list, mi_st_dev_list)}
                else:
                    average_dict[treatment][concentration] = (mi_avg_list, mi_med_list, mi_st_dev_list)

        self.working_dictionary = 'averaged'
        self.averaged_dictionary = average_dict

        fish_logger.log(Fish_Log.INFO, f'Averaged Dictionary {{{", ".join(f"{key}: {value.keys()}" for key, value in self.averaged_dictionary.items())}}}')


    def average_grouping(self):
        average_dict = {}
        for group in self.sorted_dictionary.keys():
            mi_avg_list = []
            mi_st_dev_list = []
            mi_med_list = []

            if len(self.sorted_dictionary[group]) > 1:
                for mi in range(0, len(self.sorted_dictionary[group][0])):
                    mi_repl = [self.sorted_dictionary[group][repl][mi] for repl in range(0, len(self.sorted_dictionary[group]))]
                    mi_avg = sum(mi_repl) / len(mi_repl)
                    
                    squared_diff = [(x - mi_avg) ** 2 for x in mi_repl]
                    variance = sum(squared_diff) / len(mi_repl)
                    st_dev = variance ** 0.5
                    if st_dev == 0:
                        st_dev = 0.01
                    
                    sorted_mi_repl = sorted(mi_repl)
                    n = len(sorted_mi_repl)
                    if n % 2 == 0:
                        mi_med = (sorted_mi_repl[n // 2 - 1] + sorted_mi_repl[n // 2]) / 2
                    else:
                        mi_med = sorted_mi_repl[n // 2]

                    mi_avg_list.append(mi_avg)
                    mi_st_dev_list.append(st_dev)
                    mi_med_list.append(mi_med)
                
                else:
                    mi_avg_list = self.sorted_dictionary[group][0] # no actual average
                    mi_st_dev_list = [0 for i in range(0, len(mi_avg_list))]
                    mi_med_list = self.sorted_dictionary[group][0] # no actual median

            average_dict[group] = (mi_avg_list, mi_med_list, mi_st_dev_list)

        self.working_dictionary = 'averaged'
        self.averaged_dictionary = average_dict

        fish_logger.log(Fish_Log.INFO, f'Averaged Dictionary {{{", ".join(f"{key}" for key in self.averaged_dictionary.keys())}}}')


    def splitting(self):
        if self.user_analysis_calculations == 'split' or self.user_analysis_calculations == 'full':
            if self.user_analysis_group == 'treatment':
                self.split_status = 'treatment'
                self.split_treatment()
            elif self.user_analysis_group == 'well':
                self.split_well()
                self.split_status = 'well'
            else:
                self.split_grouping()
                self.split_status = 'group'


    def split_treatment(self):
        split_result = {}

        if self.user_analysis_calculations == 'full':
            #average
            for treatment in self.averaged_dictionary.keys():
                for concentration in self.averaged_dictionary[treatment].keys():
                    split_dict = self.average_splitter(self.averaged_dictionary[treatment][concentration][0], self.averaged_dictionary[treatment][concentration][1], self.averaged_dictionary[treatment][concentration][2])

                    if treatment not in split_result.keys():
                        split_result[treatment] = {concentration : split_dict}
                    else:
                        split_result[treatment][concentration] = split_dict

        else:
            #raw
            for treatment in self.sorted_dictionary.keys():
                for concentration in self.sorted_dictionary[treatment].keys():
                    split_dict = self.raw_splitter(self.sorted_dictionary[treatment][concentration])

                    if treatment not in split_result.keys():
                        split_result[treatment] = {concentration : split_dict}
                    else:
                        split_result[treatment][concentration] = split_dict
        
        self.working_dictionary = 'split'
        self.split_dictionary = split_result

        fish_logger.log(Fish_Log.INFO, f'Split Dictionary {{{", ".join(f"{key}: {value.keys()}" for key, value in self.split_dictionary.items())}}}')

    
    def split_well(self):
        split_result = {}

        for well in self.sorted_dictionary.keys():
            split_dict = self.raw_splitter(self.sorted_dictionary[well])
            split_result[well] = split_dict

        self.working_dictionary = 'split'
        self.split_dictionary = split_result

        fish_logger.log(Fish_Log.INFO, f'Split Dictionary {{{", ".join(f"{key}" for key in self.split_dictionary.keys())}}}')


    def split_grouping(self):
        split_result = {}
        if self.user_analysis_calculations == 'full':
            #average
            for group_name in self.averaged_dictionary.keys():
                split_dict = self.average_splitter(self.averaged_dictionary[group_name][0], self.averaged_dictionary[group_name][1], self.averaged_dictionary[group_name][2])
                split_result[group_name] = split_dict

        else:
            #raw
            for group_name in self.sorted_dictionary.keys():
                split_dict = self.raw_splitter(self.sorted_dictionary[group_name])
                split_result[group_name] = split_dict
        
        self.working_dictionary = 'split'
        self.split_dictionary = split_result
        
        fish_logger.log(Fish_Log.INFO, f'Split Dictionary {{{", ".join(f"{key}" for key in self.split_dictionary.keys())}}}')

    
    def average_splitter(self, mi_average, mi_median, mi_st_dev):
        assay_name_counter = {}
        assay_dict = {}

        for assay in self.battery_info:
            stimulus_list = []
            assay_name = assay[0]

            assay_start = assay[1][0] / self.frame_rate
            assay_start = int(assay_start) + self.adjust_frame_index

            assay_end = assay[1][1] / self.frame_rate
            assay_end = int(assay_end) + self.adjust_frame_index
            
            if assay_start < 0 or assay_start > len(mi_average): 
                fish_logger.log(Fish_Log.WARNING, f"ASSAY START INDEX OUT OF MI RANGE {len(mi_average)} : Assay Name {assay_name}, Assay Start {assay_start}, Assay End {assay_end}, Frame Adjustment, {self.adjust_frame_index}")
                assay_start = 0
            if assay_end < 0  or assay_end > len(mi_average):
                fish_logger.log(Fish_Log.WARNING, f"ASSAY END INDEX OUT OF MI RANGE {len(mi_average)} : Assay Name {assay_name}, Assay Start {assay_start}, Assay End {assay_end}, Frame Adjustment, {self.adjust_frame_index}")
                assay_end = len(mi_average)

            assay_avg = mi_average[assay_start:assay_end]
            assay_median = mi_median[assay_start:assay_end]
            assay_st_dev = mi_st_dev[assay_start:assay_end]

            for stimulus in assay[2]:
                stimulus_name = stimulus[0]

                stimulus_start = stimulus[1][0] / self.frame_rate
                stimulus_start = int(stimulus_start) + self.adjust_frame_index

                stimulus_end = stimulus[1][1] / self.frame_rate
                stimulus_end = int(stimulus_end) + self.adjust_frame_index
                
                if stimulus_start < assay_start or stimulus_start > assay_end:
                    fish_logger.log(Fish_Log.WARNING, f"STIMULUS START INDEX OUT OF ASSAY RANGE : Assay Name {assay_name}, Assay Start {assay_start}, Assay End {assay_end}, Stimulus Name{stimulus_name}, Stimulus Start {stimulus_start}, Stimulus End {stimulus_end}, Frame Adjustment, {self.adjust_frame_index}")
                    stimulus_start = assay_start
                if stimulus_end < assay_start or stimulus_end > assay_end:
                    fish_logger.log(Fish_Log.WARNING, f"STIMULUS END INDEX OUT OF ASSAY RANGE : Assay Name {assay_name}, Assay Start {assay_start}, Assay End {assay_end}, Stimulus Name{stimulus_name}, Stimulus Start {stimulus_start}, Stimulus End {stimulus_end}, Frame Adjustment, {self.adjust_frame_index}")
                    stimulus_end = assay_end

                stimulus_avg = self.stimulus_calculator(mi_average[stimulus_start:stimulus_end])
                stimulus_median = self.stimulus_calculator(mi_median[stimulus_start:stimulus_end])
                stimulus_st_dev = self.stimulus_calculator(mi_st_dev[stimulus_start:stimulus_end], type='st_dev')

                stimulus_list.append((stimulus_name, stimulus_avg, stimulus_median, stimulus_st_dev, stimulus_start, stimulus_end))
            
            if not stimulus_list:
                self.no_stim_assays.append(assay_name)

            assay_dict[assay_name] = (assay_avg, assay_median, assay_st_dev, stimulus_list)
        
        return assay_dict
    
    
    def raw_splitter(self, mi_list):
        assay_dict = {}

        for assay in self.battery_info:
            stimulus_list = []
            assay_name = assay[0]

            assay_start = assay[1][0] / self.frame_rate
            assay_start = int(assay_start) + self.adjust_frame_index 

            assay_end = assay[1][1] / self.frame_rate
            assay_end = int(assay_end) + self.adjust_frame_index
            
            if assay_start < 0 or assay_start > len(mi_list[0]):
                fish_logger.log(Fish_Log.WARNING, f"ASSAY START INDEX OUT OF MI RANGE {len(mi_list[0])} : Assay Name {assay_name}, Assay Start {assay_start}, Assay End {assay_end}, Frame Adjustment, {self.adjust_frame_index}")
                assay_start = 0
            if assay_end < 0  or assay_end > len(mi_list[0]):
                fish_logger.log(Fish_Log.WARNING, f"ASSAY END INDEX OUT OF MI RANGE {len(mi_list[0])} : Assay Name {assay_name}, Assay Start {assay_start}, Assay End {assay_end}, Frame Adjustment, {self.adjust_frame_index}")
                assay_end = len(mi_list[0])

            assay_mi_list = [mi_values[assay_start:assay_end] for mi_values in mi_list]

            for stimulus in assay[2]:
                stimulus_name = stimulus[0]

                stimulus_start = stimulus[1][0] / self.frame_rate
                stimulus_start = int(stimulus_start) + self.adjust_frame_index 

                stimulus_end = stimulus[1][1] / self.frame_rate
                stimulus_end = int(stimulus_end) + self.adjust_frame_index 
                
                if stimulus_start < assay_start or stimulus_start > assay_end:
                    fish_logger.log(Fish_Log.WARNING, f"STIMULUS START INDEX OUT OF ASSAY RANGE : Assay Name {assay_name}, Assay Start {assay_start}, Assay End {assay_end}, Stimulus Name{stimulus_name}, Stimulus Start {stimulus_start}, Stimulus End {stimulus_end}, Frame Adjustment, {self.adjust_frame_index}")
                    stimulus_start = assay_start
                if stimulus_end < assay_start or stimulus_end > assay_end:
                    fish_logger.log(Fish_Log.WARNING, f"STIMULUS END INDEX OUT OF ASSAY RANGE : Assay Name {assay_name}, Assay Start {assay_start}, Assay End {assay_end}, Stimulus Name{stimulus_name}, Stimulus Start {stimulus_start}, Stimulus End {stimulus_end}, Frame Adjustment, {self.adjust_frame_index}")
                    stimulus_end = assay_end

                stim_mi_list = [self.stimulus_calculator(mi_values[stimulus_start:stimulus_end]) for mi_values in mi_list]

                stimulus_list.append((stimulus_name, stim_mi_list))

            if not stimulus_list:
                self.no_stim_assays.append(assay_name)

            assay_dict[assay_name] = (assay_mi_list, stimulus_list)

        return assay_dict
    

    def med_calc(self, median_mi_list):
        sorted_data = sorted(median_mi_list)
        n = len(sorted_data)
        return sorted_data[n // 2] if n % 2 == 1 else (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2

    
    def st_dev_calc(self, mi_list):
        n = len(mi_list)
        return ((sum((x - (sum(mi_list) / n)) ** 2 for x in mi_list) / n) ** 0.5) if n > 0 else 0


    def stimulus_calculator(self, stimulus_mi_list, type='max'):
        calc_resp_dict = {
            'max' : max(stimulus_mi_list),
            'avg' : sum(stimulus_mi_list) / len(stimulus_mi_list),
            'med' : self.med_calc(stimulus_mi_list),
            'st_dev' : self.st_dev_calc(stimulus_mi_list)
        }
    
        return calc_resp_dict[type]
    

    def finalize_info(self):
        self.treatments = [treatment for treatment in self.sorted_dictionary.keys()]
        if self.user_analysis_group == 'treatment':
            self.concentration_dict = {treatment : [concentration for concentration in self.sorted_dictionary[treatment].keys()] for treatment in self.sorted_dictionary.keys()}
    
        if self.working_dictionary == 'split' and self.no_stim_search:
            stim_cntr = 0
            zero_cntr = 0

            if self.user_analysis_group == 'treatment':  
                for treatment in self.split_dictionary.keys():
                    for concentration in self.split_dictionary[treatment].keys():
                        for assay in self.split_dictionary[treatment][concentration].keys():
                            if self.user_analysis_calculations == 'full' and assay not in self.no_stim_assays:
                                assay_avg = sum(self.split_dictionary[treatment][concentration][assay][0]) / len(self.split_dictionary[treatment][concentration][assay][0])
                                for stimulus in self.split_dictionary[treatment][concentration][assay][3]:
                                    stim_cntr += 1
                                    if stimulus[1] < assay_avg:
                                        zero_cntr += 1  

                            elif assay not in self.no_stim_assays:
                                avg_lst = [sum(assay_mi) / len(assay_mi) for assay_mi in  self.split_dictionary[treatment][concentration][assay][0]]
                                assay_avg = sum(avg_lst) / len(avg_lst)
                                for stimulus_list in self.split_dictionary[treatment][concentration][assay][1]:
                                    for lst in stimulus_list:
                                        for stimulus in lst:
                                            stim_cntr += 1
                                            avg_stm = sum(stimulus[1]) / len(stimulus[1])
                                            if avg_stm < assay_avg:
                                                zero_cntr += 1

            elif self.user_analysis_group == 'well' or self.user_analysis_group == 'group':
                for treatment in self.split_dictionary.keys():
                    for assay in self.split_dictionary[treatment].keys():
                        if self.user_analysis_calculations == 'full' and assay not in self.no_stim_assays:
                            for stimulus in self.split_dictionary[treatment][assay][3]:
                                assay_avg = sum(self.split_dictionary[treatment][assay][0]) / len(self.split_dictionary[treatment][assay][0])
                                for stimulus in self.split_dictionary[treatment][assay][3]:
                                    stim_cntr += 1
                                    if stimulus[1] < assay_avg:
                                        zero_cntr += 1

                        elif assay not in self.no_stim_assays:
                            avg_lst = [sum(assay_mi) / len(assay_mi) for assay_mi in  self.split_dictionary[treatment][assay][0]]
                            assay_avg = sum(avg_lst) / len(avg_lst)
                            for stimulus_list in self.split_dictionary[treatment][assay][1]:
                                for lst in stimulus_list:
                                    for stimulus in lst:
                                        stim_cntr += 1
                                        avg_stm = sum(stimulus[1]) / len(stimulus[1])
                                        if avg_stm < assay_avg:
                                            zero_cntr += 1
            
            responses = stim_cntr - zero_cntr

            if stim_cntr > 10 * responses:
                self.warning["NO_STIM"] = self.adjust_frame_index
                fish_logger.log(Fish_Log.WARNING, f'I do not think there are any responses within the current stimuli ranges! Stimuli {stim_cntr}, Responses {responses}; Current frame adjustment {self.adjust_frame_index}')
            else:
                fish_logger.log(Fish_Log.INFO, f'the stimuli responsiveness made the cutoff with {stim_cntr} stimuli and {stim_cntr-zero_cntr} responses')


    def stim_finder(self):
        if self.adjust_frame_index:
            self.adjust_frame_index = 0

        if self.split_status == 'treatment':
            best_frame_match = self.split_fix_treatment()

        elif self.split_status == 'well':
            best_frame_match = self.split_fix_well()

        elif self.split_status == 'group':
            best_frame_match = self.split_fix_group()
            
        return best_frame_match

    
    def split_fix_treatment(self):
        best_match_shift_list = []
        best_match = None

        if self.user_analysis_calculations == 'full':
            #average
            for treatment in self.averaged_dictionary.keys():
                for concentration in self.averaged_dictionary[treatment].keys():
                    best_match_shift = self.match_shift_finder(self.averaged_dictionary[treatment][concentration][0])
                    if best_match_shift:
                        best_match_shift_list.append(best_match_shift)

        else:
            #raw
            for treatment in self.sorted_dictionary.keys():
                for concentration in self.sorted_dictionary[treatment].keys():
                    best_match_shift = self.raw_stim_finder(self.sorted_dictionary[treatment][concentration])
                    if best_match_shift:
                        best_match_shift_list.append(best_match_shift)
        
        if best_match_shift_list:
            percentage = [ms[0] for ms in best_match_shift_list]
            shifts = [ms[1] for ms in best_match_shift_list]
            confidence = sum(percentage) / len(percentage)
            shift = sum(shifts) / (len(shifts))
            shift = int(shift)

            fish_logger.log(Fish_Log.INFO, f'I found best shift {shift} with confidence {confidence}')

            best_match = (confidence, shift)
        
        else:
            fish_logger.log(Fish_Log.WARNING, f'I was not able to find a shift!')

        return best_match


    def split_fix_well(self):
        best_match_shift_list = []
        best_match = None

        for well in self.sorted_dictionary.keys():
            best_match_shift = self.raw_stim_finder(self.sorted_dictionary[well])
            if best_match_shift:
                best_match_shift_list.append(best_match_shift)
        
        if best_match_shift_list:
            percentage = [ms[0] for ms in best_match_shift_list]
            shifts = [ms[1] for ms in best_match_shift_list]
            confidence = sum(percentage) / len(percentage)
            shift = sum(shifts) / (len(shifts))

            best_match = (confidence, int(shift))

        return best_match
            
            
    
    def split_fix_group(self):
        best_match_shift_list = []
        best_match = None

        if self.user_analysis_calculations == 'full':
            #average
            for group_name in self.averaged_dictionary.keys():
                best_match_shift = self.match_shift_finder(self.averaged_dictionary[group_name][0])
                if best_match_shift:
                    best_match_shift_list.append(best_match_shift)
                
        else:
            #raw
            for group_name in self.sorted_dictionary.keys():
                best_match_shift = self.raw_stim_finder(self.sorted_dictionary[group_name])
                if best_match_shift:
                    best_match_shift_list.append(best_match_shift)

        if best_match_shift_list:
            percentage = [ms[0] for ms in best_match_shift_list]
            shifts = [ms[1] for ms in best_match_shift_list]
            confidence = sum(percentage) / len(percentage)
            shift = sum(shifts) / (len(shifts))

            best_match = (confidence, int(shift))
                
        return best_match
                

    def match_shift_finder(self, mi_list):
        average_mi_trace = sum(mi_list) / len(mi_list)

        mi_cutoff_v = average_mi_trace * 50 # ONE OF THE THINGS !
        # this is a whole thing right here in this one line
        # # what is a "response", signal to noise ratios, how to find responses in an unbiased way

        stim_start_list = [stimulus[1][0] / self.frame_rate for assay in self.battery_info for stimulus in assay[2]]
        stim_end_list = [stimulus[1][1] / self.frame_rate for assay in self.battery_info for stimulus in assay[2]]

        stim_mid = [int((stim_start_list[n] + stim_end_list[n]) / 2) for n in range(0, len(stim_start_list))]

        stim_len = [stim_end_list[n] - stim_start_list[n] for n in range(0, len(stim_start_list))]

        stim_pattern = [stim_start_list[n+1] - stim_start_list[n] for n in range(0, len(stim_start_list)-1)]

        response_vals = [t for t, mi in enumerate(mi_list) if mi > mi_cutoff_v]

        response_val_min = [] # ONE OF THE THINGS !
        i = 0 

        while i < len(response_vals)-1:
            max_conseq_resp = 0
            max_t = 0

            if response_vals[i+1] - 1 == response_vals[i]:
                if mi_list[response_vals[i]] > max_conseq_resp:
                    max_conseq_resp = mi_list[response_vals[i]]
                    max_t = response_vals[i]
            
            else:
                if max_conseq_resp:
                    response_val_min.append(max_t)
                else:
                    response_val_min.append(response_vals[i])
            
            i+=1

        best_match = None # match ratio, frame shift

        if not response_val_min:
            pass
            #fish_logger.log(Fish_Log.ERROR, f'not enough responses detected! ASSAY STIM NUMBER {len(stim_start_list)} ; DETECTED STIM {len(response_vals)}')

        else:
            best_match = (0, 0) # match ratio, frame shift

            for t in range(0, len(response_val_min)):
                start_stim = 0
                attempt_find = 0 # in theory the while loop could get stuck infinitely between adding and subtracting
                
                lower_bound = stim_mid[start_stim] - 100
                if lower_bound < 0:
                    lower_bound = 0
                
                while attempt_find < len(stim_pattern) and response_val_min[t] > 100 + stim_mid[start_stim]:
                    attempt_find += 1
                    start_stim += 1

                    if response_val_min[t] < lower_bound:
                        start_stim -= 1
                        break

                if start_stim == -1 or start_stim > len(stim_len):
                    start_stim = 0
                            
                t_pattern = [response_val_min[t] + stim_pattern[i] for i in range(start_stim, len(stim_pattern))]
                matches = 0
                total = 0

                for i in range(0, len(t_pattern)):
                    total += 1
                    bound = 90 # ONE OF THE THINGS !
                    upper_bnd = t_pattern[i] + bound
                    lower_bnd = t_pattern[i] - bound 
                    if lower_bnd < 0:
                        lower_bnd = 0

                    for response in response_val_min:
                        if response < upper_bnd and response > lower_bnd:
                            matches += 1
                    
                match_ratio = matches / total

                if match_ratio > best_match[0]:
                    calc_shift = int(response_val_min[t] - stim_mid[start_stim])
                    best_match = (match_ratio, calc_shift) 
                
            #fish_logger.log(Fish_Log.INFO, f'I found an new alignment, {best_match[1]} frame(s), with a {best_match[0]*100:02d} percent match with the stimuli found; 
            #                stimuli found {len(response_vals)}, total stimuli {len(stim_mid)}')
            
        return best_match


    def raw_stim_finder(self, mi_lists):
        best_ms_lst = []
        best_match = None

        for mi_lst in mi_lists:
            best = self.match_shift_finder(mi_lst)
            if best:
                best_ms_lst.append(best)
        
        if best_ms_lst:
            percentage = [ms[0] for ms in best_ms_lst]
            shifts = [ms[1] for ms in best_ms_lst]
            average_percent = sum(percentage) / len(percentage)
            average_shift = sum(shifts) / (len(shifts))

            best_match = (average_percent, average_shift)

        return best_match


 

class Sauron_Secondary_Analysis():
    

    # % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ %
    # HELLO, this is the class Sauron_Secondary_Analysis  # 
    # # the main purpose of this class is to perform      #
    # # analysis on top of primary analysis information   #
    # # the class is structured to be instantiated with   #
    # # # needed inforation and the needed functions are  #
    # # # called from that instance.                      #
    # # the inputs include the sauron primary information #
    # # # and the split_str used to parse the string      #
    # # # responses of users containing                   #
    # # # treatment:concentration                         #
    # # outputs of the class are dictionaries of the      #
    # # # analysis performed ex habituation_dictionary    #
    # # this class is used by FishBrain for analysis on   #
    # # # primary analyzed info                           #
    # % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ %


    def __init__(self, sauron_primary_analysis, split_str):
        self.sauron_primary_analysis = sauron_primary_analysis
        self.split_str = split_str

        self.warning = {}


    def technical_habituation(self):
        self.habituation_dictionary = None
        self.cutoff_percentage = 0.07 # for determining habituation slope

        # require full calculations to call 
        habituation_dict = {}
        habituation_assays = ['10s Habituation Assay', '5s Habituation Assay', '2.5s Habituation Assay', 'softTap20sISI', 'softTap10sISI', 'softTap7sISI', 'softTap5sISI', 'softTap2pt5sISI', 'softTap1sISI']
        habituation_stimuli = ['soft_solenoid']

        assays_found = set()
        stimuli_found = set()

        split_dictionary = self.sauron_primary_analysis.split_dictionary

        if self.sauron_primary_analysis.user_analysis_group == 'treatment':
            for treatment in split_dictionary.keys():
                for concentration in split_dictionary[treatment].keys():
                    for assay in split_dictionary[treatment][concentration].keys():
                        if assay in habituation_assays:
                            assays_found.add(assay)
                            stimulus_dictionary = {}
                            for stimulus_name, stimulus_avg, stimulus_med, stimulus_st_dev, stim_st, stim_ed in split_dictionary[treatment][concentration][assay][3]:
                                if stimulus_name in habituation_stimuli:
                                    stimuli_found.add(stimulus_name)
                                    if stimulus_name not in stimulus_dictionary.keys():
                                        stimulus_dictionary[stimulus_name] = ([stimulus_avg], [stimulus_st_dev])
                                    else:
                                        stimulus_dictionary[stimulus_name][0].append(stimulus_avg)
                                        stimulus_dictionary[stimulus_name][1].append(stimulus_st_dev)
                                
                            stim_habit_dict = self.stimulus_dict_calcs(stimulus_dictionary) #assay_mi_average, assay_st_dev)
                    
                            if treatment not in habituation_dict.keys():
                                habituation_dict[treatment] = {concentration : {assay :stim_habit_dict}}
                            elif concentration not in habituation_dict[treatment].keys():
                                habituation_dict[treatment][concentration] = {assay :stim_habit_dict}
                            else:
                                habituation_dict[treatment][concentration][assay] = stim_habit_dict

        else:
            for group in split_dictionary.keys():
                for assay in split_dictionary[group].keys():
                    if assay in habituation_assays:
                        assays_found.add(assay)
                        stimulus_dictionary = {}
                        for stimulus_name, stimulus_avg, stimulus_med, stimulus_st_dev, stim_st, stim_ed in split_dictionary[group][assay][3]:
                            if stimulus_name in habituation_stimuli:
                                stimuli_found.add(stimulus_name)
                                if stimulus_name not in stimulus_dictionary.keys():
                                    stimulus_dictionary[stimulus_name] = ([stimulus_avg], [stimulus_st_dev])
                                else:
                                    stimulus_dictionary[stimulus_name][0].append(stimulus_avg)
                                    stimulus_dictionary[stimulus_name][1].append(stimulus_st_dev)
                                
                        stim_habit_dict = self.stimulus_dict_calcs(stimulus_dictionary) #assay_mi_average, assay_st_dev)

                        if group not in habituation_dict.keys():
                            habituation_dict[group] = {assay :stim_habit_dict}
                        else:
                            habituation_dict[group][assay] = stim_habit_dict
        
        self.habituation_dictionary = habituation_dict

        fish_logger.log(Fish_Log.INFO, f"Habituation Analysis : Habituation Assays {', '.join(asy_nm for asy_nm in assays_found)}, Stimuli Found {', '.join(stim_nm for stim_nm in stimuli_found)}, Made Habituation Dictionary {True if self.habituation_dictionary else False}")


    def stimulus_dict_calcs(self, stim_dict):
        result_dict = {}
        allowance = 2
        drops = 0
        drop_i = 0

        for stimulus_name in stim_dict.keys():
            stimulus_average_list = stim_dict[stimulus_name][0]
            stimulus_st_dev_list = stim_dict[stimulus_name][1]
            cutoff_value = max(stimulus_average_list) * self.cutoff_percentage # % of max response value

            stim_vals = []
            stim_st_devs = []
            for i, average_mi in enumerate(stimulus_average_list):
                if average_mi == 0 and not stim_vals:
                    # THIS SHOULD CATCH WHEN STIMULI ARE NOT PLAYED AT THE START OF THE ASSAY
                    pass
    
                elif average_mi > cutoff_value:
                    drops = 0
                    stim_vals.append(average_mi)
                    stim_st_devs.append(stimulus_st_dev_list[i])

                elif len(stim_vals) < 3:
                    stim_vals.append(average_mi)
                    stim_st_devs.append(stimulus_st_dev_list[i])
                
                else:
                    drops += 1
                    if drops > allowance:
                        drop_i = i - allowance
                        break
                    
            if not drop_i:
                drop_i = len(stimulus_average_list)

            if stim_vals and stim_st_devs:
                stimulus_slope, stimulus_intercept, stimulus_r_squared, average_st_dev = self.line_calculator(stim_vals, stim_st_devs)
                
                result_dict[stimulus_name] = (stimulus_average_list, stimulus_st_dev_list, stimulus_slope, stimulus_intercept, stimulus_r_squared, average_st_dev, drop_i)

        return result_dict
    
    
    def line_calculator(self, mi_list, st_dev_list):
        x_vals = [x + 1 for x in range(len(mi_list))]
        
        slope, intercept = self.calculate_slope(x_vals, mi_list, intrcpt=True)
        r_sq = self.calculate_r_squared(slope, intercept, x_vals, mi_list)
        avg_st_dev = self.calculate_avg_st_dev(st_dev_list)

        return slope, intercept, r_sq, avg_st_dev
    

    def calculate_slope(self, x_list, mi_list, intrcpt=False):
        n = len(x_list)

        x_sum = sum(x_list)
        mi_sum = sum(mi_list)
        x_mean = x_sum / n
        mi_mean = mi_sum / n

        numerator = sum((xi - x_mean) * (mi_i - mi_mean) for xi, mi_i in zip(x_list, mi_list))
        denominator = sum((xi - x_mean)**2 for xi in x_list)

        if denominator == 0:
            if intrcpt:
                return 0, 0
            else:
                return 0
        
        else:
            slope = numerator / denominator

        if intrcpt:
            intercept = mi_mean - slope * x_mean
            return slope, intercept
        else:
            return slope
    

    def calculate_r_squared(self, slope, intercept, x_list, mi_list):
        avg_mi = sum(mi_list) / len(mi_list)
        mi_mean_dev_sum_sq = sum([(mi - avg_mi)**2 for mi in mi_list])
        slope_mi = [x*slope + intercept for x in x_list] 
        slope_mean_dev_sum_sq = sum([(slp_mi - avg_mi)**2 for slp_mi in slope_mi])
        
        return slope_mean_dev_sum_sq / mi_mean_dev_sum_sq
    

    def calculate_avg_st_dev(self, st_dev_list):
        n = len(st_dev_list)
        sq_val = [st_dev**2 for st_dev in st_dev_list]
        avg = (sum(sq_val) / n)**0.5

        return avg




class Mcam_Primary_Analysis():

    # % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ %
    # HELLO, name and type 
    # # the main purpose
    # # the structure of the class
    # # inputs to the class
    # # the flow through the class
    # # outputs of the class
    # # uses of the class
    # % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ %


    def __init__(self):
        pass





