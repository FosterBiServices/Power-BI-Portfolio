DECLARE 
	@StartDateID int,  
	@EndDateID int

Set @StartDateID = (	
					SELECT Min(Date_ID) FROM NADCS_DW.dbo.dim_Date WHERE FiscalYear = 
								 ( SELECT FiscalYear /* - 3 */ FROM NADCS_DW.dbo.dim_Date WHERE CalendarDate = Cast(GetDate() as date) )
				)
Set @EndDateID = (SELECT Date_ID FROM NADCS_DW.dbo.dim_Date WHERE CalendarDate = Cast(GetDate() - 1 as date) ) 
; 

MERGE INTO [SandboxMG].[dbo].[SitelChatandEmailBilling] [T]
USING ( 

SELECT Cast(DD.CalendarDate as Date) As Calendardate
	, DD.Date_ID
	, Week_ID
	, Period_ID
	, Quarter_ID
	, FiscalYear
	, H.AssociateHierarchy_ID
	, H.Associate_LastName + ', ' + H.Associate_FirstName AS AssociateName
	, Manager1_LastName + ', ' + Manager1_FirstName AS Manager1Name
	, Manager2_LastName + ', ' + Manager2_FirstName AS Manager2Name
	, Manager3_LastName + ', ' + Manager3_FirstName AS Manager3Name
	, Manager4_LastName + ', ' + Manager4_FirstName AS Manager4Name
	, Manager5_LastName + ', ' + Manager5_FirstName AS Manager5Name
	, Manager6_LastName + ', ' + Manager6_FirstName AS Manager6Name
	, Manager7_LastName + ', ' + Manager7_FirstName AS Manager7Name
	, A.Network_ID
	, A.NetworkName
	, A.StaplesLocation_ID
	, A.StaplesLocationName
	, SUM(C.StaffedTime) AS ChatStaffedTime
	, SUM(C.Completed) as ChatCompleted
	, SUM(E.KanaStaffTime) AS EmailStaffedTime
	, SUM(E.TotalCompleted) AS EmailCompleted
	, SUM(P.AcdCalls) ACDCalls
	, SUM(P.Aux2)  Aux2
	, SUM(P.Aux8)  Aux8
	, ISNULL(SUM(C.StaffedTime),0) + ISNULL(SUM(E.KanaStaffTime),0) AS ChatEmailStaffTime
	, ISNULL(SUM(C.StaffedTime),0) + ISNULL(SUM(E.KanaStaffTime),0) - ISNULL(SUM(P.Aux8),0) AS ChatEmailMinusAux8
	, ISNULL(SUM(P.AvailTime),0) + ISNULL(SUM(P.ACDTime),0) + ISNULL(SUM(P.ACWAttached),0) + ISNULL(SUM(P.HoldTime),0) AS PhoneBilling
	, ISNULL(SUM(P.StaffTime),0) - ISNULL(SUM(P.Aux5),0) AS PhoneStaffTime
	, ISNULL(SUM(P.AvailTime),0) + ISNULL(SUM(P.ACDTime),0) + ISNULL(SUM(P.ACWAttached),0) + ISNULL(SUM(P.HoldTime),0) + ISNULL(SUM(E.KanaStaffTime),0) + ISNULL(SUM(C.StaffedTime),0) AS TotalBilling
	, ISNULL(SUM(P.AvailTime),0) + ISNULL(SUM(P.ACDTime),0) + ISNULL(SUM(P.ACWAttached),0) + ISNULL(SUM(P.HoldTime),0) + ISNULL(SUM(E.KanaStaffTime),0) + ISNULL(SUM(C.StaffedTime),0) - .17 AS TotalBillingMinus10MinBuffer


	FROM 
		NADCS_DW.dbo.Dim_AssociateHierarchy H (NOLOCK) 
	JOIN 
		NADCS_DW.dbo.Dim_Associate A (NOLOCK) ON H.Associate_ID = A.Associate_ID
	JOIN 
		NADCS_DW.dbo.Dim_Date DD (NOLOCK) ON H.Date_ID = DD.Date_ID
	LEFT JOIN
		NADCS_DW.dbo.Dim_PositionLevel PL (NOLOCK) ON A.PositionLevelCode = PL.PositionLevelCode
	LEFT JOIN
		-- SandboxMG.dbo.ChatAggregate_Load 
		( SELECT 
			CA.AssociateHierarchy_ID 
			, CA.Date_ID
			, SUM(CA.Completed) AS Completed
			, SUM(CA.StaffedTime) as StaffedTime
			FROM SandboxMG.dbo.ChatAggregate_Load CA (NOLOCK)
			WHERE CA.ConversationType IS NULL OR CA.ConversationType <> 'Proactive'
			GROUP BY CA.AssociateHierarchy_ID , CA.Date_ID
		) AS C ON H.AssociateHierarchy_ID = C.AssociateHierarchy_ID AND H.Date_ID = C.Date_ID 
	LEFT JOIN 
		-- SandboxMG.dbo.EmailAggregate_Load 
		( SELECT 
			EA.AssociateHierarchy_ID 
			, EA.Date_ID
			, SUM(EA.TotalCompleted) AS TotalCompleted
			, SUM(EA.KanaStaffTime) as KanaStaffTime
			FROM SandboxMG.dbo.EmailAggregate_Load EA (NOLOCK)
			GROUP BY EA.AssociateHierarchy_ID , EA.Date_ID
		) AS E ON H.AssociateHierarchy_ID = E.AssociateHierarchy_ID AND H.Date_ID = E.Date_ID
	LEFT JOIN 
		--SandboxMG.dbo.PhoneAggregate_Load 
		( SELECT 
			PA.AssociateHierarchy_ID 
			, PA.Date_ID
			, SUM(PA.ACDCalls)  ACDCalls
			, SUM(PA.ACDTime)  ACDTime
			, SUM(PA.HoldTime)  HoldTime
			, SUM(PA.Aux2)  Aux2
			, SUM(PA.Aux8)  Aux8
			, SUM(PA.ACWAttached)  ACWAttached
			, SUM(PA.Aux5)  Aux5
			, SUM(PA.StaffTime)  StaffTime
			, SUM(PA.AvailTime)  AvailTime
			FROM SandboxMG.dbo.PhoneAggregate_Load PA (NOLOCK)
			GROUP BY PA.AssociateHierarchy_ID , PA.Date_ID
		) AS P ON H.AssociateHierarchy_ID = P.AssociateHierarchy_ID AND H.Date_ID = P.Date_ID

WHERE 1 = 1  
	AND DD.Date_ID BETWEEN @StartDateID AND @EndDateID
	AND PL.IsDataGenerator = 1
	AND A.StaplesLocation_ID IN (27,30)
	AND A.Network_ID IN (1,2,3,11,13) 
GROUP BY 
	Cast(DD.CalendarDate as Date)
	, DD.Date_ID
	, Week_ID
	, Period_ID
	, Quarter_ID
	, FiscalYear
	, H.AssociateHierarchy_ID
	, A.Network_ID
	, A.NetworkName
	, A.StaplesLocation_ID
	, A.StaplesLocationName
	, H.Associate_LastName + ', ' + H.Associate_FirstName
	, Manager1_LastName + ', ' + Manager1_FirstName
	, Manager2_LastName + ', ' + Manager2_FirstName
	, Manager3_LastName + ', ' + Manager3_FirstName
	, Manager4_LastName + ', ' + Manager4_FirstName
	, Manager5_LastName + ', ' + Manager5_FirstName
	, Manager6_LastName + ', ' + Manager6_FirstName
	, Manager7_LastName + ', ' + Manager7_FirstName
HAVING 
	ISNULL(SUM(C.StaffedTime),0) + ISNULL(SUM(E.KanaStaffTime),0) + ISNULL(SUM(C.Completed),0) + ISNULL(SUM(E.TotalCompleted),0)  > 0 

) [S]
	 ON 
		T.Calendardate = S.Calendardate
		AND T.AssociateHierarchy_ID = S.AssociateHierarchy_ID
		AND T.Network_ID = S.Network_ID
		AND T.StaplesLocation_ID = S.StaplesLocation_ID
		AND T.Week_ID	= S.Week_ID
		AND T.Period_ID = S.Period_ID
		AND T.Quarter_ID = S.Quarter_ID
		AND T.FiscalYear = S.FiscalYear

