--- Get results based on hierarchy when all columns selected 


Select Distinct FiscalPeriodNameLong, 
BusinessGroup, 
SUM(C.ChatCompleted) Completed 
FROM NADCS_DW.dbo.vw_BPO_BusGrpType_Chat C
JOIN NADCS_DW.dbo.dim_date D ON C.date_ID = D.Date_ID
WHERE D.FiscalPeriodNameLong IN ('FY17 P10', 'FY17 P11')
GROUP BY ROLLUP (FiscalPeriodNameLong, C.BusinessGroup)

