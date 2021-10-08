import busio
import digitalio
import board
import threading 
import time
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

def setup():
   # create the spi bus
   spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

   # create the cs (chip select)
   cs = digitalio.DigitalInOut(board.D5)

   # create the mcp object
   mcp = MCP.MCP3008(spi, cs)

   # create an analog input channel on pin 0
   global chan
   chan = AnalogIn(mcp, MCP.P0)

def print_out():
   tTime = 0
   for i in range(5): 
      print(int(tTime))
      print("Raw ADC Value: ", chan.value)
      print("ADC Voltage: " + str(chan.voltage) + "V")
      startTime = time.time()
      time.sleep(2)
      endTime = time.time()
      tTime = tTime + endTime - startTime


if __name__ == "__main__":
   setup()
   print("RunTimeTemp     Reading     Temp     LightReading")
   t = threading.Thread(target = print_out) 
   t.daemon = True
   t.start()

