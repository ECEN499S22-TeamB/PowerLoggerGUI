"""
USB_HWID.py
My research into USB connection and HWID device info
Austin Hilderbrand
NOTE: pyusb tutorial --> https://github.com/pyusb/pyusb/blob/master/docs/tutorial.rst
"""

#!/usr/bin/python
import sys
import usb.core
# find USB devices
dev = usb.core.find(find_all=True)
# loop through devices, printing vendor and product ids in decimal and hex
for cfg in dev:
  sys.stdout.write('Decimal VendorID=' + str(cfg.idVendor) + ' & ProductID=' + str(cfg.idProduct) + '\n')
  sys.stdout.write('Hexadecimal VendorID=' + hex(cfg.idVendor) + ' & ProductID=' + hex(cfg.idProduct) + '\n\n')