import os
import glob
import inspect
from datetime import datetime


# % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % 
# HELLO, this is FishLog                          #
# # this file is for logging! please see below    #
# % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ %




class Fish_Log():
    # % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ %
    # HELLO, this is the class Fish_Log               #
    # # the main purpose of this class is to log info #
    # # # about how the script is being run to a log  #
    # # # file in SauronResources                     #
    # # this class is structured to be instantiated   #
    # # # once per file and the log function is used  #
    # # # to append log inforamtion to class          #
    # # # attributes which are used to make the log   #
    # # # file when the program is closing            #
    # # there are no inputs nor init function for the #
    # # # class                                       #
    # # the output of the class is a log file         #
    # # # containing information "logged" by the log  #
    # # # function                                    #
    # # the class is instantianted in nearly every    #
    # # # file and at critical points, info is logged #
    # % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ %

    LOG_STATUS = True 
    # Can be set to False to turn off logging
    # # turning off logging will increase performance (probably not by a lot) 

    save_directory = 'SauronResources/LogFiles'
    file_extension = '.log'

    INFO = 0 # working information of the script 
    WARNING = 1 # there is a problem (lightly defined) but the script is designed to handle it
    ERROR = 2 # there is a problem and functionality has been disabled to circumvent the issue
    LETHAL = 3 # there is a problem that caused the script to unexpectedly exit from error

    STATUS_KEY = {
        0 : 'INFO',
        1 : 'WARNING',
        2 : 'ERROR',
        3 : 'LETHAL'
    }
    
    LOG_LIST = []

    CURRENT_STATUS = 0


    def log(self, status, log_str):
        if Fish_Log.LOG_STATUS:
            call_class = inspect.currentframe().f_back.f_locals.get('self', None).__class__.__name__
            call_funct = inspect.currentframe().f_back.f_code.co_name
            
            call_file_full_path = inspect.currentframe().f_back.f_globals['__file__']
            fish_spectacles_dir = os.path.join(os.path.dirname(os.path.abspath(call_file_full_path)), 'Fish_Spectacles')
            call_file_rel_path = os.path.relpath(call_file_full_path, fish_spectacles_dir)
            call_file_rel_path = call_file_rel_path.replace('..', '')[1:]

            call_location = f"CALL_FILE : {call_file_rel_path}, CALL_CLASS : {call_class}, CALL_FUNCTION : {call_funct}"

            if Fish_Log.CURRENT_STATUS < status:
                Fish_Log.CURRENT_STATUS = status

            Fish_Log.LOG_LIST.append(f"[{Fish_Log.STATUS_KEY[status]}] {call_location} :: {log_str}")


    def make_filename(self):
        return f"{datetime.now().strftime('%Y%m%d_%H%M')}_FISHLOG_{Fish_Log.STATUS_KEY[Fish_Log.CURRENT_STATUS]}"


    def check_directory(self):
        os.makedirs(Fish_Log.save_directory, exist_ok=True)


    def finalize_info(self):
        self.check_directory()
        log_filename = self.make_filename()
        log_file_path = f"{Fish_Log.save_directory}/{log_filename}{Fish_Log.file_extension}"
        
        with open(log_file_path, 'w') as log_file:
            for LOG in Fish_Log.LOG_LIST:
                log_file.write(f"{LOG}\n")


    def cleanup_log_file(self):
        n_log_files_to_keep = 50
        filelist = glob.glob(os.path.join(Fish_Log.save_directory, '*.log'))

        if len(filelist) > n_log_files_to_keep:
            print('Cleaning Log Directory ...')
            filelist.sort(key=lambda x: os.path.getctime(x))
            files_to_delete = len(filelist) - n_log_files_to_keep
            for i in range(files_to_delete):
                os.remove(filelist[i])



if __name__ == '__main__':
    fish_logger = Fish_Log()

    #fish_logger.cleanup_log_file()
    
    





































