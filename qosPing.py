import MySQLdb
import os
import signal
conn = MySQLdb.connect(host="172.16.150.252",user="hpc",passwd="hpc",db="hpcQoS")
cursor = conn.cursor()
def sigHandler(signum,frame):
	if signum==signal.SIGINT:
		print "killed ,Bye"    
		conn.close()
		exit(0)

signal.signal(signal.SIGINT,sigHandler)
while(1):
	cursor.execute ("SELECT distinct  nId from qosMain")
	status=[]
	while (1):
		row = cursor.fetchone ()
		if row == None:
			break
		ipBase="172.16.150."
		ipBase=ipBase+str(row[0])
		pipe=os.popen("ping -c 1 "+ipBase+"| grep '64 bytes'")
		try :
			ping=pipe.readlines()[0]
			if ping.find("64 bytes")>-1:
				print ipBase,"alive"
				status.append([row[0],'ON'])
			
		except:
			print ipBase,"down"
			status.append([row[0],'OFF'])
				
		
		pipe.close()	
		
	for i in status:
		cursor.execute("update qosMain set status='"+i[1]+"' where nId="+str(i[0]))
		cursor.execute("commit")

conn.close()


