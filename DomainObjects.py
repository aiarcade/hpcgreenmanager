import statistics

class Node:
        def __init__(self,nId,powerUsage,memUsage,nwSRUsage,status,performance):
                self.nId = nId
                self.powerUsage = powerUsage
                self.memUsage = memUsage
                self.nwSRUsage = nwSRUsage
                self.status = status
                self.performance = performance

	def display(self):
		print "Node:" \
		     +"\n\t1.nId : "+str(self.nId)+" " \
		      +"\n\t2.powerUsage : "+str(self.powerUsage)+" " \
			+"\n\t3.memUsage : "+str(self.memUsage)+" " \
			+"\n\t4.nwSRUsage : "+str(self.nwSRUsage)+" " \
			+"\n\t5.status : "+str(self.status)+" " \
			+"\n\t6.performance : "+str(self.performance)

	def setCpuAndFans(self,cpuList,fanList):
		self.cpuList = cpuList
		self.fanList = fanList
		self.noOfCpus = len(cpuList)
		self.noOfFans = len(fanList)

	def setNetCpuParamsForNode(self):
		cpuTempList = []
		cpuLoadList = []
		cpuSpeedList = []
		cpuCacheList = []
		for cpu in self.cpuList:
			cpuTempList.append(cpu.cpuTemp)
			cpuLoadList.append(cpu.cpuLoad)
			cpuSpeedList.append(cpu.cpuSpeed)
			cpuCacheList.append(cpu.cpuCache)

		self.netNodeTemp = statistics.stat.average(cpuTempList)
		self.netNodeLoad = statistics.stat.average(cpuLoadList)
		self.netNodeSpeed = sum(cpuSpeedList)
		self.netNodeCache = sum(cpuCacheList)

	def setNetFanParamsForNode(self):
		fanSpeedList = []
		for fan in self.fanList:
			fanSpeedList.append(fan.fanSpeed)
		self.netNodeFanSpeed = sum(fanSpeedList)
		
	def displayNetParams(self):
		print "\n\t7.net node Temp:"+str(self.netNodeTemp)+" " \
			"\n\t8.net node load:"+str(self.netNodeLoad)+" " \
			"\n\t9.net node speed:"+str(self.netNodeSpeed)+" " \
			"\n\t10.net node Cache:"+str(self.netNodeCache)+" " \
			"\n\t11.net node fan speed:"+str(self.netNodeFanSpeed)	
class CPU:
        def __init__(self,nId,cpuName,cpuTemp,cpuLoad,cpuSpeed,cpuType,cpuCache,cpuState):
                self.nId = nId
                self.cpuName = cpuName
                self.cpuTemp = cpuTemp
                self.cpuLoad = cpuLoad
                self.cpuSpeed = cpuSpeed
                self.cpuType = cpuType
                self.cpuCache = cpuCache
                self.cpuState = cpuState
	def display(self):
        	print "CPU:" \
                     +"\n\tnId : "+str(self.nId)+" " \
                      +"\n\tcpuName: "+str(self.cpuName)+" " \
                        +"\n\tcpuTemp : "+str(self.cpuTemp)+" " \
                        +"\n\tcpuLoad : "+str(self.cpuLoad)+" " \
                        +"\n\tcpuSpeed : "+str(self.cpuSpeed)+" " \
                        +"\n\tcpuType : "+str(self.cpuType)+" " \
			+"\n\tcpuCache : "+str(self.cpuCache)+" " \
			+"\n\tcpuState : "+str(self.cpuState)

class Fan:
        def __init__(self,nId,fanName,fanSpeed,fanState):
                self.nId = nId
                self.fanName = fanName
                self.fanSpeed = fanSpeed
                self.fanState = fanState

	def display(self):
		 print "Fan:" \
                     +"\n\tnId : "+str(self.nId)+" " \
                      +"\n\tfanName : "+str(self.fanName)+" " \
                        +"\n\tfanSpeed : "+str(self.fanSpeed)+" " \
                        +"\n\tfanState : "+str(self.fanState)+" " 
