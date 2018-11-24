import os
import sys

os.system("crontab -l > mycron")
cmd = " /usr/sbin/ssmtp "
cmd2 = "0 0 \* \* "+sys.argv[2]
cmdemail = sys.argv[1] + " \< \~/msg.txt"
  

 # returns the exit code in unix




#echo new cron into cron file
os.system("echo "+cmd2+cmd+cmdemail+" >> mycron")
#install new cron file
returned_value = os.system("crontab mycron")
os.system("rm mycron")
print('returned value:', returned_value)
