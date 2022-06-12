"""
read_DATAQs.py
My research into reading data from multiple DATAQs simultaneously.
This script will allow the user to connect to an arbitrary number
of DATAQs and read data from them simultaneously.
Author: Austin Hilderbrand
NOTE: A large portion of this code was taken from DI_1100.py
"""

"""
    COPYRIGHT © 2018 BY DATAQ INSTRUMENTS, INC.
!!!!!!!!    VERY IMPORTANT    !!!!!!!!
!!!!!!!!    READ THIS FIRST   !!!!!!!!
This program works only with model DI-1100. 
Disconnect any other instrument models to prevent the program from 
detecting a different device model with a DATAQ Instruments VID and attempting to use it. 
Such attempts will fail.
While the DI-1100's protocol is similar to model DI-2108, it doesn't support
a decimation function. Therefore, its minimum sample rate of ~915 Hz is 
too fast for this program to work properly because of its heavy
use of print statements. The program overcomes that problem 
through use of a 'decimation_factor' variable to slow scan rate to an 
acceptable level. 
The DI-1100 used with this program MUST be placed in its CDC communication mode. 
Follow this link for guidance:
https://www.dataq.com/blog/data-acquisition/usb-daq-products-support-libusb-cdc/
The DI-1100 protocol this program uses can be downloaded from the instrument's 
product page:
https://www.dataq.com/resources/pdfs/misc/di-1100-protocol.pdf
"""
import serial
import serial.tools.list_ports
import keyboard
import time

""" 
Example slist for model DI-1100
0x0000 = Analog channel 0, ±10 V range
0x0001 = Analog channel 1, ±10 V range
0x0002 = Analog channel 2, ±10 V range
0x0003 = Analog channel 3, ±10 V range
"""
slist = [0x0000,0x0001,0x0002,0x0003]

ser_ports = [] # This will hold the serial objects

"""
Since model DI-1100 cannot scan slower that 915 Hz at the protocol level, 
and that rate or higher is not practical for this program, define a decimation 
factor to slow scan rate to a practical level. It defines the number of analog readings to average
before displaying them. By design, digital input values display instantaneously
without averaging at the same rate as decimated analog values.
Averaging n values on each analog channel is more difficult than simply using
every nth value, but is recommended since it reduces noise by a factor of n^0.5 
'decimation_factor' must be an integer value greater than zero. 
'decimation_factor' = 1 disables decimation and attemps to output all values.
"""
# Define a decimation factor variable
# decimation_factor = 1000
decimation_factor = 250

# Contains accumulated values for each analog channel used for the average calculation
# achan_accumulation_table = list(())
achan_accumulation_tables = []

# Define flag to indicate if acquiring is active 
acquiring = False


# ============================================================================
# discovery
# ============================================================================
def discovery():
    """ Discover DATAQ Instruments devices and models.  Note that if multiple devices are connected, only the 
    device discovered first is used. We leave it to you to ensure that it's a DI-1100."""
    # Get a list of active com ports to scan for possible DATAQ Instruments devices
    available_ports = list(serial.tools.list_ports.comports())
    # Will eventually hold the com port of the detected device, if any
    hooked_ports = []
    # hooked_port = "" 
    found_DAQs = []
    for port in available_ports:
        # Do we have a DATAQ Instruments device?
        if ("VID:PID=0683" in port.hwid):
            # Yes!  Dectect and assign the hooked com port
            found_DAQs.append(port)
            # hooked_port = port.device
            # break

    i = 0
    for DAQ in found_DAQs:
        """List found DAQs"""
        i += 1
        print(f"{i}. {DAQ}")
        
    # Select device(s)
    done = False
    while not done:
        # Indiv. device selection
        valid_choice = False
        while not valid_choice:
            try:
                # Select the desired port
                dev = int(input("Select device: ")) - 1
                if dev in range(len(found_DAQs)): valid_choice = True
                else: print("Invalid selection. Please try again.")
            except:
                print("ERROR: Invalid input. Please try again.")
        # print(found_DAQs[dev][0]) # DEBUG
        hooked_ports.append(found_DAQs[dev].device)
        ser_ports.append(serial.Serial()) # New ser obj for this hooked_port
        achan_accumulation_tables.append(list(())) # New achan accum. table
        done = len(hooked_ports) == len(found_DAQs)
        if not done: done = 'n' in input("Read from another device (y/n)? ")

    # Setup serial port connections
    if len(hooked_ports) > 0:
        for ser_port in range(len(hooked_ports)):
            print("Found a DATAQ Instruments device on",hooked_ports[ser_port])
            # print(found_DAQs[dev].hwid)
            # print(found_DAQs[dev].pid)
            found_DAQs[dev].pid += dev
            ser_ports[ser_port].timeout = 0
            ser_ports[ser_port].port = hooked_ports[ser_port]
            ser_ports[ser_port].baudrate = '115200'
            ser_ports[ser_port].open()
        return(True)
    else:
        # Get here if no DATAQ Instruments devices are detected
        print("Please connect a DATAQ Instruments device")
        input("Press ENTER to try again...")
        return(False)


