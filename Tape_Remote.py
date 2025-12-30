import webview
import serial_console as sercon

# for reading existsing classes in the module sercon (one above)
import inspect

# for Logging 
import logging
import os
# for parsing Arguments (for logging)
from app_logger import Logger_c

#  creating local logger
logger = logging.getLogger(__name__)

#  getting path for folder
path = os.getcwd()
# Creating and renaming the methoods from object
log_c = Logger_c(logger, path)
print_info = log_c.print_info
Logging_Decor = log_c.Logging_Decor

# Creating the Argument Parser for File
args = log_c.Create_Parser()

# API class for pywebview
class API:
    def __init__(self):
        self.Tape = None
        self.conn = None
    
    @Logging_Decor
    def connecting_serial(self, port="auto"):
        r"""connecting and listing serial ports 
           listing is for the button creation and returns array of dict of every port the dict look like that:
           {"id": "COM14", "description": "COM14 - com0com - serial port emulator CNCA1 (COM14)"}

           after clicked on button the function run again with the button id as argument(port) aka: connecting_serial(port = "COM14")
           and return that connected succesfully to the front

           usage: 
           auto \ return list of serial connection => connecting_serial()
           connect with selected port => connecting_serial(port = "<PortName>")
             """
        global conn

        if port == "auto":
            ports = sercon.Serial_connect()
            if type(ports) == list:
                print_info("there is more than 1 port got ports list")
                return ports
            elif ports == "there is no serial port connectetd":
                return "there is no serial port connectetd"

        else:
            try:
                conn = sercon.Serial_connect(port=port)
                if conn.is_open == True:
                    self.conn = conn
                    return str(conn)
            except FileNotFoundError as ext:
                logger.error(f'com port is not connected anymore please refrase page using f5', exc_info=True)
                return "com port is not connected anymore please refrase page using f5"

    @Logging_Decor
    def Get_Supported_Tapes(self):
        Cls_List = []
        #  getting the calss list from the module (using fildering with the isClass methood)
        Raw_Cls_List = inspect.getmembers(sercon, inspect.isclass)
        for Cls in Raw_Cls_List:
            Cls = Cls[0]
            if "Tape_Recorder_" in Cls:
                Cls = Cls.replace("_", " ")
                Cls_List.append(Cls)
        
        return Cls_List

    @Logging_Decor
    def Create_Tape_object(self, Mechine):
        print_info(self.conn.is_open)
        # Creating Tape Object for commands mathoods
        if self.conn.is_open == True:
            if Mechine == "A810":
                self.Tape = sercon.Tape_Recorder_A810(self.conn)
            elif Mechine == "A807":
                self.Tape = sercon.Tape_Recorder_A807(self.conn)   
            print_info("connecting...")
            print_info(f"connected - Machine {Mechine}")
            print_info(self.Tape)
            return self.Tape

    @Logging_Decor
    def Tape_Command(self, command="list_commands", command_args="None"):
        Tape_Command_Dict = {"Play": "Plays Tape ",
                             "Stop": "Stops Tape ",
                             "Foreword": "Winds foreword Tape ",
                             "Back": "Rwinds Tape ",
                             "Record": "Record nusc to Tape ",
                             "Timer_Return": "shows the timer current time",    
                             "Get_Ips": "get the ips(inches per second) speed",
                             "LOC" : "Moves the tape to the entered location - takes argument a string of timestamp in secound field",
                             "Set_Timer": r"Set_TimerSet Timer to given time(only time display\ code  not on time on tape) - take argument(exmaple Tape_Command(Set_Timer, args))",
                             "Channel_Ready": "Set Channel State to READY - take argument(exmaple Tape_Command(Channel_Ready, <CHANNEL NUM>)",
                             "Channel_Safe": "Set Channel State to SAFE - take argument(exmaple Tape_Command(Channel_Ready, <CHANNEL NUM>)",
                             "Channel_Input": "Set Channel State to INPUT - take argument(exmaple Tape_Command(Channel_Ready, <CHANNEL NUM>)",
                             "Channel_Sync": "Set Channel State to SYNCE - take argument(exmaple Tape_Command(Channel_Ready, <CHANNEL NUM>)",
                             "Channel_Repro": "Set Channel State to REPRO - take argument(exmaple Tape_Command(Channel_Ready, <CHANNEL NUM>)",
                             "Channel_Mute": "Set Channel State to MUTE - take argument(exmaple Tape_Command(Channel_Ready, <CHANNEL NUM>)",
                             "Channel_Mute_Off": "Set Channel State to MUTE OFF - take argument(exmaple Tape_Command(Channel_Ready, <CHANNEL NUM>)",
                             "Get_Status": "Get the current Tape Status code"
                             }

        if command != "list_commands":
            # setting arguments for command in case it needs it :-)
            if command_args == "None":
                com = f"self.Tape.{command}()"
            else:
                com = f"self.Tape.{command}({command_args})"
            
            print_info(com)
            Command_Response = eval(com)
            print_info(Command_Response)
            return Command_Response
        else: 
            return Tape_Command_Dict

    @Logging_Decor
    def Timer_Return(self):
        return self.Tape.Generic_command("TM?")


# Create API instance
api = API()

# Determine which page to start with and initialize connection
ports = sercon.Serial_connect()
if type(ports) == list:
    start_page = "tape_interface-serial-conn.html"
elif ports == "there is no serial port connectetd":
    start_page = "tape_interface-serial-conn.html"
else:
    api.conn = ports
    if ports.is_open == True:
        start_page = "tape_interface3.html"


# Create and show the pywebview window
window = webview.create_window(
    title='Serial Tape Remote Control',
    url=f'file://{os.path.join(os.path.dirname(__file__), "web", start_page)}',
    width=874,
    height=970,
    resizable=False,
    js_api=api
)

if __name__ == '__main__':
    webview.start(debug=False)