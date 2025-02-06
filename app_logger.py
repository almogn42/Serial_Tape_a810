# for Logging 
import logging
# for parsing Arguments (for logging)
import argparse
# for retainig function metatdata
from functools import wraps
#  for creating  log folder
import os
# for front logging
from eel import expose


##########################
#     Logging logic      #
##########################

class Logger_c:
    def __init__(self, logger, path=None):
        self.logger = logger
        # self.path = path

        # making sure there is a folder
        if path != None:
            self.Create_Log_Folder(path)
    
    def print_info(self, *args, **kargs):
        """A function to print to console and log to file istead of 2 lines every time"""
        print(*args, **kargs)
        self.logger.info(*args)

    def Logging_Decor(self, func):
        """Decorator for adding writing to log when untrited exceptions happends in the function"""

        # the inner function get the values of the function that the decorator wrapping
        # that in way it takes all the kinds and amount of arguments using *args and **kargs
        # works by taking the function as a paramenter (that works couse everithing in python is an object and you can take objects as arguments)
        # and running the function inside another function and return the data 
    
        # adding the wraps so if youll get help on the function it will give the wrapped function and not the wrapper
        @wraps(func)
        def Logging_Wrapper(*args, **kargs):
            try:
                
                return func(*args,**kargs)
            
            except Exception as ext:
                    self.logger.error(f'{ext}', exc_info=True)
                    raise
        return Logging_Wrapper

    def Create_Parser(self):
        """ 
        Create a Parser Setting and starting it 
        returns: arguments value
        usage: Create_Parser
        """
            
        Program_Description  = (
        """
        A program to remotely control Studer tape machines.
        Originally created for the Studer A810, 
        the program works by sending RS232 commands to the tape machine to manipulate it.
        """)

        parser = argparse.ArgumentParser(
                            prog='Serial_Tape_A810+',
                            description= Program_Description,
                            # epilog='this is a fine help message ?',
                            formatter_class=argparse.RawTextHelpFormatter
                            )

        # parser.add_argument('filename')           # positional argument
        parser.add_argument('-l', '--log',
                            choices= ["critical", "error", "warning", "info", "debug"],
                            metavar="<Log Level>",
                            help= "Enable logging to a log file. Expected values:\n"
                                "\t - critical\n"
                                "\t - error\n"
                                "\t - warning\n"
                                "\t - info\n"
                                "\t - debug"
                            )
        args = parser.parse_args()
        
        # Starting the Base Logger
        self.Create_Base_Logger(args.log)

        return args

    def Create_Base_Logger(self, args):
        """
        A function to create a Main logger and initiating logging 
        """

        Logging_Level_dict = {"critical": logging.CRITICAL,
                            "error": logging.ERROR, 
                            "warning": logging.WARNING, 
                            "info": logging.INFO, 
                            "debug": logging.DEBUG,
                            None : logging.CRITICAL
                            }


        #  setting Loging basic definition
        logger = logging.getLogger(__name__)
        logging.basicConfig(
            filename="./log/app.log",
            encoding="utf-8",
            filemode="a",
            format="{asctime} - {name} - {levelname} => {message}",
            style="{",
            datefmt="%Y-%m-%d %H:%M",
            level=Logging_Level_dict[args]
            # level= logging.DEBUG
        )

    def Create_Log_Folder(self, path):

        path = path.replace('"', '')
        # Specify the absolute path for the directory
        specific_path = rf"{path}/log"

        # Create the directory
        try:
            os.mkdir(specific_path)
            print(f"Directory '{specific_path}' created successfully.")
        except FileExistsError:
            print(f"Directory '{specific_path}' already exists.")
        except PermissionError:
            print(f"Permission denied: Unable to create '{specific_path}'.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def Front_Log(self, message, fname, level="info"):
        # Creating Dediceted Logger File for the front end logging
        logger = logging.getLogger("Front_Logger")

        # clearing the default handler
        logger.handlers.clear()

        # Disable propagation to prevent duplicate log entries
        logger.propagate = False

        Logging_Level_dict = {"critical": logging.CRITICAL,
                            "error": logging.ERROR, 
                            "warning": logging.WARNING, 
                            "info": logging.INFO, 
                            "debug": logging.DEBUG,
                            None : logging.CRITICAL
                            }

        level = Logging_Level_dict[level]
        # print(self.logger)
        
        # Create a temporary handler (can be FileHandler too)
        temp_handler = logging.FileHandler("./log/app.log")  
        temp_format = logging.Formatter("{asctime} - FrontEnd.{fname} - {levelname} => {message}",
                                         style="{", 
                                         datefmt="%Y-%m-%d %H:%M")
        temp_handler.setFormatter(temp_format)
        
        logger.addHandler(temp_handler)  # Attach the handler
        # Log message with new format
        # using the argument extra you can add keyvalue pairs to the logRecord(Logger Dictionary)
        logger.log(level, message, extra={"fname":fname})  
        logger.removeHandler(temp_handler)  # Remove the handler after logging