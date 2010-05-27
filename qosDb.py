import MySQLdb


class qosDb():
	def __init__(self,server,uname,passwd,db):
		self.conn = MySQLdb.connect(host=server,user=uname,passwd=passwd,db=db)
		self.cursor = self.conn.cursor()
	def close(self):
		self.conn.close()	
	def checkNodeExists(self,nId):
		self.cursor.execute("SELECT *  FROM qosMain where nId="+str(nId))
		if self.cursor.rowcount==0:
			return 0
		else:
			return 1
			
	def addNode(self,nId,nDetails):
				
		self.cursor.execute("insert into qosMain values("+str(nId)+",'"+nDetails[0]+"','"+nDetails[1]+"','"+nDetails[2]+"','"+nDetails[3]+"','"+nDetails[4]+"')")
	
		self.cursor.execute("commit;")	
	
	def updateNode(self,nId,nDetails):
		
		self.cursor.execute("update  qosMain set powerUsage='"+nDetails[0]+"',memUsage='"+nDetails[1]+"',nwSRUsage='"+nDetails[2]+"',status='"+nDetails[3]+"',performance='"+nDetails[4]+"' where nId="+str(nId))
		self.cursor.execute("commit;")


	def addCpus(self,nId,cDetails):
		self.cursor.execute("insert into nodeCpus values("+str(nId)+",'"+cDetails[0]+"','"+cDetails[1]+"','"+cDetails[2]+"','"+cDetails[3]+"','"+cDetails[4]+"','"+cDetails[5]+"','"+cDetails[6]+"','"+cDetails[7]+"')")
		self.cursor.execute("commit;")
	
	def updateCpus(self,nId,cDetails):
		self.cursor.execute("update  nodeCpus set cpuName='"+cDetails[1]+"',cpuTemp='"+cDetails[2]+"',cpuLoad='"+cDetails[3]+"',cpuSpeed='"+cDetails[4]+"',cpuType='"+cDetails[5]+"',cpuCache='"+cDetails[6]+"',cpuState='"+cDetails[7]+"' where nId="+str(nId)+" and cId='"+cDetails[0]+"'")
		self.cursor.execute("commit;")
	def addFans(self,nId,fDetails):
		self.cursor.execute("insert into nodeFans values("+str(nId)+",'"+fDetails[0]+"','"+fDetails[1]+"','"+fDetails[2]+"','"+fDetails[3]+"')")
		self.cursor.execute("commit;")		
	def updateFans(self,nId,fDetails):
		self.cursor.execute("update  nodeFans set fanName='"+fDetails[1]+"',fanSpeed='"+fDetails[2]+"',state='"+fDetails[3]+"' where nId="+str(nId)+" and fId='"+fDetails[0]+"'")
		self.cursor.execute("commit;")





	

