import sys
import numpy as np
import matplotlib.pyplot as plt
import QueryDB as qry
ax = plt.subplot(111)

def main(argv):
	data = qry.queryDB("select Date_format(First_Occurrence_Date, '%H') as 'Hour', Count(1) as 'Crime_Count' from DenverCrime where Is_Crime = 1 group by Date_format(First_Occurrence_Date, '%H');")
	queryToPlot(data, 'r', 0)
	data = qry.queryDB("select Date_format(First_Occurrence_Date, '%H') as 'Hour', Count(1) as 'Crime_Count' from DenverCrime where Is_Crime = 1 and Offense_Code = 1102 group by Date_format(First_Occurrence_Date, '%H');")
	queryToPlot(data, 'b', .3)

	plt.show()

def queryToPlot(data, color, offset):
	hourList = []
	crimeCountList = []
	for (hour, crimeCount) in data:
		if hour is not None and crimeCount is not None:
			hourList.append(float(hour)+offset)
			crimeCountList.append(float(crimeCount))

	plot(hourList, normalizeData(crimeCountList), color, offset)

def toPercent(data):
	sum = 0
	for x in data:
		sum += x
	for i, x in enumerate(data):
		data[i] = x/sum
	return data

def normalizeData(data):
	maxX = max(data)
	minX = min(data)
	diff = maxX- minX
	for i, x in enumerate(data):
		x = (x - minX) / diff
		data[i] = x

	return data 

def plot(x, y, colorValue, offset):

	ax.bar(x, y, width=.3, color=colorValue, alpha=.3)

if __name__ == "__main__":
	main(sys.argv[1:])