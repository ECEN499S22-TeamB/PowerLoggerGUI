"""
device_disc.py
My research into how python ID's and selects DATAQ's
Austin Hilderbrand
NOTE: Most of this code taken from DI_1100.py
"""

import serial
import serial.tools.list_ports
import keyboard
import time

""" Discover DATAQ Instruments devices and models.  Note that if multiple devices are connected, only the 
device discovered first is used. We leave it to you to ensure that it's a DI-1100."""
def discovery():
    # Get a list of active com ports to scan for possible DATAQ Instruments devices
    available_ports = list(serial.tools.list_ports.comports())
    # Will eventually hold the com port of the detected device, if any
    hooked_port = "" 
    for p in available_ports:
        # Do we have a DATAQ Instruments device?
        if ("VID:PID=0683" in p.hwid):
            # Yes!  Dectect and assign the hooked com port
            hooked_port = p.device
            break

    if hooked_port:
        print("Found a DATAQ Instruments device on",hooked_port)
        ser.timeout = 0
        ser.port = hooked_port
        ser.baudrate = '115200'
        ser.open()
        return(True)
    else:
        # Get here if no DATAQ Instruments devices are detected
        print("Please connect a DATAQ Instruments device")
        input("Press ENTER to try again...")
        return(False)