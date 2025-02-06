import serial
from serial.tools.list_ports import comports
from time import sleep
# # logging imports
import logging
from app_logger import Logger_c

#  creating local logger
logger = logging.getLogger(__name__)

# Creating and renaming the methoods from object
log_c = Logger_c(logger)
print_info = log_c.print_info
Logging_Decor = log_c.Logging_Decor



@Logging_Decor 
def  Serial_connect(port = "auto", baudrate = 9600):
    """ a Function to find the serial port and connect \ intial communication with serial device
        if known a port ahed it can be provided and the function will only connect 
        Usage: Serial_connect(), 
        Serial_connect(port= <str: portname>, baudrate = <int: baudrate>) """


    
    # getting the relevant port dynemiclly
    ports = list(comports())
    serial_ports = []
    
    # setting operations between specific port and finding automaticlly    
    if port != "auto":
        # getting the port object to continue running 
        for temp_port in ports:
            if temp_port.device == port:
                port = temp_port
        if type(port) == str:
            try:
                raise FileNotFoundError(f"entered port ({port}) does not exist")
            except Exception as ext:
                logger.error(f'{ext}', exc_info=True)
                
        serial_ports = [port]
    
    elif port == "auto":
        # going throgh them checking if them serial
        for port in ports:
            if(("SERIAL" in port.description.upper()) or ("SERIAL" in port.device.upper())):
                serial_ports.append(port)



    # exiting / defining port
    if len(serial_ports) > 1:
        # print_info("there is more than one serial device connected - line 61")
        
        # logging debug data
        logger.debug(f"{serial_ports}")
        # print(f"{serial_ports}")

        serial_ports_dict = []
        for port in serial_ports:
            serial_ports_dict.append({"id": port.device, "description": str(port)})
        
        logger.debug(f"port list dictionery - {serial_ports_dict}")
        return serial_ports_dict
    
    # Actually Connecting
    elif len(serial_ports) != 0:
        port = serial_ports[0].device
        print_info(f"found serial port: {port}")
        conn = serial.Serial(port, baudrate = baudrate)
        return conn
    
    else:
        print_info("there is no serial port connectetd")
        port = ""
        return "there is no serial port connectetd"

@Logging_Decor
def Serial_Terminal(conn):
    # make sure that it gets a serial connection object by checking class
    if type(conn) == serial.serialwin32.Serial :

        # terminal loop 
        command = ""
        while command != "q":

            # getting input and serial writing
            command = input("please enter command **** q will exit terminal: \n")      

            #exit condition
            if command == "q":
                break
            
            # \r for the enter press needed for the tape to read the commant (end simb)
            conn.write((command + "\r").encode("utf-8"))
            sleep(1.2)
            # for clearity
            print()

            # reading full response loop 
            while conn.in_waiting > 0:
                response = conn.read_until(size = conn.in_waiting).decode().strip()
                print_info(response)
            print()

        conn.reset_input_buffer()

    