WHEN MATCHED Then UPDATE 
	SET 
		T.Calendardate = S.Calendardate
		, T.Date_ID = S.Date_ID
		, T.Week_ID	= S.Week_ID
		, T.Period_ID = S.Period_ID
		, T.Quarter_ID = S.Quarter_ID
		, T.FiscalYear = S.FiscalYear
		, T.AssociateHierarchy_ID = S.AssociateHierarchy_ID
		, T.AssociateName = S.AssociateName
		, T.Manager1Name = S.Manager1Name
		, T.Manager2Name = S.Manager2Name
		, T.Manager3Name = S.Manager3Name
		, T.Manager4Name = S.Manager4Name
		, T.Manager5Name = S.Manager5Name
		, T.Manager6Name = S.Manager6Name
		, T.Manager7Name = S.Manager7Name
		, T.Network_ID = S.Network_ID
		, T.StaplesLocation_ID = S.StaplesLocation_ID
		, T.NetworkName = S.NetworkName
		, T.StaplesLocationName = S.StaplesLocationName
		, T.ChatStaffedTime = S.ChatStaffedTime
		, T.ChatCompleted = S.ChatCompleted
		, T.EmailStaffedTime = S.EmailStaffedTime
		, T.EmailCompleted = S.EmailCompleted
		, T.PhoneStaffTime = S.PhoneStaffTime
		, T.AcdCalls = S.AcdCalls
		, T.Aux2 = S.Aux2
		, T.Aux8 = S.Aux8
		, T.ChatEmailStaffTime = S.ChatEmailStaffTime
		, T.ChatEmailMinusAux8 = S.ChatEmailMinusAux8
		, T.PhoneBilling = S.PhoneBilling
		, T.TotalBilling = S.TotalBilling
		, T.TotalBillingMinus10MinBuffer = S.TotalBillingMinus10MinBuffer

