# Serial Tape A810+
A Studer A8xx series software controller via serial connection

![Tape visuals](https://github.com/almogn42/Serial_Tape_a810/blob/0daa5080887f1152cf56e86e43fd5f4645f5d4b0/tape_visuals.png)

## App Instructions

This App sends serial commands via USB to your Studer tape machine. for this to work you'll need to source out a USB-Serial converter. 
Please note you'll need a converter with an actual active chip that translates the commands, not just a wire to wire converter.

1. Connect your Studer A8xx tape to a USB port on your computer using the USB-Serial converter.
2. Launch the App.
3. Upon startup, the app will look for serial connections, as that's where it's expecting to see your tape. If you have more than one it'll open up all the current serial connections for you to choose from. If you're not sure which port is it you can either just try the one that seems most plausible until you find the correct one or you can unplug your USB connections until you find the right one. Usually the name of the port will give you a hint as to what it does :-)
4. Once the app is up and running, it'll ask the tape for it's current status (Location, IPS), and will set it to SAFE.

Let's go over some added features as the most common ones (PLAY, STOP etc.) are pretty obvious:
- Quick Loc: This will add a location at whatever timestamp the tape location counter is showing right now. This also works while playing, recording or winding. Very useful for tracklisting, saving locations in a song on the go while playing for punch-ins later, etc. The location names are editable and deletable, and clicking on them will wind the tape to the selected location.
- Add Loc: this will add a location button to the list at whatever location is displayed at the *Add Loc* loaction counter.  This is used to manually add locations independent of the tape location counter. Please note: the app's digital counter can ONLY accept full timestamps. For Example: [-06:00:05], [08:59:42], [00:00:00].
- Set Timer: sets your *machine's* timer to whatever value you insert at the app's digital counter. If no timestamp is inserted it'll set the machine to 00:00:00. Useful for when you've finished a part of a reel you don't want to record over; just set the machine's timer to zero after you've finished recording that part and start working from there with no worry of accidently overdubbing important material.
- Link CH: enables you to link channel status changes. Upon startup channels are not linked.


**Please note:**

**This script was written for the Studer A810 machine family.
PLAY, STOP, FF, REWIND, REC, INPUT status and SAFE status *should* also work on Studer 27x, 807, 812 and 820. 
Location coding is a bit different for some of the machine families so YMMV.
Please consult the added documantation here on a full list of all available commands your machine can read - you're welcome to edit the code and add/revise it as you need!**


## Download & Executables
**Requirements**
  -  Chrome browser


### Links
MacOS (M1-3):
https://github.com/almogn42/Serial_Tape_a810/releases/download/windows2/Studer.Serial.A810+_MacOS.zip

Windows:
 -  Folder: https://github.com/almogn42/Serial_Tape_a810/releases/download/windows2/windows-x64-Serial-Tape-a810+-Faster-load-time.zip
     *   The file can only run from within the source code folder, so our recommendation is to create a shortcut and place it in an easy to reach location
 -  Single file Version - https://github.com/almogn42/Serial_Tape_a810/releases/download/windows2/windows-Serial-Tape-a810+.exe
     *  The single file version is slower as it downloads the neccassery protocols every time it runs, use this only if you're patient ;-)

## Runnig the Script

**Requirements**
  - Python3
  - Chrome browser
  - **Libraries:**
    - eel
    - pyserial

## Module's Installation Commands \ Instructions

***These instructions refer to a script written in python3, so please note that every time the word python is mentioned we're talking about python3. Make adjustments according to whatever version or OS you're working on.**

*eel*
```
python -m pip install eel
```

*pyserial*
```
python -m pip install pyserial
```

**using the requirement**
```
python -m pip install -r ./requerments.txt
```


This app was designed for internal purposes at Rafsoda Studios and we're now offering it to the public, please use with caution - by using this software you assume all responsibility.

This work is a labor of love for the analog domain and the beautiful technology that is Tape recording. We have put time and effort into this, and if you find this app useful or if you find value in our work please kindly conside buying us a coffee, we'd highly appreciate it:
https://buymeacoffee.com/kvothe42

Have fun!
