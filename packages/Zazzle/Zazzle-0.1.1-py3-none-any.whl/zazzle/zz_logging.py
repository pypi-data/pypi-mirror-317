import logging
import os
import datetime
import traceback
import sys
import time

class Variables():
    gl_log_name = None
    gl_log_directory = None
    gl_log_format = None
    gl_log_write_method = None
    gl_log_level = None
    gl_function_tracking = False
    gl_function_tracking_style = "curved"
    gl_current_function = None
    gl_current_function_string = 0
    gl_last_message = None

# Setting up global variables
gl_log_directory = Variables.gl_log_directory
gl_log_name = Variables.gl_log_name
gl_log_format = Variables.gl_log_format
gl_log_write_method = Variables.gl_log_write_method
gl_log_level = Variables.gl_log_level
gl_function_tracking = Variables.gl_function_tracking
gl_current_function = Variables.gl_current_function
gl_function_tracking_style = Variables.gl_function_tracking_style
gl_current_function_string = Variables.gl_current_function_string
gl_last_message = Variables.gl_last_message

# ===========================================================================================
# Class Name: ZZ_Init
# Description: Bucket for initialization functions
# Input values: N/A
# Output values: N/A
# ===========================================================================================
class ZZ_Init():
    # ===================================================
    # Function Name: set_log_file_name
    # Description: Sets the global variable 'gl_log_file_name' to the name input by the user.
    # Input values: input_log_file_name(string)
    # Output values: N/A
    # ===================================================
    def set_log_file_name(input_log_file_name):
        log = ZZ_Logging.log

        try:
            global gl_log_file_name
            gl_log_file_name = input_log_file_name

        except:
            log(4, "COULDN'T SET LOG NAME")

    # ===================================================
    # Function Name: set_log_directory
    # Description: Sets the global variable 'gl_log_directory' to the directory input by the user.
    # Input values: input_log_directory(string)
    # Output values: N/A
    # ===================================================
    def set_log_directory(input_log_directory):
        log = ZZ_Logging.log

        try:
            global gl_log_directory
            gl_log_directory = input_log_directory

        except:
            log(4, "COULDN'T SET LOG DIRECTORY")

    # ===================================================
    # Function Name: set_log_format
    # Description: Sets the global variable 'gl_log_format' to the format input by the user.
    # Input values: input_log_directory(string)
    # Output values: N/A
    # ===================================================
    def set_log_format(input_log_format):
        log = ZZ_Logging.log

        try:
            global gl_log_format
            gl_log_format = input_log_format

        except:
            log(4, "COULDN'T SET LOG DIRECTORY")

    # ===================================================
    # Function Name: set_log_file_mode
    # Description: Sets the logging method for the logger (example: appending messages vs. writing a new file)
    # Input values: input_write_method(string)
    # Output values: N/A
    # ===================================================
    def set_log_file_mode(input_file_mode):
        log = ZZ_Logging.log

        try:
            global gl_log_write_method
            gl_log_write_method = input_file_mode

        except:
            log(4, "COULDN'T SET WRITE METHOD")

    # ===================================================
    # Function Name: set_log_level
    # Description: Sets the logging level
    # Input values: input_log_level(int)
    # Output values: N/A
    # ===================================================
    def set_log_level(input_log_level):
        log = ZZ_Logging.log

        try:
            global gl_log_level
            if input_log_level == 0:
                gl_log_level = logging.DEBUG
            elif input_log_level == 1:
                gl_log_level = logging.INFO
            elif input_log_level == 2:
                gl_log_level = logging.WARNING
            elif input_log_level == 3:
                gl_log_level = logging.ERROR
            elif input_log_level == 4:
                gl_log_level = logging.CRITICAL
            else:
                gl_log_level = logging.DEBUG

        except:
            log(4, "COULDN'T SET LOG LEVEL")

    # ===================================================
    # Function Name: set_function_tracking
    # Description: Turns function tracking on or off
    # Input values: input_log_level(int)
    # Output values: N/A
    # ===================================================
    def set_function_tracking(input_function_tracking):
        log = ZZ_Logging.log

        try:
            global gl_function_tracking
            gl_function_tracking = input_function_tracking

        except:
            log(4, "COULDN'T SET FUNCTION TRACKING")

    # ===================================================
    # Function Name: set_function_tracking_style
    # Description: Modifies the function tracking style. Defaults to "curved".
    # Input values: input_log_level(int)
    # Output values: N/A
    # ===================================================
    def set_function_tracking_style(input_function_tracking_style):
        log = ZZ_Logging.log

        try:
            global gl_function_tracking_style
            gl_function_tracking_style = input_function_tracking_style

        except:
            log(4, "COULDN'T SET FUNCTION TRACKING STYLE")

    # ===================================================
    # Function Name: configure_logger
    # Description: Runs the basic configuration for the logger
    # Input values: N/A
    # Output values: N/A
    # ===================================================
    def configure_logger(file_name=None, directory=os.getcwd(), log_format=None, file_mode=None, level=None, function_tracking=False, function_tracking_style="curved"):

        # Run our input parsing functions
        ZZ_Init.set_log_file_name(file_name)
        ZZ_Init.set_log_directory(directory)
        ZZ_Init.set_log_format(log_format)
        ZZ_Init.set_log_file_mode(file_mode)
        ZZ_Init.set_log_level(level)
        ZZ_Init.set_function_tracking(function_tracking)
        ZZ_Init.set_function_tracking_style(function_tracking_style)

        # Configure
        try:
            # Check for a custom directory input
            if gl_log_directory:
                config_path = gl_log_directory
            else:
                user = os.getlogin()
                config_path = f"C:/Users/{user}/Documents/Zazzle"

            # Make the directory if it doesn't exist already
            if os.path.exists(config_path):
                pass
            else:
                os.makedirs(config_path)

            # Check for a custom file name input
            if gl_log_file_name:
                config_name = f"{gl_log_file_name}.log"
            else:
                now = datetime.datetime.now()
                config_name = now.strftime(f"%Y-%m-%d.log")

            file_name = f"{config_path}/{config_name}"

            # Check for a custom internal log format
            if gl_log_format:
                config_format = gl_log_format
            else:
                config_format = "{asctime:s} | {levelname:<8s} | >   {message:s}"

            # Check for a custom log write method
            if gl_log_write_method:
                config_file_mode = gl_log_write_method
            else:
                config_file_mode = "w"

            # Check for a custom log level
            if gl_log_level:
                config_log_level = gl_log_level
            else:
                config_log_level = logging.DEBUG

            # Configure our logs based on user inputs
            logging.basicConfig(filename=file_name, filemode=config_file_mode, format=config_format, style='{', level=config_log_level, force=True)

        except:
            print('COULD NOT CONFIGURE LOGGER')

