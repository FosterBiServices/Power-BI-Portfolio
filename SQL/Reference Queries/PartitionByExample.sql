Select Distinct FiscalPeriodNameLong, 
BusinessGroup,
SUM(C.ChatCompleted) CC,
SUM(SUM(C.ChatCompleted)) OVER (PARTITION by C.BusinessGroup) CCbyBG
FROM NADCS_DW.dbo.vw_BPO_BusGrpType_Chat C
JOIN NADCS_DW.dbo.dim_date D ON C.date_ID = D.Date_ID
WHERE D.FiscalPeriodNameLong >= 'FY17 P11'
GROUP BY 
FiscalPeriodNameLong, 
BusinessGroup

