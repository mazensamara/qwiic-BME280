#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_env_bme280_ex1.py
#
# Simple Example for the Qwiic BME280 Device
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, May 2019
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem on a Raspberry Pi (and compatable) single
# board computers. 
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
#==================================================================================
# Copyright (c) 2019 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
#==================================================================================
# Example 1
#
from __future__ import print_function
#from winreg import HKEY_USERS
from rpi_lcd import LCD
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import qwiic_ccs811
import qwiic_bme280
import time
import sys
import smbus
import pigpio
import time
import subprocess
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

lcd = LCD()

# Raspberry Pi pin configuration:
RST = 24

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Load default font.
font = ImageFont.load_default()

# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

lcd = LCD()


def runExample():

    print("\nSparkFun BME280 Sensor  Example 1\n")
    mySensor = qwiic_bme280.QwiicBme280()

    if mySensor.connected == False:
        print("The Qwiic BME280 device isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return

    mySensor.begin()
    myHumidity = round(mySensor.humidity, 2)
    myPressure = round(mySensor.pressure, 2)
    myAltitude_m = round(mySensor.altitude_meters, 2)
    myAltitude_f = round(mySensor.altitude_feet, 2)
    myTemperature = round(mySensor.temperature_celsius, 2)
    
    while True:
         
            print("Humidity:\t%.3f" % mySensor.humidity, " %")
            lcd.text(("Humidity: "+ str(myHumidity) + "%"), 1) # show output on i2c lcd 16x2

            print("Pressure:\t%.3f" % mySensor.pressure, " pa")    

            print("Altitude:\t%.3f" % mySensor.altitude_feet, " f")
        
            print("Altitude:\t%.3f" % mySensor.altitude_meters, " m")

            print("Temperature:\t%.2f" % mySensor.temperature_fahrenheit, " F")  
        
            print("Temperature:\t%.2f" % mySensor.temperature_celsius, " C") 
            lcd.text(("Temp: "+ str(myTemperature) +  " C"), 2)  # show output on i2c lcd 16x2

            # print on graphic screen SSD1306
            draw.text((x, top),        str(" Hum[%d]" % myHumidity +" %"), font=font, fill=255) # line 1
            draw.text((x, top+8),      str(" Press[%d]" % myPressure +" pa"),  font=font, fill=255) # line 2
            draw.text((x, top+16),     str(" Alt[%d]" % myAltitude_m +" m"),  font=font, fill=255) # line 3
            draw.text((x, top+25),     str(" Temp[%d]" % myTemperature +" C"),  font=font, fill=255) # line 4

            # Display image.
            disp.image(image)
            disp.display()
        
            if mySensor.humidity > 65:
                print("It's Humid")
            
            if mySensor.temperature_fahrenheit > 86:
            
                print("It's hot!")   
        
            if mySensor.temperature_celsius > 30:
    
                print("It's hot!")        

            print("")

            time.sleep(3)


if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        lcd.clear() # clear i2c lcd
        disp.clear() # clear display ssd1306
        disp.display()
sys.exit(0)
