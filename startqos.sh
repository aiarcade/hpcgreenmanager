!#/bin/bash
# This code is released under GPL v3.So feel free to modify and distribute.
#Author:Mahesh C
#Release date:27-may-2010
#insert sensor   modules
modprobe  coretemp
modprobe  w83627ehf
modprobe ipmi_si
modprobe ipmi_devintf
modprobe ipmi_watchdog

#start client
python /home/qos/qosClient.py >>/var/log/dmcclog &