class Tape_Recorder:
    @Logging_Decor
    def __init__(self, conn ):
        self.serial = conn
        self.serial.port = conn.port
        self.serial.baudrate = conn.baudrate

    @Logging_Decor
    def Generic_command(self, command):
        """the Tape Serial Command Process Function 
            Written so that i dont need to copy paste a bunch
            Usage: self.Generic_command(<serial command code>) """
        
        conn = self.serial

        if type(conn) != str:
            
            # sending command
            conn.write((command + "\r\n").encode("utf-8"))
            sleep(0.1)
            total_respone = ""
            # for clearity
            print()
            logger.info(f"Command is - {command}")

            # initiating a pacehoder in case there is no response at all  (remnant of testing)
            response = "--"
            # reading full response loop 
            while conn.in_waiting > 0:
                response = conn.read_until(size = conn.in_waiting).decode().strip()
                print_info(response)
                total_respone += response
            print()
            print_info("End Command")
            conn.reset_input_buffer()
            return total_respone

    @Logging_Decor
    def Stop(self):
        """Stops Tape """
         # sopported only on all (27n 807 810 812 820 816)

        comm = self.Generic_command("STP")
        return comm
    
    @Logging_Decor
    def Back(self):
        """Rwinds Tape """
        # sopported only on all (27n 807 810 812 820 816)

        comm = self.Generic_command("RWD")
        return comm 

    @Logging_Decor
    def Foreword(self):
        """Winds foreword Tape """
        # sopported only on all (27n 807 810 812 820 816)

        comm = self.Generic_command("FWD")
        return comm
    
    @Logging_Decor
    def Play(self):
        """Plays Tape """
        # sopported only on all (27n 807 810 812 820 816)

        comm = self.Generic_command("PLY")
        return comm
    
    @Logging_Decor
    def Record(self):
        """Record nusc to Tape """
        # sopported only on all (27n 807 810 812 820 816)

        comm = self.Generic_command("REC")
        return comm

    @Logging_Decor
    def Set_varispeed(self):   
        """Set Varispeed mode"""
        # sopported only on 27n 810 812 820 816

        comm = self.Generic_command("SVS")
        return comm

    @Logging_Decor
    def Clear_varispeed(self):   
        """Clear Varispeed mode"""
        # sopported only on 27n 810 812 820 816

        comm = self.Generic_command("CVS")
        return comm
    
    @Logging_Decor
    def Channel_Ready(self, args):   
        """Set Channel State to READY (like the buttons near the Channel Volume state)"""
        # sopported only on 27n 807 810 812 820 816  - For 2 channels (because of front {read documentation})

        comm = self.Generic_command(f"REA {args}")
        return comm

    @Logging_Decor
    def Channel_Safe(self, args):   
        """Set Channel State to SAFE (like the buttons near the Channel Volume state)"""
        # sopported only on 27n 807 810 812 820 816  - For 2 channels (because of front {read documentation})

        comm = self.Generic_command(f"SAF {args}")
        return comm

    @Logging_Decor
    def Channel_Input(self, args):   
        """Set Channel State to INPUT (like the buttons near the Channel Volume state)"""
        # sopported only on 27n 807 810 812 820 816  - For 2 channels (because of front {read documentation})

        comm = self.Generic_command(f"INP {args}")
        return comm

    @Logging_Decor
    def Channel_Sync(self, args):   
        """Set Channel State to SYNCE (like the buttons near the Channel Volume state)"""
        # sopported only on 27n 807 810 812 820 816  - For 2 channels (because of front {read documentation})

        comm = self.Generic_command(f"SYN {args}")
        return comm

    @Logging_Decor
    def Channel_Repro(self, args):   
        """Set Channel State to REPRO (like the buttons near the Channel Volume state)"""
        # sopported only on 27n 807 810 812 820 816  - For 2 channels (because of front {read documentation})

        comm = self.Generic_command(f"REP {args}")
        return comm

