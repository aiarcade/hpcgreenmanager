#scheduler
import MySQLdb
import DomainObjects

#function that creates Domain objects - node, cpu and fan from the result of the sql query
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
        	if(tupleDict.has_key(int(row[0]["qosMain_1.nId"]))):
                	tupleDict[int(row[0]["qosMain_1.nId"])].append(row[0])
		else:
                	rowList = [row[0]]
                	tupleDict[int(row[0]["qosMain_1.nId"])] = rowList

	nodeList = []
	
	#printing the different node details    
	for k,v in tupleDict.items():
        	print "Node id = %d, nodes = %s" % (k,v)
        	print "\n\n\n"
		#v[0] itself is a dict for the very first appearance of the node
		nodeObject = DomainObjects.Node(k,float(v[0]["qosMain_1.powerUsage"]),float(v[0]["qosMain_1.memUsage"]),float(v[0]["qosMain_1.nwSRUsage"].split("/")[0])+float(v[0]["qosMain_1.nwSRUsage"].split("/")[1]),v[0]["qosMain_1.status"],float(v[0]["qosMain_1.performance"]))
		
		cpuDict = {}
		fanDict = {}

		for tuple in v:
			if(not cpuDict.has_key(tuple["nodeCpus_1.cpuName"])):
				cpuObject = DomainObjects.CPU(k,tuple["nodeCpus_1.cpuName"],float(tuple["nodeCpus_1.cpuTemp"]),float(tuple["nodeCpus_1.cpuLoad"]),float(tuple["nodeCpus_1.cpuSpeed"]),tuple["nodeCpus_1.cpuType"],float(tuple["nodeCpus_1.cpuCache"]),tuple["nodeCpus_1.cpuState"])		
				cpuDict[tuple["nodeCpus_1.cpuName"]] = cpuObject

			if(not fanDict.has_key(tuple["nodeFans_1.fanName"])):
                                fanObject = DomainObjects.Fan(k,tuple["nodeFans_1.fanName"],float(tuple["nodeFans_1.fanspeed"]),tuple["nodeFans_1.state"])
				fanDict[tuple["nodeFans_1.fanName"]] = fanObject

		nodeObject.setCpuAndFans(cpuDict.values(),fanDict.values())
		nodeObject.setNetCpuParamsForNode()
		nodeObject.setNetFanParamsForNode()
		nodeList.append(nodeObject)
	
	return nodeList
			


#End of function

conn = MySQLdb.connect(host="172.16.1.5",user="hpc",passwd="hpc",db="hpcQoS")

# Run a MySQL query from Python and get the result set

sqlQuery = "select * from qosMain_1 JOIN (nodeCpus_1,nodeFans_1)" \
+" ON (qosMain_1.nId = nodeCpus_1.nId AND qosMain_1.nId = nodeFans_1.nId)" \
+" where qosMain_1.status like 'Available'" \
+" and (nodeCpus_1.cpuState like 'Working' or nodeCpus_1.cpuState like 'Sleeping')"\
+" and nodeFans_1.state like 'OK'"\

conn.query(sqlQuery)

r = conn.store_result()

nodeList = createNodes(r)

for node in nodeList:
	node.display()
	node.displayNetParams()
		
conn.close()
