#scheduler
import MySQLdb
import DomainObjects
import statistics
from operator import itemgetter

#function that creates Domain objects - node, cpu and fan from the result of the sql query
#as well create an object with all the max values

def createNodes(r):
	numRows = r.num_rows()
	print  "\nNumber of Rows = ",numRows
	print "\nNumber of Columns = ",r.num_fields()

	tupleDict = {}
	#creating a dictionary of the returned results
	for i in range(1,numRows+1):

        	#first param - no.of rows, second parameter is made 2 to store row as a dict
        	row= r.fetch_row(1,2)
        	#print row

        	#check if no nodes have been added for this node id, key is the node id, value is a list of dictionaries (one for ea$
        	if(tupleDict.has_key(int(row[0]["qosMain.nId"]))):
                	tupleDict[int(row[0]["qosMain.nId"])].append(row[0])
		else:
                	rowList = [row[0]]
                	tupleDict[int(row[0]["qosMain.nId"])] = rowList

	nodeList = []
	
	maxNode = DomainObjects.Node(0,0,0,0,'ON',0);
  	maxNode.setCpuAndFans({}.values(),{}.values())
        maxNode.setNetCpuParamsForNode()
        maxNode.setNetFanParamsForNode()

	#printing the different node details    
	for k,v in tupleDict.items():
        	print "Node id = %d, nodes = %s" % (k,v)
        	print "\n\n\n"
		#v[0] itself is a dict for the very first appearance of the node
		nodeMemUsage = float(v[0]["qosMain.memUsage"].split("/")[0])+float(v[0]["qosMain.memUsage"].split("/")[1])
		
		nwSRusageArr = v[0]["qosMain.nwSRUsage"].split("/")

		nwSRUsage = 0
                nnc = 0
                itr = 0
		for nwSR in nwSRusageArr:
			nwSRUsage += float(nwSR)
			if(itr%2==0):
				nnc+=1
			itr+=1
		#nwSRUsage/=nnc   
		nodeObject = DomainObjects.Node(k,float(v[0]["qosMain.powerUsage"]),nodeMemUsage,nwSRUsage,v[0]["qosMain.status"],float(v[0]["qosMain.performance"]))

		if(nodeObject.powerUsage>maxNode.powerUsage):
			maxNode.powerUsage = nodeObject.powerUsage
		
		if(nodeObject.memUsage>maxNode.memUsage):
                        maxNode.memUsage = nodeObject.memUsage

		if(nodeObject.nwSRUsage>maxNode.nwSRUsage):
                        maxNode.nwSRUsage = nodeObject.nwSRUsage

		if(nodeObject.performance>maxNode.performance):
                        maxNode.performance = nodeObject.performance


		cpuDict = {}
		fanDict = {}

		for tuple in v:
			if(not cpuDict.has_key(tuple["nodeCpus.cId"])):
				cpuObject = DomainObjects.CPU(k,tuple["nodeCpus.cId"],tuple["nodeCpus.cpuName"],float(tuple["nodeCpus.cpuTemp"]),float(tuple["nodeCpus.cpuLoad"]),float(tuple["nodeCpus.cpuSpeed"]),tuple["nodeCpus.cpuType"],float(tuple["nodeCpus.cpuCache"]),tuple["nodeCpus.cpuState"])		
				cpuDict[tuple["nodeCpus.cId"]] = cpuObject

			if(not fanDict.has_key(tuple["nodeFans.fId"])):
                                fanObject = DomainObjects.Fan(k,tuple["nodeFans.fId"],tuple["nodeFans.fanName"],float(tuple["nodeFans.fanspeed"]),tuple["nodeFans.state"])
				fanDict[tuple["nodeFans.fId"]] = fanObject

		nodeObject.setCpuAndFans(cpuDict.values(),fanDict.values())
		nodeObject.setNetCpuParamsForNode()
		nodeObject.setNetFanParamsForNode()
	
		if(nodeObject.netNodeTemp>maxNode.netNodeTemp):
                        maxNode.netNodeTemp = nodeObject.netNodeTemp

                if(nodeObject.netNodeLoad>maxNode.netNodeLoad):
                        maxNode.netNodeLoad = nodeObject.netNodeLoad

                if(nodeObject.netNodeSpeed>maxNode.netNodeSpeed):
                        maxNode.netNodeSpeed = nodeObject.netNodeSpeed

                if(nodeObject.netNodeCache>maxNode.netNodeCache):
                        maxNode.netNodeCache = nodeObject.netNodeCache

		if(nodeObject.netNodeFanSpeed>maxNode.netNodeFanSpeed):
                        maxNode.netNodeFanSpeed = nodeObject.netNodeFanSpeed
		
	
		nodeList.append(nodeObject)

	return nodeList,maxNode

#End of function

#function to read weight from the files
def getWeights(filename):
	infile = file(filename,'r')
	map = {}
	for line in infile.readlines():
		map[line.split(":")[0]] = int(line.split(":")[1])
	infile.close()
	return map

