from FishLog import Fish_Log
import HardInformation
import math


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
    def average_primary_analysis(cls, srn_prim_anly_lst):
        status = Sauron_Primary_Analysis.primary_analysis_info_checker(srn_prim_anly_lst)
        if status:
            bio_analysis = Sauron_Primary_Analysis.__new__(Sauron_Primary_Analysis)
            
            bio_analysis.analysis_type = status[0]
            bio_analysis.run_number = status[1]
            bio_analysis.user_analysis_group = status[2]
            bio_analysis.user_group = status[3]
            bio_analysis.user_analysis_calculations = status[4]
            bio_analysis.raw_run_info = status[5]
            bio_analysis.battery_info = status[6]
            bio_analysis.frame_rate = status[7]
            bio_analysis.no_stim_search = status[8]
            
            avg = False

            sorted_dict_list = [inst.sorted_dictionary for inst in srn_prim_anly_lst if inst.sorted_dictionary]
            averaged_dict_list = [inst.averaged_dictionary for inst in srn_prim_anly_lst if inst.averaged_dictionary]
            split_dict_list = [inst.split_dictionary for inst in srn_prim_anly_lst if inst.split_dictionary]
            
            bio_analysis.sorted_dictionary = Sauron_Primary_Analysis.sorted_dictionary_collector(sorted_dict_list, srn_prim_anly_lst[0].split_status)
            
            if averaged_dict_list:
                avg = True
                bio_analysis.averaged_dictionary = Sauron_Primary_Analysis.averaged_dictionary_averager(averaged_dict_list, srn_prim_anly_lst[0].split_status)

            if split_dict_list:
                bio_analysis.split_dictionary = Sauron_Primary_Analysis.split_dictionary_averager(split_dict_list, avg, srn_prim_anly_lst[0].split_status) 
            
            fish_logger.log(Fish_Log.INFO, f'averaging primary analsises; runs : {status[1]}, averaged {avg}')

            return bio_analysis


    @staticmethod
    def primary_analysis_info_checker(sauron_primary_analysies):
        same = False 

        analysis_types = [analysis.analysis_type for analysis in sauron_primary_analysies]
        run_numbers = [analysis.run_number for analysis in sauron_primary_analysies]
        user_analysis_groups = [analysis.user_analysis_group for analysis in sauron_primary_analysies]
        user_groups = [analysis.user_group for analysis in sauron_primary_analysies]
        user_analysis_calculations = [analysis.user_analysis_calculations for analysis in sauron_primary_analysies]
        raw_run_infos = [analysis.raw_run_info for analysis in sauron_primary_analysies]
        battery_infos = [analysis.battery_info for analysis in sauron_primary_analysies]
        frame_rates = [analysis.frame_rate for analysis in sauron_primary_analysies]
        no_stim_searchs = [analysis.no_stim_search for analysis in sauron_primary_analysies]

        if len(run_numbers) != 1:
            same = True
        else:
            same = False

        if same:
            assay_lists = []
            for btry in battery_infos:
                assay_lst = [tup[0] for tup in btry]
                assay_lists.append(assay_lst)
            
            first_list = assay_lists[0]
            same = all(lst == first_list for lst in assay_lists)

        if same:
            return (analysis_types[0], run_numbers, user_analysis_groups[0], user_groups[0], user_analysis_calculations[0], raw_run_infos, battery_infos[0], frame_rates, no_stim_searchs[0])
        else:
            return False
    

    @staticmethod  
    def sorted_dictionary_collector(sorted_dictionary_list, spl_status):
        cmbnd_dict = {}
        if spl_status == 'treatment':
            for dct in sorted_dictionary_list:
                for treatment in dct.keys():
                    if treatment not in cmbnd_dict.keys():
                        cmbnd_dict.update({treatment : dct[treatment]})
                    else:
                        for concentration in dct[treatment].keys():
                            if concentration not in cmbnd_dict[treatment].keys():
                                cmbnd_dict[treatment].update({concentration : dct[treatment][concentration]})
                            else:
                                for mi_list in dct[treatment][concentration]:
                                    cmbnd_dict[treatment][concentration].append(mi_list)

        else: # group or well
            for dct in sorted_dictionary_list:
                for group in dct.keys():
                    if group not in cmbnd_dict.keys():
                        cmbnd_dict[group] = dct[group]
                        cmbnd_dict.update({group : dct[group]})
                    else:
                        for mi_list in dct[group]:
                            cmbnd_dict[group].append(mi_list) 
        
        return cmbnd_dict


    @staticmethod  
    def averaged_dictionary_averager(averaged_dictionary_list, spl_status):
        cmbnd_dict = {}
        avg_dict = {}
        if spl_status == 'treatment':
            for dct in averaged_dictionary_list:
                for treatment in dct.keys():
                    if treatment not in cmbnd_dict.keys():
                        for concentration in dct[treatment].keys():
                            if treatment in cmbnd_dict.keys():
                                cmbnd_dict[treatment].update({concentration : [dct[treatment][concentration]]})
                            else:
                                cmbnd_dict[treatment] = {concentration : [dct[treatment][concentration]]}
                    else:
                        for concentration in dct[treatment].keys():
                            if concentration not in cmbnd_dict[treatment].keys():
                                cmbnd_dict[treatment].update({concentration : [dct[treatment][concentration]]})
                            else:
                                cmbnd_dict[treatment][concentration].append(dct[treatment][concentration])

            for trt in cmbnd_dict.keys():
                for cnc in cmbnd_dict[trt].keys():
                    if len(cmbnd_dict[trt][cnc]) == 1:
                        res =  cmbnd_dict[trt][cnc][0]
                    else:
                        mi_avgs_lst = [result_tuple[0] for result_tuple in cmbnd_dict[trt][cnc]]
                        mi_st_devs_lst = [result_tuple[2] for result_tuple in cmbnd_dict[trt][cnc]]

                        res = Sauron_Primary_Analysis.b_average_analysis(mi_avgs_lst, mi_st_devs_lst)
                        

                    if trt in avg_dict.keys():
                        avg_dict[trt].update({cnc : res})
                    else:
                        avg_dict[trt] = {cnc : res}

        else: # group or well
            for dct in averaged_dictionary_list:
                for group in dct.keys():
                    if group not in cmbnd_dict.keys():
                        cmbnd_dict[group] = [dct[group]]
                    else:
                        cmbnd_dict[group].append(dct[group])
        
            for grp in cmbnd_dict.keys():
                if len(cmbnd_dict[grp]) == 1:
                    avg_dict.update({grp : cmbnd_dict[grp][0]})
                else:
                    mi_avgs_lst = [result_tuple[0] for result_tuple in cmbnd_dict[grp]]
                    mi_st_devs_lst = [result_tuple[2] for result_tuple in cmbnd_dict[grp]]

                    avg_dict.update({grp : Sauron_Primary_Analysis.b_average_analysis(mi_avgs_lst, mi_st_devs_lst)})
                    
        return avg_dict


    @staticmethod
    def b_average_analysis(mi_average_lists, st_dev_lists):
        max_avg_len = None
        for mi_list in mi_average_lists:
            if not max_avg_len:
                max_avg_len = len(mi_list)
            elif len(mi_list) < max_avg_len:
                max_avg_len = len(mi_list)

        max_std_len = None
        for mi_list in st_dev_lists:
            if not max_std_len:
                max_std_len = len(mi_list)
            elif len(mi_list) < max_std_len:
                max_std_len = len(mi_list)
        
        avg_avg_lst = []
        avg_std_v_lst = []
        for avg_mi in range(0, max_avg_len):
            avg_mi_repl = [mi_average_lists[repl][avg_mi] for repl in range(0, len(mi_average_lists))]
            avg_avg = sum(avg_mi_repl) / len(avg_mi_repl)
            avg_avg_lst.append(avg_avg)

            avg_std = Sauron_Primary_Analysis.st_dev_calc(avg_mi_repl) / len(avg_mi_repl)
            avg_std_v_lst.append(avg_std)

        return (avg_avg_lst, avg_std_v_lst)


    @staticmethod  
    def split_dictionary_averager(split_dictionary_list, avg_status, spl_status):
        cmbnd_dict = {}

        if avg_status:
            avg_dict = {}
            if spl_status == 'treatment':
                for dct in split_dictionary_list:
                    for treatment in dct.keys():
                        if treatment not in cmbnd_dict.keys():
                            for concentration in dct[treatment].keys():
                                if treatment in cmbnd_dict.keys():
                                    cmbnd_dict[treatment].update({concentration : [dct[treatment][concentration]]})
                                else:
                                    cmbnd_dict[treatment] = {concentration : [dct[treatment][concentration]]}
                        else:
                            for concentration in dct[treatment].keys():
                                if concentration not in cmbnd_dict[treatment].keys():
                                    cmbnd_dict[treatment].update({concentration : [dct[treatment][concentration]]})
                                else:
                                    cmbnd_dict[treatment][concentration].append(dct[treatment][concentration])

                for trt in cmbnd_dict.keys():
                    for cnc in cmbnd_dict[trt].keys():
                        if trt in avg_dict.keys():
                            avg_dict[trt].update({cnc : Sauron_Primary_Analysis.split_assay_dict_averager(cmbnd_dict[trt][cnc])})
                        else:
                            avg_dict[trt] = {cnc : Sauron_Primary_Analysis.split_assay_dict_averager(cmbnd_dict[trt][cnc])}
                        
            else: # group or well
                for dct in split_dictionary_list:
                    for group in dct.keys():
                        if group not in cmbnd_dict.keys():
                            cmbnd_dict[group] = [dct[group]]
                        else:
                            cmbnd_dict[group].append(dct[group])

                for grp in cmbnd_dict.keys():
                    avg_dict[grp] = Sauron_Primary_Analysis.split_assay_dict_averager(cmbnd_dict[grp])
            
            return avg_dict
        
        else:
            aggr_dict = {}
            if spl_status == 'treatment':
                for dct in split_dictionary_list:
                    for treatment in dct.keys():
                        if treatment not in cmbnd_dict.keys():
                            for concentration in dct[treatment].keys():
                                if treatment in cmbnd_dict.keys():
                                    cmbnd_dict[treatment].update({concentration : [dct[treatment][concentration]]})
                                else:
                                    cmbnd_dict[treatment] = {concentration : [dct[treatment][concentration]]}
                        else:
                            for concentration in dct[treatment].keys():
                                if concentration not in cmbnd_dict.keys():
                                    cmbnd_dict[treatment].update({concentration : [dct[treatment][concentration]]})
                                else:
                                    cmbnd_dict[treatment][concentration].append(dct[treatment][concentration])

            for trt in cmbnd_dict.keys():
                for cnc in cmbnd_dict[trt].keys():
                    if trt in aggr_dict.keys():
                        aggr_dict[trt].update({cnc : Sauron_Primary_Analysis.split_assay_dict_collector(cmbnd_dict[trt][cnc])})
                    else:
                        aggr_dict[trt] = {cnc : Sauron_Primary_Analysis.split_assay_dict_collector(cmbnd_dict[trt][cnc])}

            else: # group or well
                for dct in split_dictionary_list:
                    for group in dct.keys():
                        if group not in cmbnd_dict.keys():
                            cmbnd_dict[group]  = [dct[group]]
                        else:
                            cmbnd_dict[group].append(dct[group]) 
            
            for grp in cmbnd_dict.keys():
                aggr_dict[grp] = Sauron_Primary_Analysis.split_assay_dict_collector(cmbnd_dict[grp])

            return aggr_dict
        

    @staticmethod
    def split_assay_dict_averager(assay_dct_lst):
        rtn_dict = {}
        asy_keys = assay_dct_lst[0].keys()

        for asy in asy_keys:
            assay_mi = [dct[asy][0] for dct in assay_dct_lst]
            assay_st_dev = [dct[asy][1] for dct in assay_dct_lst]
            assay_stim_lst = [dct[asy][2] for dct in assay_dct_lst]

            avg_asy_mi_avg, avg_asy_st_dev = Sauron_Primary_Analysis.b_average_analysis(assay_mi, assay_st_dev)

            n_stims = len(assay_stim_lst[0])
            stm_list = []
            
            if n_stims:
                for stim in range(0, n_stims):
                    stim_names = [assay_stim_lst[lst][stim][0] for lst in range(0, len(assay_stim_lst))]
                    stim_avg = [assay_stim_lst[lst][stim][1] for lst in range(0, len(assay_stim_lst))]
                    stim_st_dev = [assay_stim_lst[lst][stim][2] for lst in range(0, len(assay_stim_lst))]
                    stim_starts = [assay_stim_lst[lst][stim][3] for lst in range(0, len(assay_stim_lst))]
                    stim_ends = [assay_stim_lst[lst][stim][4] for lst in range(0, len(assay_stim_lst))]
                    avg_stim_avg = sum(stim_avg) / len(stim_avg)

                    avg_stim_st_dev = sum(stim_st_dev) / len(stim_st_dev)

                    stm_list.append((stim_names[0], avg_stim_avg, avg_stim_st_dev, stim_starts[0], stim_ends[0]))

            rtn_dict[asy] = (avg_asy_mi_avg, avg_asy_st_dev, stm_list)
            
        return rtn_dict


    @staticmethod
    def split_assay_dict_collector(assay_dct_lst):
        rtn_dict = {}
        asy_keys = assay_dct_lst[0].keys()

        for asy in asy_keys:
            assay_mi_lsts = [dct[asy][0] for dct in assay_dct_lst]
            assay_stm_lsts = [dct[asy][1] for dct in assay_dct_lst]

            n_stims = len(assay_dct_lst[0][asy][1])
            stm_list = []

            if n_stims:
                for stim in range(0, n_stims):
                    stm_names = [assay_stm_lsts[lst][stim][0] for lst in assay_stm_lsts]
                    stm_mi_list = [assay_stm_lsts[lst][stim][1] for lst in assay_stm_lsts]
                    
                    stm_list.append((stm_names, stm_mi_list))
            
            rtn_dict[asy] = (assay_mi_lsts, stm_list)

        return rtn_dict


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
    
    split_response_calculation = {
        'light' : 'avg',
        'sound' : 'max',
        'purple_LED' : 'avg',
        'green_LED' : 'avg',
        'blue_LED' : 'avg',
        'red_LED' : 'avg',
        'solenoid' : 'max',
        'soft_solenoid' : 'max',
        'MP3' : 'max'
    } # sum, med, max, avg, st_dev available 


    def __init__(self, analysis_type, run_number, user_analysis_group, user_group, user_analysis_calculations, raw_run_info, battery_info, frame_rate, no_stim_search):
        self.analysis_type = analysis_type
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
        self.shift_finding_package = None

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
            self.restructure_dictionary()
    
    
    def sort_treatments(self):
        treatment_dictionary = {}

        for well, info_tuple in self.raw_run_info.items():
            if len(info_tuple[1]) == 1:
                treatment = info_tuple[1][0][0]
                concentration = str(info_tuple[1][0][1])

                if treatment not in treatment_dictionary.keys():
                    treatment_dictionary[treatment] = {concentration : [info_tuple[0]]}
                elif concentration not in treatment_dictionary[treatment].keys():
                    treatment_dictionary[treatment][concentration] = [info_tuple[0]]
                else:
                    treatment_dictionary[treatment][concentration].append(info_tuple[0])
                
            else:
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
                        st_dev = math.sqrt(variance)
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
                    st_dev = math.sqrt(variance)
                    
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
            for treatment in self.averaged_dictionary.keys():
                for concentration in self.averaged_dictionary[treatment].keys():
                    split_dict = self.average_splitter(self.averaged_dictionary[treatment][concentration][0], self.averaged_dictionary[treatment][concentration][1], self.averaged_dictionary[treatment][concentration][2])

                    if treatment not in split_result.keys():
                        split_result[treatment] = {concentration : split_dict}
                    else:
                        split_result[treatment][concentration] = split_dict

        else:
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
            for group_name in self.averaged_dictionary.keys():
                split_dict = self.average_splitter(self.averaged_dictionary[group_name][0], self.averaged_dictionary[group_name][1], self.averaged_dictionary[group_name][2])
                split_result[group_name] = split_dict

        else:
            for group_name in self.sorted_dictionary.keys():
                split_dict = self.raw_splitter(self.sorted_dictionary[group_name])
                split_result[group_name] = split_dict
        
        self.working_dictionary = 'split'
        self.split_dictionary = split_result
        
        fish_logger.log(Fish_Log.INFO, f'Split Dictionary {{{", ".join(f"{key}" for key in self.split_dictionary.keys())}}}')

    
    def average_splitter(self, mi_average, mi_median, mi_st_dev):
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
            assay_st_dev = mi_st_dev[assay_start:assay_end]

            for stimulus in assay[2]:
                stimulus_name = stimulus[0]

                stimulus_start = stimulus[1][0] / self.frame_rate
                stimulus_start = int(stimulus_start) + self.adjust_frame_index

                stimulus_end = stimulus[1][1] / self.frame_rate
                stimulus_end = int(stimulus_end) + self.adjust_frame_index
                
                if stimulus_start < 0 or stimulus_start > len(mi_average):
                    fish_logger.log(Fish_Log.WARNING, f"STIMULUS START INDEX OUT OF MI RANGE {len(mi_average)} : Assay Name {assay_name}, Assay Start {assay_start}, Assay End {assay_end}, Stimulus Name{stimulus_name}, Stimulus Start {stimulus_start}, Stimulus End {stimulus_end}, Frame Adjustment, {self.adjust_frame_index}")
                    stimulus_start = assay_start
                if stimulus_end < 0 or stimulus_end > len(mi_average):
                    fish_logger.log(Fish_Log.WARNING, f"STIMULUS END INDEX OUT OF MI RANGE {len(mi_average)} : Assay Name {assay_name}, Assay Start {assay_start}, Assay End {assay_end}, Stimulus Name{stimulus_name}, Stimulus Start {stimulus_start}, Stimulus End {stimulus_end}, Frame Adjustment, {self.adjust_frame_index}")
                    stimulus_end = assay_end

                if stimulus_name in Sauron_Primary_Analysis.split_response_calculation.keys():
                    calc_type = Sauron_Primary_Analysis.split_response_calculation[stimulus_name]
                elif 'LED' in stimulus_name:
                    calc_type = Sauron_Primary_Analysis.split_response_calculation['light']
                elif 'solenoid' in stimulus_name or 'MP3' in stimulus_name:
                    calc_type = Sauron_Primary_Analysis.split_response_calculation['sound']

                if calc_type == 'avg':
                    stimulus_resp = self.stimulus_calculator(mi_average[stimulus_start:stimulus_end], ctype=calc_type)
                    stimulus_st_dev = self.stimulus_calculator(mi_average[stimulus_start:stimulus_end], ctype='st_dev')

                elif calc_type == 'max':
                    std_ref = mi_st_dev[stimulus_start:stimulus_end]
                    stimulus_resp = 0
                    stimulus_st_dev = 0 
                    for i, mi in enumerate(mi_average[stimulus_start:stimulus_end]):
                        if mi >= stimulus_resp:
                            stimulus_resp = mi
                            stimulus_st_dev = std_ref[i]
                
                elif calc_type == 'sum':
                    stimulus_resp = self.stimulus_calculator(mi_average[stimulus_start:stimulus_end], ctype=calc_type)
                    stimulus_st_dev = self.stimulus_calculator(mi_st_dev[stimulus_start:stimulus_end], ctype=calc_type)

                elif calc_type == 'med':
                    indx_st = sorted((value, st_dev, index) for index, (value, st_dev) 
                                     in enumerate(zip(mi_average[stimulus_start:stimulus_end], mi_st_dev[stimulus_start:stimulus_end])))

                    n = len(indx_st)

                    if n % 2 == 1:
                        stimulus_resp = indx_st[n // 2][0]
                        stimulus_st_dev = indx_st[n // 2][1]
                    else:
                        mid1_value, mid1_stdev, mid1_index = indx_st[n // 2 - 1]
                        mid2_value, mid2_stdev, mid2_index = indx_st[n // 2]
                        
                        stimulus_resp = (mid1_value + mid2_value) / 2
                        stimulus_st_dev = (mid1_stdev + mid2_stdev) / 2
            
                stimulus_list.append((stimulus_name, stimulus_resp, stimulus_st_dev, stimulus_start, stimulus_end))
            
            if not stimulus_list:
                self.no_stim_assays.append(assay_name)

            assay_dict[assay_name] = (assay_avg, assay_st_dev, stimulus_list)
        
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
                
                if stimulus_start < 0 or stimulus_start > len(mi_list[0]):
                    fish_logger.log(Fish_Log.WARNING, f"STIMULUS START INDEX OUT OF MI RANGE {len(mi_list[0])} : Assay Name {assay_name}, Assay Start {assay_start}, Assay End {assay_end}, Stimulus Name{stimulus_name}, Stimulus Start {stimulus_start}, Stimulus End {stimulus_end}, Frame Adjustment, {self.adjust_frame_index}")
                    stimulus_start = assay_start
                if stimulus_end < 0 or stimulus_end > len(mi_list[0]):
                    fish_logger.log(Fish_Log.WARNING, f"STIMULUS END INDEX OUT OF MI RANGE {len(mi_list[0])} : Assay Name {assay_name}, Assay Start {assay_start}, Assay End {assay_end}, Stimulus Name{stimulus_name}, Stimulus Start {stimulus_start}, Stimulus End {stimulus_end}, Frame Adjustment, {self.adjust_frame_index}")
                    stimulus_end = assay_end

                if stimulus_name in Sauron_Primary_Analysis.split_response_calculation.keys():
                    calc_type = Sauron_Primary_Analysis.split_response_calculation[stimulus_name]
                elif 'LED' in stimulus_name:
                    calc_type = Sauron_Primary_Analysis.split_response_calculation['light']
                elif 'solenoid' in stimulus_name or 'MP3' in stimulus_name:
                    calc_type = Sauron_Primary_Analysis.split_response_calculation['sound']

                stim_mi_list = [self.stimulus_calculator(mi_values[stimulus_start:stimulus_end], ctype=calc_type) for mi_values in mi_list]

                stimulus_list.append((stimulus_name, stim_mi_list))

            if not stimulus_list:
                self.no_stim_assays.append(assay_name)

            assay_dict[assay_name] = (assay_mi_list, stimulus_list)

        return assay_dict
    

    def med_calc(self, median_mi_list):
        sorted_data = sorted(median_mi_list)
        n = len(sorted_data)
        return sorted_data[n // 2] if n % 2 == 1 else (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2


    @staticmethod
    def st_dev_calc(mi_list):
        average = sum(mi_list) / len(mi_list)
        squared_diff = [(mi - average) ** 2 for mi in mi_list]
        variance = sum(squared_diff) / len(mi_list)
        st_dev = math.sqrt(variance)

        return st_dev


    def stimulus_calculator(self, stimulus_mi_list, ctype='max'):
        calc_resp_dict = {
            'max' : max(stimulus_mi_list),
            'avg' : sum(stimulus_mi_list) / len(stimulus_mi_list),
            'med' : self.med_calc(stimulus_mi_list),
            'sum' : sum(stimulus_mi_list),
            'st_dev' : self.st_dev_calc(stimulus_mi_list)
        }
    
        return calc_resp_dict[ctype]
    

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
                                
                                for stimulus in self.split_dictionary[treatment][concentration][assay][2]:
                                    stim_cntr += 1
                                    if stimulus[1] < assay_avg:
                                        zero_cntr += 1  

                            elif assay not in self.no_stim_assays:
                                avg_lst = [sum(assay_mi) / len(assay_mi) for assay_mi in  self.split_dictionary[treatment][concentration][assay][0]]
                                assay_avg = sum(avg_lst) / len(avg_lst)
                                
                                for stimulus_list in self.split_dictionary[treatment][concentration][assay][1]:
                                    for stim in stimulus_list:
                                        stim_cntr += 1
                                        if stim < assay_avg:
                                            zero_cntr += 1

            elif self.user_analysis_group == 'group': 
                for treatment in self.split_dictionary.keys():
                    for assay in self.split_dictionary[treatment].keys():
                        if self.user_analysis_calculations == 'full' and assay not in self.no_stim_assays:
                            assay_avg = sum(self.split_dictionary[treatment][assay][0]) / len(self.split_dictionary[treatment][assay][0])

                            for stimulus in self.split_dictionary[treatment][assay][2]:
                                stim_cntr += 1
                                if stimulus[1] < assay_avg:
                                    zero_cntr += 1


                        elif assay not in self.no_stim_assays:
                            avg_lst = [sum(assay_mi) / len(assay_mi) for assay_mi in  self.split_dictionary[treatment][assay][0]]
                            assay_avg = sum(avg_lst) / len(avg_lst)
                            
                            for stimulus_list in self.split_dictionary[treatment][assay][1]:
                                for stim in stimulus_list:
                                    stim_cntr += 1
                                    if stim < assay_avg:
                                        zero_cntr += 1
            
            responses = stim_cntr - zero_cntr
            response_cutoff = 10 * responses

            if stim_cntr > response_cutoff:
                self.warning["NO_STIM"] = self.adjust_frame_index
                fish_logger.log(Fish_Log.WARNING, f'I do not think there are any responses within the current stimuli ranges! Stimuli {stim_cntr}, Responses {responses}; Current frame adjustment {self.adjust_frame_index}')
            else:
                fish_logger.log(Fish_Log.INFO, f'the stimuli responsiveness made the cutoff {response_cutoff} with {stim_cntr} stimuli and {responses} responses')

    
    def finalize_bio_info(self):
        self.treatments = [treatment for treatment in self.sorted_dictionary.keys()]
        if self.user_analysis_group == 'treatment':
            self.concentration_dict = {treatment : [concentration for concentration in self.sorted_dictionary[treatment].keys()] for treatment in self.sorted_dictionary.keys()}
    

    def stim_finder(self):
        self.shift_finding_package_maker()
        
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
            for treatment in self.averaged_dictionary.keys():
                for concentration in self.averaged_dictionary[treatment].keys():
                    best_match_shift = self.match_shift_finder(self.averaged_dictionary[treatment][concentration][0])
                    if best_match_shift:
                        best_match_shift_list.append(best_match_shift)

        else:
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
            shift = int(shift)

            fish_logger.log(Fish_Log.INFO, f'I found best shift {shift} with confidence {confidence}')

            best_match = (confidence, shift)

        return best_match
            
            
    def split_fix_group(self):
        best_match_shift_list = []
        best_match = None

        if self.user_analysis_calculations == 'full':
            for group_name in self.averaged_dictionary.keys():
                best_match_shift = self.match_shift_finder(self.averaged_dictionary[group_name][0])
                if best_match_shift:
                    best_match_shift_list.append(best_match_shift)
                
        else:
            for group_name in self.sorted_dictionary.keys():
                best_match_shift = self.raw_stim_finder(self.sorted_dictionary[group_name])
                if best_match_shift:
                    best_match_shift_list.append(best_match_shift)

        if best_match_shift_list:
            percentage = [ms[0] for ms in best_match_shift_list]
            shifts = [ms[1] for ms in best_match_shift_list]
            confidence = sum(percentage) / len(percentage)
            shift = sum(shifts) / len(shifts)
            shift = int(shift)

            fish_logger.log(Fish_Log.INFO, f'I found best shift {shift} with confidence {confidence}')

            best_match = (confidence, shift)
                
        return best_match


    def shift_finding_package_maker(self):
        stim_start_list = [int(stimulus[1][0] / self.frame_rate) for assay in self.battery_info for stimulus in assay[2]]
        stim_end_list = [int(stimulus[1][1] / self.frame_rate) for assay in self.battery_info for stimulus in assay[2]]
        
        stim_len = [stim_end_list[n] - stim_start_list[n] for n in range(0, len(stim_start_list))]

        f_stim_start = []
        f_stim_end = []
        for s in range(len(stim_start_list)-1):
            if stim_start_list[s+1] < stim_start_list[s] + stim_len[s]:
                if stim_end_list[s] > stim_end_list[s+1]:
                    pass 
                else:
                    f_stim_start.append(stim_start_list[s])
                    f_stim_end.append(stim_end_list[s])
            else:
                f_stim_start.append(stim_start_list[s])
                f_stim_end.append(stim_end_list[s])

        f_stim_mid = [int((f_stim_start[n] + f_stim_end[n]) / 2) for n in range(0, len(f_stim_start))]

        stim_pattern = [f_stim_start[n+1] - f_stim_start[n] for n in range(0, len(f_stim_start)-1)]

        self.shift_finding_package = {
            'stimulus_starts' : f_stim_start,
            'stimulus_ends' : f_stim_end, 
            'stimulus_midpoints' : f_stim_mid,
            'stimulus_pattern' : stim_pattern
        }


    def match_shift_finder(self, mi_list):
        average_mi_trace = sum(mi_list) / len(mi_list)

        mi_cutoff_v = average_mi_trace * 50 

        response_vals = [t for t, mi in enumerate(mi_list) if mi > mi_cutoff_v]

        response_val_min = [] 
        i = 0 
        max_conseq_resp = 0
        max_t = 0

        while i < len(response_vals)-1:
            if response_vals[i+1] - 1 == response_vals[i]:
                if mi_list[response_vals[i]] > max_conseq_resp:
                    max_conseq_resp = mi_list[response_vals[i]]
                    max_t = response_vals[i]
            
            elif i > 0 and response_vals[i-1] + 1 == response_vals[i]:
                if mi_list[response_vals[i]] > max_conseq_resp:
                    max_conseq_resp = mi_list[response_vals[i]]
                    max_t = response_vals[i]
                
                response_val_min.append(max_t)
                max_conseq_resp = 0
                max_t = 0

            else:
                response_val_min.append(response_vals[i])
            
            i+=1

        best_match = None # match ratio, frame shift

        if not response_val_min:
            pass

        else:
            best_match = (0, 0) # match ratio, frame shift

            for t in range(0, len(response_val_min)):
                start_stim = 0
                
                lower_bound = self.shift_finding_package['stimulus_starts'][start_stim] - 100
                if lower_bound < 0:
                    lower_bound = 0
                
                while start_stim < len(self.shift_finding_package['stimulus_pattern']) and response_val_min[t] > 100 + self.shift_finding_package['stimulus_ends'][start_stim]:
                    if response_val_min[t] < lower_bound:
                        start_stim -= 1
                        break

                    start_stim += 1

                if start_stim == -1:
                    start_stim = 0
                            
                t_pattern = [response_val_min[t] + self.shift_finding_package['stimulus_pattern'][i] for i in range(start_stim, len(self.shift_finding_package['stimulus_pattern']))]
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
                    calc_shift = int(response_val_min[t] - self.shift_finding_package['stimulus_midpoints'][start_stim])
                    best_match = (match_ratio, calc_shift) 
                
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

        self.responsive_dictionary = {}
        self.habituation_dictionary = {}
        self.prepulse_inhibition_dictionary = {}
        self.cutoff_percentage = 0.20 # for determining habituation slope
        self.habituation_responsive_dictionary = {}
        self.group_response_dictionary = {}
        self.group_habituation_dictionary = {}
        self.group_prepulse_inhibition_dictionary = {}

        self.warning = {}


    def responsiveness(self):
        # ['assay_mi_average', 'assay_mi_median', 'assay_mi_max', 'stimulus_average', 'stimulus_median', 'stimulus_min']
        # # # assays without stimuli should use assay mi calculations !
        assay_response_caclculations = {
            "Assay_Name_Example" : 'default',
            "no_stimulus" : 'assay_mi_average',
            "background" : 'assay_mi_sum',
            "5min_background" : 'assay_mi_sum',
            "StrobeBlue250ms2" : 'assay_mi_sum',
            "StrobeGreen250ms" : 'assay_mi_sum'
        }
        
        if self.sauron_primary_analysis.user_analysis_group == 'treatment':
            for treatment in self.sauron_primary_analysis.split_dictionary.keys():
                for concentration in self.sauron_primary_analysis.split_dictionary[treatment].keys():
                    for assay in self.sauron_primary_analysis.split_dictionary[treatment][concentration].keys():
                        if assay in assay_response_caclculations.keys():
                            response = self.responsive_calculator(self.sauron_primary_analysis.split_dictionary[treatment][concentration][assay], tpe=assay_response_caclculations[assay])
                        elif not self.sauron_primary_analysis.split_dictionary[treatment][concentration][assay][2]:
                            response = self.responsive_calculator(self.sauron_primary_analysis.split_dictionary[treatment][concentration][assay], tpe=assay_response_caclculations['no_stimulus'])
                        else:
                            response = self.responsive_calculator(self.sauron_primary_analysis.split_dictionary[treatment][concentration][assay])

                        if isinstance(response, dict):
                            for stimulus in response.keys():
                                asy_stim_name = f"{assay+stimulus}"

                                if asy_stim_name not in self.responsive_dictionary.keys():
                                    self.responsive_dictionary[asy_stim_name] = {treatment : {concentration : response[stimulus]}}
                                elif treatment not in self.responsive_dictionary[asy_stim_name].keys():
                                    self.responsive_dictionary[asy_stim_name].update({treatment : {concentration : response[stimulus]}})
                                else:
                                    self.responsive_dictionary[asy_stim_name][treatment].update({concentration : response[stimulus]})
                        
                        else:
                            asy_stim_name = f"{assay}"
                            if asy_stim_name not in self.responsive_dictionary.keys():
                                self.responsive_dictionary[asy_stim_name] = {treatment : {concentration : response}}
                            elif treatment not in self.responsive_dictionary[asy_stim_name].keys():
                                self.responsive_dictionary[asy_stim_name].update({treatment : {concentration : response}})
                            else:
                                self.responsive_dictionary[asy_stim_name][treatment].update({concentration : response})
        
        else:
            for group in self.sauron_primary_analysis.split_dictionary.keys():
                for assay in self.sauron_primary_analysis.split_dictionary[group].keys():
                    if assay in assay_response_caclculations.keys():
                        response = self.responsive_calculator(self.sauron_primary_analysis.split_dictionary[group][assay], tpe=assay_response_caclculations[assay])
                    else:
                        response = self.responsive_calculator(self.sauron_primary_analysis.split_dictionary[group][assay])
                    
                    if isinstance(response, dict):
                        for stimulus in response.keys():
                            asy_stim_name = f"{assay+stimulus}"
                            if asy_stim_name not in self.responsive_dictionary.keys():
                                self.responsive_dictionary[asy_stim_name] = {group : response[stimulus]}
                            else:
                                self.responsive_dictionary[asy_stim_name].update({group : response[stimulus]})
                            
                    else:
                        asy_stim_name = f"{assay}"
                        if asy_stim_name not in self.responsive_dictionary.keys():
                            self.responsive_dictionary[asy_stim_name] = {group : response}
                        else:
                            self.responsive_dictionary[asy_stim_name].update({group : response})

        fish_logger.log(Fish_Log.INFO, f'responsive dictionary {list(self.responsive_dictionary.keys())}')

    
    def habituation_response(self):
        if self.habituation_dictionary:
            if self.sauron_primary_analysis.user_analysis_group == 'treatment':
                for treatment in self.habituation_dictionary.keys():
                    for concentration in self.habituation_dictionary[treatment].keys():
                        for assay in self.habituation_dictionary[treatment][concentration].keys():
                            for stimulus in self.habituation_dictionary[treatment][concentration][assay].keys():
                                assay_stim_str = f"{assay} :: {stimulus}"
                                if assay_stim_str not in self.habituation_responsive_dictionary.keys():
                                    self.habituation_responsive_dictionary[assay_stim_str] = {treatment : {concentration : (-1 * self.habituation_dictionary[treatment][concentration][assay][stimulus][2], self.habituation_dictionary[treatment][concentration][assay][stimulus][5])}}
                                elif treatment not in self.habituation_responsive_dictionary[assay_stim_str].keys():
                                    self.habituation_responsive_dictionary[assay_stim_str].update({treatment : {concentration : (-1 * self.habituation_dictionary[treatment][concentration][assay][stimulus][2], self.habituation_dictionary[treatment][concentration][assay][stimulus][5])}})
                                else:
                                    self.habituation_responsive_dictionary[assay_stim_str][treatment].update({concentration : (-1 * self.habituation_dictionary[treatment][concentration][assay][stimulus][2], self.habituation_dictionary[treatment][concentration][assay][stimulus][5])})
            
            else:
                for group in self.habituation_dictionary.keys():
                    for assay in self.habituation_dictionary[group].keys():
                        for stimulus in self.habituation_dictionary[group][assay].keys():
                                assay_stim_str = f"{assay} :: {stimulus}"
                                if assay_stim_str not in self.habituation_responsive_dictionary.keys():
                                    self.habituation_responsive_dictionary[assay_stim_str] = {group : (-1 * self.habituation_dictionary[group][assay][stimulus][2], self.habituation_dictionary[group][assay][stimulus][5])}
                                else:
                                    self.habituation_responsive_dictionary[assay_stim_str].update({group : (-1 * self.habituation_dictionary[group][assay][stimulus][2], self.habituation_dictionary[group][assay][stimulus][5])})

        fish_logger.log(Fish_Log.INFO, f'habituation response dictionary {list(self.habituation_responsive_dictionary.keys())}')


    def grouping(self):        
        if self.responsive_dictionary:
            self.group_response_dictionary = self.activity_grouper(self.responsive_dictionary)
            fish_logger.log(Fish_Log.INFO, f'group response dictionary {list(self.group_response_dictionary.keys())}')

        if self.habituation_responsive_dictionary:
            self.group_habituation_dictionary = self.activity_grouper(self.habituation_responsive_dictionary)
            fish_logger.log(Fish_Log.INFO, f'group habituation dictionary {list(self.group_habituation_dictionary.keys())}')
        
        if self.prepulse_inhibition_dictionary:
            self.group_prepulse_inhibition_dictionary = self.activity_grouper(self.prepulse_inhibition_dictionary)
            fish_logger.log(Fish_Log.INFO, f'group ppi dictionary {list(self.prepulse_inhibition_dictionary.keys())}')
    

    def activity_grouper(self, dictionary):
        sigma = 1
        return_dict = {}
        if self.sauron_primary_analysis.user_analysis_group == 'treatment':
            for asy_stm in dictionary.keys():
                full_tup_lst = [(dictionary[asy_stm][trt][cnc][0], dictionary[asy_stm][trt][cnc][1], (dictionary[asy_stm][trt][cnc][0] - sigma * dictionary[asy_stm][trt][cnc][1]), (dictionary[asy_stm][trt][cnc][0] + sigma * dictionary[asy_stm][trt][cnc][1]), trt, cnc) for trt in dictionary[asy_stm].keys() for cnc in dictionary[asy_stm][trt].keys()]

                web = []
                for tup in full_tup_lst:
                    connections = []
                    for trt in dictionary[asy_stm].keys(): 
                        for cnc in dictionary[asy_stm][trt].keys():
                            if dictionary[asy_stm][trt][cnc][0] >= tup[2] and dictionary[asy_stm][trt][cnc][0] <= tup[3]:
                                c_tup = (trt, cnc)
                                connections.append(c_tup)
                    
                    web_tup = (tup[4], tup[5], tup[0], tup[1], tup[2], tup[3], connections, len(connections))
                    web.append(web_tup)

                sorted_web = sorted(web, key=lambda item: (item[7], item[2]))

                group_dict = {
                    f"{sorted_web[0][0]} {sorted_web[0][1]}" : (sorted_web[0][2], sorted_web[0][3], sorted_web[0][6])
                }

                key_dict = {(point[0], point[1]) : (point[2], point[3]) for point in sorted_web}

                for point in sorted_web:
                    not_found = True
                    point_tup = (point[0], point[1])
                    for trt_cnc, srt_tup in group_dict.items():
                        if point_tup in srt_tup[2]:
                            not_found = False
                    
                    if not_found:
                        name = f"{point[0]} {point[1]}"
                        group_dict.update({name : (point[2], point[3], point[6])})
                return_dict[asy_stm] = (group_dict, key_dict)

        else:
            for asy_stm in dictionary.keys():
                full_tup_lst = [(dictionary[asy_stm][grp][0], dictionary[asy_stm][grp][1], (dictionary[asy_stm][grp][0] - sigma * dictionary[asy_stm][grp][1]), (dictionary[asy_stm][grp][0] + sigma * dictionary[asy_stm][grp][1]), grp) for grp in dictionary[asy_stm].keys()]
                
                web = []
                for tup in full_tup_lst:
                    connections = []
                    for grp in dictionary[asy_stm].keys(): 
                        if dictionary[asy_stm][grp][0] >= tup[2] and dictionary[asy_stm][grp][0] <= tup[3]:
                            connections.append(grp)
                    
                    connect_tup = (tup[4], tup[0], tup[1], tup[2], tup[3], connections, len(connections))
                    web.append(connect_tup)

                sorted_web = sorted(web, key=lambda item: (item[6], item[2]))

                group_dict = {
                    sorted_web[0][0] : (sorted_web[0][1], sorted_web[0][2], sorted_web[0][5])
                }
                
                key_dict = {point[0] : (point[1], point[2]) for point in sorted_web}
                curr_total = [sorted_web[0][0]]
                for point in sorted_web:
                    not_found = True
                    for grp, srt_tup in group_dict.items():
                        if point[0] in srt_tup[2]:
                            not_found = False
                    
                    if not_found:
                        if point[0] not in curr_total:
                            group_dict.update({point[0] : (point[1], point[2], point[5])})
                            curr_total.append(point[0])
                return_dict[asy_stm] = (group_dict, key_dict) 
        
        return return_dict


    def habituation(self):
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
                            for stimulus_name, stimulus_avg, stimulus_st_dev, stim_st, stim_ed in split_dictionary[treatment][concentration][assay][2]:
                                if stimulus_name in habituation_stimuli:
                                    stimuli_found.add(stimulus_name)
                                    if stimulus_name not in stimulus_dictionary.keys():
                                        stimulus_dictionary[stimulus_name] = ([stimulus_avg], [stimulus_st_dev])
                                    else:
                                        stimulus_dictionary[stimulus_name][0].append(stimulus_avg)
                                        stimulus_dictionary[stimulus_name][1].append(stimulus_st_dev)
                                
                            stim_habit_dict = self.stimulus_dict_calcs(stimulus_dictionary) #assay_mi_average, assay_st_dev)
                    
                            if treatment not in habituation_dict.keys():
                                habituation_dict[treatment] = {concentration : {assay : stim_habit_dict}}
                            elif concentration not in habituation_dict[treatment].keys():
                                habituation_dict[treatment][concentration] = {assay : stim_habit_dict}
                            else:
                                habituation_dict[treatment][concentration][assay] = stim_habit_dict

        else:
            for group in split_dictionary.keys():
                for assay in split_dictionary[group].keys():
                    if assay in habituation_assays:
                        assays_found.add(assay)
                        stimulus_dictionary = {}
                        for stimulus_name, stimulus_avg, stimulus_st_dev, stim_st, stim_ed in split_dictionary[group][assay][2]:
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


    def prepulse_inhibition(self):
        ppi_dict = {}

        ppi_assays = ['ppi_100x_4peak']

        if self.sauron_primary_analysis.user_analysis_group == 'treatment':
            for treatment in self.sauron_primary_analysis.split_dictionary.keys():
                for concentration in self.sauron_primary_analysis.split_dictionary[treatment].keys():
                    for assay in self.sauron_primary_analysis.split_dictionary[treatment][concentration].keys():
                        if assay in ppi_assays:
                            index_d = {}
                            
                            for stimulus_name, stimulus_avg, stimulus_st_dev, stim_st, stim_ed in self.sauron_primary_analysis.split_dictionary[treatment][concentration][assay][2]:
                                if stimulus_name not in index_d.keys():
                                    index_d[stimulus_name] = 1
                                else:
                                    index_d[stimulus_name] += 1 

                                index = index_d[stimulus_name]
                                
                                asy_stm_i = f"{assay} {stimulus_name}_{index+1}"

                                if asy_stm_i not in ppi_dict.keys():
                                    ppi_dict[asy_stm_i] = {treatment : {concentration : (stimulus_avg, stimulus_st_dev)}}
                                elif treatment not in ppi_dict[asy_stm_i].keys():
                                    ppi_dict[asy_stm_i].update({treatment : {concentration : (stimulus_avg, stimulus_st_dev)}})
                                else:
                                    ppi_dict[asy_stm_i][treatment].update({concentration : (stimulus_avg, stimulus_st_dev)})
                                
                                

        else:
            for group in self.sauron_primary_analysis.split_dictionary.keys():
                for assay in self.sauron_primary_analysis.split_dictionary[group].keys():
                    if assay in ppi_assays:
                        index_d = {}
                        for stimulus_name, stimulus_avg, stimulus_st_dev, stim_st, stim_ed in self.sauron_primary_analysis.split_dictionary[group][assay][2]:
                            if stimulus_name not in index_d.keys():
                                index_d[stimulus_name] = 1
                            else:
                                index_d[stimulus_name] += 1

                            index = index_d[stimulus_name] 
                        
                            asy_stm_i = f"{assay} {stimulus_name}_{index+1}"

                            if asy_stm_i not in ppi_dict.keys():
                                ppi_dict[asy_stm_i] = {group : (stimulus_avg, stimulus_st_dev)}
                            else: 
                                ppi_dict[asy_stm_i].update({group : (stimulus_avg, stimulus_st_dev)})
                            
        
        self.prepulse_inhibition_dictionary = ppi_dict


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
                stimulus_slope, stimulus_intercept, stimulus_r_squared, average_st_dev = self.weighted_line_calculator(stim_vals, stim_st_devs)
                
                result_dict[stimulus_name] = (stimulus_average_list, stimulus_st_dev_list, stimulus_slope, stimulus_intercept, stimulus_r_squared, average_st_dev, drop_i)

        return result_dict
    

    def responsive_calculator(self, assay_tup, tpe='default'):
        if tpe == 'default':
            value = self.stimuli_responsive_calculator(assay_tup[2])

        elif tpe == 'assay_mi_average':
            value = round(float(sum(assay_tup[0]) / len(assay_tup[0])), 2)
            st_dev = self.basic_calculator(assay_tup[0], "st_dev")
            value = (value, st_dev)

        elif tpe == 'assay_mi_median':
            value, st_dev = self.med_calc(assay_tup[0], std_list=assay_tup[2])
            value = (value, st_dev)

        elif tpe == 'assay_mi_max':
            value = max(assay_tup[0])   
            for idx in range(len(assay_tup[0])):
                if assay_tup[0][idx] == value:
                    st_dev = assay_tup[1][idx]
            value = (value, st_dev)

        elif tpe == 'assay_mi_sum':
            value = sum(assay_tup[0])
            st_dev = sum(assay_tup[1])
            value = (value, st_dev)

        elif tpe == 'stimulus_average':
            value = self.stimuli_responsive_calculator(assay_tup[2], ty='average')

        elif tpe == 'stimulus_median':
            value = self.stimuli_responsive_calculator(assay_tup[2], ty='median')

        elif tpe == 'stimulus_max':
            value = self.stimuli_responsive_calculator(assay_tup[2], ty='max')

        elif tpe == 'stimulus_min':
            value = self.stimuli_responsive_calculator(assay_tup[2], ty='min')

        elif tpe == 'stimulus_sum':
            value = self.stimuli_responsive_calculator(assay_tup[2], ty='sum')


        return value
    

    def stimuli_responsive_calculator(self, stimulus_list, ty='average'):
        result_dict = {}

        stimulus_names = [stim[0] for stim in stimulus_list]
        stimulus_names = set(stimulus_names)

        stim_resp_dict = {}
        
        for name in stimulus_names:
            s_lst = []
            for stimulus in stimulus_list:
                if stimulus[0] == name:
                    s_tup = (stimulus[1], stimulus[2])
                    s_lst.append(s_tup)
            stim_resp_dict[name] = s_lst

        for stim_name, stim_list in stim_resp_dict.items():
            response, st_dev = self.stim_tup_calculator(stim_list, ty)
            
            result_dict[stim_name] = (response, st_dev)

        return result_dict
        
    
    def line_calculator(self, mi_list, st_dev_list):
        x_vals = [x + 1 for x in range(len(mi_list))]
        
        slope, intercept = self.calculate_slope(x_vals, mi_list, intrcpt=True)
        r_sq = self.calculate_r_squared(slope, intercept, x_vals, mi_list)
        avg_st_dev = self.calculate_avg_st_dev(st_dev_list)

        return slope, intercept, r_sq, avg_st_dev
    

    def weighted_line_calculator(self, y_lst, st_dev_lst):
        x_lst = [x + 1 for x in range(len(y_lst))]
        weights = [1 / (st_dev**2) if st_dev else 0.01 for st_dev in st_dev_lst]
        total_weight = sum(weights)

        weighted_x = sum(w * x_i for w, x_i in zip(weights, x_lst))
        weighted_y = sum(w * y_i for w, y_i in zip(weights, y_lst))

        mean_x_weight = weighted_x / total_weight
        mean_y_weight = weighted_y / total_weight

        numerator = sum(w * (x_i - mean_x_weight) * (y_i - mean_y_weight) for w, x_i, y_i in zip(weights, x_lst, y_lst))
        denominator = sum(w * (x_i - mean_x_weight) ** 2 for w, x_i in zip(weights, x_lst))
        slope = numerator / denominator

        intercept = mean_y_weight - slope * mean_x_weight
        slope_error = (1 / denominator) ** 0.5

        r_sq = self.calculate_r_squared(slope, intercept, x_lst, y_lst)

        return slope, intercept, r_sq, slope_error
    

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


    def basic_calculator(self, lst_v, operation):
        calculator = {
            "average" : round(float(sum(lst_v) / len(lst_v)), 2),
            "median" : self.med_calc(lst_v),
            "max" : max(lst_v),
            "min" : min(lst_v),
            "sum" : sum(lst_v),
            "st_dev" : self.st_dev_calc(lst_v)
        }

        return calculator[operation]
    

    def stim_tup_calculator(self, stim_tup_list, operation):
        value = 0
        st_dev = 0

        if operation == 'average':
            stim_v = [s[0] for s in stim_tup_list]
            stim_std = [s[1] for s in stim_tup_list]

            value = self.basic_calculator(stim_v, 'average')
            st_dev = self.basic_calculator(stim_v, 'st_dev')
        
        elif operation == 'median':
            indx_st_tup = sorted((value, st_dev, index) for index, (value, st_dev) in enumerate(stim_tup_list))
            
            n = len(indx_st_tup)

            if n % 2 == 1:
                value = indx_st_tup[n // 2][0]
                st_dev = indx_st_tup[n // 2][1]
            else:
                mid1_value, mid1_stdev, mid1_index = indx_st_tup[n // 2 - 1]
                mid2_value, mid2_stdev, mid2_index = indx_st_tup[n // 2]
                
                value = (mid1_value + mid2_value) / 2
                st_dev = (mid1_stdev + mid2_stdev) / 2 
    
        elif operation == 'max':
            value = 0
            for s_t in stim_tup_list:
                if s_t[0] > value:
                    value = s_t[0]
                    st_dev = s_t[1]
        
        elif operation == 'min':
            stim_v = [s[0] for s in stim_tup_list]
            value = max(stim_v)
            for s_t in stim_tup_list:
                if s_t[0] < value:
                    value = s_t[0]
                    st_dev = s_t[1]

        elif operation == 'sum':
            stim_v = [s[0] for s in stim_tup_list]
            stim_std = [s[1] for s in stim_tup_list]

            value = self.basic_calculator(stim_v, 'sum')
            st_dev = self.basic_calculator(stim_std, 'sum')
            
        return value, st_dev
    

    def med_calc(self, median_mi_list, std_list=False):
        sorted_data = sorted(median_mi_list)
        n = len(sorted_data)
        
        if n % 2 == 1:
            median = sorted_data[n // 2]
        else:
            median = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
        
        if not std_list:
            return median
        
        sorted_std = [s for _, s in sorted(zip(median_mi_list, std_list))]  # sort std_list to match sorted_data
        if n % 2 == 1:
            median_std = sorted_std[n // 2]
        else:
            median_std = (sorted_std[n // 2 - 1] + sorted_std[n // 2]) / 2
    
        return median, median_std


    def st_dev_calc(self, mi_list):
        n = len(mi_list)
        return ((sum((x - (sum(mi_list) / n)) ** 2 for x in mi_list) / n) ** 0.5) if n > 0 else 0






