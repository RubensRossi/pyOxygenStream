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
measurementDevice.getChannelList()
# Configure Data Stream
measurementDevice.DataStream.reset()
items = [
#"AI 1/1 IEPE-U-01"  ,
"Lat_Latitude",
"Lon_Longitude",
"TmpInnen_XR 0/0",
"TmpAussen_XR 0/1",
"GPSTime_GPSSeconds",
"GPSTime_GPSWeek",
"Height_TimeStamp",
"Height_Height",
"SpeedTrack_TrackGround",
"SpeedTrack_SpeedHor",
"AccLatLon_AccelLong",
"AccLatLon_AccelLat",
"AccVert_AccelVert",
#"Latitude_GPS 0/1"  ,
#"Longitude_GPS 0/1" ,
#"Altitude_GPS 0/1"  ,
#"Velocity_GPS 0/1"  ,
#"Date_GPS 0/1"      ,
 ]
measurementDevice.DataStream.setItems(items)
chlist = measurementDevice.DataStream.ChannelList
print("DST Items Set:", chlist)
if len(items) != len(chlist):
    print("some channels were not found!", len(items), len(chlist))
measurementDevice.DataStream.setTcpPort(stream_port)
measurementDevice.DataStream.init()

# Create Stream Receiver Instance
dt_stream = pyOxygenStream.OxygenStreamReceiver()
if not dt_stream.connectTo(ip_addr, stream_port):
    sys.exit()
print(f"Connected via DST to {ip_addr:s}:{stream_port:d}")

# Create Data Container and start stream
data = {}
for chName in measurementDevice.DataStream.ChannelList:
    data[chName] = []
measurementDevice.DataStream.start()
print("Stream Started!")

start_time = time.time()
# Set Time to Stream here in Seconds
time_to_stream = 10

last_logged_time = start_time
pkg_count = 0

# This is the Main Loop!
# Read Data via data stream interface for time_to_stream seconds
while time.time() < (start_time + time_to_stream):
    try:
        data_pkg, timestamps = dt_stream.readPacket()
        if len(timestamps) > 1:
            t = timestamps
        else:
            t = np.zeros(1)


        print([len(x) for x in data_pkg], t[0], np.all(t == np.ones(len(t)) * t[0]))
    except:
        print("Error Reading Data:", sys.exc_info())
        try:
            print("Stream State:", measurementDevice.DataStream.getState()) # TODO terminate this function after 2 seconds
        except:
            sys.exit("Aborted due to error")
        sys.exit("Aborted due to error")
    # Non-Empty Data Packet - unpack data for each channel
    if data_pkg:
        pkg_count+=1
        # Iterate over each Channel in the channel list
        for idx, chName in enumerate(measurementDevice.DataStream.ChannelList):
            # Only append data, if available for the specific channel
            if data_pkg[idx].size > 0:
                data[chName].append(data_pkg[idx])
            # Do additional things here for live processing of received data
    
    # Log Number of received packages every second
    if time.time() > (last_logged_time + 1):
        print(f"Streaming... {pkg_count:d} packages rceived")
        last_logged_time = time.time()
        
# Stop Streaming
measurementDevice.DataStream.stop()
print("Stream stopping...")

# Empty the TCP Queue and disconnect stream port
while dt_stream.packet_info.stream_status != 2:
    data_pkg = dt_stream.readPacket()
    print("Stream emptying queue...")
print("Stream Stopped")

dt_stream.disconnect()
print("Disconnected from DST")

# Concat Data
print("Following Channels Received with Shape:")
for chName, val in data.items():
    print(chName, ":", np.concatenate(val).shape)
    data[chName] = np.concatenate(val)

# Disconnect SCPI Connection
measurementDevice.disconnect()
print("Disconnected from SCPI")

# Print Data
#print(data["Lat_Latitude"]) #), min(data["AI 1/1 IEPE-U-01"]), max(data["AI 1/1 IEPE-U-01"]))
#print(data["Lon_Longitude"]) #, min(data["AI 1/2 IEPE-U-02"]), max(data["AI 1/2 IEPE-U-02"]))
#print(data["TmpInnen_XR 0/0"])
print(data)
