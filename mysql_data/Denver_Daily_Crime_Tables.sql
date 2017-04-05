DROP TABLE IF EXISTS DenverDailyCrime;
create table DenverDailyCrime as
	select 
		Date_format(First_Occurrence_Date, '%Y-%m-%d') as 'Date',
		Count(1) as 'Crime_Count'
	from DenverCrime 
	where Is_Crime = 1 
	group by Date_format(First_Occurrence_Date, '%Y-%m-%d');

DROP TABLE IF EXISTS DenverDailyTMax;
create table DenverDailyTMax as
	select 
		Date,
		Round(Avg(TMax)) as 'TMax'
	from DenverTemp
	where TMax_Measurement_Flag = '' 
		and TMax_Quality_Flag = '' 
		and TMax between -50 and 150
	group by Date;

DROP TABLE IF EXISTS DenverDailyTMin;
create table DenverDailyTMin as
	select 
		Date,
		Round(Avg(TMin)) as 'TMin'
	from DenverTemp
	where TMin_Measurement_Flag = '' 
		and TMin_Quality_Flag = '' 
		and TMin between -50 and 150
	group by Date;
	

DROP TABLE IF EXISTS DenverDailyPrcp;
create table DenverDailyPrcp as
	select 
		Date,
		Avg(Prcp) as 'Prcp'
	from DenverPrec
	where Prcp_Measurement_Flag = '' 
		and Prcp_Quality_Flag = '' 
		and Prcp between 0 and 250
	group by Date;

DROP TABLE IF EXISTS DenverDailySnwd;
create table DenverDailySnwd as
	select 
		Date,
		Avg(Snwd) as 'Snwd'
	from DenverPrec 
	where Snwd_Measurement_Flag = '' 
		and Snwd_Quality_Flag = '' 
		and Snwd between 0 and 250
	group by Date;

DROP TABLE IF EXISTS DenverDailySnow;
create table DenverDailySnow as
	select 
		Date,
		Avg(Snow) as 'Snow'
	from DenverPrec 
	where Snow_Measurement_Flag = '' 
		and Snow_Quality_Flag = '' 
		and Snow between 0 and 250
	group by Date;

DROP TABLE IF EXISTS DenverDailyWeather;
create table DenverDailyWeather as
	select
		DenverDailyTMax.Date,
		DenverDailyTMax.TMax,
		DenverDailyTMin.TMin,
		DenverDailyPrcp.Prcp,
		DenverDailySnwd.Snwd,
		DenverDailySnow.Snow
	from DenverDailyTMax
	left join DenverDailyTMin
		on DenverDailyTMax.Date = DenverDailyTMin.Date
	left join DenverDailyPrcp
		on DenverDailyTMin.Date = DenverDailyPrcp.Date
	left join DenverDailySnwd
		on DenverDailyPrcp.Date = DenverDailySnwd.Date
	left join DenverDailySnow
		on DenverDailySnwd.Date = DenverDailySnow.Date;

DROP TABLE IF EXISTS DenverDailyTMax;
DROP TABLE IF EXISTS DenverDailyTMin;
DROP TABLE IF EXISTS DenverDailyPrcp;
DROP TABLE IF EXISTS DenverDailySnwd;
DROP TABLE IF EXISTS DenverDailySnow;

DROP TABLE IF EXISTS DenverDailyCrimeWeather;
create table DenverDailyCrimeWeather as 
	select 
		t1.Date,
		t1.Crime_Count,
		t2.TMax,
		t2.TMin,
		t2.Prcp,
		t2.Snwd,
		t2.Snow
	from DenverDAilyCrime t1 
	inner join DenverDailyWeather t2
		on t1.Date = t2.Date;
	

