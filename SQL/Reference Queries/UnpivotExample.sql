
SELECT Final_A.AHDCallID, C.DispCatName, Final_A.CatID, Final_A.RN
FROM Nadcs_dw.dbo.TicketingConAHDDispositionCategory C
	JOIN ( 
SELECT AHDCallID, CatID, DispCatID, ROW_NUMBER() OVER (PARTITION BY AHDCallID order by DispCatID DESC) as RN 

FROM (
	SELECT 
	  A.AHDCallID
	  ,C1.DispositionCatID AS DispCatID1
	  ,C1.DispCatName AS DispCatName1
	  ,C2.DispositionCatID AS DispCatID2
	  ,C2.DispCatName AS DispCatName2
	  ,C3.DispositionCatID AS DispCatID3
	  ,C3.DispCatName AS DispCatName3
	  ,C4.DispositionCatID AS DispCatID4
	  ,C4.DispCatName AS DispCatName4
	  ,C5.DispositionCatID AS DispCatID5
	  ,C5.DispCatName AS DispCatName5
	  ,C6.DispositionCatID AS DispCatID6
	  ,C6.DispCatName AS DispCatName6
	  ,C7.DispositionCatID AS DispCatID7
	  ,C7.DispCatName AS DispCatName7
	  ,C8.DispositionCatID AS DispCatID8
	  ,C8.DispCatName AS DispCatName8
	  ,C9.DispositionCatID AS DispCatID9
	  ,C9.DispCatName AS DispCatName9
	  ,C10.DispositionCatID AS DispCatID10
	  ,C10.DispCatName AS DispCatName10
	FROM Nadcs_dw.dbo.TicketingContractAHDCalls A
	JOIN Nadcs_dw.dbo.TicketingConAHDDispositionCategory C1 ON A.DispositionCatID = C1.DispositionCatID
	LEFT JOIN Nadcs_dw.dbo.TicketingConAHDDispositionCategory C2 ON C1.ParentDispositionCatID = C2.DispositionCatID
	LEFT JOIN Nadcs_dw.dbo.TicketingConAHDDispositionCategory C3 ON C2.ParentDispositionCatID = C3.DispositionCatID
	LEFT JOIN Nadcs_dw.dbo.TicketingConAHDDispositionCategory C4 ON C3.ParentDispositionCatID = C4.DispositionCatID
	LEFT JOIN Nadcs_dw.dbo.TicketingConAHDDispositionCategory C5 ON C4.ParentDispositionCatID = C5.DispositionCatID
	LEFT JOIN Nadcs_dw.dbo.TicketingConAHDDispositionCategory C6 ON C5.ParentDispositionCatID = C6.DispositionCatID
	LEFT JOIN Nadcs_dw.dbo.TicketingConAHDDispositionCategory C7 ON C6.ParentDispositionCatID = C7.DispositionCatID
	LEFT JOIN Nadcs_dw.dbo.TicketingConAHDDispositionCategory C8 ON C7.ParentDispositionCatID = C8.DispositionCatID
	LEFT JOIN Nadcs_dw.dbo.TicketingConAHDDispositionCategory C9 ON C8.ParentDispositionCatID = C9.DispositionCatID
	LEFT JOIN Nadcs_dw.dbo.TicketingConAHDDispositionCategory C10 ON C9.ParentDispositionCatID = C10.DispositionCatID
) as A

UNPIVOT
	(CatID
		FOR DispCatID IN (DispCatID1,DispCatID2,DispCatID3,DispCatID4,DispCatID5,DispCatID6,
			DispCatID7,DispCatID8,DispCatID9,DispCatID10)
	) unpiv2
) Final_A ON C.DispositionCatID = Final_A.CatID

ORDER BY AHDCallID, RN 