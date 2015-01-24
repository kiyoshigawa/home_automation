#This file will be setup with crontab to run every 5-10 minutes and check if my scripts are runing.
#It's using pgrep to search for the strings, and if it doesn't find any, it will start them.
#Since the scripts all need GPIO access, it has to be run as root.

import os
import subprocess

#Start by naming the scripts you want to check for / cmd to run if they are off

procs = [
  ('nixie_time.py','python /home/tim/home_automation/home_server/nixie_time.py &'),
  ('gps_time_sync.py','python /home/tim/home_automation/home_server/gps_time_sync.py &')
]

#use pgrep to set flags if they are not on.
def check_proc(str):
  "This uses subprocess and pgrep to check if a process is runing that matches str, and if it does, returns true."
  try:
    pgrep_out = subprocess.check_output(['pgrep','-f',str])
  except subprocess.CalledProcessError as e:
    return False
  else:
    return True

#iterate through procs and check if processes are running. If not, restart them with their command
for proc in procs:
  print proc[0]
  if(check_proc(proc[0]) == True):
    print("%s is runing."%proc[0]);
    #do nothing
  else:
    print("%s is not runing."%proc[0]);
    #restart the process with the command in the array above
    os.system(proc[1])
