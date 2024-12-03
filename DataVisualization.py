import os 
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.patches as mpatches
from matplotlib.colorbar import ColorbarBase
import matplotlib.backends.backend_pdf as pdf
import numpy as np
from datetime import datetime

from FishLog import Fish_Log


# % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % 
# HELLO, this is DataVisualization                #
# # the file contains classes for the purposes of #
# # visualizing information. The currently two    #
# # classes are for outputting info via text or   #
# # graphs in a .txt or .pdf file respectively    #
# % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ %


fish_logger = Fish_Log()
    



class Sauron_Text_Visualization():
    # % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ %
    # HELLO, this is the class Sauron_Text_Visualization  # 
    # # the main purpose of this class is to first sort   # 
    # # # the info to be written in a string and then     # 
    # # # write the string to a text file                 # 
    # # the class is structured such that when it is      # 
    # # # instantiated, the init function initialized the # 
    # # # finial attributes as None and calls a sorting   # 
    # # # function to determine which information to put  # 
    # # # into the string. Separate string making         # 
    # # # functions are called before a final text_write  # 
    # # # function.                                       #  
    # # inputs to the class are the user responses        # 
    # # # battery info, analyzed info (when poss.)        # 
    # # # and secondary info (when poss.)                 # 
    # # output of the class is a text file                # 
    # # the class is instantiated by FishBrain with the   # 
    # # # necessary information from other parts of the   # 
    # # # script                                          # 
    # % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ %


    save_directory = "SauronResults/TextOutput/"


    def __init__(self, run_number, analysis_type, battery_info, name_file, user_file, treatments=None, concentration_dict=None, habituation_dict=None):
        self.run_number = run_number
        self.analysis_type = analysis_type
        self.battery_info = battery_info
        self.name_file = name_file
        self.user_file = user_file
        self.treatments = treatments
        self.concentration_dict = concentration_dict
        self.habituation_dict = habituation_dict

        self.warning = {}

        self.datetime_date = self.get_datetime()

        self.check_save_dir()

        self.text_sort()

    
    def check_save_dir(self):
        os.makedirs(self.save_directory, exist_ok=True)

    
    def get_datetime(self):
        return datetime.now().strftime("%Y%m%d")
        


    def make_filename(self):
        if self.user_file:
            return f"{self.user_file}"
        elif self.analysis_type == 'battery':
            return f"{self.datetime_date}_BATTERY_{self.battery_info.battery_number}_{self.analysis_type}" 
        else:
            return f"{self.datetime_date}_RUN_{self.run_number}_{self.analysis_type}" 

    
    def filename_helper(self, filename, extension):
        not_fixed = True
        name_iter = 1

        while not_fixed:
            new_filename = f'{filename}_{name_iter:02d}' #if numbers greater than 99 are desired, this needs to be changed!
            new_filepath = f'{self.save_directory}{new_filename}{extension}'

            if os.path.exists(new_filepath):
                if name_iter > 99:
                    self.warning['FILENAME_HELPER'] = filename
                    return 
                name_iter += 1
            else:
                not_fixed = False
            
        return new_filename


    def text_sort(self):
        if self.analysis_type == 'battery':
            f_str = f'{self.battery_details(stimulus=True)}'
        elif self.analysis_type == 'preview':
            f_str = f'{self.run_details()}{self.treatment_details()}{self.battery_details(stimulus=True)}'
        elif self.habituation_dict:
            f_str = f'{self.run_details()}{self.habituation_details()}'
        else:
            f_str = f'{self.run_details()}{self.treatment_details()}{self.battery_details()}'
        
        self.text_write(f_str)

    
    def run_details(self):
        return f'RUN {self.run_number}\n'


    def treatment_details(self):
        return '\n'.join([f"\n{treatment}\n" + '\n'.join([f"\t{concentration}uM" for concentration in self.concentration_dict[treatment]]) for treatment in self.treatments])
        

    def battery_details(self, stimulus=False):
        btry_str = f'\n*****\nBattery Number : {self.battery_info.battery_number}\n'
        if self.battery_info.frame_rate and stimulus:
            btry_str = f'{btry_str}Frame Rate: {self.battery_info.frame_rate} frames\n'
            return btry_str + '\n'.join([f"Assay: {assay_name} ({int(assay_start/self.battery_info.frame_rate)} nframe : {int(assay_end/self.battery_info.frame_rate)} nframe)\n" +
                              '\n'.join([f"\t- {stimulus_name} ({int(stimulus_start/self.battery_info.frame_rate)} nframe : {int(stimulus_end/self.battery_info.frame_rate)} nframe)"
                                         for stimulus_name, (stimulus_start, stimulus_end) in stimulus_list])
                              for assay_name, (assay_start, assay_end), stimulus_list in self.battery_info.battery_info])
        
        elif self.battery_info.frame_rate:
            btry_str = f'{btry_str}Frame Rate: {self.battery_info.frame_rate}\n'
            return btry_str + '\n'.join([f"Assay: {assay_name} ({int(assay_start/self.battery_info.frame_rate)} nframe : {int(assay_end/self.battery_info.frame_rate)} nframe)\n"
                              for assay_name, (assay_start, assay_end), stimulus_list in self.battery_info.battery_info])

        
        elif stimulus:
            return btry_str + '\n'.join([f"Assay: {assay_name} ({assay_start} ms : {assay_end} ms)\n" +
                              '\n'.join([f"\t- {stimulus_name} ({stimulus_start} ms, {stimulus_end} ms)"
                                         for stimulus_name, (stimulus_start, stimulus_end) in stimulus_list])
                              for assay_name, (assay_start, assay_end), stimulus_list in self.battery_info.battery_info])
        
        else:
            return btry_str + '\n'.join([f"Assay: {assay_name} ({assay_start} ms : {assay_end} ms)\n"
                              for assay_name, (assay_start, assay_end), stimulus_list in self.battery_info.battery_info])


    def habituation_details(self):
        habit_start = f'--*-*-*-Habituation Analysis-*-*-*--\n'
        if self.concentration_dict:
            habit_str = [
                        f"{assay} : {stimulus_name}\n{treatment}\n" +
                        "\n".join([
                            f"- {concentration} : (slope, {data[2]}), (r squared, {data[4]}), (average st dev, {data[5]})"
                            for concentration, assays in concentrations.items()
                            for assay_name, stim_habit_dict in assays.items()
                            for stimulus_name, data in stim_habit_dict.items()
                        ])
                        for treatment, concentrations in self.habituation_dict.items()
                        for concentration, assay in concentrations.items()
                        for assay_name, stim_habit_dict in assay.items()
                        for stimulus_name, data in stim_habit_dict.items()
                    ]

            habit_out_str = "\n".join(habit_str)
            
        else:
            habit_str = [
                        f"{assay_name} : {stimulus_name}\n{treatment}\n" +
                        "\n".join([
                            f"- (slope, {data[2]}), (r squared, {data[4]}), (average st dev, {data[5]})"
                            for treatment, assay in self.habituation_dict.items()
                            for assay_name, stim_habit_dict in assay.items()
                            for stimulus_name, data in stim_habit_dict.items()
                        ])
                        for treatment, assay in self.habituation_dict.items()
                        for assay_name, stim_habit_dict in assay.items()
                        for stimulus_name, data in stim_habit_dict.items()
                    ]

            habit_out_str = "\n".join(habit_str)
        
        return f'{habit_start}{habit_out_str}'


    def text_write(self, write_string):
        filename = self.make_filename()
        file_path = f"{self.save_directory}/{filename}.txt"

        if os.path.exists(file_path):
            filename = self.filename_helper(filename, '.txt')
            file_path = f"{self.save_directory}/{filename}.txt"

        fish_logger.log(Fish_Log.INFO, f"File Name {filename}, File Path {file_path}")
        with open(file_path, 'w') as textfile:
            textfile.write(write_string)




