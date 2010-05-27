# This code is released under GPL v3.So feel free to modify and distribute.
#Author:Mahesh C
#Release date:27-may-2010



from compNode import *
import signal

#Find ip and set the node identification
pipe=os.popen("hostname  -i")
ip=pipe.readlines()[0].strip().split(".")
nId=ip[len(ip)-1]
pipe.close()
db=qosDb('172.16.150.252','hpc','hpc','hpcQoS')
cn=compNode(int(nId),db)

#Close db and exit
def sigHandler(signum,frame):
	if signum==signal.SIGINT:
		print "killed ,Bye"    
		db.close()
		exit(0)
		


signal.signal(signal.SIGINT,sigHandler)

#Loop forever
while(1):
	cn.updateDb()