# ============================================================================
# send_cmd
# ============================================================================
def send_cmd(command, ser_port):
    """Sends a passed command string after appending <cr>"""
    ser_ports[ser_port].write((command+'\r').encode())
    time.sleep(.1)
    if not(acquiring):
        # Echo commands if not acquiring
        while True:
            if(ser_ports[ser_port].inWaiting() > 0):
                while True:
                    try:
                        s = ser_ports[ser_port].readline().decode()
                        s = s.strip('\n')
                        s = s.strip('\r')
                        s = s.strip(chr(0))
                        break
                    except:
                        continue
                if s != "":
                    print (s)
                    break


# ============================================================================
# config_scn_lst
# ============================================================================
def config_scn_lst(ser_port):    # Scan list position must start with 0 and increment sequentially
    """Configure the instrument's scan list"""
    position = 0
    for item in slist:
        send_cmd("slist "+ str(position ) + " " + str(item), ser_port)
        # Add the channel to the logical list.
        achan_accumulation_tables[ser_port].append(0)
        position += 1


# ----------------------------------------------------------------------------
# Setup hooked DATAQ units prior to collecting readings
# ----------------------------------------------------------------------------
while discovery() == False:
    discovery()
for ser_port in range(len(ser_ports)):
    # print(ser_ports) # DEBUG
    print(f"Device on: {ser_ports[ser_port].port}")
    # Stop in case DI-1100 is already scanning
    send_cmd("stop", ser_port)
    # Define binary output mode
    send_cmd("encode 0", ser_port)
    # Keep the packet size small for responsiveness
    send_cmd("ps 0", ser_port)
    # Configure the instrument's scan list
    config_scn_lst(ser_port)

    # Define sample rate = 1 Hz, where decimation_factor = 1000:
    # 60,000,000/(srate) = 60,000,000 / 60000 / decimation_factor = 1 Hz
    send_cmd("srate 60000", ser_port)
    print("")
    print("Ready to acquire...")
    print ("")
    # print("Press <g> to go, <s> to stop, and <q> to quit:")

    # This is the slist position pointer. Ranges from 0 (first position)
    # to len(slist)
    slist_pointers = [0] * len(ser_ports)

    # Init a decimation counter:
    dec_counts = [decimation_factor] * len(ser_ports)

    # Init the logical channel number for enabled analog channels
    achan_numbers = [0] * len(ser_ports)

    # This is the constructed output string
    # output_string = ""
    output_strings = [""] * len(ser_ports)

print("Press <g> to go, <s> to stop, and <q> to quit:")


