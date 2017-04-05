CREATE TABLE DenverCrime (Crime_Id BIGINT PRIMARY KEY AUTO_INCREMENT, Incident_Id BIGINT, Offense_Id BIGINT, Offense_Code SMALLINT, Offense_Code_Extension TINYINT, Offense_Type_Id VARCHAR(63), Offense_Category_Id VARCHAR(63), First_Occurrence_Date DATETIME, Last_Occurrence_Date DATETIME, Reported_Date DATETIME, Incident_Address VARCHAR(255), Geo_X INT, Geo_Y INT, Geo_Lon FLOAT(12,8), Geo_Lat FLOAT(12,8), District_Id TINYINT, Precinct_Id SMALLINT, Neighborhood_Id VARCHAR(63), Is_Crime TINYINT, Is_Traffic TINYINT);

CREATE TABLE DenverTemp (Temp_Id INT PRIMARY KEY AUTO_INCREMENT, Station VARCHAR(63), Station_Name VARCHAR(63), Elevation FLOAT(6,1), Lat FLOAT(8,4), Lon FLOAT(8,3), Date DATE, TMax SMALLINT, TMax_Measurement_Flag VARCHAR(2), TMax_Quality_Flag VARCHAR(2), TMIx SMALLINT, TMix_Measurement_Flag VARCHAR(2), TMix_Quality_Flag VARCHAR(2));

CREATE TABLE DenverWind (Wnd_Id INT PRIMARY KEY AUTO_INCREMENT, Station VARCHAR(63), Station_Name VARCHAR(63), Elevation FLOAT(6,1), Lat FLOAT(8,4), Lon FLOAT(8,3), Date DATE, Avg_Wnd FLOAT(4,1), Avg_Wnd_Measurement_Flag VARCHAR(2), Avg_Wnd_Quality_Flag VARCHAR(2));

CREATE TABLE DenverPrec (Prec_Id INT PRIMARY KEY AUTO_INCREMENT, Station VARCHAR(63), Station_Name VARCHAR(63), Elevation FLOAT(6,1), Lat FLOAT(8,4), Lon FLOAT(8,3), Date DATE, Prcp FLOAT(6,2), Prcp_Measurement_Flag VARCHAR(2), Prcp_Quality_Flag VARCHAR(2), Snwd FLOAT(6,1), Snwd_Measurement_Flag VARCHAR(2), Snwd_Quality_Flag VARCHAR(2), Snow FLOAT(6,1), Snow_Measurement_Flag VARCHAR(2), Snow_Quality_Flag VARCHAR(2));

LOAD DATA LOCAL INFILE 'denver_crime.csv' INTO TABLE DenverCrime FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES (Incident_Id, Offense_Id, Offense_Code, Offense_Code_Extension, Offense_Type_Id, Offense_Category_Id, @var1, @var2, @var3, Incident_Address, Geo_X, Geo_Y, Geo_Lon, Geo_Lat, District_Id, Precinct_Id, Neighborhood_Id, Is_Crime, Is_Traffic) SET First_Occurrence_Date = STR_TO_DATE(@var1, '%Y-%m-%d %H:%i:%s'), Last_Occurrence_Date = STR_TO_DATE(@var2, '%Y-%m-%d %H:%i:%s'), Reported_Date = STR_TO_DATE(@var3, '%Y-%m-%d %H:%i:%s');

LOAD DATA LOCAL INFILE 'Denver_Temperature.csv' INTO TABLE DenverTemp FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES (Station, Station_Name, Elevation, Lat, Lon, @var1, TMax, TMax_Measurement_Flag, TMax_Quality_Flag, TMIx, TMix_Measurement_Flag, TMix_Quality_Flag) SET Date = STR_TO_DATE(@var1, '%Y%m%d');

LOAD DATA LOCAL INFILE 'Denver_Wind.csv' INTO TABLE DenverWind FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES (Station, Station_Name, Elevation, Lat, Lon, @var1, Avg_Wnd, Avg_Wnd_Measurement_Flag, Avg_Wnd_Quality_Flag) SET Date = STR_TO_DATE(@var1, '%Y%m%d');

LOAD DATA LOCAL INFILE 'Denver_Precipitation.csv' INTO TABLE DenverPrec FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES (Station, Station_Name, Elevation, Lat, Lon, @var1, Prcp, Prcp_Measurement_Flag, Prcp_Quality_Flag, Snwd, Snwd_Measurement_Flag, Snwd_Quality_Flag, Snow, Snow_Measurement_Flag, Snow_Quality_Flag) SET Date = STR_TO_DATE(@var1, '%Y%m%d');