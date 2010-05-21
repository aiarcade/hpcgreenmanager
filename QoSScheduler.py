#scheduler
import MySQLdb

conn = MySQLdb.connect(host="172.16.1.5",user="hpc",passwd="hpc",db="hpcQoS")

# Run a MySQL query from Python and get the result set

sqlQuery = "select * from qosMain_1 JOIN (nodeCpus_1,nodeFans_1)" \
+" ON (qosMain_1.nId = nodeCpus_1.nId AND qosMain_1.nId = nodeFans_1.nId)" \
+" where qosMain_1.status like 'Available'" \
+" and (nodeCpus_1.cpuState like 'Working' or nodeCpus_1.cpuState like 'Sleeping')"\
+" and nodeFans_1.state like 'OK'"\

conn.query(sqlQuery)

r = conn.store_result()

numRows = r.num_rows()
print  "\nnumRows = ",numRows
print "\nnum of fields = ",r.num_fields()

tupleDict = {}
for i in range(1,numRows+1):
	#first param - no.of rows, second parameter is made 2 to store row as a dict
	row= r.fetch_row(1,2)
	#print row
	
	#check if no nodes have been added with this node id, key is the node id, value is a list of dictionaries (one for each row)
	if(tupleDict.has_key(int(row[0]["qosMain_1.nId"]))):
		tupleDict[int(row[0]["qosMain_1.nId"])].append(row[0])
	else:
		rowList = [row[0]]
		tupleDict[int(row[0]["qosMain_1.nId"])] = rowList

#printing the different node details	
for k,v in tupleDict.items():
	print "Node id = %d, nodes = %s" % (k,v)
	print "\n\n\n"

powerUsageDict = {}
for k,v in tupleDict.items():
	netPowerUsage = 0
	for tuple in v:
		netPowerUsage+=float(tuple["qosMain_1.powerUsage"])
	powerUsageDict[k] = netPowerUsage

for k1,v1 in powerUsageDict.items():
	print "NId = %d , power usage = %s" % (k1,str(v1))
		
conn.close()