class Tape_Recorder_A810(Tape_Recorder):
    
    @Logging_Decor
    def __init__(self, conn ):
        Tape_Recorder.__init__(self, conn)
    
    @Logging_Decor
    def Tape_Load(self):
        """Tesion loosley threded tape ("tape load") """
        # sopported only on 810

        comm = self.Generic_command("TPL")
        return comm
    
    @Logging_Decor
    def Higher_capsen(self):
        """Set Higher capstan Speed"""
        # sopported only on 810 27n

        comm = self.Generic_command("SHS")
        return comm
    
    @Logging_Decor
    def Lower_capsen(self):
        """Set Lower capstan Speed"""
         # sopported only on 810 27n

        comm = self.Generic_command("SLS")
        return comm

    @Logging_Decor
    def Mono(self):
        """Set Mono\Stereo switch to mono"""
        # sopported only on 810 812 820 816

        comm = self.Generic_command("SMN")
        return comm
    
    @Logging_Decor
    def Stereo(self):
        """Set Mono\Stereo switch to stereo"""
        # sopported only on 810 812 820 816

        comm = self.Generic_command("SST")
        return comm

    @Logging_Decor
    def EQ_nab(self):   
        """Set equalizer to NAB"""
        # sopported only on 807 810 812 820 816

        comm = self.Generic_command("SNB")
        return comm

    @Logging_Decor
    def EQ_ccir(self):   
        """Set equalizer to CCIR"""
        # sopported only on 807 810 812 820 816

        comm = self.Generic_command("SCR")
        return comm

    @Logging_Decor
    def Set_rehearsal(self):   
        """Set rehearsal mod"""
        # sopported only on 807 810 812 820 816

        comm = self.Generic_command("SRH")
        return comm

    @Logging_Decor
    def Clear_rehearsal(self):   
        """Set rehearsal mode"""
        # sopported only on 807 810 812 820 816

        comm = self.Generic_command("CRH")
        return comm    
    
    @Logging_Decor
    def Time_c_delay_on(self):   
        """Set Time code delay on"""
        # sopported only on 810 812 820

        comm = self.Generic_command("TDN")
        return comm

    @Logging_Decor
    def Time_c_delay_off(self):   
        """Set Time code delay off (bypassed)"""
        # sopported only on 810 812 820

        comm = self.Generic_command("TDF")
        return comm

    @Logging_Decor
    def LOC(self, args):
        """Moves the tape to the entered location  old func name <Go_To_location>"""
        # sopported only on 807 810 with the current formating (look documentation)
        # sopported currently only on 810 because of Tape_Status that return number instead 
        # of state and managed on the from end (Logic_Classes-> Loc_Button-> Tape_Loc-> Tape_Loc_Response_stat)

        comm = self.Generic_command(f"LOC {args}")
        return comm
    
    @Logging_Decor
    def Set_Timer(self, args):   
        """Set Timer to given time(only time display\ code  not on time on tape)"""
        # sopported only on 27n 807 810 - because of timestamp format

        comm = self.Generic_command(f"STM {args}")
        return comm
    
    @Logging_Decor
    def Channel_Mute(self, args):   
        """Set Channel State to MUTE (like the buttons near the Channel Volume state)"""
        # sopported only on 807 810 812 820 816  - For 2 channels (because of front {read documentation})

        comm = self.Generic_command(f"MTN {args}")
        return comm
    
    @Logging_Decor
    def Channel_Mute_Off(self, args):   
        """Set Channel State to MUTE OFF (like the buttons near the Channel Volume state)"""
        # sopported only on 807 810 812 820 816  - For 2 channels (because of front {read documentation})

        comm = self.Generic_command(f"MTF {args}")
        return comm
    
    @Logging_Decor
    def Get_Ips(self):   
        """get the ips(inches per second) speed """
        # sopported only on 807 810 - because of the return speed code format (read documentation)

        # written in upper case only to indicate it is a const
        TIME_DICT = {"00":"3.75", "01":"7.5", "02":"15", "03":"30" }

        comm = self.Generic_command("NS?")
        #  for clearing the output string
        comm = comm.replace("NS?", "")
        comm = comm.replace("\r", "").strip()
        comm = comm.replace(">", "").strip()
        if comm != "":
            return TIME_DICT[comm]
        else:
            return "Did not Get Answer from Tape Please make sure that you are cnnected \ the Tape is turned on \n press F5 on windows or command+R on mac to retry"
    
    @Logging_Decor
    def Get_Status(self):   
        """Get The tape Cirrent Status code"""
        # sopported only on 807 cause this is a mess with status code compatability :-(

        # the mighty Status Dictionary (made to make the programe more Tape Dynamic so that the front will get textual status
        # instead of the direct status code which will enable front agnosticity (agnosticyty? i dont know.. dear reader i belive you will survive that))
        status_dict = {
            "00" : "tape out",
            "02" : "tape dump",
            "82" : "tape dump achieved",
            "03" : "rewind",
            "83" : "rewind achieved",
            "04" : "stop",
            "84" : "stop achieved",
            "05" : "play",
            "85" : "play achieved",
            "06" : "rewind achieved",
            "08" : "forward",
            "88" : "forward achieved",
            "0A" : "play",
            "8A" : "play achieved",
            "0C" : "record",
            "8C" : "record achieved",
            "10" : "locate wind",
            "12" : "locate play",
            "42" : "locate rewind",
            "C2" : "locate rewind achieved",
            "43" : "locate forward",
            "C3" : "locate forward achieved",
            "4A" : "rewind controlled",
            "CA" : "rewind controlled achieved",
            "4B" : "wind forward controlled",
            "CB" : "wind forward controlled achieved",
            "59" : "tape dump",
            "D9" : "tape dump achieved"
            }

        comm = self.Generic_command(f"ST?")
        # clening output
        comm = comm.replace("\r", "").replace("\n", "").replace(">","").replace("ST?","")
        print_info(status_dict[comm])

        return status_dict[comm]      
    
    @Logging_Decor
    def Timer_Return(self):
        """A methood to return the timer data from the machine"""
        # sopported only on 27n 807 810 because the rimestemp format


        
        comm = self.Generic_command("TM?")
        comm = comm.replace("TM?", "")
        comm = comm.replace("\r", "")
        comm = comm.replace(">", "").strip()

        #  getting the same time as on screen because the display rounds the secounds basde on the percent of the last secound 
        time, sec_part = (comm.split(","))
        houers, minutes, sec = time.split(":")

        # the percent of the sewcound were in is sent as hexodecimal (16 bit data) value that needed to be translated to decimal (int represention data) 
        # deviding by 256 as said to do in the ascii commands guide  i... i donno ¯\_(ツ)_/¯
        sec_part = int(sec_part,16) / 256

        # actual rounding
        if sec_part > 0.55:
            sec = int(sec) +1
            if sec < 10:
                sec = f"0{sec}"
        timestamp = f"{houers}:{minutes}:{sec}"

        print_info(f"Time is - {timestamp}")
        return timestamp
    
