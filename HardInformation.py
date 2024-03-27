import os
from FishLog import Fish_Log


# % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % 
# HELLO, this is HardInformation                  #
# # this file is for keeping track of information #
# # that has to be hard coded / cannot be         #
# # interpreted from just the information in the  #
# # files. This includes treatment names, assay   #
# # names and information like how many frames    #
# # to shift the stimuli indexes to align the     #
# # trace                                         #
# % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ %


fish_logger = Fish_Log()




class Information_Textbase():
    # % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ %
    # HELLO, this is the class Information_Textbase   #  
    # # the main purpose of this class is to manage   #
    # # # "textbases" of different types of           #
    # # # information. these functions write python   #
    # # # dictionaries to text files, read text files #
    # # # do python dictionaries, and can add a lines #
    # # # of information to the files.                #
    # # the class is structured to be initialized     #
    # # # with a textbase name and the necessary      #
    # # # functions are called from the instance      #
    # # inputs to the class are the textbase name     #
    # # the output of the class is a text file which  #
    # # # corresponds to information from python      #
    # # # dictionaries or vise versa                  # 
    # # this class is used independently of the main  #
    # # # script for the time being                   #
    # % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ %


    def __init__(self, textbase_name):
        self.textbase_name = textbase_name
        self.textbase_path = f'SauronResources/TextBase/{textbase_name}.txt'


    def write_dict_to_text(self, dictionary):
        if os.path.isfile(self.textbase_path):
            continue_resp = input('\n***WARNING! You are about to overwrite the existing TextBase! \nDo you want to continue?\n-->')
            
            if continue_resp.lower().strip() == 'yes':
                with open(self.textbase_path, 'w') as textfile:
                    for key, value in dictionary.items():
                        textfile.write(f"{key},{value}\n")
                
                fish_logger.log(Fish_Log.WARNING, f"TextBase {self.textbase_name} was OVERWRITTEN with a new dictionary")

        else:
            with open(self.textbase_path, 'w') as textfile:
                for key, value in dictionary.items():
                    textfile.write(f"{key},{value}\n")
                
            fish_logger.log(Fish_Log.Info, f"TextBase {self.textbase_name} was written")


    def read_text_to_dict(self):
        if os.path.isfile(self.textbase_path):
            result_dict = {}
            with open(self.textbase_path, 'r') as textfile:
                for line in textfile:
                    key, value = line.strip().split(',')
                    result_dict[key] = value
            return result_dict

        else:
            fish_logger.log(Fish_Log.LETHAL, f"UNABLE TO FIND TEXT FILE FOR {self.textbase_name} AT PATH {self.textbase_path}")
            print(f'I was not able to find the text file for {self.textbase_name} at path {self.textbase_path}')


    def add_line_to_text(self, dictionary):
        if os.path.isfile(self.textbase_path):
            with open(self.textbase_path, 'a') as textfile:
                for key, value in dictionary.items():
                    textfile.write(f"{key},{value}\n")
            
            fish_logger.log(Fish_Log.INFO, f'TextBase {self.textbase_name} Updated With {{{", ".join(f"{key}: {value}" for key, value in dictionary.items())}}}')
        
        else:
            fish_logger.log(Fish_Log.LETHAL, f"UNABLE TO FIND TEXT FILE FOR {self.textbase_name} AT PATH {self.textbase_path}")
            print(f'I was not able to find the text file for {self.textbase_name} at path {self.textbase_path}')


if __name__ == '__main__':
    treatments = 'TreatmentNames'
    assays = 'AssayNames'
    frame_adjustments = 'FrameAdjustments'

    treatment_dict = {
        'b59393': 'brexpiprazole',
        'b59394' : 'desipramine'
    }

    #treatment_textbase = Information_Textbase(treatments)
    #treatment_textbase.write_dict_to_text(treatment_dict)
    #treatment_textbase.add_line_to_text(treatment_dict)
    
    assay_dict = {
        ' habit_2s5x' : '2.5s Habituation Assay',
        ' gb_5s_habit_120' : '5s Habituation Assay', 
        ' habit_10sx' : '10s Habituation Assay' 
    }

    #assay_textbase = Information_Textbase(assays)
    #assay_textbase.write_dict_to_text(assay_dict)
    #assay_textbase.add_line_to_text(assay_dict)

    frame_adjustments_dict = {
        9117 : 21,
        8840 : 35,
        8855 : 51
    }

    #frame_adjustments_textbase = Information_Textbase(frame_adjustments)
    #frame_adjustments_textbase.write_dict_to_text(frame_adjustments_dict)
    #frame_adjustments_textbase.add_line_to_text(frame_adjustments_dict)

    #print('I ADDED IT TO THE TEXTBASE!')




























if __name__ == '__main__':
    fish_logger.finalize_info()





