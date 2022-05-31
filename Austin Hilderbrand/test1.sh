#!/bin/bash

export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0

#Run two python scripts simultaneously
python3.8 two_windows.py &
python3.8 GUI_practice.py &