class Tape_Recorder_A807(Tape_Recorder):
    
    @Logging_Decor
    def __init__(self, conn ):
        Tape_Recorder.__init__(self, conn)
    
    @Logging_Decor
    def Mono(self):
        """Set Mono\Stereo switch to mono   ( from docs: Insert on (set mono))"""
        # sopported only on 807

        comm = self.Generic_command("ION")
        return comm
    
    @Logging_Decor
    def Stereo(self):
        """Set Mono\Stereo switch to stereo  (from docs: Insert off (set stereo))"""
        # sopported only on 807

        comm = self.Generic_command("IOF")
        return comm

    @Logging_Decor
    def EQ_nab(self):   
        """Set equalizer to NAB"""
        # sopported only on 807 810 812 820 816

        comm = self.Generic_command("SNB")
        return comm

    @Logging_Decor
    def EQ_ccir(self):   
        """Set equalizer to CCIR"""
        # sopported only on 807 810 812 820 816

        comm = self.Generic_command("SCR")
        return comm

    @Logging_Decor
    def Set_rehearsal(self):   
        """Set rehearsal mod"""
        # sopported only on 807 810 812 820 816

        comm = self.Generic_command("SRH")
        return comm

    @Logging_Decor
    def Clear_rehearsal(self):   
        """Set rehearsal mode"""
        # sopported only on 807 810 812 820 816

        comm = self.Generic_command("CRH")
        return comm    
    
    @Logging_Decor
    def Time_c_delay_on(self):   
        """Set Time code delay on - 807 vriante? (from docs: Set time code delay active)"""
        # sopported only on 807

        comm = self.Generic_command("TCN")
        return comm

    @Logging_Decor
    def Time_c_delay_off(self):   
        """Set Time code delay off (bypassed) (from docs: Set time code delay bypassed)"""
        # sopported only on 807

        comm = self.Generic_command("TCF")
        return comm

    @Logging_Decor
    def LOC(self, args):
        """Moves the tape to the entered location  old func name <Go_To_location>"""
        # sopported only on 807 810 with the current formating (look documentation)

        comm = self.Generic_command(f"LOC {args}")
        return comm
    
    @Logging_Decor
    def Set_Timer(self, args):   
        """Set Timer to given time(only time display\ code  not on time on tape)"""
        # sopported only on 27n 807 810 - because of timestamp format

        comm = self.Generic_command(f"STM {args}")
        return comm

    @Logging_Decor
    def Channel_Mute(self, args):   
        """Set Channel State to MUTE (like the buttons near the Channel Volume state)"""
        # sopported only on 807 810 812 820 816  - For first 2 channels only (because of frontEnd {read documentation})

        comm = self.Generic_command(f"MTN {args}")
        return comm

    @Logging_Decor
    def Channel_Mute_Off(self, args):   
        """Set Channel State to MUTE OFF (like the buttons near the Channel Volume state)"""
        # sopported only on 807 810 812 820 816  - For first 2 channels only (because of frontEnd {read documentation})

        comm = self.Generic_command(f"MTF {args}")
        return comm
    
    @Logging_Decor
    def Get_Ips(self):   
        """get the ips(inches per second) speed """
        # sopported only on 807 810 - because of the return speed code format (read documentation)

        # written in upper case only to indicate it is a const
        TIME_DICT = {"00":"3.75", "01":"7.5", "02":"15", "03":"30" }

        comm = self.Generic_command("NS?")
        #  for clearing the output string
        comm = comm.replace("NS?", "")
        comm = comm.replace("\r", "").strip()
        comm = comm.replace(">", "").strip()
        if comm != "":
            return TIME_DICT[comm]
        else:
            return "Did not Get Answer from Tape Please make sure that you are cnnected \ the Tape is turned on \n press F5 on windows or command+R on mac to retry"
    
    @Logging_Decor
    def Get_Status(self):   
        """Get The tape Cirrent Status code"""
        # sopported only on 807 cause this is a mess with status code compatability :-(

        # the mighty Status Dictionary (made to make the programe more Tape Dynamic so that the front will get textual status
        # instead of the direct status code which will enable front agnosticity (agnosticyty? i dont know.. dear reader i belive you will survive that))
        status_dict = {
            "01" : "tape out",
            "81" : "tape out achieved",
            "02" : "stop",
            "82" : "stop achieved",
            "03" : "rewind",
            "83" : "rewind achieved",
            "04" : "forward",
            "84" : "forward achieved",
            "05" : "play",
            "85" : "play achieved",
            "86" : "play vari achieved",
            "08" : "play ext ref",
            "88" : "play ext ref achieved",
            "09" : "rec or rehearse rec",
            "89" : "rec/rehearse rec achieved",
            "25" : "reverse play",
            "A5" : "reverse play achieved",
            "40" : "shuttle reverse",
            "C0" : "shuttle reverse achieved",
            "41" : "shuttle forward",
            "C1" : "shuttle forward achieved",
            "42" : "locate wind", # the Original status meaning is  "locate rewind"   which is the same as locate wind just to a specific direction
                                  # changed for noramlaized status with the Front-End                        
            "C2" : "locate rewind achieved",
            "43" : "locate wind", # the Original status meaning is "locate forward" which is the same as locate wind just to a specific direction
                                  # changed for noramlaized status with the Front-End
            "C3" : "locate forward achieved",
            "4A" : "rewind controlled",
            "CA" : "rewind controlled achieved",
            "4B" : "wind forward controlled",
            "CB" : "wind forward controlled achieved",
            "59" : "tape dump",
            "D9" : "tape dump achieved",
            
            }

        comm = self.Generic_command(f"ST?")
        # clening output
        comm = comm.replace("\r", "").replace("\n", "").replace(">","").replace("ST?","")
        print_info(status_dict[comm])

        return status_dict[comm]      
    
    @Logging_Decor
    def Timer_Return(self):
        """A methood to return the timer data from the machine"""
        # sopported only on 27n 807 810 because the rimestemp format


        
        comm = self.Generic_command("TM?")
        comm = comm.replace("TM?", "")
        comm = comm.replace("\r", "")
        comm = comm.replace(">", "").strip()

        #  getting the same time as on screen because the display rounds the secounds basde on the percent of the last secound 
        time, sec_part = (comm.split(","))
        houers, minutes, sec = time.split(":")

        # the percent of the sewcound were in is sent as hexodecimal (16 bit data) value that needed to be translated to decimal (int represention data) 
        # deviding by 256 as said to do in the ascii commands guide  i... i donno ¯\_(ツ)_/¯
        sec_part = int(sec_part,16) / 256

        # actual rounding
        if sec_part > 0.55:
            sec = int(sec) +1
            if sec < 10:
                sec = f"0{sec}"
        timestamp = f"{houers}:{minutes}:{sec}"

        print(f"Time is - {timestamp}")
        # comm.replace("TM? \r", "")
        return timestamp
 

if __name__== "__main__":
    pass


# CTRL - X Command 

# \x18


# conn.write(("\x18").encode("utf-8"))