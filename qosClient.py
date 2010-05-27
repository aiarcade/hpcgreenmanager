from compNode import *
import signal


pipe=os.popen("hostname  -i")
ip=pipe.readlines()[0].strip().split(".")
nId=ip[len(ip)-1]
pipe.close()
db=qosDb('172.16.150.252','hpc','hpc','hpcQoS')
cn=compNode(int(nId),db)
i=0

def sigHandler(signum,frame):
	if signum==signal.SIGINT:
		print "killed ,Bye"    
		db.close()
		exit(0)
		


signal.signal(signal.SIGINT,sigHandler)
while(1):
	cn.updateDb()


