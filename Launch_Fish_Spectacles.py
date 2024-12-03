import os
import sys
import traceback

import FishHead
from FishLog import Fish_Log
from TextColors import Text_Colors


# % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % ^ % 
# HELLO, this file is for starting the            #
# # the Fish_Spectacles script and any errors not #
# # already caught by the script are caught here  #
# # such that the error can be logged and python  #
# # can run the garbage collector / return memory # 
# % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ % ~ %


fish_logger = Fish_Log()


try:
    FishHead.Fish_Face()

except Exception as e:
    error_type = type(e).__name__
    error_str = str(e)
    traceback_info = traceback.extract_tb(sys.exc_info()[2])[-1]
    file_path, line_number, func_name, code_line = traceback_info

    fish_spectacles_dir = os.path.join(os.path.dirname(os.path.abspath(file_path)), 'Fish_Spectacles')
    file_name = os.path.relpath(file_path, fish_spectacles_dir)
    file_name = file_name.replace('..', '')[1:]

    fish_logger.log(Fish_Log.LETHAL, f"EXCEPTION {error_type} : {error_str}, CALL_FILE {file_name}, CALL_FUNCTION {func_name}, LINE {line_number}, CODE {code_line}")

    FishHead.Fish_Face.unexpected_error_message()

finally:
    fish_logger.finalize_info()
    print(f'{Text_Colors.DEFAULT}')




























