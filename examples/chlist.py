#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import numpy as np
import time
#import matplotlib.pyplot as plt
import pyOxygenSCPI
import pyOxygenStream

#%%
# Measurement Device IP Settings
#ip_addr = '127.0.0.1'
ip_addr = '192.168.100.100'
scpi_port = 10001
stream_port = 10005
timeout = 20

# Connect to Measurement Device and setup data stream
print("starting the SCPI")
measurementDevice = pyOxygenSCPI.OxygenSCPI(ip_addr, scpi_port, timeout)
print("connecting to the Oxygen")
if not measurementDevice.connect():
    sys.exit()
print(f"Connected via SCPI to {ip_addr:s}:{scpi_port:d}")
lst = measurementDevice.getChannelList()
# lst = measurementDevice.getChannelListDict()
measurementDevice.disconnect()
print("Disconnected from SCPI")
print(lst)