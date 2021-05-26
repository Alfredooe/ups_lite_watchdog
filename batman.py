#!/usr/bin/env python
import struct
import smbus
import sys
import time
import RPi.GPIO as GPIO
import syslog
import os

def readVoltage(bus):
        address = 0x36
        read = bus.read_word_data(address, 0X02)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        voltage = swapped * 1.25 /1000/16
        return voltage


def readCapacity(bus):
        address = 0x36
        read = bus.read_word_data(address, 0X04)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        capacity = swapped/256
        return capacity


def QuickStart(bus):
        address = 0x36
        bus.write_word_data(address, 0x06,0x4000)
      

def PowerOnReset(bus):
        address = 0x36
        bus.write_word_data(address, 0xfe,0x0054)
       	   
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4,GPIO.IN)
	   
bus = smbus.SMBus(1)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
syslog.syslog("Batman Staring.")
PowerOnReset(bus)
QuickStart(bus)
time.sleep(5)
syslog.syslog("Batman Started.")

while True:

 voltage = round(readVoltage(bus), 2)

 capacity = round(readCapacity(bus), 2)
 		
 # if (GPIO.input(4) == GPIO.HIGH):
        
        # charging = True
		
 # if (GPIO.input(4) == GPIO.LOW):
 
        # charging = False
        
 if capacity < 15:

        syslog.syslog(syslog.LOG_EMERG, "LOW POWER ALERT, SHUTTING DOWN.")
        os.system("sudo shutdown now -h")
		
 syslog.syslog(f"Voltage: {voltage}V Capacity: {capacity}%")
 time.sleep(60)
