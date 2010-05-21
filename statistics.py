import math
import random

class stat:
        def __init__(self,list):
                self.list = list
                
	def average(list):
		if len(list):
			return float( sum(list) / len(list))
		else:
			return 0.0
        average = staticmethod(average)#bounding the static-like function

	def histogram(list,binSize):
                
                if(len(list)<binSize):
                        return
                                
                #sorting the list in descending order
                list = sorted(list,reverse=True)
                listUnique = []
                
                #print self.list
                #getting the list of unique values in the list
                for x in list:
                        if x not in listUnique:
                                listUnique.append(x)

                gradeMap = {}
                
                binNo = 1
                i =1
                j =1
                binWidth = math.floor(len(listUnique)/binSize)
                for x in listUnique:
                        # check if the value falls in a new bin
                        if(i==binWidth):
                                #check if the remaining values are big enough to generate a new bin
                                if(len(listUnique)-j>=binWidth):
                                        i = 0
                                        binNo+=1
                        
                        gradeMap[x] = binNo
                        i+=1
                        j+=1            
                #return the graded map for the concerned list
                return gradeMap

	histogram = staticmethod(histogram)

#list = []
#for i in range(0,101):
#        list.append(random.randint(1,100))

#statObj = stat(list)
#gradeMap = statObj.histogram(8)
#print gradeMap
