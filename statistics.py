import math
import random

class stat:
	def __init__(self,list,binSize):
		self.list = list
		self.binSize = binSize

	def histogram(self):
		
		if(len(self.list)<self.binSize):
			return
				
		#sorting the list in descending order
		self.list = sorted(self.list,reverse=True)
		self.listUnique = []
		
		print self.list
		#getting the list of unique values in the list
		for x in self.list:
			if x not in self.listUnique:
				self.listUnique.append(x)

		gradeMap = {}
		
		binNo = 1
		i =1
		j =1
		binWidth = math.floor(len(self.listUnique)/self.binSize)
		for x in self.listUnique:
			# check if the value falls in a new bin
			if(i==binWidth):
				#check if the remaining values are big enough to generate a new bin
				if(len(self.listUnique)-j>=binWidth):
					i = 0
					binNo+=1
			
			gradeMap[x] = binNo
			i+=1
			j+=1		
		#return the graded map for the concerned list
		return gradeMap


list = []
for i in range(0,101):
	list.append(random.randint(1,100))

statObj = stat(list,8)
gradeMap = statObj.histogram()
print gradeMap