WHEN NOT MATCHED THEN INSERT 
	( 
		Calendardate
		, Date_ID
		, Week_ID
		, Period_ID
		, Quarter_ID
		, FiscalYear
		, AssociateHierarchy_ID
		, AssociateName
		, Manager1Name
		, Manager2Name
		, Manager3Name
		, Manager4Name
		, Manager5Name
		, Manager6Name
		, Manager7Name
		, Network_ID 
		, NetworkName 
		, StaplesLocation_ID
		, StaplesLocationName 
		, ChatStaffedTime
		, ChatCompleted
		, EmailStaffedTime
		, EmailCompleted
		, AcdCalls
		, PhoneStaffTime
		, Aux2
		, Aux8
		, ChatEmailStaffTime
		, ChatEmailMinusAux8
		, PhoneBilling
		, TotalBilling
		, TotalBillingMinus10MinBuffer
)

VALUES (
	
		S.Calendardate
		, S.Date_ID
		, S.Week_ID
		, S.Period_ID
		, S.Quarter_ID
		, S.FiscalYear
		, S.AssociateHierarchy_ID
		, S.AssociateName
		, S.Manager1Name
		, S.Manager2Name
		, S.Manager3Name
		, S.Manager4Name
		, S.Manager5Name
		, S.Manager6Name
		, S.Manager7Name
		, S.Network_ID
		, S.NetworkName
		, S.StaplesLocation_ID
		, S.StaplesLocationName
		, S.ChatStaffedTime
		, S.ChatCompleted
		, S.EmailStaffedTime
		, S.EmailCompleted
		, S.AcdCalls
		, S.PhoneStaffTime
		, S.Aux2
		, S.Aux8
		, S.ChatEmailStaffTime
		, S.ChatEmailMinusAux8
		, S.PhoneBilling
		, S.TotalBilling
		, S.TotalBillingMinus10MinBuffer
	)
; 
