#This is a simple python script to send times to a nixie clock. Set the server IP and Port, and it should work with the arduino on the other end via an ESP8266.

srv = "192.168.2.17"
prt = 80

import sys
import time
import telnetlib

lead_str = "XXAZAZAZXX"
end_str = "XXZAZAZAXX\r\n"
time_str = "00.00.00"

#print("Sending times to clock indefinitely...");

while True:
  old_time_str = time_str
  time_str = time.strftime("%I.%M.%S")
  if(old_time_str != time_str):
    tn = telnetlib.Telnet(srv,prt)
    tn.write(lead_str.encode('ascii')+time_str.encode('ascii')+end_str.encode('ascii'))
    tn.close()
    #print(time_str);
  time.sleep(0.01);
