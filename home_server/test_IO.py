import Adafruit_BBIO.UART as UART
import serial

UART.setup("UART4")

ser = serial.Serial(port = "/dev/ttyO4", baudrate=115200)
ser.close()
ser.open()
if ser.isOpen():
  while True:
    line = ser.readline()
    if line.startswith("$GPZDA,"):
      print line
ser.close()