# ===========================================================================================
# Class Name: ZZ_Files
# Description: Bucket for functions focused on file manipulation.
# Input values: N/A
# Output values: N/A
# ===========================================================================================
class ZZ_Files():
    # ===================================================
    # Function Name: delete_old_log_files
    # Description: Searches for and deletes any old log files detected in the currently set log directory
    # Input values: keep_amount(int)
    # Output values: N/A
    # ===================================================
    def delete_old_log_files(keep_amount=5):
        global gl_log_directory
        global gl_log_file_name
        logs = []
        oldest_file = []
        log = ZZ_Logging.ah_log

        try:
            # Scan the log directory for all files, and isolate any files that end with '.log'
            directory_scan = os.listdir(gl_log_directory)
            for i in directory_scan:
                if ".log" in i:
                    logs.append(i)

            for i in range(len(logs)):
                logs[i] = f"{os.getcwd()}\{logs[i]}"
            full_path = ["{0}".format(x) for x in logs]

            if len(logs) > keep_amount:
                oldest_file.append(min(full_path, key=os.path.getctime))
                os.remove(oldest_file[0])

        except:
            log(4, "UNABLE TO DELETE OLD LOG FILES")

# ===========================================================================================
# Class Name: ZZ_Logging
# Description: Bucket for logging functions
# Input values: N/A
# Output values: N/A
# ===========================================================================================
class ZZ_Logging():
    # ===================================================
    # Function Name: log
    # Description: Takes a log level and a message for the logger. Logs to a file.
    # Input values: input_level(int), log_message(string), flag(bool)
    # Output values: N/A
    # ===================================================
    def log(input_level=0, log_message="I'm an empty log message!", flag=True):
        tracker_prefix = ""
        selected_trackers = []
        trackers = {"curved":["╭", "│", "╰"], "solid":["┏", "┃", "┗"]}
        try:
            # Setup for function tracking prefixes
            if gl_function_tracking:
                # Get global variables
                global gl_current_function
                global gl_current_function_string
                global gl_last_message

                # Get the style of the lines
                if gl_function_tracking_style == "curved":
                    selected_trackers = trackers['curved']
                elif gl_function_tracking_style == "solid":
                    selected_trackers = trackers['solid']
                else:
                    selected_trackers = trackers['curved']

                # Get the current function name that is calling the log
                name = ZZ_Logging.get_func_name(2)
                if name == gl_current_function:
                    gl_current_function_string = 1
                else:
                    # Get setup for the new function
                    gl_current_function = name
                    gl_current_function_string = 0

                    if gl_last_message:
                        reset = ZZ_Colors.reset
                        underline = ""
                        if f"|{'DEBUG':<8s}|" in gl_last_message:
                            color = ZZ_Colors.fg.darkgrey
                        elif f"|{'INFO':<8s}|" in gl_last_message:
                            color = ZZ_Colors.fg.green
                        elif f"|{'WARNING':<8s}|" in gl_last_message:
                            color = ZZ_Colors.fg.yellow
                        elif f"|{'ERROR':<8s}|" in gl_last_message:
                            color = ZZ_Colors.fg.red
                        elif f"|{'CRITICAL':<8s}|" in gl_last_message:
                            color = ZZ_Colors.fg.red
                            underline = ZZ_Colors.underline
                        else:
                            color = ZZ_Colors.fg.darkgrey

                        # Delete and rewrite the last print line to the console
                        LINE_UP = '\033[1A'
                        LINE_CLEAR = '\x1b[2K'
                        print(LINE_UP, end=LINE_CLEAR)
                        redraw = gl_last_message[6:]
                        redraw = f"{color}{underline}{selected_trackers[2]}{redraw}{reset}"
                        print(redraw)

                # Get the string we should use at the front of the log message
                if gl_current_function_string == 0:
                    tracker_prefix = selected_trackers[0]
                    gl_current_function_string = 1
                elif gl_current_function_string == 1:
                    tracker_prefix = selected_trackers[1]
                elif gl_current_function_string == 2:
                    tracker_prefix = selected_trackers[2]
                else:
                    tracker_prefix = selected_trackers[0]

            # Debug
            if input_level == 0:
                # String variables
                color = ZZ_Colors.fg.darkgrey
                reset = ZZ_Colors.reset
                flag_text = f"|{'DEBUG':<8s}|\t"

                # Print the level flag if enabled
                if flag:
                    gl_last_message = f"{color}{tracker_prefix}{flag_text}{log_message}{reset}"
                    print(gl_last_message)
                else:
                    gl_last_message = f"{color}{tracker_prefix}{log_message}{reset}"
                    print(gl_last_message)

                # Write to the log file
                logging.debug(log_message)

            # Info
            elif input_level == 1:
                # String variables
                color = ZZ_Colors.fg.green
                reset = ZZ_Colors.reset
                flag_text = f"|{'INFO':<8s}|\t"

                # Print the level flag if enabled
                if flag:
                    gl_last_message = f"{color}{tracker_prefix}{flag_text}{log_message}{reset}"
                    print(gl_last_message)
                else:
                    gl_last_message = f"{color}{tracker_prefix}{log_message}{reset}"
                    print(gl_last_message)

                # Write to the log file
                logging.info(log_message)

            # Warning
            elif input_level == 2:
                # String variables
                color = ZZ_Colors.fg.yellow
                reset = ZZ_Colors.reset
                flag_text = f"|{'WARNING':<8s}|\t"

                # Print the level flag if enabled
                if flag:
                    gl_last_message = f"{color}{tracker_prefix}{flag_text}{log_message}{reset}"
                    print(gl_last_message)
                else:
                    gl_last_message = f"{color}{tracker_prefix}{log_message}{reset}"
                    print(gl_last_message)

                # Write to the log file
                logging.warning(log_message)

            # Error
            elif input_level == 3:
                # String variables
                color = ZZ_Colors.fg.red
                reset = ZZ_Colors.reset
                flag_text = f"|{'ERROR':<8s}|\t"

                # Print the level flag if enabled
                if flag:
                    gl_last_message = f"{color}{tracker_prefix}{flag_text}{log_message}{reset}"
                    print(gl_last_message)
                else:
                    gl_last_message = f"{color}{tracker_prefix}{log_message}{reset}"
                    print(gl_last_message)

                # Write to the log file
                logging.error(log_message)

            # Critical
            elif input_level == 4:
                # String variables
                color = ZZ_Colors.fg.red
                reset = ZZ_Colors.reset
                underline = ZZ_Colors.underline
                flag_text = f"|{'CRITICAL':<8s}|\t"
                exc = traceback.format_exc()

                # Print the level flag if enabled
                if flag:
                    gl_last_message = f"{color}{underline}{tracker_prefix}{flag_text}{log_message}{reset}"
                    print(gl_last_message)
                else:
                    gl_last_message = f"{color}{underline}{tracker_prefix}{log_message}{reset}"
                    print(gl_last_message)

                print(f"{color}{exc}{reset}")

                # Write to the log file
                logging.exception(log_message)

            # Anything else prints as a debug message
            else:
                color = ZZ_Colors.fg.darkgrey
                reset = ZZ_Colors.reset
                flag_text = f"|{'DEBUG':<8s}|\t"

                if flag:
                    print(f"{ZZ_Colors.fg.darkgrey}{tracker_prefix}{log_message}{ZZ_Colors.reset}")
                    logging.debug(log_message)
                    check = True
                else:
                    print(f"{ZZ_Colors.fg.darkgrey}{tracker_prefix}{flag_text}{log_message}{ZZ_Colors.reset}")
                    logging.debug(log_message)

        # If something goes wrong, get the traceback and log to both the console and the log
        except:
            print(f"{ZZ_Colors.fg.red}{log_message}{ZZ_Colors.reset}")
            exc = traceback.format_exc()
            print(f"{ZZ_Colors.fg.red}{exc}{ZZ_Colors.reset}")
            logging.exception(log_message)

    # ===================================================
    # Function Name: log_wide
    # Description: Logs a string at the specified level, console width, and character.
    # Input values: log_level(int), log_message(string), log_width(int), log_character(string)
    # Output values: N/A
    # ===================================================
    def log_wide(log_level=0, log_message="", log_width=None, log_character="*"):

        # There's definitley a better way to do this

        log = ZZ_Logging.log

        if log_width == None:
            log_width = os.get_terminal_size().columns

        if log_width > 110:
            log_width = 110

        log(log_level, f"{log_message:{log_character}^{log_width}}", False)

    # ===================================================
    # Function Name: get_func_name
    # Description: Returns the name of the function it was run from.
    # Input values: frame(int)
    # Output values: name(string)
    # ===================================================
    def get_func_name(frame=0):
        try:
            name = sys._getframe(frame).f_code.co_name
            return(name)

        except:
            log = ZZ_Logging.log
            log(4, f"CAN'T GET FUNCTION NAME")

# ===========================================================================================
# Class Name: ZZ_Colors
# Description: Bucket for foreground, background, and modifiers for console colors
# Input values: N/A
# Output values: N/A
# ===========================================================================================
class ZZ_Colors():
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

    # ===========================================================================================
    # Class Name: fg
    # Description: Bucket for foreground console colors.
    # Input values: N/A
    # Output values: N/A
    # ===========================================================================================
    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

    # ===========================================================================================
    # Class Name: bg
    # Description: Bucket for background console colors.
    # Input values: N/A
    # Output values: N/A
    # ===========================================================================================
    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'

if __name__ == "__main__":
    #test()
    pass