# ----------------------------------------------------------------------------
# This is the main program loop, broken only by typing a command key as 
#   defined
# ----------------------------------------------------------------------------
while True:
    # If key 'G' start scanning
    if keyboard.is_pressed('g' or  'G'):
        keyboard.read_key()
        acquiring = True
        for ser_port in range(len(ser_ports)):
            send_cmd("start", ser_port)
    # If key 'S' stop scanning
    if keyboard.is_pressed('s' or 'S'):
        keyboard.read_key()
        for ser_port in range(len(ser_ports)):
            send_cmd("stop", ser_port)
            time.sleep(1)
            ser_ports[ser_port].flushInput()
            print (f"{ser_ports[ser_port].port} stopped")
        acquiring = False
    # If key 'Q' exit 
    if keyboard.is_pressed('q' or 'Q'):
        keyboard.read_key()
        for ser_port in range(len(ser_ports)):
            send_cmd("stop", ser_port)
            ser_ports[ser_port].flushInput()
            ser_ports[ser_port].close()
        break
    for ser_port in range(len(ser_ports)):
        while (ser_ports[ser_port].inWaiting() > (2 * len(slist))):
            for i in range(len(slist)):
                # Always two bytes per sample...read them
                bytes = ser_ports[ser_port].read(2)
                # Only analog channels for a DI-1100, with dig_in states appearing in the two LSBs of ONLY the first slist position
                result = int.from_bytes(bytes,byteorder='little', signed=True)

                # Since digital input states are embedded into the analog data stream there are four possibilities:
                if (dec_counts[ser_port] == 1) and (slist_pointers[ser_port] == 0):
                    # Decimation loop finished and first slist position
                    # Two LSBs carry information only for first slist posiiton. So, ...
                    # Preserve lower two bits representing digital input states
                    dig_in = result & 0x3
                    # Strip two LSBs from value to be added to the analog channel accumulation, preserving sign
                    result = result >> 2
                    result = result << 2
                    # Add the value to the accumulator
                    achan_accumulation_tables[ser_port][achan_numbers[ser_port]] = result + achan_accumulation_tables[ser_port][achan_numbers[ser_port]]
                    achan_numbers[ser_port] += 1
                    # End of a decimation loop. So, append accumulator value / decimation_factor  to the output string
                    output_strings[ser_port] = output_strings[ser_port] + "{: 3.3f}, ".format(achan_accumulation_tables[ser_port][achan_numbers[ser_port]-1] * 10 / 32768 / decimation_factor)

                elif (dec_counts[ser_port] == 1) and (slist_pointers[ser_port] != 0):
                    # Decimation loop finished and NOT the first slist position
                    # Two LSBs carry information only for first slist posiiton, which this isn't. So, ...
                    # Just add value to the accumulator
                    achan_accumulation_tables[ser_port][achan_numbers[ser_port]] = result + achan_accumulation_tables[ser_port][achan_numbers[ser_port]]
                    achan_numbers[ser_port] += 1
                    # End of a decimation loop. So, append accumulator value / decimation_factor  to the output string
                    output_strings[ser_port] = output_strings[ser_port] + "{: 3.3f}, ".format(achan_accumulation_tables[ser_port][achan_numbers[ser_port]-1] * 10 / 32768 / decimation_factor)

                elif (dec_counts[ser_port] != 1) and (slist_pointers[ser_port] == 0):
                    # Decimation loop NOT finished and first slist position
                    # Not the end of a decimation loop, but this is the first position in slist. So, ...
                    # Just strip two LSBs, preserving sign...
                    result = result >> 2
                    result = result << 2
                    # ...and add the value to the accumulator
                    achan_accumulation_tables[ser_port][achan_numbers[ser_port]] = result + achan_accumulation_tables[ser_port][achan_numbers[ser_port]]
                    achan_numbers[ser_port] += 1
                else:
                    # Decimation loop NOT finished and NOT first slist position
                    # Nothing to do except add the value to the accumlator
                    achan_accumulation_tables[ser_port][achan_numbers[ser_port]] = result + achan_accumulation_tables[ser_port][achan_numbers[ser_port]]
                    achan_numbers[ser_port] += 1

                # Get the next position in slist
                slist_pointers[ser_port] += 1

                if (slist_pointers[ser_port] + 1) > (len(slist)):
                    # End of a pass through slist items
                    if dec_counts[ser_port] == 1:
                        # Get here if decimation loop has finished
                        dec_counts[ser_port] = decimation_factor
                        # Reset analog channel accumulators to zero
                        achan_accumulation_tables[ser_port] = [0] * len(achan_accumulation_tables[ser_port])
                        # Append digital inputs to output string
                        output_strings[ser_port] = output_strings[ser_port] + "{: 3d}, ".format(dig_in)
                        # print(output_strings) # DEBUG
                        print("Device: {}   -   ".format(ser_ports[ser_port].port), end='')
                        # print(output_strings[ser_port].rstrip(", ") + "           ", end="\r")
                        print(output_strings[ser_port].rstrip(", ") + "           ")
                        if ser_port == len(ser_ports) - 1:
                            print()
                        output_strings[ser_port] = ""
                    else:
                        dec_counts[ser_port] -= 1             
                    slist_pointers[ser_port] = 0
                    achan_numbers[ser_port] = 0

# ser_ports[ser_port].close()
SystemExit