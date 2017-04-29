import sys
import random
import math
import matplotlib.pyplot as plt
import QueryDB as qry
import urllib

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

	def update(self):
		self.loc.x = self.newX / self.newXCount
		self.loc.y = self.newY / self.newYCount

maxGeoLat = 39.812
minGeoLat = 39.645
maxGeoLon = -104.854
minGeoLon = -105.075
colors = ["#B11E0C", "#2F7F24", "#0F4D97", "#970f95", "#34B7C2", "#BB811B"]

crime = ["Shoplifting2", "2303"]
k = 5
iteration = 5

def main(argv):
	cursor = qry.queryDB("select Geo_Lon, Geo_Lat from DenverCrime where Geo_Lat > " + str(minGeoLat) + " and Geo_Lat < " + str(maxGeoLat) + " and Geo_Lon < " + str(maxGeoLon) + " and Geo_Lon > " + str(minGeoLon) + " and Offense_Code = " + crime[1])
	locations = []
	for (geoLon, geoLat) in cursor:
		if geoLon is not None and geoLat is not None:
			locations.append(Location(geoLon, geoLat))
	
	#downloadMap()

	kMeans(locations, k, iteration)

def kMeans(data, k, maxIterations):
	formatPlot()
	centroids = []
	for i in range(0, k):
		centroids.append(Centroid(Location(random.uniform(minGeoLon, maxGeoLon), random.uniform(minGeoLat, maxGeoLat))))

	for i in range(0, maxIterations):
		for point in data:
			minDistance = sys.float_info.max
			for i, centroid in enumerate(centroids):
				distance = point.distanceTo(centroid.loc)
				if distance < minDistance:
					minDistance = distance
					point.currentCentroid = i
			centroids[point.currentCentroid].assignLocationToSelf(point)

		for centroid in centroids:
			centroid.update()

	for point in data:
		plt.plot(point.x, point.y, marker="o",color=colors[point.currentCentroid])

	img = plt.imread("map.png")
	plt.imshow(img, zorder=0, extent=[minGeoLon, maxGeoLon, minGeoLat, maxGeoLat])
	#plt.show()
	plt.savefig("CrimeClustering/" + crime[0] + "-k" + str(k) + "Cluster.png", bbox_inches="tight", dpi=300)

def downloadMap():
	urllib.urlretrieve("https://maps.googleapis.com/maps/api/staticmap?center=39.729,-104.9645&zoom=12&size=640x640&scale=2&key=*Your Key Here*", "map.png")
	
def formatPlot():
	plt.figure(figsize=(7, 7))
	plt.rc("axes", edgecolor="#FFFFFF")

	ax = plt.subplot(111)
	ax.spines["top"].set_visible(False)
	ax.spines["right"].set_visible(False)

	plt.tick_params(bottom='off', top='off', right='off', left='off')

	plt.yticks(fontsize=5)
	plt.xticks(fontsize=5)

if __name__ == "__main__":
	main(sys.argv[1:])