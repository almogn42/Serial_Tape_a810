import serial
from serial.tools.list_ports import comports
from time import sleep



def Serial_connect(port = "auto", baudrate = 9600):
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
            raise FileNotFoundError("entered port does not exist")
        serial_ports = [port]
    
    elif port == "auto":
        # going throgh them checking if them serial
        for port in ports:
            if(("SERIAL" in port.description.upper()) or ("SERIAL" in port.device.upper())):
                serial_ports.append(port)



    # exiting / defining port
    if len(serial_ports) > 1:
        print("there is more than one serial device connected")
        # print(f"{serial_ports}")
        serial_ports_dict = []
        for port in serial_ports:
            serial_ports_dict.append({"id": port.device, "description": str(port)})
        return serial_ports_dict
    
    # Actually Connecting
    elif len(serial_ports) != 0:
        port = serial_ports[0].device
        print(f"found serial port: {port}")
        conn = serial.Serial(port, baudrate = baudrate)
        return conn
    
    else:
        print("there is no serial port connectetd")
        port = ""
        return "there is no serial port connectetd"

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
                print(response)
            print()

        conn.reset_input_buffer()

class Tape_Recorder:
    def __init__(self, conn ):
        self.serial = conn
        self.serial.port = conn.port
        self.serial.baudrate = conn.baudrate

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

            # initiating a pacehoder in case there is no response at all  (remnant of testing)
            response = "--"
            # reading full response loop 
            while conn.in_waiting > 0:
                response = conn.read_until(size = conn.in_waiting).decode().strip()
                print(response)
                total_respone += response
            print()
            print("End Command")
            conn.reset_input_buffer()
            return total_respone

    def Stop(self):
        """Stops Tape """

        comm = self.Generic_command("STP")
        return comm
    
    def Back(self):
        """Rwinds Tape """

        comm = self.Generic_command("RWD")
        return comm 

    def Foreword(self):
        """Winds foreword Tape """

        comm = self.Generic_command("FWD")
        return comm

    def Play(self):
        """Plays Tape """

        comm = self.Generic_command("PLY")
        return comm
    
    def Record(self):
        """Record nusc to Tape """

        comm = self.Generic_command("REC")
        return comm
    
    def Tape_Load(self):
        """Tesion loosley threded tape ("tape load") """

        comm = self.Generic_command("TPL")
        return comm

    def Higher_capsen(self):
        """Set Higher capstan Speed"""

        comm = self.Generic_command("SHS")
        return comm
    
    def Lower_capsen(self):
        """Set Lower capstan Speed"""

        comm = self.Generic_command("SLS")
        return comm

    def Mono(self):
        """Set Mono\Stereo switch to mono"""

        comm = self.Generic_command("SMN")
        return comm
    
    def Stereo(self):
        """Set Mono\Stereo switch to stereo"""

        comm = self.Generic_command("SST")
        return comm

    def EQ_nab(self):   
        """Set equalizer to NAB"""

        comm = self.Generic_command("SNB")
        return comm

    def EQ_ccir(self):   
        """Set equalizer to CCIR"""

        comm = self.Generic_command("SCR")
        return comm

    def Set_varispeed(self):   
        """Set Varispeed mode"""

        comm = self.Generic_command("SVS")
        return comm
    
    def Clear_varispeed(self):   
        """Clear Varispeed mode"""

        comm = self.Generic_command("CVS")
        return comm
    
    def Set_rehearsal(self):   
        """Set rehearsal mod"""

        comm = self.Generic_command("SRH")
        return comm

    def Clear_rehearsal(self):   
        """Set rehearsal mod"""

        comm = self.Generic_command("CRH")
        return comm    
    
    def Time_c_delay_on(self):   
        """Set Time code delay on"""

        comm = self.Generic_command("TDN")
        return comm

    def Time_c_delay_off(self):   
        """Set Time code delay off (bypassed)"""

        comm = self.Generic_command("TDF")
        return comm
    
    # def LOC(self, args):
    #     """Moves the tape to the entered location  old func name <Go_To_location>"""

    #     comm = self.Generic_command(f"LOC {args}")
    #     # wind_status = self.Generic_command("ST?")
    #     for t in range(10000000000000000000):
    #         wind_status = self.Generic_command("ST?")
    #         wind_status.replace("\r", "").replace("\n", "")
    #         print(wind_status)
    #         sleep(0.6)
    #         if  wind_status != "10":
    #             print( f"ended Output -> {wind_status}")
    #             return wind_status
    #         else:
    #             print(f"in winding to LOC  Tape Output -> {wind_status}")
    #         sleep(0.8)
    #     return comm

    def LOC(self, args):
        """Moves the tape to the entered location  old func name <Go_To_location>"""

        comm = self.Generic_command(f"LOC {args}")
        return comm
    
    def Set_Timer(self, args):   
        """Set Timer to given time(only time display\ code  not on time on tape)"""

        comm = self.Generic_command(f"STM {args}")
        return comm

    def Channel_Ready(self, args):   
        """Set Channel State to READY (like the buttons near the Channel Volume state)"""

        comm = self.Generic_command(f"REA {args}")
        return comm

    def Channel_Safe(self, args):   
        """Set Channel State to SAFE (like the buttons near the Channel Volume state)"""

        comm = self.Generic_command(f"SAF {args}")
        return comm

    def Channel_Input(self, args):   
        """Set Channel State to INPUT (like the buttons near the Channel Volume state)"""

        comm = self.Generic_command(f"INP {args}")
        return comm

    def Channel_Sync(self, args):   
        """Set Channel State to SYNCE (like the buttons near the Channel Volume state)"""

        comm = self.Generic_command(f"SYN {args}")
        return comm

    def Channel_Repro(self, args):   
        """Set Channel State to REPRO (like the buttons near the Channel Volume state)"""

        comm = self.Generic_command(f"REP {args}")
        return comm

    def Channel_Mute(self, args):   
        """Set Channel State to MUTE (like the buttons near the Channel Volume state)"""

        comm = self.Generic_command(f"MTN {args}")
        return comm

    def Channel_Mute_Off(self, args):   
        """Set Channel State to MUTE OFF (like the buttons near the Channel Volume state)"""

        comm = self.Generic_command(f"MTF {args}")
        return comm
    
    def Get_Ips(self):   
        """get the ips(inches per second) speed """
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

    def Get_Status(self):   
        """Get The tape Cirrent Status code"""

        comm = self.Generic_command(f"ST?")
        # clening output
        comm = comm.replace("\r", "").replace("\n", "").replace(">","").replace("ST?","")

        return comm       

    def timer(self):   
        """A methood to return the timer data from the machine"""

        comm = self.Generic_command("TM?")
        print(f"tests{comm}")
        return comm

    def Timer_Return(self):
        """A methood to return the timer data from the machine"""
        # print("object_meth")
        comm = self.Generic_command("TM?")
        comm = comm.replace("TM?", "")
        comm = comm.replace("\r", "")
        comm = comm.replace(">", "").strip()
        # if (comm.split(","))[1] > 50:
            # comm = int((comm.split(","))[0]) +1
        # else:
        #  getting the same time as on screen becouse the display rounds the secounds basde on the percent of the last secound 
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

        print(timestamp)
        # comm.replace("TM? \r", "")
        return timestamp
    

