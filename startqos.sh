!#/bin/bash

#insert sensor   modules
modprobe  coretemp
modprobe  w83627ehf
modprobe ipmi_si
modprobe ipmi_devintf
modprobe ipmi_watchdog

python /home/qos/qosClient.py >>/var/log/dmcclog &




