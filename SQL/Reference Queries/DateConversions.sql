--Date Key to date = CONVERT(DATE, CAST(NULLIF(FBPF.skBillingPeriodEndDateKey, -1) AS VARCHAR(10)))

-- Date to DateKey = CONVERT(INT, CONVERT(VARCHAR(8), DE.StartOfCareDate, 112)) AS skSOCDateKey



--- Start of previous week 

 --SELECT DATEADD(wk, -1, DATEADD(wk, DATEDIFF(wk, 0,getdate()), -1)) [Week_Start_Date]

--- End of previous week
--SELECT DATEADD(wk, DATEDIFF(wk, 0, getdate()), -2) [Week_End_Date]
