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

for i in range(1,numRows+1):
	row= r.fetch_row(1)
	print row

conn.close()
