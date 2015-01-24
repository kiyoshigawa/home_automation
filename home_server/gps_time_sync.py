import Adafruit_BBIO.UART as UART
import serial
import time
import pytz
from tzlocal import get_localzone
from datetime import datetime, timedelta
import subprocess
import os

leap_seconds = 16 #change this when a leap second happens

local_tz = get_localzone()

UART.setup("UART4")

last_run = 0 #this is for now reading the hwclock command too often. It'll only check and compare times every 10 seconds or so.
total_updates = 0 #This keeps track of the total number of times the hwclock has been off enough to update since the program started.

ser = serial.Serial(port = "/dev/ttyO4", baudrate=115200)
ser.close()
ser.open()
if ser.isOpen():
  while True:
    line = ser.readline()
    if line.startswith("$GPZDA,"):
      #string of format "$GPZDA,181826.000,18,01,2015,00,00*5C"
      year=line[24:28]
      month=line[21:23]
      day=line[18:20]
      hour=line[7:9]
      min=line[9:11]
      sec=line[11:13]
      #The GPS defaults to 2006 when it doesn't have a lock on at least one sattelite, this should keep it from resetting time improperly
      if ( int(year) >= 2015 ) and ( last_run >= 10 ):
        #print("%s/%s/%s %s:%s:%s" % (year, month, day, hour, min, sec))
        #Now we need to convert from the gps to UTC by subtracting the leap seconds. The system will fix time zone differences
        current_gps_time = datetime(int(year), int(month), int(day), int(hour), int(min), int(sec))
        #print("GPS: ",current_gps_time)
        current_UTC_time = current_gps_time - timedelta(seconds=leap_seconds)
        utc_timestamp = ((current_UTC_time - datetime(1970, 1, 1)).total_seconds())
        #convert UTC time into local time:
        current_local_time = current_UTC_time.replace(tzinfo=pytz.utc).astimezone(local_tz)
        lt = local_tz.normalize(current_local_time)
        #print("UTC: ",current_UTC_time)
        date_str = ("%04d-%02d-%02d %02d:%02d:%02d" % (lt.year, lt.month, lt.day, lt.hour, lt.minute, lt.second))
        #print date_strA

        #this reads the current system clock so we'll only update if we're more than a couple seconds off from the normal UTC time
        hwtime_str = subprocess.check_output('hwclock', shell=False)
        hwtime_str = hwtime_str[0:24]
        hwtime_struct = time.strptime(hwtime_str)
        hwtime = datetime(hwtime_struct.tm_year, hwtime_struct.tm_mon, hwtime_struct.tm_mday, hwtime_struct.tm_hour, hwtime_struct.tm_min, hwtime_struct.tm_sec)

        #this is the actual time setting command:
        set_cmd = 'hwclock --set --date \"%s\"' % date_str
        copy_to_date_cmd = 'hwclock --hctosys'
        #the first if fixed hwclock if it's off by more than 5 seconds, reset hwclock
        utc_secs = time.mktime(lt.timetuple())
        hwtime_secs = time.mktime(hwtime.timetuple())
        if (abs( utc_secs - hwtime_secs ) > 5):
          os.system(set_cmd)
          os.system(copy_to_date_cmd)
          total_updates = total_updates+1
          print("%s Time has updated %d times." % (date_str,total_updates))
        last_run = 0
      last_run = last_run+1
ser.close()
