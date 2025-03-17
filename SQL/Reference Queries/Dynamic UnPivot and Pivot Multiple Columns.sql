DECLARE @columns NVARCHAR(MAX), @sql NVARCHAR(MAX), @columns2 NVARCHAR(MAX);
SET @columns = N'';
SELECT @columns += N', SUM(pvt.[' + x.BusinessUnit + '])' + '[' + x.BusinessUnit + ']'
  FROM (SELECT DISTINCT BusinessUnit
		FROM gard.wfm.SmryWFMServiceLevelChat) AS x;
SET @columns2 = N'';
SELECT @columns2 += N', [' + y.BusinessUnit + ']'
  FROM (SELECT DISTINCT BusinessUnit
		FROM gard.wfm.SmryWFMServiceLevelChat) AS y;

SET @sql = N'
SELECT * 
FROM ( 

SELECT 
	FiscalYear, 
	FiscalPeriodName, 
	FiscalWeekOfPeriodName,
	CalendarDate,
	StartTime, 
	BusinessUnit,
	col AS Measure, 
	value	
FROM ( 
SELECT 
	FiscalYear, 
	FiscalPeriodName, 
	FiscalWeekOfPeriodName,
	Cast(CalendarDate as date) as CalendarDate,
	StartTime, 
	BusinessUnit, 	 
	CAST(CAST(Sum(NumChatSessionsAbandoned)*1.00 / NULLIF(Sum(NumCustomersEnteredServiceLine),0) AS DECIMAL(10,4))*100 AS DECIMAL(10,2)) AS AbnPercent,
	CAST(Sum(TotalSessionDuration)*1.00 / NULLIF(Sum(NumChatSessionsCompleted),0) AS DECIMAL(10,2))AS AHTActual, 
	CAST(Sum(TotalWaitTimeInServiceLine)*1.00 / NULLIF(Sum(NumCustomersEnteredServiceLine),0) AS DECIMAL(10,2)) AS AvgWait,
	CAST(Sum(NumChatSessionsAbandoned) AS DECIMAL(10,2)) AS ChatsAbandoned, 
	CAST(SUM(NumChatSessionsCompleted) AS DECIMAL(10,2)) AS ContactsAnswered, 
	CAST(Sum(NumChatSessionsWithinServiceLevel) AS DECIMAL(10,2)) AS ChatSessionsWithinServiceLevel, 
	CAST(SUM(NumCustomersEnteredServiceLine) AS DECIMAL(10,2)) AS ContactsOffered, 
	CAST(Max( [MaxWaitTimeInServiceLine] ) AS DECIMAL(10,2)) AS ChatMaxDelay, 
	CAST(CAST(Sum(NumChatSessionsWithinServiceLevel)*1.00 / Nullif(Sum(NumCustomersEnteredServiceLine),0) AS DECIMAL(10,4))*100 AS DECIMAL(10,2)) As ChatServiceLevel,
    CAST(SUM([TotalWaitTimeInServiceLine])*1.00 / Nullif(SUM(NumCustomersEnteredServiceLine),0)AS DECIMAL(10,2)) AS ChatASA 
 
FROM gard.wfm.SmryWFMServiceLevelChat
WHERE Cast(CalendarDate as date) = ''2019-08-26''
GROUP BY FiscalYear, 
	FiscalPeriodName, 
	FiscalWeekOfPeriodName,
	Cast(CalendarDate as date),
	StartTime, 
	BusinessUnit
) Orig

Unpivot( 
	value
		for col in (AbnPercent, AHTActual, AvgWait, ChatsAbandoned, ContactsAnswered, ChatSessionsWithinServiceLevel, ContactsOffered, ChatMaxDelay, ChatServiceLevel, ChatASA
		)
	) Unpiv
) Step2

Pivot ( 
	Sum(value) 
	for BusinessUnit in (' +STUFF(@columns2, 1,2, '') + ')
) Piv;'
Print @sql