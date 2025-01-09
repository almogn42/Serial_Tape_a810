import eel
import serial_console as sercon



# Set web files folder
eel.init('web')


# Set web files folder and optionally specify which file types to check for eel.expose()
#   *Default allowed_extensions are: ['.js', '.html', '.txt', '.htm', '.xhtml']eel.init('web', allowed_extensions=['.js', '.html'])@eel.expose  #This is how you expose the py functions below for javascript.

@eel.expose
def Knob_Perc_SendBack(data):
    knob_input = str(data)
    # pformat the sowing strings
    k_percent, k_id = knob_input.split("|")
    out_str = f"knob: {k_id} | percent {k_percent}"
    print(out_str)
    global knobs_perc
    knobs_perc[k_id] = k_percent
    # return str(data)




# Vals Dicts Declaration
knobs_perc = {"kc1": "", "kc2": "", "kl1": "", "kl2": ""}
print(knobs_perc)
conn = "" # conn variable exists globally from the function connecting_serial


# initiating serial connection to tape
@eel.expose
def connecting_serial(port = "auto"):
    r"""connecting and listing serial ports 
       listing is for the button creation and returns array of dict of every port the dict look like that:
       {"id": "COM14", "description": "COM14 - com0com - serial port emulator CNCA1 (COM14)"}

       after clicked on button the function run again with the button id as argument(port) aka: connecting_serial(port = "COM14")
       and return that connected succesfully to the front

       usage: 
       auto \ return list of serial connection => connecting_serial()
       connect with selected port => connecting_serial(port = "<PortName>")
         """
    # declaring conn as global varible for future refrance
    global conn

    if port == "auto":
        ports = sercon.Serial_connect()
        if type(ports) == list:
            print("there is more than 1 port got ports list")
            return ports
        elif ports == "there is no serial port connectetd":
            return "there is no serial port connectetd"
    # can be deleted stays for now only for roll back perpuse
        # else:
        #     conn = ports
        #     if conn.is_open == True:
        #         # moving to the main page
        #         eel.go_to_page("tape_interface3.html")()
        #         return str(conn)
        
    else:
        try:
            conn = sercon.Serial_connect(port= port)
            if conn.is_open == True:
                # moving to the main page
                eel.go_to_page("tape_interface3.html")()
                return str(conn)
        except FileNotFoundError:
            return "com port is not connected anymore please refrase page using f5"


# initiating a Tape object 
@eel.expose
def Create_Tape_object():
    print(conn.is_open)
    # Creating Tape Object for commands mathoods
    if conn.is_open == True:
        global Tape
        Tape = sercon.Tape_Recorder(conn)
        print("connecting...")
        print("connected")
        print(Tape)
        return Tape

@eel.expose
def Tape_Command(command = "list_commands", command_args = "None"):
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
            com = f"Tape.{command}()"
        else:
            com = f"Tape.{command}({command_args})"
        
        print(com)
        Command_Response = eval(com)
        print(Command_Response)
        return Command_Response
    else: 
        return Tape_Command_Dict

@eel.expose
def Timer_Return():
    return Tape.Generic_command("TM?")

# declaring global conn varible for future refrance
# global conn 

ports = sercon.Serial_connect()
if type(ports) == list:
    eel.start("tape_interface-serial-conn.html", size = (874, 970))             # Eel command for starting app. size is for window sizing    
    # eel.start("tape_interface-serial-conn.html",  mode='custom', cmdline_args=['chrome-win/chrome.exe', '--app=http://localhost:8000/tape_interface-serial-conn.html'], size = (874, 970))             # Eel command for starting app. size is for window sizing    

elif ports == "there is no serial port connectetd":
    eel.start("tape_interface-serial-conn.html", size = (874, 970))             # Eel command for starting app. size is for window sizing    

else:
    conn = ports
    if conn.is_open == True:
        conn = ports
        eel.start("tape_interface3.html", size = (874, 970))             # Eel command for starting app. size is for window sizing



# eel.start("tape_interface3.html", size = (874, 970))             # Eel command for starting app. size is for window sizing
# eel.start("tape_interface-serial-conn.html", size = (1280, 720))             # Eel command for starting app. size is for window sizing
# --app