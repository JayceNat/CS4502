import mysql.connector

def queryDB(query):
	connection = mysql.connector.connect(user='*user*', password='*password*', host='localhost', database='CrimeTime')
	cursor = connection.cursor()
	#query = ("select TMax, Round(Sum(Crime_Count)/Count(1)) as CrimeCountAvg from DenverDailyCrimeWeather group by TMax")
	#query = ("select Date_format(First_Occurrence_Date, '%H') as 'Date', Count(1) as 'Crime_Count' from DenverCrime where Is_Crime = 1 group by Date_format(First_Occurrence_Date, '%H');")
	cursor.execute(query)
	data = []
	for entry in cursor:
		if entry is not None:
			data.append(entry)
	cursor.close()
	connection.close()
	return data