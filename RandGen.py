#scheduler
import MySQLdb
import random
import DomainObjects


conn = MySQLdb.connect(host="172.16.1.5",user="hpc",passwd="hpc",db="hpcQoS")


# prepare a cursor object using cursor() method
cursor = conn.cursor()

nodeStates = ["Available","NA"]
cpuTypes = ["SC","MC"]
cpuStates = ["Working","Sleeping","Off"]
fanStates = ["OK","NotOK"]
alphabet = 'abcdefghijklmnopqrstuvwxyz'

nodeList = []
cpuList = []
fanList = []

sqlCommandList1 = []
sqlCommandList2 = []

print ("Hello user! How many records do you want to create?")
ul = raw_input(">")
print ("Please enter the start node Id")
nIdStr = raw_input(">")
nId = int(nIdStr)

print ("Please enter the max.no. of CPUs per node")
mcStr = raw_input(">")
mc = int(mcStr)
print ("Please enter the max no. of fans per node")
mfStr = raw_input(">")
mf = int(mfStr)


#randomly inserting 100 records in the database table
for i in range(0,int(ul)+1):
	
	powerUsage = random.randint(100,1000)
	memUsage = random.randint(50,500)
	nwSUsage = random.randint(1,600)
	nwRUsage = random.randint(1,700)
	nodeStateId = random.randint(0,1)
	nodeState = nodeStates[nodeStateId]
	performance = random.randint(5000,10000)
	
	#creating a node object
	nodeObj = DomainObjects.Node(nId, str(powerUsage), str(memUsage), str(nwSUsage)+"/"+str(nwRUsage),nodeState,str(performance))

	print "\n\n"
	nodeObj.display()
	
	#adding node to list
	nodeList.append(nodeObj)

	#Prepare SQL query to INSERT a record into the database.
	sql = "INSERT INTO qosMain_1(nId, \
       powerUsage, memUsage, nwSRUsage, status, performance) \
       VALUES ('%d', '%s', '%s','%s','%s','%s' )" % \
      (nodeObj.nId, nodeObj.powerUsage, nodeObj.memUsage, nodeObj.nwSRUsage,nodeObj.status,nodeObj.performance)

	for j in range(0,random.randint(1,mc)):
		cpuName = ' '
		for x in random.sample(alphabet,random.randint(5,10)):
      			cpuName+=x
		cpuTemp = random.randint(100,1000)
		cpuLoad = random.randint(0,100)
		cpuSpeed = random.randint(300,700)
		cpuTypeId = random.randint(0,1)
		cpuType = cpuTypes[cpuTypeId]
		cpuCache = random.randint(25,400)
		cpuStateId = random.randint(0,2)
		cpuState = cpuStates[cpuStateId]

        	cpuObj = DomainObjects.CPU(nId,str(cpuName),str(cpuTemp),str(cpuLoad),str(cpuSpeed),cpuType,str(cpuCache),cpuState);
		print "\n\n"
		cpuObj.display()

		#adding CPU to list
		cpuList.append(cpuObj)
		
	 	#Prepare SQL query to INSERT a record into the database.
        	sql1 = "INSERT INTO nodeCpus_1(nId, \
       	cpuName, cpuTemp, cpuLoad, cpuSpeed, cpuType,cpuCache, cpuState) \
       	VALUES ('%d', '%s', '%s','%s','%s','%s','%s','%s' )" % \
      	(cpuObj.nId, cpuObj.cpuName, cpuObj.cpuTemp, cpuObj.cpuLoad, cpuObj.cpuSpeed, cpuObj.cpuType,cpuObj.cpuCache, cpuObj.cpuState)

		sqlCommandList1.append(sql1)
	
	for k in range(0,random.randint(1,mf)):
		fanName = "F"+str(nId)
		fanSpeed = random.randint(200,500)
		fanStateId = random.randint(0,1)
		fanState = fanStates[fanStateId]

		fanObj = DomainObjects.Fan(nId,fanName,str(fanSpeed),fanState)
		print "\n\n"
		fanObj.display()

	 	#Prepare SQL query to INSERT a record into the database.
        	sql2 = "INSERT INTO nodeFans_1(nId,fanName, fanspeed, state) \
       	VALUES ('%d', '%s', '%s','%s' )" % \
      	(fanObj.nId,fanObj.fanName,fanObj.fanSpeed,fanObj.fanState)
		
		sqlCommandList2.append(sql2)	
	
	try:
	   	# Execute the SQL commands
		cursor.execute(sql)
		conn.commit()
		
		for sqlCommand1 in sqlCommandList1:
			cursor.execute(sqlCommand1)
			conn.commit()
		#emptying the command list
		del sqlCommandList1[:]	
	
		for sqlCommand2 in sqlCommandList2:
			cursor.execute(sqlCommand2)
   			conn.commit()
		del sqlCommandList2[:]

		print "Executed the SQL command!"	
	except:
   		print "Sorry!Failed to execute"
		# Rollback in case there is any error
   		conn.rollback()
	
	nId = nId+1

conn.close()