if __name__== "__main__":
    pass
    # initating connection
    # conn = Serial_connect()
    # print(conn.is_open)
    # Creating Tape Object for commands mathoods
    # if conn.is_open == True:
    #     Tape = Tape_Recorder(conn)
    #     print("connecting...")
    #     for t in range(4):
    #         sleep(0.5)
    #         print(".")
    #     print("stop")
    #     Tape.Stop()
    #     print("Back")
    #     Tape.Back()
    #     print("Foreword")
    #     Tape.Foreword()
    #     print("Play")
    #     Tape.Play()
    #     print("Clear_rehearsal")
    #     Tape.Clear_rehearsal()
    #     print("Clear_varispeed")
    #     Tape.Clear_varispeed()
    #     print("EQ_ccir")
    #     Tape.EQ_ccir()
    #     print("EQ_nab")
    #     Tape.EQ_nab()
    #     print("Higher_capsen")
    #     Tape.Higher_capsen()
    #     print("Lower_capsen")
    #     Tape.Lower_capsen()
    #     print("Mono")
    #     Tape.Mono()
    #     print("Stereo")
    #     Tape.Stereo()

    # opening terminal
    # Serial_Terminal(conn)









# CTRL - X Command 

# \x18


# conn.write(("\x18").encode("utf-8"))