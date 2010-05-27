import sys
import time
import os
from qosDb import *
import platform

TIMEFORMAT = "%m/%d/%y %H:%M:%S"
INTERVAL = 2

class compNode():
	
	def __init__(self,nodeId,dbObject):
		self.nId=nodeId
		self.db=dbObject
		self.cpuNumber=[]
		self.cpuName=[]
		self.cpuSpeed=[]
		self.cpuCache=[]
		self.cpuLoad=[]
		self.cpuTemp=[]
		self.cpuState=[]
		self.cpuType=platform.machine()
		self.nwUsage=""
		self.memUsage="0/1"
		self.powUsage="0"
		self.flops="0"
		self.fanName=[]
		self.fanSpeed=[]
		self.fanNumber=[]

	def findMemInfo(self):
		fp=open("/proc/meminfo","r")
		memTotal=fp.readline().split(":")[1].replace(" ","").split("k")[0]
        	memFree=fp.readline().split(":")[1].replace(" ","").split("k")[0]
		self.memUsage=memFree+"/"+memTotal
		fp.close()
	def findnwUsage(self):
		sndBytes="0"
		rcvBytes="0"
		self.nwUsage=""
		fp=open("/proc/net/dev","r")
		for i in fp.readlines():
    			i=i.strip()
    			if i.find("eth")>-1:
				i=i[5:].split()        	        	
				rcvBytes=i[0]
        	        	sndBytes=i[8]
				self.nwUsage=self.nwUsage+rcvBytes+"/"+sndBytes+"/"
				
		self.nwUsage=self.nwUsage[:len(self.nwUsage)-1]		
		fp.close()
	def findPowUsage(self):
		self.powUsage="100"
		pipe=os.popen("ipmitool sensor | grep AVG")
		for pow in pipe.readlines():
			self.powUsage=pow.split("|")[1].strip()
			
		pipe.close()
	def findFlops(self):
		self.flops="10"
	
	def findCpuFeatures(self):
		self.cpuNumber=[]
		self.cpuName=[]
		self.cpuSpeed=[]
		self.cpuCache=[]		
		cpuFile = file("/proc/cpuinfo", "r")
		cpuData=cpuFile.readlines()
		for data in cpuData:
			found="None"			
			if data[0:2]=='pr':
				self.cpuNumber.append(data.split(":")[1].replace("\n","").strip())
			if data.find("name")>-1:
				self.cpuName.append(data.split(":")[1].replace("\n","").replace("\t"," "))
			if data.find("MHz")>-1:
				self.cpuSpeed.append(data.split(":")[1].replace("\n","").replace("\t"," "))
			if data.find("cache size")>-1:
				self.cpuCache.append(data.split(":")[1].replace("\n","").replace("\t"," ").replace("KB",""))			
					
			
	def getTimeList(self,cpu):
		statFile = file("/proc/stat", "r")
   		statList = statFile.readlines()
		for data in statList:
			if  data.find("cpu"+cpu)>-1:
				timeList = data.split(" ")[1:5]
				
		for j in range(len(timeList))  :
       			timeList[j] = int(timeList[j])
		return timeList


	def findCpuLoad(self):
		
		t1=[]
		t2=[]		
		Dt=[]
		self.cpuLoad=[]		
		for i in self.cpuNumber:
			t1.append(self.getTimeList(i.replace(" ","")))
		time.sleep(INTERVAL)
		for i in self.cpuNumber:
			t2.append(self.getTimeList(i.replace(" ","")))
		t=zip(t1,t2)
		
		for i in range(0,len(self.cpuNumber)):
			dt=[]
			for j in range(0,4):			
				dt.append(t[i][1][j]-t[i][0][j])
				 
			Dt.append(dt)
		
		for dt in Dt:		
			if sum(dt)==0:
				cpuPct='NONE'
			else:
				cpuPct = 100 - (dt[len(dt) - 1] * 100.00 / sum(dt))
			self.cpuLoad.append(str(cpuPct))
		

	#TODO remove lmsensors dependency	
	def findCpuTemp(self):
		self.cpuTemp=[]
		for filename in os.listdir("/sys/class/hwmon"):
    			f=open("/sys/class/hwmon/"+filename+"/device/name",'r')
			name=f.readlines()[0]			
			if name.find("coretemp") >-1 :
				ft=open("/sys/class/hwmon/"+filename+"/device/temp1_input")		
				temp=ft.readlines()[0].replace("\n","")
				self.cpuTemp.append(temp)
				ft.close()	
			elif name.find("w83627ehf") >-1 :
				ft=open("/sys/class/hwmon/"+filename+"/device/temp2_input")		
				temp=ft.readlines()[0].replace("\n","")
				self.cpuTemp.append(temp)
				ft.close()		
			f.close()

	def findCpuState(self):
		self.cpuState=[]
		for filename in os.listdir("/proc/acpi/processor"):
    			fp=open("/proc/acpi/processor/"+filename+"/power",'r')
			pstate=fp.readlines()[0].split(":")[1].replace("\n","").replace(" ","")
			self.cpuState.append(pstate)
			fp.close()
		
	
	def findFans(self):
		self.fanName=[]
		self.fanSpeed=[]
		self.fanNumber=[]
		pipe=os.popen("ipmitool  sensor | grep RPM")
		name="NONE"
		number=0		
		for fan in pipe.readlines():
			name=fan.split("|")[0].strip()
			speed=fan.split("|")[1].strip()
			self.fanName.append(name)
			self.fanSpeed.append(speed)
			self.fanNumber.append(str(number))
			number=number+1
		pipe.close()
		if name=="NONE":
			for filename in os.listdir("/sys/class/hwmon"):
				f=open("/sys/class/hwmon/"+filename+"/device/name",'r')
				cname=f.readlines()[0]
				if cname.find("w83627ehf") >-1 :
					f1=open("/sys/class/hwmon/"+filename+"/device/fan1_input")		
					speed=f1.readlines()[0].replace("\n","")
					self.fanSpeed.append(speed)
					self.fanName.append("Sys Fan")
					self.fanNumber.append("0")
					f1.close()
					f2=open("/sys/class/hwmon/"+filename+"/device/fan2_input")		
					speed=f2.readlines()[0].replace("\n","")
					self.fanSpeed.append(speed)
					self.fanName.append("CPU Fan")
					self.fanNumber.append("1")
					f2.close()		
			f.close()
		


	

	def updateDb(self):
		self.findCpuFeatures()
		self.findCpuLoad()
		self.findCpuTemp()
		self.findCpuState()
		self.findnwUsage()
		self.findMemInfo()
		self.findPowUsage()
		self.findFlops()
		self.findFans()		
		cpuData=zip(self.cpuNumber,self.cpuName,self.cpuTemp,self.cpuLoad,self.cpuSpeed,self.cpuCache,self.cpuState)
	        print cpuData,self.cpuNumber,self.cpuName,self.cpuTemp,self.cpuLoad,self.cpuSpeed,self.cpuCache,self.cpuState
		if self.db.checkNodeExists(self.nId)==0:
			self.db.addNode(self.nId,[self.powUsage,self.memUsage,self.nwUsage,"ON",self.flops])
			for i in range(0,len(self.cpuNumber)):
				self.db.addCpus(self.nId,[self.cpuNumber[i],self.cpuName[i],self.cpuTemp[i],self.cpuLoad[i],self.cpuSpeed[i],self.cpuType,self.cpuCache[i],self.cpuState[i]])
			for i in range(0,len(self.fanNumber)):
				self.db.addFans(self.nId,[self.fanNumber[i],self.fanName[i],self.fanSpeed[i],'OK'])
		else:
			self.db.updateNode(self.nId,[self.powUsage,self.memUsage,self.nwUsage,"ON",self.flops])
			for i in range(0,len(self.cpuNumber)):
				self.db.updateCpus(self.nId,[self.cpuNumber[i],self.cpuName[i],self.cpuTemp[i],self.cpuLoad[i],self.cpuSpeed[i],self.cpuType,self.cpuCache[i],self.cpuState[i]])
			for i in range(0,len(self.fanNumber)):
				self.db.updateFans(self.nId,[self.fanNumber[i],self.fanName[i],self.fanSpeed[i],'OK'])
		
		







"""
db=qosDb('172.16.150.252','hpc','hpc','hpcQoS')
cn=compNode(2,db)
cn.updateDb()
db.close()
"""
