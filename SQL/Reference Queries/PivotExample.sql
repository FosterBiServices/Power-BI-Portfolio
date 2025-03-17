DECLARE
	 @StartDate AS DATE
	,@EndDate AS DATE 

SET @StartDate = '2018-03-02'
SET	@EndDate = '2018-03-02';

SELECT 'TotalCompleted' as TotalCompletedbyQ,
[5620],[6213],[5565]
FROM 
(
SELECT K.KanaQueue_Id,
SUM(K.TotalCompleted) TC
FROM NADCS_DW.dbo.Fact_Kana K
JOIN NADCS_DW.dbo.Dim_KanaQueue Q ON K.KanaQueue_Id = Q.KanaQueue_ID
JOIN NADCS_DW.dbo.Dim_Date DD ON K.Date_ID = DD.Date_ID
WHERE 1 = 1 
AND DD.CalendarDate BETWEEN @startDate and @EndDate
GROUP BY K.KanaQueue_Id
) AS Kana

PIVOT(
	SUM(Kana.TC)
		FOR KanaQueue_ID IN ([5620],[6213],[5565])
			)
			 AS PVT 