import os

import FishBrain
from FishLog import Fish_Log
from TextColors import Text_Colors


# % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % 
# HELLO, this is where Fish_Spectacles begins     #
# # the main purpose of this file FishHead        #
# # is to gather information from the user to     # 
# # feed into FishBrain. The inputs are filtered  #
# # and checked against known answers when        #
# # possible.                                     #
# % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ %


script_name = "Fish Spectacles"
script_version = "0.3.3"
updated_date = "2024/03/25"
script_version_write_date = "2023/12/11" # start

fish_logger = Fish_Log()




class Fish_Face():
    # % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ %
    # HELLO, this is the class Fish_Face              #
    # # the main purpose of this class is to gather   #
    # # # information about what inforamation the     #
    # # # user wants to visualize. This class gathers #
    # # # information about the correct answers to    #
    # # # questions to check user input               #
    # # this class is structured such that when it is #
    # # # instantiated, information about the script  #
    # # # is printed to the user, several important   #
    # # # dictionaries are initialized, and the       #
    # # # user prompting functions are called from    #
    # # # the init function. This class also          #
    # # # instiantiates the analysis before prompting #
    # # # which graphs to view to grab important info #
    # # # to present to the user about graphing       #
    # # there are no inputs to this class nor any     #
    # # # direct outputs of the class                 #
    # # this class is used to gather user input and   # 
    # # # feed into FishBrain                         #
    # % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ %

    alive = True
    n_files_analyzed = 0
    
    kill_words = ['stop', 'quit', 'exit', 'close', 'done'] 
    # prompt answer value strings should not be in kill words!

    prompt_questions = {
        'analysis_machine' : f'{Text_Colors.NORMAL}\tWhich machine was used to collect data?\n\t-Sauron \n\t-MCAM : [INPROGRESS DO NOT USE]\n--> ',
        'analysis_type' : f'{Text_Colors.NORMAL}\n\tWhat type of analysis do you want to perform?\n\t-preview : show battery and treatment information for run \n\t-technical : individual run \n\t-biological : [INPROGRESS DO NOT USE] analyze multiple runs together\n\t\t(must use same battery) \n\t-battery : show battery information \n--> ',
        'run_number' : f'{Text_Colors.NORMAL}\n\tWhich run number to view?\n--> ',
        'battery_number' : f'{Text_Colors.NORMAL}\n\tWhich battery number to view?\n--> ',
        'battery_plot' : f'{Text_Colors.NORMAL}\n\tDo you want to plot stimuli on the MI trace?\n\t-yes\n\t-no\n--> ',
        'analysis_group' : f'{Text_Colors.NORMAL}\n\tHow do you want to group the data?\n\t-treatment : sort by treatment / concentration\n\t-well : sort by well\n\t-error : sorts by rows, columns, and halves\n\t-custom : custom input for grouping \n--> ',
        'analysis_calculations' : f'{Text_Colors.NORMAL}\n\tHow do you want to analyze the results?\n\t-raw : overlays replicates of same treatment/group\n\t-average : averages mi traces of same treatment/group\n\t-split : does not average mi traces but splits them\n\t\tinto individual assays and stimuli responses \n\t-full : averages and splits mi traces\n--> ',
        'secondary_calculations' : f'{Text_Colors.NORMAL}\n\tDo you want to perform secondary analysis?\n\t-habituation : returns habituation results\n\t-prepulse inhibition : [INPROGRESS DO NOT USE] returns prepulse inhibition results\n\t-no\n--> ',
        'name_title' : f'{Text_Colors.NORMAL}\n\tDo you want to set the title of the plots?\n\t-default : analysisType RUN(S) runNumber(s) (ASSAY assayNames) (STIMULUS stimulusNames)\n\t-custom\n--> ',
        'user_title' : f'{Text_Colors.NORMAL}\n\tPlease input the the title for the plots below:\n-->',
        'name_file' : f'{Text_Colors.NORMAL}\n\tDo you want to set the name of the file?\n\t-default : YYYYMMDD_RUNS_runNumbers_plotType_analysisType\n\t-custom\n--> ',
        'user_file' : f'{Text_Colors.NORMAL}\n\tPlease input the name for the file below:\n-->',
        'specific_treatment' : f'{Text_Colors.NORMAL}\n\tDo you want to view specific treatments/groupings or treatment concenctrations?\n\t-treatment : view specific treatments or groupings\n\t-treatment-concentration : view specific treatment concentration graphs\n\t-no\n--> ',
        'specific_assay' : f'{Text_Colors.NORMAL}\n\tDo you want to view specific assays?\n\t-yes\n\t-no\n--> ',
        'isolate_stimuli' : f'{Text_Colors.NORMAL}\n\tDo you want to isolate the stimuli?\n\t-yes\n\t-no\n--> ',
        'continue_analysis' : f'{Text_Colors.NORMAL}\n\tDo you want to generate more results from this data?\n\t-yes\n\t-no\n--> ',
        'visualize_secondary' : f'{Text_Colors.NORMAL}\n\tDo you want to view the secondary analysis?\n\t-yes\n\t-no\n--> '
    }

    prompt_answers = {
        'analysis_machine' : ['sauron', 'mcam'],
        'analysis_type' : ['preview', 'technical', 'biological', 'battery'],
        'battery_plot' : ['yes', 'no'],
        'analysis_group' : ['treatment', 'well', 'error', 'custom'],
        'analysis_calculations' : ['raw', 'average', 'split', 'full'],
        'name_title' : ['default', 'custom'],
        'name_file' : ['default', 'custom'],
        'specific_treatment' : ['treatment', 'treatment-concentration', 'no'], # needs treatments from csvs added or display options afterwards
        'specific_assay' : ['yes', 'no'], # needs assays from csvs added or display options afterwards
        'isolate_stimuli' : ['yes', 'no'],
        'secondary_calculations' : ['habituation', 'arousal', 'no'],
        'visualize_secondary' : ['yes', 'no']
    }

    none_responses = {
        'analysis_machine' : None,
        'analysis_type' : None,
        'run_number' : None,
        'battery_number' : None,
        'battery_plot' : None,
        'analysis_group' : None,
        'user_group' : None,
        'analysis_calculations' : None,
        'secondary_calculations': None,
        'name_title' : None,
        'user_title' : None,
        'name_file' : None,
        'user_file' : None,
        'specific_treatment' : None,
        'user_treatment' : None,
        'specific_assay' : None,
        'user_assay' : None,
        'visualize_secondary' : None,
        'user_habituation' : None,  
        'isolate_stimuli' : None 
    }


    def __init__(self):
        self.split_str = '+'

        self.prompt_filter_maker()
        self.warning_response_maker()

        self.welcome_user()
        self.usage_detail()

        self.load_run_list()
        self.load_battery_list()

        self.live_fish()

        self.last_words()

    
    def load_run_list(self):
        csv_files = [file for file in os.listdir('SauronResources/SauronRuns') if file.endswith('.csv')]
        self.prompt_answers.update({'run_number' : [int(file.split('.')[0]) for file in csv_files]})

    
    def load_battery_list(self):
        files = [file for file in os.listdir('SauronResources/SauronBatteryInfo') if file.endswith('.csv')]
        battery_numbers = {int(file.split('_')[0]) for file in files}
        self.prompt_answers.update({'battery_number' : list(battery_numbers)})


    def user_is_alive_check(function_name):
        def is_alive_check(self, *args, **kwargs):
            if self.alive:
                return function_name(self, *args, **kwargs)
            
        return is_alive_check
    

    def new_fish(self):
        del self.analysis
        print(f'{Text_Colors.NORMAL}]\n\n\t**********************\n\tStarting a New Prompt\n\t**********************\n')
        self.usage_detail()
        self.live_fish()

    
    @user_is_alive_check
    def live_fish(self):
        self.user_responses = Fish_Face.none_responses.copy()
        self.analysis_prompt()
        
        if not self.alive:
            return
        self.analysis = FishBrain.Fish_Analysis(self.user_responses, self.split_str)

        if self.analysis.warning:
            self.warning_handler(self.analysis.warning) 
        
        if not self.alive:
            return
    
        if self.user_responses['analysis_type'] != 'battery' and self.user_responses['analysis_type'] != 'preview':    
            if self.user_responses['analysis_group'] == 'treatment':
                self.graph_prompt(self.analysis.analyzed_info.treatments, self.analysis.battery_info.assays, cncs=self.analysis.analyzed_info.concentration_dict)
            else:
                self.graph_prompt(self.analysis.analyzed_info.treatments, self.analysis.battery_info.assays)
            
        if not self.alive:
            return
        self.analysis.visualize_information(self.user_responses)
        
        if self.analysis.warning:
            self.warning_handler(self.analysis.warning)
        
        self.n_files_analyzed += 1
        
        if self.user_responses['analysis_type'] != 'battery' and self.user_responses['analysis_type'] != 'preview':
            if self.user_responses['analysis_calculations'] == 'split' or self.user_responses['analysis_calculations'] == 'full':
                ask_continue_str = f"{Text_Colors.NORMAL}\n\tDo you want to create more graphs from this data?\n--> "
                continue_response = self.check_continue(ask_continue_str)
                
                if self.alive:
                    if continue_response:
                        self.live_fish_loop(ask_continue_str)

        if self.alive:
            self.new_fish()
        

    @user_is_alive_check
    def live_fish_loop(self, ask_str):
        continue_analysis = True
        while continue_analysis:    
            if self.user_responses['analysis_group'] == 'treatment':
                self.graph_prompt(self.analysis.analyzed_info.treatments, self.analysis.battery_info.assays, cncs=self.analysis.analyzed_info.concentration_dict)
            else:
                self.graph_prompt(self.analysis.analyzed_info.treatments, self.analysis.battery_info.assays)

            if not self.alive:
                return
            
            self.analysis.visualize_information(self.user_responses)

            continue_analysis = self.check_continue(ask_str)
            if not self.alive:
                return


    def analysis_prompt(self):
        self.prompt_package('analysis_machine')
        
        self.prompt_package('analysis_type')
        
        if self.user_responses['analysis_type'] == 'battery':
            self.prompt_package('battery_number')
            if self.user_responses['name_file'] == 'custom':
                self.prompt_package('user_file')
            return

        self.prompt_package('run_number')

        self.prompt_package('analysis_group')
        if self.user_responses['analysis_group'] == 'custom':
            self.custom_grouping()

        self.prompt_package('analysis_calculations')
        
        if self.user_responses['analysis_calculations'] == 'full':
            self.prompt_package('secondary_calculations')            

        self.prompt_package('name_file')
        if self.user_responses['name_file'] == 'custom':
            self.prompt_package('user_file')

        if self.user_responses['analysis_type'] == 'preview':
            return

        self.prompt_package('name_title')
        
        if self.user_responses['name_title'] == 'custom':
            self.prompt_package('user_title')

        self.prompt_package('battery_plot')

        

        fish_logger.log(Fish_Log.INFO, f'user_responses {{{", ".join(f"{key}: {value}" for key, value in self.user_responses.items())}}}')
        

    def graph_prompt(self, treatments, assays, cncs=None):
        self.prompt_package('specific_treatment')
        
        if self.user_responses['specific_treatment'] == 'treatment':
            self.user_treatment(treatments)
        elif self.user_responses['specific_treatment'] == 'treatment-concentration':
            self.user_treatment(treatments, concentration_dict=cncs)
            
        if self.user_responses['analysis_calculations'] == 'split' or self.user_responses['analysis_calculations'] == 'full': 
            self.prompt_package('specific_assay')
            
            if self.user_responses['specific_assay'] == 'yes':
                self.user_assay(assays)

            self.prompt_package('isolate_stimuli')

            if self.user_responses['secondary_calculations'] == 'habituation':
                self.prompt_package('visualize_secondary')
                if self.user_responses['visualize_secondary'] == 'yes':
                    self.user_habituation(treatments, cncs)


    @user_is_alive_check
    def prompt_package(self, prompt_name):
        self.user_responses[prompt_name] = self.prompt_user(prompt_name)
        fish_logger.log(Fish_Log.INFO, f'{prompt_name} with response : {self.user_responses[prompt_name]}')


    def prompt_user(self, prompt):
        response = self.prompt_filter[prompt](input(self.prompt_questions[prompt]))
        
        if response in self.kill_words:
            self.alive = False
            return
        
        if prompt == "run_number" or prompt == 'battery_number':
            if isinstance(response, str):
                print(f'''{Text_Colors.NORMAL}
                      I am sorry, I did not understand your input : {response}
                      I was expecting an integer (numbers only)
                ''')
                response = self.prompt_user(prompt)
            
            elif response not in self.prompt_answers[prompt]:
                print(f"""{Text_Colors.NORMAL}
                    I am sorry, I could not find your input : {response}
                    in the correct directory. Please check your number input
                    or update the run .csv files in SauronResoures/SauronRuns
                """)
                response = self.prompt_user(prompt)
        
        elif prompt == 'user_file' or prompt == 'user_title':
            response = response.replace(' ', '_')
        
        else:            
            if response not in self.prompt_answers[prompt]:
                print(f'''{Text_Colors.NORMAL}
                    I am sorry, I did not understand your input : {response} 
                    I was expecting one of the following : 
                    {", ".join(str(answer) for answer in self.prompt_answers[prompt])}
                    ''')
                response = self.prompt_user(prompt)
        
        return response


    def prompt_filter_maker(self):
        self.prompt_filter = {
            'analysis_machine' : self.str_response,
            'analysis_type' : self.str_response,
            'run_number' : self.int_response,
            'battery_number' : self.int_response,
            'battery_plot' : self.str_response,
            'analysis_group' : self.str_response,
            'analysis_calculations' : self.str_response,
            'name_title' : self.str_response,
            'user_title' : self.str_response,
            'name_file' : self.str_response,
            'user_file' : self.str_response,
            'specific_treatment' : self.str_response,
            'specific_assay' : self.str_response,
            'isolate_stimuli' : self.str_response,
            'secondary_calculations' : self.str_response,
            'visualize_secondary' : self.str_response
        }


    def check_continue(self, ask_string):
        continue_response = self.str_response(input(ask_string))
        if continue_response.strip().lower() in self.kill_words:
            self.alive = False
            return 
        
        if continue_response == 'no':
            return False
        elif continue_response == 'yes':
            return True
        else:
            print(f'''{Text_Colors.NORMAL}
                    I am sorry, I did not understand your reponse : {continue_response}
                    I was expecting yes or no
                ''')
            return self.check_continue(ask_string)


    @user_is_alive_check
    def user_treatment(self, treatment_list, concentration_dict=None):
        result_list = []
        ask_user = True
        ask_repeat_string = f"{Text_Colors.NORMAL}\tDo you want to input another?\n-->"

        if self.user_responses['specific_treatment'] == 'treatment-concentration' or self.user_responses['visualize_secondary'] == 'habituation':
            treatment_concentrations = [f"\t{self.interpret_treatment_concentration(treatment, concentration)}\n" for treatment in treatment_list for concentration in concentration_dict[treatment]]
            instruction_str = f"""{Text_Colors.NORMAL}
                Please input one condition
                For each treatment concentration pair, please separate 
                with a semicolon and separate the two conditions 
                with a space as follows below : 
                \ttreatmentName1;concentration1 treatmentName2;concenctration2 treatmentNameN;concenctrationN

            """
            print(instruction_str)

            while ask_user:
                treatment_prompt = f'{Text_Colors.NORMAL}\ttreatments and concentrations found:\n{"".join(treatment_concentrations)}'
                user_prompt = f"{instruction_str}{treatment_prompt}"
                
                result = self.treatment_concentration_response(user_prompt, treatment_list, concentration_dict)
                if not self.alive:
                    return
                result_list.append(result)
                
                ask_user = self.check_continue(ask_repeat_string)
                if not self.alive:
                    return
                    
        else:
            instruction_str = f"""{Text_Colors.NORMAL}
                Please input the treatments as follows.
                For a singlular treatment :
                \ttreatmentName1, treatmentName2, treatmentNameN
                For multiple treatments :
                \ttreatmentName1A::treatmentName1B, treatmentName2A::Treatmentname2B::Treatmentname2C, treatmentNameN::TreatmentnameN 
                these can be used interchangably within a single response

            """
            print(instruction_str)
            treatment_strings = [f"\n\t{treatment}" for treatment in treatment_list]
            treatment_prompt = f'{Text_Colors.NORMAL}treatments found:{"".join([trt_str for trt_str in treatment_strings])}'
            user_prompt = f"{instruction_str}{treatment_prompt}"
            result = self.treatment_response(user_prompt, treatment_list)
            if not self.alive:
                return
            result_list = result
            
        self.user_responses['user_treatment'] = result_list


    def treatment_concentration_response(self, prompt, treatments, concentration_dict, no=False):
        response = input(f"{prompt}\n-->")
        
        if response.strip().lower() in self.kill_words:
            self.alive = False
            return

        if no:
            if response.strip().lower() == 'no':
                return None

        if ' ' in response and ';' in response:
            not_found = False
            treatment_concentrations = response.split(' ')
            for trt_cnc in treatment_concentrations:
                trt_cnc_split = trt_cnc.split(';')
                for trt_cnc_spl in trt_cnc_split:
                    if not trt_cnc_spl:
                        if trt_cnc_spl[0].strip() in treatments:
                            concentration = trt_cnc_spl[1].strip()
                            if concentration in concentration_dict[treatments]:
                                pass
                            else:
                                not_found = True
                        else:
                            not_found = True
            
            if not not_found:
                print(f'{Text_Colors.NORMAL}\tI am sorry I could not find your treatment or concentration for that treatment : {response}\n\tPlease try again')
                return self.treatment_concentration_response(prompt, treatments, concentration_dict)
            
            else:
                treatment = '::'.join(trt_cnc_split[0] for trt_cnc in treatment_concentrations for trt_cnc_split in trt_cnc.split())
                concentration = '::'.join(trt_cnc_split[1] for trt_cnc in treatment_concentrations for trt_cnc_split in trt_cnc.split())
                return f"{treatment}{self.split_str}{concentration}"

        elif ';' in response:
            not_found = False
            trt_cnc_split = response.split(';')
            for trt_cnc_spl in trt_cnc_split:
                if not trt_cnc_spl:
                    if trt_cnc_spl[0].strip() in treatments:
                        concentration = trt_cnc_spl[1].strip()
                        if concentration in concentration_dict[treatments]:
                            pass
                        else:
                            not_found = True
                    else:
                        not_found = True
            
            if not_found:
                print(f'{Text_Colors.NORMAL}\tI am sorry I could not find your treatment or concentration for that treatment : {response}\n\tPlease try again')
                return self.treatment_concentration_response(prompt, treatments, concentration_dict)
            else:
                return f"{response.split(';')[0]}{self.split_str}{response.split(';')[1]}"

        else:
            print(f'{Text_Colors.NORMAL}\tI am sorry I did not understand your response formatting\n\tPlease try again')
            return self.treatment_concentration_response(prompt, treatments, concentration_dict)
    
    
    def treatment_response(self, prompt, treatments, no=False):
        response = input(f"{prompt}\n-->")
        
        if response.strip().lower() in self.kill_words:
            self.alive = False
            return
        
        if no:
            if response.strip().lower() == 'no':
                return 'no'
        
        if ',' in response:
            not_found = False
            split_response = response.split(',')
            for spl_resp in split_response:
                if spl_resp.strip() in treatments:
                    pass
                else:
                    not_found = True

            if not_found:
                print(f'{Text_Colors.NORMAL}\tI am sorry I could not find the treatments for {response}\n\tPlease try again')
                return self.treatment_response(prompt, treatments)
            else:
                return [spl_resp.strip() for spl_resp in split_response]
            
        else:
            if response.strip() in treatments:
                return [response.strip()]
            else:
                print(f'{Text_Colors.NORMAL}\tI am sorry I could not find the treatment for {response}\n\tPlease try again')
                return self.treatment_response(prompt, treatments)

    @user_is_alive_check
    def user_assay(self, assays):
        instruction_str = f"""{Text_Colors.NORMAL}
            Please input the assay or assays you want to view
            To view multiple assays, separate them with a comma
            such as :
                assay1, assay2, assayn

        """
        assay_strings = [f'\n\t{assay}' for assay in assays]
        assay_prompt = f'{Text_Colors.NORMAL}assays found :{"".join(assay_string for assay_string in assay_strings)}'
        user_prompt = f'{instruction_str}{assay_prompt}'

        self.user_responses['user_assay'] = self.assay_response(user_prompt, assays)
    
    
    def assay_response(self, prompt, assays):
        response = input(f"{prompt}\n-->")

        if response.strip().lower() in self.kill_words:
            self.alive = False
            return
        
        if ',' in response:
            not_found = False
            split_response = response.split(',')
            for spl_resp in split_response:
                if spl_resp.strip() in assays:
                    pass
                else:
                    not_found = True

            if not_found:
                print(f'{Text_Colors.NORMAL}\tI am sorry I could not find the assays for {response}\n\tPlease try again')
                return self.assay_response(prompt, assays)
            else:
                return [spl_resp.strip() for spl_resp in response.split(',')]
            
        else:
            if response.strip() in assays:
                return [response.strip()]
            else:
                print(f'{Text_Colors.NORMAL}\tI am sorry I could not find the assay for {response}\n\tPlease try again')
                return self.assay_response(prompt, assays)


    @user_is_alive_check
    def custom_grouping(self):
        # this is for creating a dictionary {user_group_name : [list of wells for group]}
        ask_user = True
        result_dict = {}
        instruction_str = f'''{Text_Colors.NORMAL}
            Please enter the name of your group and wells to group 
            one at a time as follows :
                group_name ; well1, well2, well3, welln

        '''
        well_string = f'''{Text_Colors.NORMAL}
            some common grouping of wells :
                - by row
            A01, A02, A03, A04, A05, A06, A07, A08, A09, A10, A11, A12
            B01, B02, B03, B04, B05, B06, B07, B08, B09, B10, B11, B12
            C01, C02, C03, C04, C05, C06, C07, C08, C09, C10, C11, C12
            D01, D02, D03, D04, D05, D06, D07, D08, D09, D10, D11, D12
            E01, E02, E03, E04, E05, E06, E07, E08, E09, E10, E11, E12
            F01, F02, F03, F04, F05, F06, F07, F08, F09, F10, F11, F12
            G01, G02, G03, G04, G05, G06, G07, G08, G09, G10, G11, G12
            H01, H02, H03, H04, H05, H06, H07, H08, H09, H10, H11, H12
                - by column
            A01, B01, C01, D01, E01, F01, G01, H01
            A02, B02, C02, D02, E02, F02, G02, H02
            A03, B03, C03, D03, E03, F03, G03, H03
            A04, B04, C04, D04, E04, F04, G04, H04
            A05, B05, C05, D05, E05, F05, G05, H05
            A06, B06, C06, D06, E06, F06, G06, H06
            A07, B07, C07, D07, E07, F07, G07, H07
            A08, B08, C08, D08, E08, F08, G08, H08
            A09, B09, C09, D09, E09, F09, G09, H09
            A10, B10, C10, D10, E10, F10, G10, H10
            A11, B11, C11, D11, E11, F11, G11, H11
            A12, B12, C12, D12, E12, F12, G12, H12

        '''
        
        user_prompt = f"{instruction_str}{well_string}"
        ask_repeat_string = f"{Text_Colors.NORMAL}\tDo you want to input another?\n-->"
        while ask_user:
            group_name, wells_to_group = self.custom_response(user_prompt)
            if not self.alive:
                return
            result_dict[group_name] = wells_to_group

            ask_user = self.check_continue(ask_repeat_string)
            if not self.alive:
                return
            
        self.user_responses['user_group'] = result_dict



    def custom_response(self, prompt):
        full_well_plate = [
            'A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12',
            'B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B09', 'B10', 'B11', 'B12',
            'C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08', 'C09', 'C10', 'C11', 'C12',
            'D01', 'D02', 'D03', 'D04', 'D05', 'D06', 'D07', 'D08', 'D09', 'D10', 'D11', 'D12', 
            'H01', 'H02', 'H03', 'H04', 'H05', 'H06', 'H07', 'H08', 'H09', 'H10', 'H11', 'H12',
            'G01', 'G02', 'G03', 'G04', 'G05', 'G06', 'G07', 'G08', 'G09', 'G10', 'G11', 'G12',
            'F01', 'F02', 'F03', 'F04', 'F05', 'F06', 'F07', 'F08', 'F09', 'F10', 'F11', 'F12',
            'E01', 'E02', 'E03', 'E04', 'E05', 'E06', 'E07', 'E08', 'E09', 'E10', 'E11', 'E12'
            ]
        

        response = input(f"{prompt}\n-->")

        if response.strip().lower() in self.kill_words:
            self.alive = False
            return
        
        if ';' in response:
            split_response = response.split(';')
            group_name = split_response[0].strip()
            well_list = []
            not_found = False
            if ',' in split_response[1]:
                split_split = split_response[1].split(',')
                for well in split_split:
                    if well.strip() in full_well_plate:
                        well_list.append(well.strip())
                    else:
                        print(f'{Text_Colors.NORMAL}\tI am sorry I could not find the wells {response}\n\tPlease try again')
                        not_found = True
                        break
            else:
                if split_response[1].strip() in full_well_plate:
                    well_list = [split_response[1].strip()]
                else:
                    print(f'{Text_Colors.NORMAL}\tI am sorry I could not find the well {response}\n\tPlease try again')
                    not_found = True

            if not_found:
                return self.custom_response(prompt)
            else:
                return group_name, well_list
        
        else:
            print(f'{Text_Colors.NORMAL}\tI am sorry I did not understand your response formatting : {response}\n\tPlease try again')
            return self.custom_response(prompt)


    @user_is_alive_check
    def user_habituation(self, treatment_list, concentration_dict):
        if self.user_responses['analysis_group'] == 'treatment':
            instruction_str = f"""{Text_Colors.NORMAL}
                If you have a control for this run, please input it below
                * * * otherwise enter 'no' * * *

                Please input one condition
                For each treatment concentration pair, please separate 
                with a semicolon and separate the two conditions 
                with a space as follows below : 
                \ttreatmentName1;concentration1 treatmentName2;concenctration2 treatmentNameN;concenctrationN

            """
            treatment_concentrations = [f"\t{self.interpret_treatment_concentration(treatment, concentration)}\n" for treatment in treatment_list for concentration in concentration_dict[treatment]]
            treatment_prompt = f'{Text_Colors.NORMAL}\ttreatments and concentrations found:\n{"".join(treatment_concentrations)}'
            user_prompt = f"{instruction_str}{treatment_prompt}"
            result = self.treatment_concentration_response(user_prompt, treatment_list, concentration_dict, no=True)
        
        else:
            instruction_str = f"""{Text_Colors.NORMAL}
                If you have a control for this run, please input it below
                * * * otherwise enter 'no' * * *

                Please input one condition
                For a singlular treatment :
                \ttreatmentName1
                For multiple treatments :
                \ttreatmentName1::treatmentName2

            """
            treatment_strings = [f"\n\t{treatment}" for treatment in treatment_list]
            treatment_prompt = f'{Text_Colors.NORMAL}treatments found:{"".join([trt_str for trt_str in treatment_strings])}'
            user_prompt = f"{instruction_str}{treatment_prompt}"
            result = self.treatment_response(user_prompt, treatment_list, concentration_dict, no=True)
        
        if not self.alive:
            return
        
        self.user_responses['user_habituation'] = result


    def warning_handler(self, warning_tup):
        if warning_tup[0] in self.warning_response.keys():
            self.warning_response[warning_tup[0]](warning_tup)
        else:
            self.alive = False


    def warning_response_maker(self):
        self.warning_response = {
            'NO_RUN_CSV' : self.no_run_csv_response,
            'NO_BATTERY_CSV' : self.no_battery_csv_response,
            'NO_STIM_FRAME_CSV' : self.no_stim_frame_csv_response,
            'UNKNOWN_TREATMENT' : self.unknown_treatment_response,
            'FILENAME_HELPER' : self.filename_helper_response
        }


    def no_run_csv_response(self, warning_tuple):
        warning_string = f"""{Text_Colors.WARNING}
            Oh No! I was not able to find the run csv! 
            I was looking for run number, {warning_tuple[1]}, 
            in the location, {warning_tuple[2]},
            with the path, {warning_tuple[3]}.
            
            You can check the folder to either fix the name 
                / add the file to the location
            or run the script with different run number

            
            rerun : rechecks for same run csv 
                (assuming the issue has been resolved by the user)
            new : start new prompt
        """

        decision = input(f'{warning_string}\n-->').strip().lower()

        fish_logger.log(Fish_Log.INFO, f'user_decision {decision}')

        if decision == 'rerun':
            self.analysis.no_run_csv_pipe()
        elif decision == 'new':
            self.new_fish()
        else:
            confused = f"""{Text_Colors.WARNING}
                I did not understand your response {decision}
                Please input one of the following:
                rerun, new

                I am restarting the prompt\n
            """

            print(confused)
            self.no_run_csv_response(warning_string)
        

    
    def no_battery_csv_response(self, warning_tuple):
        warning_string = f"""{Text_Colors.WARNING}
            Oh No! I was not able to find the battery csv! 
            I was looking for battery number, {warning_tuple[1]}, 
            in the location, {warning_tuple[2]},
            with the path, {warning_tuple[3]}.
            
            You can check the folder to either fix the name 
                / add the file to the location
            or run the script with different run/battery number

            
            rerun : rechecks for same battery csv 
                (assuming the issue has been resolved by the user)
            new : start new prompt
        """

        decision = input(f'{warning_string}\n-->').strip().lower()

        fish_logger.log(Fish_Log.INFO, f'user_decision {decision}')

        if decision == 'rerun':
            self.analysis.no_battery_stimf_pipe()
        elif decision == 'new':
            self.new_fish()
        else:
            confused = f"""{Text_Colors.WARNING}
                I did not understand your response {decision}
                Please input one of the following:
                rerun, new

                I am restarting the prompt\n
            """

            print(confused)
            self.no_battery_csv_response(warning_string)


    def no_stim_frame_csv_response(self, warning_tuple):
        warning_string = f"""{Text_Colors.WARNING}
            Oh No! I was not able to find the stim frame csv! 
            I was looking for battery number, {warning_tuple[1]}, 
            in the location, {warning_tuple[2]},
            with the path, {warning_tuple[3]}.
            
            You can check the folder to either fix the name 
                / add the file to the location
            or run the script with different run number

            
            rerun : rechecks for same battery csv 
                (assuming the issue has been resolved by the user)
            new : start new prompt
        """

        decision = input(f'{warning_string}\n-->').strip().lower()

        fish_logger.log(Fish_Log.INFO, f'user_decision {decision}')

        if decision == 'rerun':
            self.analysis.no_battery_stimf_pipe()
        elif decision == 'new':
            self.new_fish()
        else:
            confused = f"""{Text_Colors.WARNING}
                I did not understand your response {decision}
                Please input one of the following:
                rerun, new

                I am restarting the previous prompt\n
            """

            print(confused)
            self.no_stim_frame_csv_response(warning_string)


    def unknown_treatment_response(self, warning_tuple):
        new_name_dict = {}

        warning_string = f"""{Text_Colors.CAUTION}
            Oh No! I was not able to find one or multiple treatment
            name(s) in my knowledge! (textbase)

            Can you input what the names of these treatments are?
            
            ... 
        """

        print(warning_string)

        unknown_trt_dict = self.unknown_treatment_sorter(warning_tuple[1])

        for unknown_name in unknown_trt_dict.keys():
            conc_str = "\n\t\t\t".join([f"{conc} : {unknown_trt_dict[unknown_name][conc]}" for conc in unknown_trt_dict[unknown_name].keys()])
            prompt_string = f"""{Text_Colors.CAUTION}
                NAME 
                    CONCENTRATION : WELLS

                {unknown_name}
                    \t{conc_str} 

                Input one of the following
                    unknown : for (an) unknown treatment(s)
                    treatment_name : known name (will be updated in textbase)
            """ #yea the tabs of conc_str is really weird but it works ¯\_(ツ)_/¯ 

            new_nm = input(f'{prompt_string}\n-->').strip().lower().replace(' ', '_')
            
            if new_nm in self.kill_words:
                self.alive = False
                return
            elif new_nm == 'unknown':
                new_name_dict[unknown_name] = unknown_name
            else:
                new_name_dict[unknown_name] = new_nm

        fish_logger.log(Fish_Log.INFO, f'NEW TREATMENT NAME USER INPUT,  {",".join([f"{unk_nm} to {new_nm}" for unk_nm, new_name in new_name_dict.items()])}')

        if not all(key == value for key, value in new_name_dict.items()):
            self.analysis.unknwn_trt_pipe(new_name_dict)
        else:
            self.analysis.unknwn_trt_pipe()

    
    def unknown_treatment_sorter(self, unknown_treatment_list):
        return_dict = {}
        for well, unknown_name, concentration in unknown_treatment_list:
            if unknown_name not in return_dict.keys():
                return_dict.update({unknown_name : {concentration : [well] }})
            elif concentration not in return_dict[unknown_name].keys():
                return_dict[unknown_name].update({concentration : [well] })
            else:
                return_dict[unknown_name][concentration].append(well)
        
        return return_dict
        

    
    def filename_helper_response(self, warning_tuple):
        # max iter for current name has been exceded, need new name from user or override
        # # (should be rare, low priority)
        # print old name and ask for new
        # run pipe 
        warning_string = f"""{Text_Colors.WARNING}
            Oh No! The max iteration for this file name has been exceeded (99)!
            Numbers greater than this will require adjustments to the script

            Please input another name for this file
        """


    @staticmethod
    def interpret_treatment_concentration(treatment, concentration):
        if '::' in treatment and '::' in concentration:
            return f"{treatment.split('::')[0]} {concentration.split('::')[0]}uM and {treatment.split('::')[1]} {concentration.split('::')[1]}uM"
        else:
            return f"{treatment} {concentration}uM"
        

    @staticmethod
    def str_response(response):
        return response.strip().lower().replace(' ', '_')


    @staticmethod
    def int_response(response):
        if ',' in response:
            multi_response = response.split(',')
            number_list = []
            for resp in multi_response:
                try:
                    number = int(resp.strip().replace(' ', ''))
                    number_list.append(number)
                except ValueError:
                    return multi_response
            return number_list
        
        else:
            try: 
                return int(response.strip().replace(' ',  ''))
            except ValueError:
                return response
        

    @staticmethod
    def float_response(response):
        return float(response.strip().replace(' ',  ''))


    @staticmethod
    def welcome_user():
        welcome_str = f"""{Text_Colors.NORMAL}
        # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
        # # # # # # # # # # # # # # # # # # # # # # # # # # # #

         ___ _    _      ___             _           _        
        | __(_)__| |_   / __|_ __ ___ __| |_ __ _ __| |___ ___
        | _|| (_-| ' \  \__ | '_ / -_/ _|  _/ _` / _| / -_(_-<
        |_| |_/__|_||_| |___| .__\___\__|\__\__,_\__|_\___/__/
                            |_|                               
           
                                 ,__
                                 |  `'.
               __           |`-._/_.:---`-.._
               \='.       _/..--'`__         `'-._
                \- '-.--"`      ===        /   o  `',
                 )= (                 .--_ |       _.'
                /_=.'-._             [=_-_ |   .--`-.
               /_.'    `\`'-._        '-=   \    _.'
                         )  _.-'`'-..       _..-'`
                        /_.'         `/";';`|
                                      \` .'/
                                       '--'

                  Welcome to {script_name} by Grant
                    for zebrafish behavior analysis
                      * * Sello Lab / UCSF * *
                         * % * {script_version} * % *
                       * % * {updated_date} * % * 

        # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
        # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        
        """

        print(welcome_str)


    def usage_detail(self):
        instruction_str = f"""{Text_Colors.NORMAL}\n
        ********************************************************
            You will be guided through questions on what 
            data to view and what type of analysis you 
            want to perform.

            At any time you can input any of these kill 
            words to exit the program :
            {", ".join(str(word) for word in self.kill_words)}
        ********************************************************\n
        """

        print(instruction_str)


    @staticmethod
    def last_words():
        closing_str = f"""{Text_Colors.NORMAL}
        # # # # # # # # # # # # # # # # # # # # # # #
        @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
        # # # # # # # # # # # # # # # # # # # # # # #

            Thank you for using {script_name} 
                          v{script_version}
          Please report any issues or bugs to Grant

                             ,__
                             |  `'.
           __           |`-._/_.:---`-.._
           \='.       _/..--'`__         `'-._
            \- '-.--"`      ===        /   o  `',
             )= (                 .--_ |       _.'
            /_=.'-._             [=_-_ |   .--`-.
           /_.'    `\`'-._        '-=   \    _.'
                     )  _.-'`'-..       _..-'`
                    /_.'         `/";';`|
                                  \` .'/
                                   '--'

        # # # # # # # # # # # # # # # # # # # # # # #
        @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
        # # # # # # # # # # # # # # # # # # # # # # #
        """

        print(closing_str)

    
    @staticmethod
    def unexpected_error_message():
        error_message = f"""{Text_Colors.WARNING}
        ! * ! * ! * ! * ! * ! * ! * ! * ! * ! * ! * ! * !
        -------------------------------------------------
        ! * ! * ! * ! * ! * ! * ! * ! * ! * ! * ! * ! * !

            I have encountered and unexpected error!
            I have to close the script, please check
            the log files for the error message.
            Sorry for any incoviences !

        
                |\    \ \ \ \ \ \ \       
                |  \    \ \ \ \ \ \ \   | O~-_     
                |   >----|-|-|-|-|-|-|--|  __/   
                |  /    / / / / / / /   |__\   
                |/     / / / / / / /             
                                                

        ! * ! * ! * ! * ! * ! * ! * ! * ! * ! * ! * ! * !
        -------------------------------------------------
        ! * ! * ! * ! * ! * ! * ! * ! * ! * ! * ! * ! * !
        """
        print(error_message)



#if __name__ == '__main__':
#    try:
#        analysis = Fish_Face()
#
#    except Exception as e:
#        error_type = type(e).__name__
#        error_str = str(e)
#        traceback_info = traceback.extract_tb(sys.exc_info()[2])[-1]
#        file_path, line_number, func_name, code_line = traceback_info
#
#        fish_spectacles_dir = os.path.join(os.path.dirname(os.path.abspath(file_path)), 'Fish_Spectacles')
#        file_name = os.path.relpath(file_path, fish_spectacles_dir)
#        file_name = file_name.replace('..', '')[1:]
#
#        fish_logger.log(Fish_Log.LETHAL, f"EXCEPTION {error_type} : {error_str}, FILE {file_name}, LINE {line_number}, CODE {code_line}, FUNCT {func_name}")

#        Fish_Face.unexpected_error_message()
    
#    finally:
#        fish_logger.finalize_info()
#        print(f'{Text_Colors.DEFAULT}')
    