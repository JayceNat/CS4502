import sys
import numpy as np
import matplotlib.pyplot as plt
import QueryDB as qry

def main(argv):
	cursor = qry.queryDB("select TMax, Round(Sum(Crime_Count)/Count(1)) as CrimeCountAvg from DenverDailyCrimeWeather group by TMax")
	tMaxList = []
	crimeCountAvgList = []
	for (tMax, crimeCountAvg) in cursor:
		if tMax is not None:
			tMaxList.append(float(tMax))
			crimeCountAvgList.append(int(crimeCountAvg))

	plot(tMaxList, crimeCountAvgList)

def plot(x, y):
	#Pieces of code for matplotlib visualizations taken from http://www.randalolson.com/2014/06/28/how-to-make-beautiful-data-visualizations-in-python-with-matplotlib/
	
	plt.rc("axes", edgecolor="#BFBFBF")

	plt.figure(figsize=(11, 6))

	ax = plt.subplot(111)
	ax.spines["top"].set_visible(False)
	ax.spines["right"].set_visible(False)

	plt.tick_params(bottom='off', top='off', right='off', left='off')

	for y2 in range(30, 200, 30):
		plt.plot([1,105], [y2, y2], "--", lw=0.4, color="black", alpha=0.2)

	plt.yticks(range(0, 200, 30), fontsize=14)
	plt.xticks(fontsize=14)

	plt.xlabel("Max Daily Temperature (F)")
	plt.ylabel("Average Daily Crimes")

	plot1 = plt.plot(x, y, color="#E8B14F", lw=1.4, label="Avg Crimes", alpha=.9)
	plot2 = plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 4))(np.unique(x)), color='red', linestyle='--', dashes=(5, 10), label="Trend (poly 4)")
	
	plt.axis([0, 106, 0, 200])
	plt.legend(loc="lower right", frameon=False, fontsize=12)
	#plt.show()
	plt.savefig("DenverCrimeTMax.png", bbox_inches="tight", dpi=300)

if __name__ == "__main__":
	main(sys.argv[1:])