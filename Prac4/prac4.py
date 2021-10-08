import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import threading
import datetime
import RPi.GPIO as GPIO
import random
import os
import time
import sys
import datetime

#intialise
btn = 23
global Sampling_rate 
Sampling_rate = 1 #intial smapling rate = 1
count = 0 # counts the number of times button is pressed
global intial
runtime = 0 

GPIO.setmode(GPIO.BCM) 

def setup():
     #set up buttons
     global spi
     spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
     global cs
     cs  = digitalio.DigitalInOut(board.D5)
     global mcp
     mcp  = MCP.MCP3008(spi, cs)
     
     global final
     global runtime
     runtime = 0

    # GPIO.setmode(GPIO.BOARD)
     GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
     GPIO.add_event_detect(btn, GPIO.FALLING, callback=callback1, bouncetime=200)
     
     print("%7s %7s %2s %7s %7s %7s" % ("Runtime", "Temp Reading", "V" ,"Temp", "C" ,"Light Reading"))
     global intial
     intial = datetime.datetime.now().second
    

 

def callback1(channel):
      global count 
      global Sampling_rate
      count = count +1
      print("Button pressed")
      if count == 1 : #pressed first time = sampling rate = 5
       Sampling_rate = 5
      elif count == 2 :
       Sampling_rate = 10 #second press sampling rate = 10
      else :
       Sampling_rate = 1
       count =0           #else reset
      print("New Sampling rate :" ,Sampling_rate)
      
def print_time_thread():

    thread = threading.Timer(Sampling_rate, print_time_thread)
    thread.daemon = True  
    
    final = datetime.datetime.now().second
    global intial
    diff = abs(final - intial)
    intial = final
    global runtime
    runtime = runtime + diff

    
    thread.start()

    temp = AnalogIn(mcp, MCP.P1)
    chan = AnalogIn(mcp, MCP.P2)
    degree = round((temp.voltage-0.5)*100,3) #from datasheet
    
    
    print("%7s %7s %7s %7s %7s %7s "  %(str(runtime), str(temp.value), "V" , str(degree) , "C" , str(chan.value)))
    
  
if __name__ == "__main__":
    setup()
    print_time_thread() # call it once to start the thread
    while True:
          pass
if __name__ == "__main__":
    setup()
    print_time_thread() # call it once to start the thread
    while True:
          pass
        