#function to get node weights
def getNodeWeights(nodeList,maxNode,pw,gw):
	nodePowerUsageList = []
	nodeMemUsageList = []
	nodeNwSRUsageList = []
	nodePerformanceList = []
	nodeNetNodeTempList = []
	nodeNetNodeLoadList = []
	nodeNetNodeSpeedList = []
	nodeNetNodeCacheList = []
	nodeNetNodeFanSpeedList = []

	for node in nodeList:
		nodePowerUsageList.append(node.powerUsage*-1/maxNode.powerUsage)
		nodeMemUsageList.append(node.memUsage*-1/maxNode.memUsage)
		nodeNwSRUsageList.append(node.nwSRUsage*-1/maxNode.nwSRUsage)
		nodePerformanceList.append(node.performance/maxNode.performance)
		nodeNetNodeTempList.append(node.netNodeTemp*-1/maxNode.netNodeTemp)
		nodeNetNodeLoadList.append(node.netNodeLoad*-1/maxNode.netNodeLoad)
		nodeNetNodeSpeedList.append(node.netNodeSpeed/maxNode.netNodeSpeed)
		nodeNetNodeCacheList.append(node.netNodeCache/maxNode.netNodeCache)
		nodeNetNodeFanSpeedList.append(node.netNodeFanSpeed*-1/maxNode.netNodeFanSpeed)

	print "Power :"
	print nodePowerUsageList
	print gw
	nodePowerUsageGrade = statistics.stat.histogram(nodePowerUsageList,len(gw.values()))
	print nodePowerUsageGrade


	print "Mem Usage :"
       	nodeMemUsageGrade = statistics.stat.histogram(nodeMemUsageList,len(gw.values()))
        print nodeMemUsageGrade

	print "Nw SR usage :"
       	nodeNwSRUsageGrade = statistics.stat.histogram(nodeNwSRUsageList,len(gw.values()))
        print nodeNwSRUsageGrade

	print "Performance :"
       	nodePerformanceGrade = statistics.stat.histogram(nodePerformanceList,len(gw.values()))
        print nodePerformanceGrade

	print "Temp :"
       	nodeNetNodeTempGrade = statistics.stat.histogram(nodeNetNodeTempList,len(gw.values()))
        print nodeNetNodeTempGrade

	print "Load :"
       	nodeNetNodeLoadGrade = statistics.stat.histogram(nodeNetNodeLoadList,len(gw.values()))
        print nodeNetNodeLoadGrade

	print "Speed :"
       	nodeNetNodeSpeedGrade = statistics.stat.histogram(nodeNetNodeSpeedList,len(gw.values()))
        print nodeNetNodeSpeedGrade

	print "Cache :"
       	nodeNetNodeCacheGrade = statistics.stat.histogram(nodeNetNodeCacheList,len(gw.values()))
        print nodeNetNodeCacheGrade

	print "FanSpeed :"
       	nodeNetFanSpeedGrade = statistics.stat.histogram(nodeNetNodeFanSpeedList,len(gw.values()))
        print nodeNetFanSpeedGrade

	nodeWeight = {}
	netPw = 0
	for node in nodeList:
		if(netPw==0):
			netPw += pw['powerUsage']+pw['memUsage']+pw['nwSRUsage']+pw['performance']+pw['cpuTemp']+pw['cpuLoad']+pw['cpuSpeed']+pw['cpuCache']+pw['fanSpeed']
		nw = 0
#		print "\nhello\n"+str(gw[str(nodePowerUsageGrade[node.powerUsage*-1])])
		nw +=gw[str(nodePowerUsageGrade[node.powerUsage*-1/maxNode.powerUsage])]*pw['powerUsage']
		nw +=gw[str(nodeMemUsageGrade[node.memUsage*-1/maxNode.memUsage])]*pw['memUsage']
		nw +=gw[str(nodeNwSRUsageGrade[node.nwSRUsage*-1/maxNode.nwSRUsage])]*pw['nwSRUsage']
                nw +=gw[str(nodePerformanceGrade[node.performance/maxNode.performance])]*pw['performance']
		nw +=gw[str(nodeNetNodeTempGrade[node.netNodeTemp*-1/maxNode.netNodeTemp])]*pw['cpuTemp']
                nw +=gw[str(nodeNetNodeLoadGrade[node.netNodeLoad*-1/maxNode.netNodeLoad])]*pw['cpuLoad']
		nw +=gw[str(nodeNetNodeSpeedGrade[node.netNodeSpeed/maxNode.netNodeSpeed])]*pw['cpuSpeed']
		nw +=gw[str(nodeNetNodeCacheGrade[node.netNodeCache/maxNode.netNodeCache])]*pw['cpuCache']

	
		print "\nNodeWeight = "+str(nw) 
		print "nNetPw = "+str(netPw)

                nw = float(nw)/float(netPw) #calculating on a cpu basis
		nw = (float(nw) + float(gw[str(nodeNetFanSpeedGrade[node.netNodeFanSpeed*-1/maxNode.netNodeFanSpeed])]))/2            
               
		nodeWeight[node.nId] = nw

	sortedNodeWeight = sorted(nodeWeight.items(), key=itemgetter(1))

	print "\n\nHere is printing the node Weights"
	print sortedNodeWeight

	return sortedNodeWeight

conn = MySQLdb.connect(host="172.16.150.252",user="hpc",passwd="hpc",db="hpcQoS")

# Run a MySQL query from Python and get the result set

sqlQuery = "select * from qosMain JOIN (nodeCpus,nodeFans)" \
+" ON (qosMain.nId = nodeCpus.nId AND qosMain.nId = nodeFans.nId)" \
+" where qosMain.status like 'ON'" \
+" and (nodeCpus.cpuState like 'C0' or nodeCpus.cpuState like 'C1')"\
+" and nodeFans.state like 'OK'"\

conn.query(sqlQuery)

r = conn.store_result()

(nodeList,maxNode) = createNodes(r)

for node in nodeList:
	node.display()
	node.displayNetParams()

gw = getWeights("GradeWeight.txt")
print gw

pw = getWeights("ParamsCredit.txt")
print pw	

getNodeWeights(nodeList,maxNode,pw,gw)
	
conn.close()