class Sauron_Plot_Visualization():
    # % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ %
    # HELLO, this is the class Sauron_Plot_Visualization  #
    # # the main purpose is to sort the information       #
    # # # into plottable dictionarys which are then       # 
    # # # plotted into pdf files                          #
    # # this class is structured such that when it is     # 
    # # # instantiated, the dictionary with               #
    # # # info is called based on user input, the info    # 
    # # # is sorted into a dictionary before calling      # 
    # # # a plotting function on the dictionary to        #
    # # # generate the plots and save them as a pdf       #
    # # inputs to the class are user input, the           #
    # # # finalized primary and secondary information     #
    # # outputs are pdf files with plots                  #
    # # this class is used by FishBrain to identify       #
    # # # which plots to make / make them                 #
    # % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ %

    save_directory = "SauronResults/PdfOutput/"

    overlay_line_colors = {
        0 : '#2583E6', # blue      
        1 : '#EB00AC', # magenta
        2 : '#2CB507', # green  
        3 : '#8D00EB', # dark_purple   
        4 : '#E69307', # orange
        5 : '#40E6E4', # light_blue   
        6 : '#994683', # light_purple
        7 : '#E6CE28', # yellow
        8 : '#93E660', # light_green
        9 : '#56728F', # gray_blue
        10 : '#EB401A', # red
        11 : '#966442' # brown
    }

    habit_line_colors = {
        0 : '#2594E6', # blue      
        1 : 'gray',
        2 : '#186399',
        3 : 'black'
    }

    stimulus_colors = {
        'purple_LED' : '#9696D1', # light purple
        'soft_solenoid' : '#EB00AC', # magenta
        'blue_LED' : '#2465E6', # blue
        'red_LED' : '#EB401A', # red
        'solenoid' : '#28DBBB', # light blue
        'MP3' : '#DBBD00', # yellow
        'green_LED' : '#37B833' # green
    }

    group_colors = {
        0 : '#2465E6', # blue
        1 : '#EB401A', # red
        2 : '#37B833', # green
        3 : '#EB00AC', # magenta
        4 : '#DBBD00', # yellow
        5 : '#28DBBB', # light blue
        6 : '#FFA4D7', # pink
        7 : '#600CAD', # dark purple
        8 : '#9696D1', # light purple
        9 : '#BDAA67', # tan
        10 : '#7B30BD', # purple
        11 : '#025E1B', # dark green
        12 : '#5C2600', # orange brown
        13 : '#5C294F', # mauve
        14 : '#1E1D41' # navy blue
    }


    def __init__(self, analysis_type, run_number, battery_plot, analysis_group, analysis_calculations, 
                 visualize_battery, specific_treatment, user_treatments, specific_assay, user_assay, 
                 isolate_stimuli, name_title, user_title, name_file, user_file, visualize_secondary, 
                 user_control, battery_information, final_information, split_str):
        self.analysis_type = analysis_type
        self.run_number = run_number
        self.battery_plot = battery_plot
        self.analysis_group = analysis_group
        self.analysis_calculations = analysis_calculations
        self.visualize_battery = visualize_battery
        self.specific_treatment = specific_treatment
        self.user_treatments = user_treatments
        self.specific_assay = specific_assay
        self.user_assay = user_assay
        self.isolate_stimuli = isolate_stimuli
        self.name_title = name_title
        self.user_title = user_title
        self.name_file = name_file
        self.user_file = user_file
        self.visualize_secondary = visualize_secondary
        self.user_control = user_control
        self.battery_information = battery_information
        self.final_information = final_information
        self.split_str = split_str 
        
        self.calc = 'average' # hidden setting
        self.calc_plot = {
            'average' : 1, # tuple index for average 
            'median' : 2 # tuple index for median
        }
        self.calc_indx = self.calc_plot[self.calc] # call index for plotting 

        self.colorbar = False # currently for testing purposes only, does not work! 

        self.check_save_directory()
        self.datetime_date = self.get_datetime()
        self.plot_type_string = None # [ASSAYS_assayNames/full]_[mi_graph/stimuli_graph]_[all_treatment/specific_treatment].pdf
        
        self.warning = {}

        self.visualization_path()

    
    def check_save_directory(self):
        os.makedirs(self.save_directory, exist_ok=True)


    def get_datetime(self):
        return datetime.now().strftime("%Y%m%d")
        

    def generate_filename(self, battery=False):
        if self.user_file:
            return f"{self.user_file}"
        elif battery:
            return f"{self.datetime_date}_BATTERY_{self.battery_information.battery_number}_{self.plot_type_string}"
        else:
            return f"{self.datetime_date}_RUN_{self.run_number}_{self.plot_type_string}_{self.analysis_calculations}" 
        

    def filename_helper(self, filename, extension):
        not_fixed = True
        name_iter = 1

        while not_fixed:
            new_filename = f'{filename}_{name_iter:02d}'
            new_filepath = f'{self.save_directory}{new_filename}{extension}'

            if os.path.exists(new_filepath):
                if name_iter > 99:
                    self.warning['FILENAME_HELPER'] = filename
                    return 
                name_iter += 1
            else:
                not_fixed = False
            
        return new_filename
    

    def generate_title(self, assay=None, stimulus=None):
        if self.user_title:
            return self.user_title
        elif isinstance(self.run_number, int) and assay and stimulus:
            return f"{self.analysis_calculations.capitalize()} RUN {self.run_number} ; ASSAY {assay} ; STIMULUS {stimulus}"
        elif isinstance(self.run_number, int) and assay:
            return f"{self.analysis_calculations.capitalize()} RUN {self.run_number} ; ASSAY {assay}"
        elif isinstance(self.run_number, int) and stimulus:
            return f"{self.analysis_calculations.capitalize()} RUN {self.run_number} ; STIMULUS {stimulus}"
        elif isinstance(self.run_number, int):
            return f"{self.analysis_calculations.capitalize()} RUN {self.run_number}"
        elif assay:
            return f"{self.analysis_calculations.capitalize()} RUNS [{'_'.join([str(run_number) for run_number in self.run_number])}] ; ASSAY {assay}"
        elif stimulus:
            return f"{self.analysis_calculations.capitalize()} RUNS [{'_'.join([str(run_number) for run_number in self.run_number])}] ; STIMULUS {stimulus}"
        else:
            return f"{self.analysis_calculations.capitalize()} RUNS [{'_'.join([str(run_number) for run_number in self.run_number])}]"


    def interpret_treatment_concentration(self, treatment, concentration):
        if '::' in treatment and '::' in concentration:
            return f"{treatment.split('::')[0]} {concentration.split('::')[0]}uM and {treatment.split('::')[1]} {concentration.split('::')[1]}uM"
        else:
            return f"{treatment} {concentration}uM"
        

    def interpret_secondary_lists(self, cnc_list, val_list, avg_std_list):
        tup_list = []
        dual = False
        for cnc in cnc_list:
            if '::' in cnc:
                dual = True
                spl_cnc = cnc.split('::')
                tup_list.append((float(spl_cnc[0]), float(spl_cnc[0])))
            else:
                tup_flt = (float(cnc), 0)
                tup_list.append(tup_flt)

        if dual:
            tup0 = set(tup[0] for tup in tup_list)
            tup1 = set(tup[1] for tup in tup_list)
            if len(tup1) > len(tup0):
                tup_list = [(tup[1], tup[0]) for tup in tup_list]

        srt_i = sorted(range(len(tup_list)), key=lambda k: tup_list[k][0])

        ordrd_cncs = [np.log(tup_list[i][0]) for i in srt_i]
        ordrd_vals = [val_list[i] for i in srt_i]
        ordrd_st_devs = [avg_std_list[i] for i in srt_i] 

        axis_list = [f"{cnc.split('::')[0]}uM and {cnc.split('::')[1]}uM" if dual else f'{cnc}uM' for cnc in cnc_list]

        return axis_list, ordrd_cncs, ordrd_vals, ordrd_st_devs


    def visualization_path(self):
        if self.visualize_battery == 'yes':
            self.graphing_battery_information()
        
        if self.visualize_secondary == 'yes':
            if self.final_information.group_response_dictionary:
                self.graphing_secondary_group_dict(self.final_information.group_response_dictionary, 'general')
            if self.final_information.responsive_dictionary:
                self.graphing_secondary_response_dict(self.final_information.responsive_dictionary, 'general')
            
            if self.final_information.group_habituation_dictionary:
                self.graphing_secondary_group_dict(self.final_information.group_habituation_dictionary, 'habituation')
            #if self.final_information.habituation_responsive_dictionary:
            #    self.graphing_secondary_response_dict(self.final_information.habituation_responsive_dictionary, 'habituation')
            if self.final_information.habituation_dictionary:
                self.graphing_habituation_dict(self.final_information.habituation_dictionary)

            if self.final_information.prepulse_inhibition_dictionary:
                self.graphing_secondary_ppi(self.final_information.prepulse_inhibition_dictionary)

            if self.final_information.group_prepulse_inhibition_dictionary:
                self.graphing_secondary_group_dict(self.final_information.group_prepulse_inhibition_dictionary, 'ppi')

        
        elif self.analysis_type == "preview":
            pass 

        else:
            if self.analysis_calculations == 'raw' or self.analysis_calculations == 'split':
                if self.analysis_group == 'treatment':
                    if self.isolate_stimuli == 'yes':
                        self.graphing_overlay_treat_bar_dict()
                    else:
                        self.graphing_overlay_treat_line_dict()
                else:
                    if self.isolate_stimuli == 'yes':
                        self.graphing_overlay_group_bar_dict()
                    else:
                        self.graphing_overlay_group_line_dict()
            
            else:
                if self.analysis_group == 'treatment':
                    if self.isolate_stimuli == 'yes':
                        self.graphing_singlular_treat_bar_dict()
                    else:
                        self.graphing_singlular_treat_line_dict()
                else:
                    if self.isolate_stimuli == 'yes':
                        self.graphing_singlular_group_bar_dict()
                    else:
                        self.graphing_singlular_group_line_dict()


    def graphing_battery_information(self):
        self.plot_type_string = f"battery_assay_stimulus_plot"
        
        pdf_file_name = self.generate_filename()
        pdf_file_path = f"{self.save_directory}{pdf_file_name}.pdf"

        if os.path.exists(pdf_file_path):
            pdf_file_name = self.filename_helper(pdf_file_name, '.pdf')
            pdf_file_path = f"{self.save_directory}{pdf_file_name}.pdf"
        
        
        fish_logger.log(Fish_Log.INFO, f"Pdf File Name {pdf_file_name}, Pdf File Path {pdf_file_path}")

        with pdf.PdfPages(pdf_file_path) as pdf_pages:
            fig, ax = plt.subplots(figsize=(14.5, 7.5))

            y_assay = 2.0
            y_stimuli = 0 
            y_axis_distance = 1.5

            assay_handles = []
            stimuli_handles = []

            for index, (assay_name, (assay_start, assay_stop), stimuli) in enumerate(self.battery_information.battery_info):
                clr_indx = index % 15
                
                assay_line = ax.hlines(
                    y=y_assay + y_axis_distance, xmin=assay_start, xmax=assay_stop, 
                    color=self.group_colors[clr_indx], linewidth=6, label=f'{assay_name}'
                )
                
                if f'{assay_name}' not in [handle.get_label() for handle in assay_handles]:
                    assay_handles.append(assay_line)

                if stimuli:
                    for stim_name, (stim_start, stim_stop) in stimuli:
                        color = self.stimulus_colors.get(stim_name, 'gray')  
                        stim_line = ax.hlines(
                            y=y_stimuli + y_axis_distance, xmin=stim_start, xmax=stim_stop, 
                            color=color, linewidth=4, label=f'{stim_name}'
                        )
                        if f'{stim_name}' not in [handle.get_label() for handle in stimuli_handles]:
                            stimuli_handles.append(stim_line)

            ax.set_yticks([]) 
            ax.spines['top'].set_visible(False)  
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False) 
            ax.set_xlabel("Time (s)")
            ax.set_ylim(0, 5)  

            #legend1 = ax.legend(handles=assay_handles, title="Assays", loc='upper left', bbox_to_anchor=(1.05, 1.5))
            #ax.add_artist(legend1) 
            #ax.legend(handles=stimuli_handles, title="Stimuli", loc='upper left', bbox_to_anchor=(1.55, 1.5))

            plt.tight_layout()

            pdf_pages.savefig(fig, bbox_inches='tight')
            plt.close(fig)
                
    
    def graphing_overlay_treat_bar_dict(self):
        # bar dict {f"title" : [(stimulus_name, [stimulus_mi_list, stimulus_mi_list])]}
        if self.specific_assay == 'yes':
            if self.specific_treatment == "treatment":
                plot_dict = {f"{self.interpret_treatment_concentration(treatment, concentration)}+{assay}" : self.final_information.split_dictionary[treatment][concentration][assay][1] for treatment in self.user_treatments for concentration in self.final_information.split_dictionary[treatment].keys() for assay in self.user_assay}
                self.plot_type_string = f"ASSAYs_{'_'.join([assay for assay in self.user_assay])}_isolated_stimuli_specific_treatments"

            elif self.specific_treatment == 'treatment-concentration':
                plot_dict = {f"{self.interpret_treatment_concentration(trt_cnc.split(self.split_str)[0], trt_cnc.split(self.split_str)[1])}+{assay}" : self.final_information.split_dictionary[trt_cnc.split(self.split_str)[0]][trt_cnc.split(self.split_str)[1]][assay][1] for trt_cnc in self.user_treatments for assay in self.user_assay}
                self.plot_type_string = f"ASSAYs_{'_'.join([assay for assay in self.user_assay])}_isolated_stimuli_specific_treatments"

            else:
                plot_dict = {f"{self.interpret_treatment_concentration(treatment, concentration)}+{assay}" : self.final_information.split_dictionary[treatment][concentration][assay][1] for treatment in self.final_information.split_dictionary.keys() for concentration in self.final_information.split_dictionary[treatment].keys() for assay in self.user_assay}
                self.plot_type_string = f"ASSAYs_{'_'.join([assay for assay in self.user_assay])}_isolated_stimuli_all_treatments"

        elif self.specific_treatment == "treatment":
            plot_dict = {f"{self.interpret_treatment_concentration(treatment, concentration)}+{assay}" : assay_stimulus_list for treatment in self.user_treatments for concentration in self.final_information.split_dictionary[treatment].keys() for assay, (assay_mi_list, assay_stimulus_list) in self.final_information.split_dictionary[treatment][concentration].items()}
            self.plot_type_string = f"all_assays_isolated_stimuli_specific_treatments"

        elif self.specific_treatment == 'treatment-concentration':
            plot_dict = {f"{self.interpret_treatment_concentration(trt_cnc.split(self.split_str)[0], trt_cnc.split(self.split_str)[1])}+{assay}" : assay_stimulus_list for trt_cnc in self.user_treatments for assay, (assay_mi_list, assay_stimulus_list) in self.final_information.split_dictionary[trt_cnc.split(self.split_str)[0]][trt_cnc.split(self.split_str)[1]].items()}
            self.plot_type_string = f"all_assays_isolated_stimuli_specific_treatments"
                
        else:
            plot_dict = {f"{self.interpret_treatment_concentration(treatment, concentration)}+{assay}" : assay_stimulus_list for treatment in self.final_information.split_dictionary.keys() for concentration in self.final_information.split_dictionary[treatment].keys() for assay, (assay_mi_list, assay_stimulus_list) in self.final_information.split_dictionary[treatment][concentration].items()}
            self.plot_type_string = f"all_assays_isolated_stimuli_all_treatments"
        
        fish_logger.log(Fish_Log.INFO, f"Plot Type String {self.plot_type_string}, N Plots {len(plot_dict.keys())}")
        self.graph_stimuli_overlay(plot_dict)
                

    def graphing_singlular_treat_bar_dict(self):
        # bar dict {f"title" : stimulus_list}
        # # stimulus_list = [(stimulus_name1, stimulus_avg1, stimulus_median1, stimulus_st_dev1, stimulus_start1, stimulus_end1), (another tuple), ...]
        if self.specific_assay == 'yes':
            if self.specific_treatment == "treatment":
                plot_dict = {f"{self.interpret_treatment_concentration(treatment, concentration)}+{assay}" : self.final_information.split_dictionary[treatment][concentration][assay][2] for treatment in self.user_treatments for concentration in self.final_information.split_dictionary[treatment].keys() for assay in self.user_assay}
                self.plot_type_string = f"ASSAYs_{'_'.join([assay for assay in self.user_assay])}_isolated_stimuli_specific_treatments"
                
            elif self.specific_treatment == 'treatment-concentration':
                plot_dict = {f"{self.interpret_treatment_concentration(trt_cnc.split(self.split_str)[0], trt_cnc.split(self.split_str)[1])}+{assay}" : self.final_information.split_dictionary[trt_cnc.split(self.split_str)[0]][trt_cnc.split(self.split_str)[1]][assay][2] for trt_cnc in self.user_treatments for assay in self.user_assay}
                self.plot_type_string = f"ASSAYs_{'_'.join([assay for assay in self.user_assay])}_isolated_stimuli_specific_treatments"
                
            else:
                plot_dict = {f"{self.interpret_treatment_concentration(treatment, concentration)}+{assay}" : self.final_information.split_dictionary[treatment][concentration][assay][2] for treatment in self.final_information.split_dictionary.keys() for concentration in self.final_information.split_dictionary[treatment].keys() for assay in self.user_assay}
                self.plot_type_string = f"ASSAYs_{'_'.join([assay for assay in self.user_assay])}_isolated_stimuli_all_treatments"
                
        elif self.specific_treatment == "treatment":
                plot_dict = {f"{self.interpret_treatment_concentration(treatment, concentration)}+{assay}" : assay_stimulus_list for treatment in self.user_treatments for concentration in self.final_information.split_dictionary[treatment].keys() for assay, (assay_avg_mi, assay_st_dev, assay_stimulus_list) in self.final_information.split_dictionary[treatment][concentration].items()}
                self.plot_type_string = f"all_assays_isolated_stimuli_specific_treatments"
                
        elif self.specific_treatment == 'treatment-concentration':
            plot_dict = {f"{self.interpret_treatment_concentration(trt_cnc.split(self.split_str)[0], trt_cnc.split(self.split_str)[1])}+{assay}" : assay_stimulus_list for trt_cnc in self.user_treatments for assay, (assay_avg_mi, assay_st_dev, assay_stimulus_list) in self.final_information.split_dictionary[trt_cnc.split(self.split_str)[0]][trt_cnc.split(self.split_str)[1]].items()}
            self.plot_type_string = f"all_assays_isolated_stimuli_all_treatmentps"
                
        else:
            plot_dict = {f"{self.interpret_treatment_concentration(treatment, concentration)}+{assay}" : assay_stimulus_list for treatment in self.final_information.split_dictionary.keys() for concentration in self.final_information.split_dictionary[treatment].keys() for assay, (assay_avg_mi, assay_st_dev, assay_stimulus_list) in self.final_information.split_dictionary[treatment][concentration].items()}
            self.plot_type_string = f"all_assays_isolated_stimuli_all_treatments"                

        fish_logger.log(Fish_Log.INFO, f"Plot Type String {self.plot_type_string}, N Plots {len(plot_dict.keys())}")
        self.graph_stimuli_singluar(plot_dict)
 

    def graphing_overlay_group_bar_dict(self):
        # bar dict {f"title" : [(stimulus_name, [stimulus_mi_list1, stimulus_mi_list2])]}
        if self.specific_assay == 'yes':
            if self.specific_treatment == "treatment":
                plot_dict = {f"{group}+{assay}" : self.final_information.split_dictionary[group][assay][1] for group in self.user_treatments for assay in self.user_assay}
                self.plot_type_string = f"ASSAYs_{'_'.join([assay for assay in self.user_assay])}_isolated_stimuli_specific_groupings"
                
            else:
                plot_dict = {f"{group}+{assay}" : self.final_information.split_dictionary[group][assay][1] for group in self.final_information.split_dictionary.keys() for assay in self.user_assay}
                self.plot_type_string = f"ASSAYs_{'_'.join([assay for assay in self.user_assay])}_isolated_stimuli_all_groupings"
                
        elif self.specific_treatment == "treatment":
            plot_dict = {f"{group}+{assay}" : assay_stimulus_list for group in self.user_treatments for assay, (assay_mi_list, assay_stimulus_list) in self.final_information.split_dictionary[group].items()}
            self.plot_type_string = f"all_assays_isolated_stimuli_specific_groupings"
                
        else:
            plot_dict = {f"{group}+{assay}" : assay_stimulus_list for group in self.final_information.split_dictionary.keys() for assay, (assay_mi_list, assay_stimulus_list) in self.final_information.split_dictionary[group].items()}
            self.plot_type_string = f"all_assays_isolated_stimuli_all_groupings"

        fish_logger.log(Fish_Log.INFO, f"Plot Type String {self.plot_type_string}, N Plots {len(plot_dict.keys())}")
        self.graph_stimuli_overlay(plot_dict)


    def graphing_singlular_group_bar_dict(self):
        # bar dict {f"title" : stimulus_list}
        # # stimulus_list = [(stimulus_name1, stimulus_avg1, stimulus_median1, stimulus_st_dev1, stimulus_start1, stimulus_end1), (another tuple), ...]
        if self.specific_assay == 'yes':
            if self.specific_treatment == "treatment":
                plot_dict = {f"{group}uM+{assay}" : self.final_information.split_dictionary[group][assay][2] for group in self.user_treatments for assay in self.user_assay}
                self.plot_type_string = f"ASSAYs_{'_'.join([assay for assay in self.user_assay])}_isolated_stimuli_specific_groupings"
                
            else:
                plot_dict = {f"{group}+{assay}" : self.final_information.split_dictionary[group][assay][2] for group in self.final_information.split_dictionary.keys() for assay in self.user_assay}
                self.plot_type_string = f"ASSAYs_{'_'.join([assay for assay in self.user_assay])}_isolated_stimuli_all_groupings"
                
        elif self.specific_treatment == "treatment":
                plot_dict = {f"{group}+{assay}" : assay_stimulus_list for group in self.user_treatments for assay, (assay_avg_mi, assay_st_dev, assay_stimulus_list) in self.final_information.split_dictionary[group].items()}
                self.plot_type_string = f"all_assays_isolated_stimuli_specific_groupings"
                
        else:
            plot_dict = {f"{group}+{assay}" : assay_stimulus_list for group in self.final_information.split_dictionary.keys() for assay, (assay_avg_mi, assay_st_dev, assay_stimulus_list) in self.final_information.split_dictionary[group].items()}
            self.plot_type_string = f"all_assays_isolated_stimuli_all_groupings"

        fish_logger.log(Fish_Log.INFO, f"Plot Type String {self.plot_type_string}, N Plots {len(plot_dict.keys())}")

        self.graph_stimuli_singluar(plot_dict)


    def graphing_overlay_treat_line_dict(self):
        # line dict {f"title" : [mi_list, mi_list]} 
        if self.specific_assay == 'yes':
            if self.specific_treatment == "treatment":
                plot_dict = {f"{self.interpret_treatment_concentration(treatment, concentration)}+{assay}" : self.final_information.split_dictionary[treatment][concentration][assay][0] for treatment in self.user_treatments for concentration in self.final_information.split_dictionary[treatment].keys() for assay in self.user_assay}
                self.plot_type_string = f"ASSAYs_{'_'.join([assay for assay in self.user_assay])}_mi_traces_specific_treatments"
                
            elif self.specific_treatment == 'treatment-concentration':
                plot_dict = {f"{self.interpret_treatment_concentration(trt_cnc.split(self.split_str)[0], trt_cnc.split(self.split_str)[1])}+{assay}" : self.final_information.split_dictionary[trt_cnc.split(self.split_str)[0]][trt_cnc.split(self.split_str)[0]][assay][0] for trt_cnc in self.user_treatments for assay in self.user_assay}
                self.plot_type_string = f"ASSAYs_{'_'.join([assay for assay in self.user_assay])}_mi_traces_specific_treatments"
                
            else:
                plot_dict = {f"{self.interpret_treatment_concentration(treatment, concentration)}+{assay}" : self.final_information.split_dictionary[treatment][concentration][assay][0] for treatment in self.final_information.split_dictionary.keys() for concentration in self.final_information.split_dictionary[treatment].keys() for assay in self.user_assay}
                self.plot_type_string = f"ASSAYs_{'_'.join([assay for assay in self.user_assay])}_mi_traces_all_treatments"
                
        elif self.specific_treatment == "treatment":
                plot_dict = {f"{self.interpret_treatment_concentration(treatment, concentration)}" : self.final_information.sorted_dictionary[treatment][concentration] for treatment in self.user_treatments for concentration in self.final_information.sorted_dictionary[treatment].keys()}
                self.plot_type_string = f"full_mi_traces_specific_treatments"
                
        elif self.specific_treatment == 'treatment-concentration':
            plot_dict = {f"{self.interpret_treatment_concentration(trt_cnc.split(self.split_str)[0], trt_cnc.split(self.split_str)[1])}" : self.final_information.sorted_dictionary[trt_cnc.split(self.split_str)[0]][trt_cnc.split(self.split_str)[1]] for trt_cnc in self.user_treatments}
            self.plot_type_string = f"full_mi_traces_specific_treatments"
                
        else:
            plot_dict = {f"{self.interpret_treatment_concentration(treatment, concentration)}" : self.final_information.sorted_dictionary[treatment][concentration] for treatment in self.final_information.sorted_dictionary.keys() for concentration in self.final_information.sorted_dictionary[treatment].keys()}
            self.plot_type_string = f"full_mi_traces_all_treatments"

        fish_logger.log(Fish_Log.INFO, f"Plot Type String {self.plot_type_string}, N Plots {len(plot_dict.keys())}")
        self.graph_mi_overlay(plot_dict)


    def graphing_singlular_treat_line_dict(self):
        # line dict {f"title" : (average_mi_list, std_list)}
        a_type_plot = self.calc_indx-1
        if self.specific_assay == 'yes':
            if self.specific_treatment == "treatment":
                plot_dict = {f"{self.interpret_treatment_concentration(treatment, concentration)}+{assay}" : (self.final_information.split_dictionary[treatment][concentration][assay][a_type_plot], self.final_information.split_dictionary[treatment][concentration][assay][1]) for treatment in self.user_treatments for concentration in self.final_information.split_dictionary[treatment].keys() for assay in self.user_assay}
                self.plot_type_string = f"ASSAYs_{'_'.join([assay for assay in self.user_assay])}_mi_traces_specific_treatments"
                
            elif self.specific_treatment == 'treatment-concentration':
                plot_dict = {f"{self.interpret_treatment_concentration(trt_cnc.split(self.split_str)[0], trt_cnc.split(self.split_str)[1])}+{assay}" : (self.final_information.split_dictionary[trt_cnc.split(self.split_str)[0]][trt_cnc.split(self.split_str)[1]][assay][a_type_plot], self.final_information.split_dictionary[trt_cnc.split(self.split_str)[0]][trt_cnc.split(self.split_str)[1]][assay][1]) for trt_cnc in self.user_treatments for assay in self.user_assay}
                self.plot_type_string = f"ASSAYs_{'_'.join([assay for assay in self.user_assay])}_mi_traces_specific_treatments"
                
            else:
                plot_dict = {f"{self.interpret_treatment_concentration(treatment, concentration)}+{assay}" : (self.final_information.split_dictionary[treatment][concentration][assay][a_type_plot], self.final_information.split_dictionary[treatment][concentration][assay][1]) for treatment in self.final_information.split_dictionary.keys() for concentration in self.final_information.split_dictionary[treatment].keys() for assay in self.user_assay}
                self.plot_type_string = f"ASSAYs_{'_'.join([assay for assay in self.user_assay])}_mi_traces_all_treatments"
                
        elif self.specific_treatment == "treatment":
            plot_dict = {f"{self.interpret_treatment_concentration(treatment, concentration)}" : (self.final_information.averaged_dictionary[treatment][concentration][a_type_plot], self.final_information.averaged_dictionary[treatment][concentration][1]) for treatment in self.user_treatments for concentration in self.final_information.averaged_dictionary[treatment].keys()}
            self.plot_type_string = f"full_mi_traces_specific_treatments"
            
        elif self.specific_treatment == 'treatment-concentration':
            plot_dict = {f"{self.interpret_treatment_concentration(trt_cnc.split(self.split_str)[0], trt_cnc.split(self.split_str)[1])}" : (self.final_information.averaged_dictionary[trt_cnc.split(self.split_str)[0]][trt_cnc.split(self.split_str)[1]][a_type_plot], self.final_information.averaged_dictionary[trt_cnc.split(self.split_str)[0]][trt_cnc.split(self.split_str)[1]][1]) for trt_cnc in self.user_treatments}
            self.plot_type_string = f"full_mi_traces_specific_treatments"
                
        else:
            plot_dict = {f"{self.interpret_treatment_concentration(treatment, concentration)}" : (self.final_information.averaged_dictionary[treatment][concentration][a_type_plot], self.final_information.averaged_dictionary[treatment][concentration][1]) for treatment in self.final_information.averaged_dictionary.keys() for concentration in self.final_information.averaged_dictionary[treatment].keys()}
            self.plot_type_string = f"full_mi_traces_all_treatments"
                
        fish_logger.log(Fish_Log.INFO, f"Plot Type String {self.plot_type_string}, N Plots {len(plot_dict.keys())}")
        self.graph_mi_singluar(plot_dict)


    def graphing_overlay_group_line_dict(self):
        # line dict {f"title" : [mi_list, mi_list]}
        if self.specific_assay == 'yes':
            if self.specific_treatment == "treatment":
                plot_dict = {f"{group}+{assay}" : self.final_information.split_dictionary[group][assay][0] for group in self.user_treatments for assay in self.user_assay}
                self.plot_type_string = f"ASSAYs_{'_'.join([assay for assay in self.user_assay])}_mi_traces_specific_groupings"
                
            else:
                plot_dict = {f"{group}+{assay}" : self.final_information.split_dictionary[group][assay][0] for group in self.final_information.split_dictionary.keys() for assay in self.user_assay}
                self.plot_type_string = f"ASSAYs_{'_'.join([assay for assay in self.user_assay])}_mi_traces_all_groupings"
                
        elif self.specific_treatment == "treatment":
                plot_dict = {f"{group}" : self.final_information.sorted_dictionary[group] for group in self.user_treatments}
                self.plot_type_string = f"all_assays_mi_traces_specific_groupings"
                
        else:
            plot_dict = {f"{group}" : self.final_information.sorted_dictionary[group] for group in self.final_information.sorted_dictionary.keys()}
            self.plot_type_string = f"all_assays_mi_traces_all_groupings"
        
        fish_logger.log(Fish_Log.INFO, f"Plot Type String {self.plot_type_string}, N Plots {len(plot_dict.keys())}")
        self.graph_mi_overlay(plot_dict)
                

    def graphing_singlular_group_line_dict(self):
        # # # I AM PRETTY SURE THIS FUNCTION DOES NOT WORK !!! 
        
        # line dict {f"title" : (average_mi_list, std_list)}
        a_type_plot = self.calc_indx-1
        if self.specific_assay == 'yes':
            if self.specific_treatment == "treatment":
                plot_dict = {f"{group}+{assay}" : (self.final_information.split_dictionary[group][assay][a_type_plot], self.final_information.split_dictionary[group][assay][1]) for group in self.user_treatments for assay in self.user_assay}
                self.plot_type_string = f"ASSAYs_{'_'.join([assay for assay in self.user_assay])}_mi_traces_specific_groupings"
                
            else:
                plot_dict = {f"{group}+{assay}" : (self.final_information.split_dictionary[group][assay][a_type_plot], self.final_information.split_dictionary[group][assay][1]) for group in self.final_information.split_dictionary.keys() for assay in self.user_assay}
                self.plot_type_string = f"ASSAYs_{'_'.join([assay for assay in self.user_assay])}_mi_traces_all_groupings"
                
        elif self.specific_treatment == "treatment":
            if self.analysis_group == 'well': # this condition is needed because wells are not averaged !
                plot_dict = {f"{group}" : (self.final_information.sorted_dictionary[group][0], [0 for i in range(0, len(self.final_information.sorted_dictionary[group][0]))]) for group in self.user_treatments}
            else:
                plot_dict = {f"{group}" : (self.final_information.averaged_dictionary[group][a_type_plot], self.final_information.averaged_dictionary[group][1]) for group in self.user_treatments}
            self.plot_type_string = f"all_assays_mi_traces_specific_groupings"

        else:
            if self.analysis_group == 'well': # see above same if statement comment
                plot_dict = {f"{group}" : (self.final_information.sorted_dictionary[group][0], [0 for i in range(0, len(self.final_information.sorted_dictionary[group][0]))]) for group in self.final_information.sorted_dictionary.keys()} 
            else:
                plot_dict = {f"{group}" : (self.final_information.averaged_dictionary[group][a_type_plot], self.final_information.averaged_dictionary[group][1]) for group in self.final_information.averaged_dictionary.keys()}
            self.plot_type_string = f"all_assays_mi_traces_all_groupings"
        
        fish_logger.log(Fish_Log.INFO, f"Plot Type String {self.plot_type_string}, N Plots {len(plot_dict.keys())}")
        self.graph_mi_singluar(plot_dict)


    def graphing_habituation_dict(self, habituation_dictionary):
        plt_dict = {} 
        plt_dict1 = {} #{assay_stim : ([value], [std], [condition])}
        treatment_slope_dict = {} # {ASSAY : {STIMULUS : {TREATMENT : {CONCENTRATION : (stim_slope, stim_r_sqrd, stim_avg_std)] }}}}
        cntrl_dict = {}
        cntrl_name = None
        cntrl_cnc = None
        n_reps_bar = 1

        if self.user_control and self.user_control != 'no':
            n_reps_bar = 2
                  
            if self.final_information.sauron_primary_analysis.user_analysis_group == 'treatment':
                cntrl_name = self.user_control.split(self.split_str)[0].strip()
                cntrl_cnc = self.user_control.split(self.split_str)[1].strip()
            else:
                cntrl_name = self.user_control.split(self.split_str)[0]

        if self.analysis_group == 'treatment':
            for treatment in habituation_dictionary.keys():
                for concentration in habituation_dictionary[treatment].keys():
                    for assay in habituation_dictionary[treatment][concentration].keys():
                        for stimulus in habituation_dictionary[treatment][concentration][assay].keys():
                            assay = assay.strip()
                            if treatment == cntrl_name and concentration == cntrl_cnc:
                                cntrl_dict[assay] = habituation_dictionary[treatment][concentration][assay][stimulus] 
                            
                            asy_str = f"{assay}"
                            asy_stm_str = f'{assay} + {stimulus}'
                            
                            trt_cnc_str = f"{self.interpret_treatment_concentration(treatment, concentration)} : {assay}+{stimulus}"
                            cnditn_str = f"{self.interpret_treatment_concentration(treatment, concentration)}"

                            plt_dict.update({trt_cnc_str : habituation_dictionary[treatment][concentration][assay][stimulus]})

                            if asy_str not in treatment_slope_dict.keys():  
                                treatment_slope_dict[asy_str] = {treatment : {concentration : (habituation_dictionary[treatment][concentration][assay][stimulus][2], habituation_dictionary[treatment][concentration][assay][stimulus][4], habituation_dictionary[treatment][concentration][assay][stimulus][5])}}
                            elif treatment  not in treatment_slope_dict[asy_str].keys():
                                treatment_slope_dict[asy_str][treatment] = {concentration : (habituation_dictionary[treatment][concentration][assay][stimulus][2], habituation_dictionary[treatment][concentration][assay][stimulus][4], habituation_dictionary[treatment][concentration][assay][stimulus][5])}
                            elif concentration  not in treatment_slope_dict[asy_str][treatment].keys():
                                treatment_slope_dict[asy_str][treatment][concentration] = (habituation_dictionary[treatment][concentration][assay][stimulus][2], habituation_dictionary[treatment][concentration][assay][stimulus][4], habituation_dictionary[treatment][concentration][assay][stimulus][5])

                            if asy_stm_str not in plt_dict1.keys():
                                plt_dict1[asy_stm_str] = ([habituation_dictionary[treatment][concentration][assay][stimulus][2]], [habituation_dictionary[treatment][concentration][assay][stimulus][5]], [cnditn_str])
                            else:
                                plt_dict1[asy_stm_str][0].append(habituation_dictionary[treatment][concentration][assay][stimulus][2])
                                plt_dict1[asy_stm_str][1].append(habituation_dictionary[treatment][concentration][assay][stimulus][5])
                                plt_dict1[asy_stm_str][2].append(cnditn_str)

        else:
            for group in habituation_dictionary.keys():
                for assay in habituation_dictionary[group].keys():
                    assay = assay.strip()
                    for stimulus in habituation_dictionary[group][assay].keys():
                        if group == cntrl_name:
                            cntrl_dict[assay] = habituation_dictionary[group][assay][stimulus]

                        asy_str = f'{assay}'
                        asy_stm_str = f'{assay} + {stimulus}'
                        
                        plt_dict.update({f"{group} : {assay}+{stimulus}" : habituation_dictionary[group][assay][stimulus]})

                        if asy_str not in treatment_slope_dict.keys():  
                            treatment_slope_dict[asy_str] = {group : (habituation_dictionary[group][assay][stimulus][2], habituation_dictionary[group][assay][stimulus][4], habituation_dictionary[group][assay][stimulus][5])}
                        elif group  not in treatment_slope_dict[asy_str].keys():
                            treatment_slope_dict[asy_str][group] = (habituation_dictionary[group][assay][stimulus][2], habituation_dictionary[group][assay][stimulus][4], habituation_dictionary[group][assay][stimulus][5])

                        if asy_stm_str not in plt_dict1.keys():
                            plt_dict1[asy_stm_str] = ([habituation_dictionary[group][assay][stimulus][2]], [habituation_dictionary[group][assay][stimulus][5]], [group])
                        else:
                            plt_dict1[asy_stm_str][0].append(habituation_dictionary[group][assay][stimulus][2])
                            plt_dict1[asy_stm_str][1].append(habituation_dictionary[group][assay][stimulus][5])
                            plt_dict1[asy_stm_str][2].append(group)


        slope_plt = {}
        if self.analysis_group == 'treatment':
            for assay_stim_nm in treatment_slope_dict:
                for treatment in treatment_slope_dict[assay_stim_nm].keys():
                    concentration_list = [concentration for concentration in treatment_slope_dict[assay_stim_nm][treatment].keys()]
                    slope_list = [treatment_slope_dict[assay_stim_nm][treatment][concentration][0] for concentration in treatment_slope_dict[assay_stim_nm][treatment].keys()]
                    avg_std_list = [treatment_slope_dict[assay_stim_nm][treatment][concentration][2] for concentration in treatment_slope_dict[assay_stim_nm][treatment].keys()]
                    axis_list, conc_list, slps_list, avg_st_devs = self.interpret_secondary_lists(concentration_list, slope_list, avg_std_list)
                    slope_plt[f"{treatment}+{assay_stim_nm}"] = (axis_list, conc_list, slps_list, avg_st_devs)

        self.plot_type_string = f"habituation_analysis_slopes"

        if cntrl_dict and slope_plt:
            self.graph_slope_lines(slope_plt, control_dict=cntrl_dict)
        elif slope_plt:
            self.graph_slope_lines(slope_plt)
        
        self.plot_type_string = f"habituation_analysis_stimulus"     

        if cntrl_dict:
            self.graph_habituation(plt_dict, n_reps_bar, control_dict=cntrl_dict)
        else:
            self.graph_habituation(plt_dict, n_reps_bar)

        self.plot_type_string = f"habituation_analysis"
        #self.graph_oneD_points(plt_dict1)
        self.graph_oneD_bars(plt_dict1)

    
    def graphing_secondary_response_dict(self, response_dictionary, typ_str):
        plt_dict = {} # {assay_stim_treatment : ([value], [std], [concentration])}
        plt_dict1 = {} # {assay_stim : ([value], [std], [condition])}

        if self.analysis_group == 'treatment':
            for assay_stim in response_dictionary.keys():
                val_lst1 = []
                std_lst1 = []
                cndt_lst = []
                for treatment in response_dictionary[assay_stim].keys():
                    val_lst = []
                    std_lst = []
                    cnc_lst = list(response_dictionary[assay_stim][treatment].keys())

                    for concentration, activ_tup in response_dictionary[assay_stim][treatment].items():
                        condition = self.interpret_treatment_concentration(treatment, concentration)

                        val_lst.append(activ_tup[0])
                        std_lst.append(activ_tup[1])
                        val_lst1.append(activ_tup[0])
                        std_lst1.append(activ_tup[1])
                        cndt_lst.append(condition)
                    
                    assay_stim_trt = f"{assay_stim}&{treatment}"

                    axis_list, conc_list, vals_list, st_devs = self.interpret_secondary_lists(cnc_lst, val_lst, std_lst)

                    plt_dict[assay_stim_trt] = (axis_list, conc_list, vals_list, st_devs)

                plt_dict1[assay_stim] = (val_lst1, std_lst1, cndt_lst)

            self.plot_type_string = f'concentration_dependent_{typ_str}_response_analysis'
            self.graph_conc_depend_points(plt_dict)   
             
            self.plot_type_string = f'{typ_str}_response_analysis'
            #self.graph_oneD_points(plt_dict1)
            self.graph_oneD_bars(plt_dict1)         

        else:
            for assay_stim in response_dictionary.keys():
                val_lst1 = []
                std_lst1 = []
                cndt_lst = []
                for group, activ_tup in response_dictionary[assay_stim].items():
                    val_lst1.append(activ_tup[0])
                    std_lst1.append(activ_tup[1])
                    cndt_lst.append(group)
                
                plt_dict1[assay_stim] = (val_lst1, std_lst1, cndt_lst)

            self.plot_type_string = 'general_response_analysis'
            #self.graph_oneD_points(plt_dict1)
            self.graph_oneD_bars(plt_dict1)


    def graphing_secondary_group_dict(self, group_dictionary, type_str):
        plt_dict = {} # {assay_stim : ([trt_cnc] [vals] [std] [clrs])}
        
        if self.analysis_group == 'treatment':
            for assay_stim in group_dictionary.keys():
                color_legend = []
                clr = 0
                cndt_lst = []
                vals_lst = []
                std_lst = []
                clr_lst = []

                g_dict = group_dictionary[assay_stim][0]
                key_dict = group_dictionary[assay_stim][1]

                for cndt_grp, info_tup in g_dict.items():
                    clr_indx = clr % 15
                    grp_clr = Sauron_Plot_Visualization.group_colors[clr_indx]
                    color_legend.append((cndt_grp, grp_clr))

                    for point in info_tup[2]:
                        if point not in cndt_lst:
                            cndt_lst.append(point)
                            vals_lst.append(key_dict[point][0])
                            std_lst.append(key_dict[point][1])
                            clr_lst.append(grp_clr)

                    clr += 1

                plt_dict[assay_stim] = (vals_lst, std_lst, cndt_lst, clr_lst, color_legend)

        else:
            for assay_stim in group_dictionary.keys():
                color_legend = []
                clr = 0
                cndt_lst = []
                vals_lst = []
                std_lst = []
                clr_lst = []
                
                g_dict = group_dictionary[assay_stim][0]
                key_dict = group_dictionary[assay_stim][1]

                for cndt_grp, info_tup in g_dict.items():
                    clr_indx = clr % 15
                    grp_clr = Sauron_Plot_Visualization.group_colors[clr_indx]
                    color_legend.append((cndt_grp, grp_clr))

                    for point in info_tup[2]:
                        if point not in cndt_lst:
                            cndt_lst.append(point)
                            vals_lst.append(key_dict[point][0])
                            std_lst.append(key_dict[point][1])
                            clr_lst.append(grp_clr)

                    clr += 1

                plt_dict[assay_stim] = (vals_lst, std_lst, cndt_lst, clr_lst, color_legend)
        
        self.plot_type_string = f'{type_str}_grouping_analysis'
        #self.graph_oneD_points(plt_dict, grouping=True)
        self.graph_oneD_bars(plt_dict, grouping=True)

    
    def graphing_secondary_ppi(self, ppi_dict):
        plt_dict = {} # {assay_stim : ([value], [std], [condition])}
        plt_dict1 = {} # {assay_stim_treatment : ([value], [std], [concentration])}

        if self.analysis_group == 'treatment':
            for asy_stm_i in ppi_dict.keys():
                for treatment in ppi_dict[asy_stm_i].keys():
                    asy_stm_i_trt = f"{asy_stm_i}&{treatment}"
                    cnc_list = list(ppi_dict[asy_stm_i][treatment].keys())
                    val_list = []
                    std_list = []
                    
                    for concentration in ppi_dict[asy_stm_i][treatment].keys():
                        condition = f"{self.interpret_treatment_concentration(treatment, concentration)}"

                        if asy_stm_i not in plt_dict.keys():
                            plt_dict[asy_stm_i] = ([ppi_dict[asy_stm_i][treatment][concentration][0]], [ppi_dict[asy_stm_i][treatment][concentration][1]], [condition])
                        else:
                            plt_dict[asy_stm_i][0].append(ppi_dict[asy_stm_i][treatment][concentration][0])
                            plt_dict[asy_stm_i][1].append(ppi_dict[asy_stm_i][treatment][concentration][1])
                            plt_dict[asy_stm_i][2].append(condition) 

                        val_list.append(ppi_dict[asy_stm_i][treatment][concentration][0])
                        std_list.append(ppi_dict[asy_stm_i][treatment][concentration][1])
                    
                    axis_list, conc_list, vals_list, st_devs = self.interpret_secondary_lists(cnc_list, val_list, std_list)
                    
                    plt_dict1[asy_stm_i_trt] = (axis_list, conc_list, vals_list, st_devs)

            self.plot_type_string = f'prepulse_inhbition_analysis'
            self.graph_oneD_bars(plt_dict)

            self.plot_type_string = f'prepulse_inhbition_conc_depend_analysis'
            self.graph_conc_depend_points(plt_dict1) 

        else:
            for asy_stm_i in ppi_dict.keys():
                for group in ppi_dict[asy_stm_i].keys():
                    condition = group

                    if asy_stm_i not in plt_dict.keys():
                        plt_dict[asy_stm_i] = ([ppi_dict[asy_stm_i][group][0]], [ppi_dict[asy_stm_i][group][1]], [condition])
                    else:
                        plt_dict[asy_stm_i][0].append(ppi_dict[asy_stm_i][group][0])
                        plt_dict[asy_stm_i][1].append(ppi_dict[asy_stm_i][group][1])
                        plt_dict[asy_stm_i][2].append(condition)

            self.plot_type_string = f'prepulse_inhbition_analysis'
            self.graph_oneD_bars(plt_dict) 


    def graph_mi_singluar(self, plt_dict):
        max_mi = 0
        for plt_name in plt_dict.keys():
            if max(plt_dict[plt_name][0]) > max_mi:
                max_mi = max(plt_dict[plt_name][0])

        max_mi *= 1.1 

        pdf_file_name = self.generate_filename()
        pdf_file_path = f"{self.save_directory}{pdf_file_name}.pdf"

        if os.path.exists(pdf_file_path):

            pdf_file_name = self.filename_helper(pdf_file_name, '.pdf')
            pdf_file_path = f"{self.save_directory}{pdf_file_name}.pdf"
            
        fish_logger.log(Fish_Log.INFO, f"Pdf File Name {pdf_file_name}, Pdf File Path {pdf_file_path}")
        
        with pdf.PdfPages(pdf_file_path) as pdf_pages:
            for plt_label, (mi_list, st_dev) in plt_dict.items():
                fig, ax = plt.subplots(figsize=(14.5, 5.5))
                ax.set_ylim(0, max_mi)
                ax.set_xlim(0, len(mi_list))

                if "+" in plt_label:
                    f_label = plt_label.split("+")[0]
                    assay_name = plt_label.split("+")[1].strip()
                    plt_title = self.generate_title(assay=assay_name)
                else:
                    f_label = plt_label
                    assay_name = None
                    plt_title = self.generate_title()

                x_vals = [i for i in range(len(mi_list))]
                
                
                if self.colorbar and self.battery_plot == 'yes':
                    # # # # # # #
                    # WARNING this is in testing and is not functional !
                    # # also known bug of two different stimuli starting at same time
                    # # # can be fixed by making an {int : color_value}
                    # # # # # # # 
                    color_list = []
                    color_indx = []
                    if assay_name:
                        for assay_info in self.battery_information.battery_info:
                            if assay_info[0] == assay_name:
                                assay_start = assay_info[1][0] / self.battery_information.frame_rate
                                for stimulus_name, (stimulus_start, stimulus_end) in assay_info[2]:
                                    stimulus_color = self.stimulus_colors.get(stimulus_name, '#E69307')
                                    
                                    stimulus_start_x = (stimulus_start / self.battery_information.frame_rate) - assay_start
                                    stimulus_end_x = (stimulus_end / self.battery_information.frame_rate) - assay_start
                                    
                                    color_indx.append(int(stimulus_start_x))
                                    color_list.append(stimulus_color)
                                    
                                    color_indx.append(int(stimulus_end_x))
                                    color_list.append('white')
                    else:
                        for stimulus_name, (stimulus_start, stimulus_end) in self.battery_information.battery_lines:
                            stimulus_color = self.stimulus_colors.get(stimulus_name, '#E69307')
                            
                            color_indx.append(int(stimulus_start))
                            color_list.append(stimulus_color)
                            
                            color_indx.append(int(stimulus_end))
                            color_list.append('white')
                    if color_indx[0] != 0:
                        color_indx.insert(0, 0)
                        color_list.insert(0, 'white')
                    print(f'\nCOLOR LIST :\n{color_list}')
                    print(f'\nCOLOR INDX :\n{color_indx}')
                    cmap = ListedColormap(color_list)
                    norm = BoundaryNorm(color_indx, cmap.N)

                    colorbar = ColorbarBase(ax.inset_axes([0, -0.1, 1.0, 0.03]), cmap=cmap, norm=norm, orientation='horizontal', ticks=color_indx)
                    colorbar.set_ticklabels([str(x) for x  in color_indx])
                
                if self.battery_plot == 'yes':
                    color_list = []
                    color_x = []
                    if assay_name:
                        for assay_info in self.battery_information.battery_info:
                            if assay_info[0] == assay_name:
                                assay_start = assay_info[1][0] / self.battery_information.frame_rate
                                for stimulus_name, (stimulus_start, stimulus_end) in assay_info[2]:
                                    stimulus_color = self.stimulus_colors.get(stimulus_name, '#E69307')
                                    stimulus_start_x = (stimulus_start / self.battery_information.frame_rate) - assay_start
                                    stimulus_end_x = (stimulus_end / self.battery_information.frame_rate) - assay_start
                                    
                                    color_x.append(int(stimulus_start_x))
                                    color_list.append(stimulus_color)
                                    color_x.append(int(stimulus_end_x))
                                    color_list.append(stimulus_color)
                                    
                    else:
                        for stimulus_name, (stimulus_start, stimulus_end) in self.battery_information.battery_lines:
                            stimulus_color = self.stimulus_colors.get(stimulus_name, '#E69307')
                            
                            color_x.append(int(stimulus_start))
                            color_list.append(stimulus_color)
                            color_x.append(int(stimulus_end))
                            color_list.append(stimulus_color)
                            
                
                    ax.vlines(color_x, ymin=0, ymax=max_mi, color=color_list, linewidths=0.1, alpha=0.3)

                
                ax.plot(x_vals, mi_list, label=f_label, linewidth=0.5, color='k')
                ax.errorbar(x_vals, st_dev, linestyle='', linewidth=0.1, color='red',alpha=0.5)

                ax.set_xlabel('Time (frames)')
                ax.set_ylabel('Motion Index (MI) Average')
                ax.set_title(plt_title)
                ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

                plt.tight_layout()

                pdf_pages.savefig(fig)
                plt.close(fig)


    def graph_mi_overlay(self, plt_dict):
        max_mi = 0
        for plt_name in plt_dict.keys():
            for repl in range(0, len(plt_dict[plt_name])):
                if max(plt_dict[plt_name][repl]) > max_mi:
                    max_mi = max(plt_dict[plt_name][repl])
        
        max_mi *= 1.1

        pdf_file_name = self.generate_filename()
        pdf_file_path = f"{self.save_directory}{pdf_file_name}.pdf"

        if os.path.exists(pdf_file_path):
            pdf_file_name = self.filename_helper(pdf_file_name, '.pdf')
            pdf_file_path = f"{self.save_directory}{pdf_file_name}.pdf"

        fish_logger.log(Fish_Log.INFO, f"Pdf File Name {pdf_file_name}, Pdf File Path {pdf_file_path}")

        with pdf.PdfPages(pdf_file_path) as pdf_pages:
            for plt_label, mi_lists in plt_dict.items():
                fig, ax = plt.subplots(figsize=(14.5, 5.5))

                if "+" in plt_label:
                    assay_name = plt_label.split("+")[1]
                    f_label = plt_label.split("+")[0]
                    plt_title = self.generate_title(assay=plt_label.split("+")[1])
                else:
                    assay_name = None
                    f_label = plt_label
                    plt_title = self.generate_title()
                
                if self.battery_plot == "yes":
                    color_list = []
                    color_x = []
                    if assay_name:
                        for assay_info in self.battery_information.battery_info:
                            if assay_info[0] == assay_name:
                                assay_start = assay_info[1][0] / self.battery_information.frame_rate
                                for stimulus_name, (stimulus_start, stimulus_end) in assay_info[2]:
                                    stimulus_color = self.stimulus_colors.get(stimulus_name, '#E69307')
                                    stimulus_start_x = (stimulus_start / self.battery_information.frame_rate) - assay_start
                                    stimulus_end_x = (stimulus_end / self.battery_information.frame_rate) - assay_start
                                    
                                    color_x.append(int(stimulus_start_x))
                                    color_list.append(stimulus_color)
                                    color_x.append(int(stimulus_end_x))
                                    color_list.append(stimulus_color)
                                    
                    else:
                        for stimulus_name, (stimulus_start, stimulus_end) in self.battery_information.battery_lines:
                            stimulus_color = self.stimulus_colors.get(stimulus_name, '#E69307')
                            
                            color_x.append(int(stimulus_start))
                            color_list.append(stimulus_color)
                            color_x.append(int(stimulus_end))
                            color_list.append(stimulus_color)
                            
                
                    ax.vlines(color_x, ymin=0, ymax=max_mi, color=color_list, linewidths=0.1, alpha=0.3)

                for i, mi_list in enumerate(mi_lists):
                    x_vals = [i for i in range(len(mi_list))]
                    clr_i_end = len(list(self.overlay_line_colors.keys())) - 1
                    if i > clr_i_end:
                        clr = i - clr_i_end
                    else:
                        clr = i
                    clr_plot = clr % 12
                    ax.plot(x_vals, mi_list, linewidth=0.5, color=self.overlay_line_colors[clr_plot])

                legend_elements = [
                    Line2D([0], [0], color=self.overlay_line_colors[i%12], linestyle='-', linewidth=2, label=f"Replicate {i + 1}")
                    for i in range(len(mi_lists))
                    ]

                legend_title = f'{f_label}'
                ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5), title=legend_title)

                
                ax.set_ylim(0, max_mi)

                ax.set_xlabel('Time (frames)')
                ax.set_ylabel('Motion Index (MI) Average')
                ax.set_title(plt_title)

                plt.tight_layout()

                pdf_pages.savefig(fig)
                plt.close(fig)

    
    def graph_stimuli_singluar(self, plt_dict):
        pdf_file_name = self.generate_filename()
        pdf_file_path = f"{self.save_directory}{pdf_file_name}.pdf"

        if os.path.exists(pdf_file_path):
            pdf_file_name = self.filename_helper(pdf_file_name, '.pdf')
            pdf_file_path = f"{self.save_directory}{pdf_file_name}.pdf"

        max_val = 0
        for plt_label, stim_list in plt_dict.items():
            for stim_tup in stim_list:
                val = stim_tup[self.calc_indx]+stim_tup[2]
                if val > max_val:
                    max_val = val
        max_val *= 1.1

        fish_logger.log(Fish_Log.INFO, f"Pdf File Name {pdf_file_name}, Pdf File Path {pdf_file_path}")

        with pdf.PdfPages(pdf_file_path) as pdf_pages:
            for plt_label, stim_info_list in plt_dict.items():
                stimulus_dictionary = {} # maintain multiple lines for readability
                for stimulus_tuple in stim_info_list:
                    if stimulus_tuple[0] not in stimulus_dictionary.keys():
                        stimulus_dictionary[stimulus_tuple[0]] = ([stimulus_tuple[self.calc_indx]], [stimulus_tuple[2]])
                    else:
                        stimulus_dictionary[stimulus_tuple[0]][0].append(stimulus_tuple[self.calc_indx])
                        stimulus_dictionary[stimulus_tuple[0]][1].append(stimulus_tuple[2])

                for stimulus_name in stimulus_dictionary.keys():
                    fig, ax = plt.subplots(figsize=(14.5, 5.5))

                    if "+" in plt_label:
                        f_label = plt_label.split("+")[0]
                        plt_title = self.generate_title(assay=plt_label.split("+")[1], stimulus=stimulus_name)
                    else:
                        f_label = plt_label
                        plt_title = self.generate_title()

                    x_vals = [i for i in range(len(stimulus_dictionary[stimulus_name][0]))]
                    stimulus_mi_list = stimulus_dictionary[stimulus_name][0]
                    stimulus_st_dev = stimulus_dictionary[stimulus_name][1]

                    bars = ax.bar(x_vals, stimulus_mi_list, label=f_label, color='gray')

                    error_bar_color = 'red'
                    error_bar_linewidth = 0.8
                    error_bar_capsize = 2

                    for bar, std in zip(bars, stimulus_st_dev):
                        ax.errorbar(bar.get_x() + bar.get_width() / 2, bar.get_height(), yerr=std, 
                                    color=error_bar_color, linewidth=error_bar_linewidth, 
                                    capsize=error_bar_capsize)

                    
                    ax.set_ylim(0, max_val)

                    ax.set_xlabel('Time (frames)')
                    ax.set_ylabel('Motion Index (MI) Average')
                    ax.set_title(plt_title)
                    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

                    plt.tight_layout()

                    pdf_pages.savefig(fig)
                    plt.close(fig)


    def graph_stimuli_overlay(self, plt_dict):
        pdf_file_name = self.generate_filename()
        pdf_file_path = f"{self.save_directory}{pdf_file_name}.pdf"

        if os.path.exists(pdf_file_path):
            pdf_file_name = self.filename_helper(pdf_file_name, '.pdf')
            pdf_file_path = f"{self.save_directory}{pdf_file_name}.pdf"

        max_mi = 0
        n_reps = None
        for plt_label, stim_list in plt_dict.items():
            for stim_tup in stim_list:
                if max(stim_tup[1]) > max_mi:
                    max_mi = max(stim_tup[1])
                if not n_reps:
                    n_reps = len(stim_tup[1])
        max_mi *= 1.5

        fish_logger.log(Fish_Log.INFO, f"Pdf File Name {pdf_file_name}, Pdf File Path {pdf_file_path}")

        with pdf.PdfPages(pdf_file_path) as pdf_pages:
            for plt_label, stim_info_list in plt_dict.items():
                n_reps = None 
                stimulus_dictionary = {} # maintain multiple lines for readability
                for stimulus_tuple in stim_info_list:
                    if stimulus_tuple[0] not in stimulus_dictionary.keys():
                        stimulus_dictionary[stimulus_tuple[0]] = [stimulus_tuple[1]]
                    else:
                        stimulus_dictionary[stimulus_tuple[0]].append(stimulus_tuple[1])
                    if not n_reps:
                        n_reps = len(stimulus_tuple[1])

                for stimulus_name in stimulus_dictionary.keys():
                    fig, ax = plt.subplots(figsize=(14.5, 5.5))

                    if "+" in plt_label:
                        f_label = plt_label.split("+")[0]
                        plt_title = self.generate_title(assay=plt_label.split("+")[1], stimulus=stimulus_name)
                    else:
                        f_label = plt_label
                        plt_title = self.generate_title()

                    width_baseline = 0.8
                    new_width = width_baseline / n_reps
        
                    for repl in range(n_reps):
                        x_vals = [x + (new_width * repl) for x in range(len(stimulus_dictionary[stimulus_name]))]
                        mi_vals = [stimulus_dictionary[stimulus_name][x][repl] for x in range(len(stimulus_dictionary[stimulus_name]))]

                        ax.bar(x_vals, mi_vals, width=new_width, label=f_label, linewidth=0.5, color=self.overlay_line_colors[repl])

                    legend_elements = [
                        Line2D([0], [0], color=self.overlay_line_colors[i], linestyle='-', linewidth=2, label=f"Replicate {i + 1}")
                        for i in range(n_reps)
                        ]

                    legend_title = f'{f_label}'
                    ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5), title=legend_title)

                    ax.set_ylim(0, max_mi)

                    ax.set_xlabel('Time (frames)')
                    ax.set_ylabel('Motion Index (MI) Average')
                    ax.set_title(plt_title)

                    plt.tight_layout()

                    pdf_pages.savefig(fig)
                    plt.close(fig)

    
    def graph_habituation(self, plt_dict, n_reps, control_dict=False):
        pdf_file_name = self.generate_filename()
        pdf_file_path = f"{self.save_directory}{pdf_file_name}.pdf"

        if os.path.exists(pdf_file_path):
            pdf_file_name = self.filename_helper(pdf_file_name, '.pdf')
            pdf_file_path = f"{self.save_directory}{pdf_file_name}.pdf"

        max_mi = 0

        for plt_lbl in plt_dict.keys():
            if max(plt_dict[plt_lbl][0]) > max_mi:
                max_mi = max(plt_dict[plt_lbl][0])

        fish_logger.log(Fish_Log.INFO, f"Pdf File Name {pdf_file_name}, Pdf File Path {pdf_file_path}")

        if control_dict:
            with pdf.PdfPages(pdf_file_path) as pdf_pages:
                for plt_label, (stim_mi_avg, stim_st_dev, stim_slope, stim_intercept, stim_r_sqrd, stim_avg_std, drop_indx) in plt_dict.items():
                    fig, ax = plt.subplots(figsize=(14.5, 5.5))
                    
                    f_label = plt_label.split("+")[0]
                    assay_name = f_label.split(':')[1].strip()
                    f_label = f_label.split(':')[0]
                    stimulus_name = plt_label.split("+")[1].strip()
                    
                    plt_title = self.generate_title(assay=assay_name)
                
                    new_width = 0.4

                    stm_line_x = [x for x in range(drop_indx)]
                    stm_line_y = [(x * stim_slope) + stim_intercept for x in range(drop_indx)]
        
                    stm_x = [x for x in range(len(stim_mi_avg))]
                    
                    cntrl_line_x = [x for x in range(control_dict[assay_name][6])]
                    cntrl_line_y = [(x * control_dict[assay_name][2]) + control_dict[assay_name][3] for x in range(control_dict[assay_name][6])]

                    control_x = [x + new_width for x in range(len(control_dict[assay_name][0]))]

                    trt_bars = ax.bar(stm_x, stim_mi_avg, label=f_label, width=new_width, linewidth=0.5, color=self.habit_line_colors[0])
                    cntrl_bars = ax.bar(control_x, control_dict[assay_name][0], label=f'Control', width=new_width, linewidth=0.5, color=self.habit_line_colors[1])

                    avg_line = ax.plot(stm_line_x, stm_line_y, linewidth=3, color="blue")
                    cntrl_line = ax.plot(cntrl_line_x, cntrl_line_y, linewidth=3, color="gray")

                    error_bar_color = 'red'
                    error_bar_linewidth = 0.8
                    error_bar_capsize = 2

                    for bar, std in zip(trt_bars, stim_st_dev):
                        ax.errorbar(bar.get_x() + bar.get_width() / 2, bar.get_height(), yerr=std, 
                                    color=error_bar_color, linewidth=error_bar_linewidth, 
                                    capsize=error_bar_capsize)
                    
                    for bar, std in zip(cntrl_bars, control_dict[assay_name][1]):
                        ax.errorbar(bar.get_x() + bar.get_width() / 2, bar.get_height(), yerr=std, 
                                    color=error_bar_color, linewidth=error_bar_linewidth, 
                                    capsize=error_bar_capsize)

                    legend_labels = [
                        f'{f_label}',
                        'Control'
                    ]

                    legend_elements = [
                        Line2D([0], [0], color=self.habit_line_colors[i], linestyle='-', linewidth=2, label=legend_labels[i])
                        for i in range(n_reps)
                        ]

                    legend_title = f'{f_label}'
                    ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5), title=legend_title)

                    ax.set_ylim(0, max_mi)

                    ax.set_xlabel('Time (frames)')
                    ax.set_ylabel('Motion Index (MI) Average')
                    ax.set_title(plt_title)

                    plt.tight_layout()

                    pdf_pages.savefig(fig)
                    plt.close(fig)
        
        else:
            with pdf.PdfPages(pdf_file_path) as pdf_pages:
                for plt_label, (stim_mi_avg, stim_st_dev, stim_slope, stim_intercept, stim_r_sqrd, stim_avg_std, drop_indx) in plt_dict.items():
                    fig, ax = plt.subplots(figsize=(14.5, 5.5))
                    
                    f_label = plt_label.split("+")[0]
                    assay_name = f_label.split(':')[1]
                    f_label = f_label.split(':')[0]
                    stimulus_name = plt_label.split("+")[1].strip()
                    
                    plt_title = self.generate_title(assay=assay_name, stimulus=stimulus_name)
        
                    stim_x = [x for x in range(len(stim_mi_avg))]

                    stm_line_x = [x for x in range(drop_indx)]
                    stm_line_y = [x * stim_slope + stim_intercept for x in range(drop_indx)]

                    bars = ax.bar(stim_x, stim_mi_avg, label=f_label, linewidth=0.5, color=self.habit_line_colors[0])

                    avg_line = ax.plot(stm_line_x, stm_line_y, linewidth=3, color='black')

                    error_bar_color = 'red'
                    error_bar_linewidth = 0.8
                    error_bar_capsize = 2

                    for bar, std in zip(bars, stim_st_dev):
                        ax.errorbar(bar.get_x() + bar.get_width() / 2, bar.get_height(), yerr=std, 
                                    color=error_bar_color, linewidth=error_bar_linewidth, 
                                    capsize=error_bar_capsize)
                    
                    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
                    ax.set_ylim(0, max_mi)

                    ax.set_xlabel('Time (frames)')
                    ax.set_ylabel('Motion Index (MI) Average')
                    ax.set_title(plt_title)

                    plt.tight_layout()

                    pdf_pages.savefig(fig)
                    plt.close(fig)

    
    def graph_conc_depend_points(self, plt_dict):
        ttl_vals = []
        for asy_stm in plt_dict.keys():
            info_tup = plt_dict[asy_stm]
            for v in info_tup[2]:
                av = float(v)
                ttl_vals.append(av)

        max_y = 1.2 * max(ttl_vals)
        min_y = min(ttl_vals) /  1.2

        max_y = int(max_y)
        min_y = int(min_y)

        pdf_file_name = self.generate_filename()
        pdf_file_path = f"{self.save_directory}{pdf_file_name}.pdf"

        if os.path.exists(pdf_file_path):
            pdf_file_name = self.filename_helper(pdf_file_name, '.pdf')
            pdf_file_path = f"{self.save_directory}{pdf_file_name}.pdf"

        fish_logger.log(Fish_Log.INFO, f"Pdf File Name {pdf_file_name}, Pdf File Path {pdf_file_path}")

        with pdf.PdfPages(pdf_file_path) as pdf_pages:
            for plt_label, (x_axis_names, x_list, vals_list, std_list) in plt_dict.items():
                fig, ax = plt.subplots(figsize=(14.5, 5.5))
                #ax.set_ylim(min_y, max_y)

                condition = plt_label.split('&')[1]
                asy_stm = plt_label.split('&')[0]
                
                if "+" in asy_stm:
                    plt_title = self.generate_title(assay=asy_stm.split("+")[0], stimulus=asy_stm.split("+")[1])
                else: 
                    plt_title = self.generate_title(assay=asy_stm)
                
                final_x = np.arange(len(x_list))
                final_names = [str(name) for name in x_axis_names]
                final_vals = [val for val in vals_list]
                final_std = [std for std in std_list]

                ax.errorbar(final_x, final_vals, yerr=final_std, fmt='none', ecolor='k', alpha=0.5, capsize=5)
                ax.scatter(final_x, final_vals, label=condition, marker='s', color='k')
                
                ax.set_xticks(final_x)
                ax.set_xticklabels(final_names)

                ax.set_xlabel('Concentrations')
                ax.set_ylabel('Activity')
                ax.set_title(plt_title)
                ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

                plt.tight_layout()

                pdf_pages.savefig(fig)
                plt.close(fig)


    def graph_slope_lines(self, plt_dict, control_dict=False):
        max_mi = 0 
        min_mi = 0 # min function does not grab min? but max works
        for plt_name in plt_dict.keys():
            if max(plt_dict[plt_name][2]) > max_mi:
                max_mi = max(plt_dict[plt_name][2])
            if min(plt_dict[plt_name][2]) < min_mi:
                min_mi = min(plt_dict[plt_name][2])

        max_mi *= 1.2 

        pdf_file_name = self.generate_filename()
        pdf_file_path = f"{self.save_directory}{pdf_file_name}.pdf"

        if os.path.exists(pdf_file_path):
            pdf_file_name = self.filename_helper(pdf_file_name, '.pdf')
            pdf_file_path = f"{self.save_directory}{pdf_file_name}.pdf"

        fish_logger.log(Fish_Log.INFO, f"Pdf File Name {pdf_file_name}, Pdf File Path {pdf_file_path}")

        with pdf.PdfPages(pdf_file_path) as pdf_pages:
            for plt_label, (x_axis_names, x_list, slp_list, avg_std_list) in plt_dict.items():
                fig, ax = plt.subplots(figsize=(14.5, 5.5))
                #ax.set_ylim(min_mi, max_mi) 
                #ax.set_xlim(0, len(x_list))

                f_label = plt_label.split("+")[0]
                assay_name = plt_label.split("+")[1].strip()
                plt_title = self.generate_title(assay=assay_name)            
                
                if control_dict:
                    norm_slope = -1*control_dict[assay_name][2]
                    norm_std = control_dict[assay_name][5]
                    slp_list = [-1*slp for slp in slp_list]
                    #slp_list = [-1*(slp - norm_slope) for slp in slp_list]

                    x_list.insert(0, 0)
                    x_axis_names.insert(0, '0uM')
                    slp_list.insert(0, norm_slope)
                    avg_std_list.insert(0, 0)
            
                # THIS THE DUMBEST SHIT BUT IT WORKS 
                final_x = np.arange(len(x_list))
                final_names = [str(name) for name in x_axis_names]
                final_slp = [slp for slp in slp_list]
                final_avg_std = [avg_std for avg_std in avg_std_list]

                ax.errorbar(final_x, final_slp, yerr=final_avg_std, fmt='none', linewidth=0.1, color='k', alpha=0.5, capsize=5)

                ax.scatter(final_x, final_slp, label=f_label, marker='s', color='k')
                
                ax.set_xticks(final_x)
                ax.set_xticklabels(final_names)

                ax.set_xlabel('Concentrations')
                ax.set_ylabel('Habituation Rate')
                ax.set_title(plt_title)
                ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

                plt.tight_layout()

                pdf_pages.savefig(fig)
                plt.close(fig)


    def graph_oneD_points(self, plt_dict, grouping=False):
        pdf_file_name = self.generate_filename()
        pdf_file_path = f"{self.save_directory}{pdf_file_name}.pdf"

        if os.path.exists(pdf_file_path):
            pdf_file_name = self.filename_helper(pdf_file_name, '.pdf')
            pdf_file_path = f"{self.save_directory}{pdf_file_name}.pdf"

        fish_logger.log(Fish_Log.INFO, f"Pdf File Name {pdf_file_name}, Pdf File Path {pdf_file_path}")

        with pdf.PdfPages(pdf_file_path) as pdf_pages:
            if grouping:
                for plt_label, (val_list, std_list, cndt_list, clr_lst, clr_lgnd) in plt_dict.items():
                    fig, ax = plt.subplots(figsize=(14.5, 5.5))
                    y_level = 0.5

                    if "+" in plt_label:
                        plt_title = self.generate_title(assay=plt_label.split("+")[0], stimulus=plt_label.split("+")[1])
                    else: 
                        plt_title = self.generate_title(assay=plt_label)

                    for i, (value, std_dev, color) in enumerate(zip(val_list, std_list, clr_lst)):
                        ax.errorbar(value, y_level, xerr=std_dev, marker='o', markersize=7, 
                                    color=color, linestyle='None', capsize=5, ecolor='black', elinewidth=3)

                    for i, cndt in enumerate(cndt_list):
                        ax.text(val_list[i], y_level + 0.02, cndt, ha='center', fontsize=5, rotation=90)

                    ax.get_yaxis().set_visible(False)
                    ax.xaxis.set_ticks_position('none') 
                    
                    if min(val_list) < 0:
                        xmin =  min(val_list) * 1.2 - 1
                    else:
                        xmin = min(val_list) - (max(val_list) * 0.2) - 1

                    if max(val_list) <= 0:
                        xmax = max(val_list) - (min(val_list) * 0.2) + 1
                    else:
                        xmax = max(val_list) * 1.2 + 1

                    ax.hlines(0, xmin, xmax, color='black')
                    ax.set_xlim(xmin, xmax)
                    ax.set_ylim(0, y_level + 0.5)

                    legend_patches = [mpatches.Patch(color=clr_info_tup[1], label=clr_info_tup[0]) for clr_info_tup in clr_lgnd]
                    ax.legend(handles=legend_patches, loc='center left', bbox_to_anchor=(1, 0.5), title='Statistically Separate Groups')  # Set legend title here
                    ax.set_xlabel('Activity')
                    ax.set_title(plt_title)

                    plt.tight_layout()

                    pdf_pages.savefig(fig)
                    plt.close(fig)

            else:
                for plt_label, (val_list, std_list, cndt_list) in plt_dict.items():
                    fig, ax = plt.subplots(figsize=(14.5, 5.5))
                    y_level = 0.5

                    if "+" in plt_label:
                        plt_title = self.generate_title(assay=plt_label.split("+")[0], stimulus=plt_label.split("+")[1])
                    else: 
                        plt_title = self.generate_title(assay=plt_label)

                    ax.errorbar(val_list, [y_level] * len(val_list), xerr=std_list, marker='o', markersize=7, 
                        color='blue', linestyle='None', capsize=5, ecolor='black', elinewidth=3)

                    for i, cndt in enumerate(cndt_list):
                        ax.text(val_list[i], y_level + 0.05, cndt, ha='center', fontsize=5, rotation=90)

                    ax.get_yaxis().set_visible(False)
                    ax.xaxis.set_ticks_position('none') 
                    if min(val_list) < 0:
                        xmin =  min(val_list) * 1.2 
                    elif min(val_list) >= 0:
                        xmin = min(val_list) - (max(val_list) * 0.2) - 1

                    if max(val_list) <= 0:
                        xmax = max(val_list) - (min(val_list) * 0.2) + 1
                    else:
                        xmax = max(val_list) * 1.2 + 1

                    ax.hlines(0, xmin, xmax, color='black')
                    ax.set_xlim(xmin, xmax)

                    ax.set_ylim(0, y_level + 0.5)

                    ax.set_xlabel('Activity')
                    ax.set_title(plt_title)

                    plt.tight_layout()

                    pdf_pages.savefig(fig)
                    plt.close(fig)


    def graph_oneD_bars(self, plt_dict, grouping=False):
        pdf_file_name = self.generate_filename()
        pdf_file_path = f"{self.save_directory}{pdf_file_name}.pdf"

        if os.path.exists(pdf_file_path):
            pdf_file_name = self.filename_helper(pdf_file_name, '.pdf')
            pdf_file_path = f"{self.save_directory}{pdf_file_name}.pdf"

        fish_logger.log(Fish_Log.INFO, f"Pdf File Name {pdf_file_name}, Pdf File Path {pdf_file_path}")

        with pdf.PdfPages(pdf_file_path) as pdf_pages:
            if grouping:
                for plt_label, (val_list, std_list, cndt_list, clr_lst, clr_lgnd) in plt_dict.items():
                    fig, ax = plt.subplots(figsize=(14.5, 5.5))

                    sorted_indices = sorted(range(len(val_list)), key=lambda i: val_list[i])
                    val_list = [val_list[i] for i in sorted_indices]
                    std_list = [std_list[i] for i in sorted_indices]
                    cndt_list = [cndt_list[i] for i in sorted_indices]
                    clr_lst = [clr_lst[i] for i in sorted_indices]

                    if "+" in plt_label:
                        plt_title = self.generate_title(assay=plt_label.split("+")[0], stimulus=plt_label.split("+")[1])
                    else: 
                        plt_title = self.generate_title(assay=plt_label)

                    bar_positions = range(len(val_list))
                    ax.bar(bar_positions, val_list, yerr=std_list, capsize=5,
                        color=clr_lst, edgecolor='black', align='center')
                    
                    ax.set_xticks(bar_positions)
                    ax.set_xticklabels(cndt_list, rotation=90, ha='center', fontsize=8)

                    legend_patches = [mpatches.Patch(color=clr_info_tup[1], label=clr_info_tup[0]) for clr_info_tup in clr_lgnd]
                    ax.legend(handles=legend_patches, loc='center left', bbox_to_anchor=(1, 0.5), title='Statistically Separate Groups')
                    
                    ax.set_ylabel('Activity')
                    ax.set_title(plt_title)

                    plt.tight_layout()
                    pdf_pages.savefig(fig)
                    plt.close(fig)

            else:
                for plt_label, (val_list, std_list, cndt_list) in plt_dict.items():
                    fig, ax = plt.subplots(figsize=(14.5, 5.5))

                    # Sort values from low to high along with associated lists
                    sorted_indices = sorted(range(len(val_list)), key=lambda i: val_list[i])
                    val_list = [val_list[i] for i in sorted_indices]
                    std_list = [std_list[i] for i in sorted_indices]
                    cndt_list = [cndt_list[i] for i in sorted_indices]

                    # Determine title
                    if "+" in plt_label:
                        plt_title = self.generate_title(assay=plt_label.split("+")[0], stimulus=plt_label.split("+")[1])
                    else: 
                        plt_title = self.generate_title(assay=plt_label)

                    # Plot bar graph without color list
                    bar_positions = range(len(val_list))
                    ax.bar(bar_positions, val_list, yerr=std_list, capsize=5,
                        color='c', edgecolor='black', align='center')

                    # Set x-axis labels and their positions
                    ax.set_xticks(bar_positions)
                    ax.set_xticklabels(cndt_list, rotation=90, ha='center', fontsize=8)

                    # Labels and title
                    ax.set_ylabel('Activity')
                    ax.set_title(plt_title)

                    plt.tight_layout()
                    pdf_pages.savefig(fig)
                    plt.close(fig)



















