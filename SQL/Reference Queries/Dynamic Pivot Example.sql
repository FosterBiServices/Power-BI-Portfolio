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
SELECT FiscalYear, FiscalPeriodName, FiscalWeekOfPeriodName,Cast(CalendarDate as date) as Calendardate, StartTime,' + STUFF(@columns, 1, 2, '') + ' 
FROM (
SELECT *
FROM gard.wfm.SmryWFMServiceLevelChat
WHERE Cast(CalendarDate as date) = ''2019-08-26''
) AS A

PIVOT (
	SUM(NumCustomersEnteredServiceLine)
		FOR BusinessUnit IN ('
  + STUFF(@columns2, 1, 2, '')
  + ')
) AS pvt
GROUP BY FiscalYear, FiscalPeriodName, FiscalWeekOfPeriodName,Cast(CalendarDate as date), StartTime;'
----PRINT @sql;
EXEC sp_executesql @sql;
