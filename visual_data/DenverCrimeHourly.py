import sys
import numpy as np
import matplotlib.pyplot as plt
import QueryDB as qry

def main(argv):
	setPlotDesign()
	data = qry.queryDB("select Date_format(First_Occurrence_Date, '%H') as 'Hour', Count(1) as 'Crime_Count' from DenverCrime where Is_Crime = 1 group by Date_format(First_Occurrence_Date, '%H');")
	queryToPlot(data, "#6DA2BE", 0, "All Crimes")
	data = qry.queryDB("select Date_format(First_Occurrence_Date, '%H') as 'Hour', Count(1) as 'Crime_Count' from DenverCrime where Is_Crime = 1 and Offense_Code = 1102 group by Date_format(First_Occurrence_Date, '%H');")
	queryToPlot(data, "#C16256", .3, "Sexual Assault - rape")

	plt.legend(loc="upper center", frameon=False, fontsize=12)
	plt.show()

def queryToPlot(data, color, offset, label):
	hourList = []
	crimeCountList = []
	for (hour, crimeCount) in data:
		if hour is not None and crimeCount is not None:
			hourList.append(float(hour)+offset)
			crimeCountList.append(float(crimeCount))

	plot(hourList, normalize(crimeCountList), color, offset, label)

def percentage(data):
	sum = 0
	for x in data:
		sum += x
	for i, x in enumerate(data):
		data[i] = x/sum
	return data

def normalize(data):
	maxX = max(data)
	minX = min(data)
	diff = maxX- minX
	for i, x in enumerate(data):
		x = (x - minX) / diff
		data[i] = x

	return data

def setPlotDesign():
	plt.rc("axes", edgecolor="#BFBFBF")

	plt.figure(figsize=(10, 6))

	ax = plt.subplot(111)
	ax.spines["top"].set_visible(False)
	ax.spines["right"].set_visible(False)

	plt.xlabel("Time of Day")
	plt.ylabel("Offenses Normalized")

	plt.tick_params(bottom='off', top='off', right='off', left='off')

	plt.xticks(range(0, 24, 6), ["12 am", "6 am", "12 pm", "6 pm"], rotation=30, fontsize=14)
	plt.yticks([0, .25, .5, .75, 1], fontsize=14)

def plot(x, y, colorValue, offset, label):
	plt.bar(x, y, width=.3, color=colorValue, label=label, edgecolor="none")

if __name__ == "__main__":
	main(sys.argv[1:])