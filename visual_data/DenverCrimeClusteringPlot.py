import sys
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import QueryDB as qry

class Location:
	def __init__(self, x, y):
		self.x = x;
		self.y = y;

	def distanceTo(self, location):
		xdif = location.x - self.x
		ydif = location.y - self.y
		return math.sqrt((xdif * xdif) + (ydif * ydif))

class Centroid:
	newX = 0
	newXCount = 0
	newY = 0
	newYCount = 0
	def __init__(self, location):
		self.loc = location

	def assignLocationToSelf(self, location):
		self.newX += location.x
		self.newXCount += 1;
		self.newY += location.y
		self.newYCount += 1;

	def computeNew(self):
		self.loc.x = newX / newXCount
		self.loc.y = newY / newYCount



maxGeoLat = 39.8
minGeoLat = 39.658
maxGeoLon = -104.913
minGeoLon = -105.134

def main(argv):
	cursor = qry.queryDB("select Geo_Lon, Geo_Lat from DenverCrime where Geo_Lat > " + str(minGeoLat) + " and Geo_Lat < " + str(maxGeoLat) + " and Geo_Lon < " + str(maxGeoLon) + " and Geo_Lon > " + str(minGeoLon) + " and Offense_Code = 2303")
	locations = []
	for (geoLon, geoLat) in cursor:
		if geoLon is not None and geoLat is not None:
			locations.append(Location(geoLon, geoLat))
			

	#plot(tMaxList, crimeCountAvgList)
	kMeans(locations, 3, 5)
	#plt.plot(lon, lat, "o")
	#plt.show()

def kMeans(data, k, maxIterations):
	centroids = []
	for i in range(0, k):
		centroids.append(Centroid(Location(random.uniform(minGeoLon, maxGeoLon), random.uniform(minGeoLat, maxGeoLat))))
		print(str(centroids[i].loc.x) + " " + str(centroids[i].loc.y))

	for point in data:
		minDistance = sys.float_info.max
		for i, centroid in enumerate(centroids):
			distance = point.distanceTo(centroid.loc)
			if distance < minDistance:
				minDistance = distance
				point.currentCentroid = i
		centroids[point.currentCentroid].assignLocationToSelf(point)

	for y in centroids:
		plt.plot(y.loc.x, y.loc.y, "bo")

	for x in data:
		if x.currentCentroid == 1:
			plt.plot(x.x, x.y, "ro")

	plt.show()

	
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