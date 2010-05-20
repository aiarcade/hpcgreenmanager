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
		     +"\n\tnId : "+str(self.nId)+" " \
		      +"\n\tpowerUsage : "+self.powerUsage+" " \
			+"\n\tmemUsage : "+self.memUsage+" " \
			+"\n\tnwSRUsage : "+self.nwSRUsage+" " \
			+"\n\tstatus : "+self.status+" " \
			+"\n\tperformance : "+self.performance
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
                      +"\n\tcpuName: "+self.cpuName+" " \
                        +"\n\tcpuTemp : "+self.cpuTemp+" " \
                        +"\n\tcpuLoad : "+self.cpuLoad+" " \
                        +"\n\tcpuSpeed : "+self.cpuSpeed+" " \
                        +"\n\tcpuType : "+self.cpuType+" " \
			+"\n\tcpuCache : "+self.cpuCache+" " \
			+"\n\tcpuState : "+self.cpuState

class Fan:
        def __init__(self,nId,fanName,fanSpeed,fanState):
                self.nId = nId
                self.fanName = fanName
                self.fanSpeed = fanSpeed
                self.fanState = fanState

	def display(self):
		 print "Fan:" \
                     +"\n\tnId : "+str(self.nId)+" " \
                      +"\n\tfanName : "+self.fanName+" " \
                        +"\n\tfanSpeed : "+self.fanSpeed+" " \
                        +"\n\tfanState : "+self.fanState+" " 
