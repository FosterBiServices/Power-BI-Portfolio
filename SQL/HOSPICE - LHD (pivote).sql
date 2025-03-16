WITH HoursCode_CTE
AS (
	/****** Script for SelectTopNRows command from SSMS  ******/
	SELECT id
		,[LH Detail]
		,[EarningsCode] --	EarningsCodeDescription	CreatedDateTime	ModifiedDateTime
	FROM (
		SELECT id
			,CASE 
				WHEN [EarningsCode] IN (
						'1'
						,'12'
						,'13'
						,'148'
						,'150'
						,'154'
						,'19'
						,'191'
						,'192'
						,'193'
						,'20'
						,'205'
						,'206'
						,'207'
						,'208'
						,'209'
						,'21'
						,'210'
						,'211'
						,'212'
						,'213'
						,'214'
						,'215'
						,'222'
						,'224'
						,'225'
						,'226'
						,'229'
						,'231'
						,'234'
						,'235'
						,'238'
						,'239'
						,'240'
						,'241'
						,'242'
						,'243'
						,'244'
						,'27'
						,'275'
						,'278'
						,'28'
						,'282'
						,'283'
						,'284'
						,'285'
						,'287'
						,'288'
						,'289'
						,'29'
						,'292'
						,'293'
						,'296'
						,'297'
						,'298'
						,'299'
						,'300'
						,'301'
						,'302'
						,'311'
						,'312'
						,'314'
						,'316'
						,'317'
						,'33'
						,'38'
						,'43'
						,'51'
						,'705'
						,'706'
						,'707'
						,'710'
						,'711'
						,'712'
						,'713'
						,'714'
						,'715'
						,'716'
						,'717'
						,'719'
						,'721'
						,'722'
						,'723'
						,'730'
						,'766'
						,'794'
						,'807'
						,'CIN'
						,'FR'
						,'N'
						,'sop'
						,'SLP'
						,'VA'
						,'X'
						)
					THEN 'REG HOURS'
				WHEN [EarningsCode] IN (
						'2'
						,'329'
						,'34'
						,'35'
						,'37'
						,'41'
						,'Z'
						)
					THEN 'OT HOURS'
				WHEN [EarningsCode] IN (
						'152'
						,'308'
						,'541'
						,'542'
						,'558'
						,'736'
						,'740'
						,'768'
						,'781'
						,'805'
						,'817'
						,'MEN'
						,'T'
						,'TRI'
						,'TR2'
						,'TR3'
						)
					THEN 'TRN HOURS'
				WHEN [EarningsCode] IN (
						'45'
						,'P'
						,'P70'
						,'P75'
						,'V'
						,'V75'
						)
					THEN 'VAC HOURS'
				WHEN [EarningsCode] IN (
						'S'
						,'SK1'
						,'SK2'
						,'SK8'
						)
					THEN 'SICK HOURS'
				WHEN [EarningsCode] IN (
						'FHO'
						,'H'
						,'HOW'
						)
					THEN 'HOL HOURS'
				WHEN [EarningsCode] IN (
						'32'
						,'44'
						,'8'
						,'8'
						,'BEN'
						,'CHR'
						,'CNT'
						,'COM'
						,'CON'
						,'DIS'
						,'DVV'
						,'GRW'
						,'l'
						,'MID'
						,'PRO'
						,'GPI'
						,'RET'
						,'SGN'
						,'SHE'
						,'SLS'
						,'SPY'
						,'STE'
						,'UNI'
						)
					THEN 'BON HOURS'
				WHEN [EarningsCode] IN (
						'116'
						,'177'
						,'199'
						,'220'
						,'221'
						,'249'
						,'274'
						,'303'
						,'307'
						,'322'
						,'324'
						,'328'
						,'559'
						,'828'
						,'830'
						,'FYP'
						,'HOW'
						,'Sl'
						,'SIO'
						,'Sli'
						,'S12'
						,'SIS'
						,'S14'
						,'S15'
						,'S16'
						,'S17'
						,'58'
						,'SO'
						,'S2'
						,'S20'
						,'S23'
						,'S24'
						,'SS'
						,'sa'
						,'S5'
						,'S6'
						,'S7'
						,'S8'
						,'s9'
						)
					THEN 'PREM HOURS'
				WHEN [EarningsCode] IN ('X')
					THEN 'CST HOURS'
				WHEN [EarningsCode] IN ('D')
					THEN 'DBL HOURS'
				WHEN [EarningsCode] IN (
						'R'
						,'U'
						)
					THEN 'RTO HOURS'
				WHEN [EarningsCode] IN (
						'36'
						,'39'
						,'40'
						,'500'
						,'501'
						,'503'
						,'505'
						,'506'
						,'507'
						,'508'
						,'509'
						,'510'
						,'511'
						,'512'
						,'513'
						,'516'
						,'517'
						,'518'
						,'519'
						,'537'
						,'538'
						,'543'
						,'548'
						,'549'
						,'726'
						,'729'
						,'737'
						,'738'
						,'745'
						,'746'
						,'757'
						,'759'
						,'760'
						,'761'
						,'762'
						,'764'
						,'773'
						,'776'
						,'777'
						,'778'
						,'785'
						,'787'
						,'788'
						,'793'
						,'797'
						,'800'
						,'806'
						,'809'
						,'810'
						,'813'
						,'821'
						,'DEV'
						,'E'
						,'MDV'
						,'NPV'
						,'PPE'
						,'PRV'
						,'RNA'
						)
					THEN 'VST HOURS'
				WHEN [EarningsCode] IN (
						'158'
						,'173'
						,'174'
						,'175'
						,'176'
						,'514'
						,'515'
						,'539'
						,'540'
						,'544'
						,'545'
						,'550'
						,'552'
						,'553'
						,'555'
						,'557'
						,'700'
						,'701'
						,'702'
						,'708'
						,'709'
						,'720'
						,'724'
						,'725'
						,'727'
						,'728'
						,'731'
						,'733'
						,'735'
						,'741'
						,'742'
						,'743'
						,'744'
						,'747'
						,'748'
						,'749'
						,'750'
						,'751'
						,'753'
						,'754'
						,'755'
						,'756'
						,'758'
						,'763'
						,'765'
						,'767'
						,'769'
						,'770'
						,'771'
						,'772'
						,'774'
						,'775'
						,'779'
						,'780'
						,'782'
						,'783'
						,'786'
						,'790'
						,'791'
						,'792'
						,'795'
						,'796'
						,'799'
						,'801'
						,'803'
						,'804'
						,'808'
						,'811'
						,'812'
						,'814'
						,'815'
						,'816'
						,'818'
						,'819'
						,'820'
						,'822'
						,'823'
						,'829'
						,'831'
						,'832'
						,'833'
						,'o'
						,'poc'
						)
					THEN 'ONC HOURS'
				WHEN [EarningsCode] IN ('7')
					THEN 'WCP HOURS'
				ELSE 'OTR HOURS'
				END AS [LH Detail]
			,[EarningsCode]
			,[EarningsCodeDescription]
			,[CreatedDateTime]
			,[ModifiedDateTime]
		FROM [dbo].[dimJobEarningCode]
		) EarningType
	)
	,Hours_CTE
AS (
	SELECT fche.[PayGroup]
		,[CheckDate]
		,de.EmployeeId
		,CASE 
			WHEN EarningCodeKey = - 1
				AND RowNumber = 1
				THEN 'REG HOURS'
			WHEN EarningCodeKey = - 1
				AND RowNumber = 2
				THEN 'OT HOURS'
			ELSE [LH Detail]
			END AS [LH Detail]
		,[EarningCode]
		,[CheckNumber]
		,SUM([Hours]) Hours
	FROM [dbo].[factCheckHoursEarnings](NOLOCK) fche
	JOIN [dbo].[dimJobEarningCode](NOLOCK) ec ON fche.EarningCodeKey = ec.Id
	JOIN dbo.dimemployeepaygroup(NOLOCK) deg ON fche.PayGroupKey = deg.Id
	JOIN [dbo].[DimEmployee](NOLOCK) de ON fche.EmployeeKey = de.id
	JOIN dimLocationHierarchy(NOLOCK) lh ON de.ReportingLocation = lh.Location
	LEFT JOIN HoursCode_CTE c ON fche.EarningCodekey = c.id
	WHERE 1 = 1
		AND checkdate BETWEEN '2025-01-01'
			AND '2025-01-31'
		AND deg.currentflag = 'Y'
		AND EntryNumber <> '0'
		AND lh.OperationsOfficer = '09145'
	GROUP BY fche.[PayGroup]
		,[CheckDate]
		,de.EmployeeId
		,CASE 
			WHEN EarningCodeKey = - 1
				AND RowNumber = 1
				THEN 'REG HOURS'
			WHEN EarningCodeKey = - 1
				AND RowNumber = 2
				THEN 'OT HOURS'
			ELSE [LH Detail]
			END
		,[EarningCode]
		,[CheckNumber]
	)
	,EarningsCode_CTE
AS (
	/****** Script for SelectTopNRows command from SSMS  ******/
	SELECT id
		,[LH Detail]
		,[EarningsCode] --	EarningsCodeDescription	CreatedDateTime	ModifiedDateTime
	FROM (
		SELECT id
			,CASE 
				WHEN [EarningsCode] IN (
						'1'
						,'12'
						,'13'
						,'148'
						,'150'
						,'154'
						,'19'
						,'191'
						,'192'
						,'193'
						,'20'
						,'205'
						,'206'
						,'207'
						,'208'
						,'209'
						,'21'
						,'210'
						,'211'
						,'212'
						,'213'
						,'214'
						,'215'
						,'222'
						,'224'
						,'225'
						,'226'
						,'229'
						,'231'
						,'234'
						,'235'
						,'238'
						,'239'
						,'240'
						,'241'
						,'242'
						,'243'
						,'244'
						,'27'
						,'275'
						,'278'
						,'28'
						,'282'
						,'283'
						,'284'
						,'285'
						,'287'
						,'288'
						,'289'
						,'29'
						,'292'
						,'293'
						,'296'
						,'297'
						,'298'
						,'299'
						,'300'
						,'301'
						,'302'
						,'311'
						,'312'
						,'314'
						,'316'
						,'317'
						,'33'
						,'38'
						,'43'
						,'51'
						,'705'
						,'706'
						,'707'
						,'710'
						,'711'
						,'712'
						,'713'
						,'714'
						,'715'
						,'716'
						,'717'
						,'719'
						,'721'
						,'722'
						,'723'
						,'730'
						,'766'
						,'794'
						,'807'
						,'CIN'
						,'FR'
						,'N'
						,'sop'
						,'SLP'
						,'VA'
						,'X'
						)
					THEN 'REG ERN'
				WHEN [EarningsCode] IN (
						'2'
						,'329'
						,'34'
						,'35'
						,'37'
						,'41'
						,'Z'
						)
					THEN 'OT ERN'
				WHEN [EarningsCode] IN (
						'152'
						,'308'
						,'541'
						,'542'
						,'558'
						,'736'
						,'740'
						,'768'
						,'781'
						,'805'
						,'817'
						,'MEN'
						,'T'
						,'TRI'
						,'TR2'
						,'TR3'
						)
					THEN 'TRN ERN'
				WHEN [EarningsCode] IN (
						'45'
						,'P'
						,'P70'
						,'P75'
						,'V'
						,'V75'
						)
					THEN 'VAC ERN'
				WHEN [EarningsCode] IN (
						'S'
						,'SK1'
						,'SK2'
						,'SK8'
						)
					THEN 'SICK ERN'
				WHEN [EarningsCode] IN (
						'FHO'
						,'H'
						,'HOW'
						)
					THEN 'HOL ERN'
				WHEN [EarningsCode] IN (
						'32'
						,'44'
						,'8'
						,'8'
						,'BEN'
						,'CHR'
						,'CNT'
						,'COM'
						,'CON'
						,'DIS'
						,'DVV'
						,'GRW'
						,'l'
						,'MID'
						,'PRO'
						,'GPI'
						,'RET'
						,'SGN'
						,'SHE'
						,'SLS'
						,'SPY'
						,'STE'
						,'UNI'
						)
					THEN 'BON ERN'
				WHEN [EarningsCode] IN (
						'116'
						,'177'
						,'199'
						,'220'
						,'221'
						,'249'
						,'274'
						,'303'
						,'307'
						,'322'
						,'324'
						,'328'
						,'559'
						,'828'
						,'830'
						,'FYP'
						,'HOW'
						,'Sl'
						,'SIO'
						,'Sli'
						,'S12'
						,'SIS'
						,'S14'
						,'S15'
						,'S16'
						,'S17'
						,'58'
						,'SO'
						,'S2'
						,'S20'
						,'S23'
						,'S24'
						,'SS'
						,'sa'
						,'S5'
						,'S6'
						,'S7'
						,'S8'
						,'s9'
						)
					THEN 'PREM ERN'
				WHEN [EarningsCode] IN ('X')
					THEN 'CST ERN'
				WHEN [EarningsCode] IN ('D')
					THEN 'DBL ERN'
				WHEN [EarningsCode] IN (
						'R'
						,'U'
						)
					THEN 'RTO ERN'
				WHEN [EarningsCode] IN (
						'36'
						,'39'
						,'40'
						,'500'
						,'501'
						,'503'
						,'505'
						,'506'
						,'507'
						,'508'
						,'509'
						,'510'
						,'511'
						,'512'
						,'513'
						,'516'
						,'517'
						,'518'
						,'519'
						,'537'
						,'538'
						,'543'
						,'548'
						,'549'
						,'726'
						,'729'
						,'737'
						,'738'
						,'745'
						,'746'
						,'757'
						,'759'
						,'760'
						,'761'
						,'762'
						,'764'
						,'773'
						,'776'
						,'777'
						,'778'
						,'785'
						,'787'
						,'788'
						,'793'
						,'797'
						,'800'
						,'806'
						,'809'
						,'810'
						,'813'
						,'821'
						,'DEV'
						,'E'
						,'MDV'
						,'NPV'
						,'PPE'
						,'PRV'
						,'RNA'
						)
					THEN 'VST ERN'
				WHEN [EarningsCode] IN (
						'158'
						,'173'
						,'174'
						,'175'
						,'176'
						,'514'
						,'515'
						,'539'
						,'540'
						,'544'
						,'545'
						,'550'
						,'552'
						,'553'
						,'555'
						,'557'
						,'700'
						,'701'
						,'702'
						,'708'
						,'709'
						,'720'
						,'724'
						,'725'
						,'727'
						,'728'
						,'731'
						,'733'
						,'735'
						,'741'
						,'742'
						,'743'
						,'744'
						,'747'
						,'748'
						,'749'
						,'750'
						,'751'
						,'753'
						,'754'
						,'755'
						,'756'
						,'758'
						,'763'
						,'765'
						,'767'
						,'769'
						,'770'
						,'771'
						,'772'
						,'774'
						,'775'
						,'779'
						,'780'
						,'782'
						,'783'
						,'786'
						,'790'
						,'791'
						,'792'
						,'795'
						,'796'
						,'799'
						,'801'
						,'803'
						,'804'
						,'808'
						,'811'
						,'812'
						,'814'
						,'815'
						,'816'
						,'818'
						,'819'
						,'820'
						,'822'
						,'823'
						,'829'
						,'831'
						,'832'
						,'833'
						,'o'
						,'poc'
						)
					THEN 'ONC ERN'
				WHEN [EarningsCode] IN ('7')
					THEN 'WCP ERN'
				ELSE 'OTR ERN'
				END AS [LH Detail]
			,[EarningsCode]
			,[EarningsCodeDescription]
			,[CreatedDateTime]
			,[ModifiedDateTime]
		FROM [dbo].[dimJobEarningCode]
		) EarningType
	)
	,Earnings_CTE
AS (
	SELECT fche.[PayGroup]
		,[CheckDate]
		,de.EmployeeId
		,CASE 
			WHEN EarningCodeKey = - 1
				AND RowNumber = 1
				THEN 'REG ERN'
			WHEN EarningCodeKey = - 1
				AND RowNumber = 2
				THEN 'OT ERN'
			ELSE [LH Detail]
			END AS [LH Detail]
		,[EarningCode]
		,[CheckNumber]
		,SUM([Earnings]) Earnings
	FROM [dbo].[factCheckHoursEarnings](NOLOCK) fche
	JOIN [dbo].[dimJobEarningCode](NOLOCK) ec ON fche.EarningCodeKey = ec.Id
	JOIN dbo.dimemployeepaygroup(NOLOCK) deg ON fche.PayGroupKey = deg.Id
	JOIN [dbo].[DimEmployee](NOLOCK) de ON fche.EmployeeKey = de.id
	JOIN dimLocationHierarchy(NOLOCK) lh ON de.ReportingLocation = lh.Location
	LEFT JOIN EarningsCode_CTE c ON fche.EarningCodekey = c.id
	WHERE 1 = 1
		AND checkdate BETWEEN '2025-01-01'
			AND '2025-01-31'
		AND deg.currentflag = 'Y'
		AND EntryNumber <> '0'
	GROUP BY fche.[PayGroup]
		,[CheckDate]
		,de.EmployeeId
		,CASE 
			WHEN EarningCodeKey = - 1
				AND RowNumber = 1
				THEN 'REG ERN'
			WHEN EarningCodeKey = - 1
				AND RowNumber = 2
				THEN 'OT ERN'
			ELSE [LH Detail]
			END
		,[EarningCode]
		,[CheckNumber]
	)
	,Pivoted_Hours
AS (
	SELECT *
	FROM (
		SELECT PayGroup
			,CheckDate
			,EmployeeID
			,CheckNumber
			,[LH Detail]
			,Hours
		FROM Hours_CTE
		) AS SourceTable
	PIVOT(SUM(Hours) FOR [LH Detail] IN (
				[REG HOURS]
				,[VAC HOURS]
				,[TRN HOURS]
				,[OT HOURS]
				,[ONC HOURS]
				,[DBL HOURS]
				,[PREM HOURS]
				,[VST HOURS]
				,[HOL HOURS]
				,[SICK HOURS]
				,[BON HOURS]
				,[OTR HOURS]
				,[CST HOURS]
				,[RTO HOURS]
				,[WCP HOURS]
				)) AS PivotHours
	)
	,Pivoted_Earnings
AS (
	SELECT *
	FROM (
		SELECT PayGroup
			,CheckDate
			,EmployeeID
			,CheckNumber
			,[LH Detail]
			,Earnings
		FROM Earnings_CTE
		) AS SourceTable
	PIVOT(SUM(Earnings) FOR [LH Detail] IN (
				[REG ERN]
				,[VAC ERN]
				,[OT ERN]
				,[TRN ERN]
				,[ONC ERN]
				,[VST ERN]
				,[DBL ERN]
				,[PREM ERN]
				,[HOL ERN]
				,[SICK ERN]
				,[BON ERN]
				,[OTR ERN]
				,[CST ERN]
				,[RTO ERN]
				,[WCP ERN]
				)) AS PivotEarnings
	)
SELECT h.PayGroup
	,h.CheckDate
	,h.EmployeeID
	,h.CheckNumber
	,
	/* HOURS */
	COALESCE(SUM(h.[REG HOURS]), 0) AS [REG HOURS]
	,COALESCE(SUM(h.[OT HOURS]), 0) AS [OT HOURS]
	,COALESCE(SUM(h.[TRN HOURS]), 0) AS [TRN HOURS]
	,COALESCE(SUM(h.[VAC HOURS]), 0) AS [VAC HOURS]
	,COALESCE(SUM(h.[SICK HOURS]), 0) AS [SICK HOURS]
	,COALESCE(SUM(h.[HOL HOURS]), 0) AS [HOL HOURS]
	,COALESCE(SUM(h.[BON HOURS]), 0) AS [BON HOURS]
	,COALESCE(SUM(h.[PREM HOURS]), 0) AS [PREM HOURS]
	,COALESCE(SUM(h.[CST HOURS]), 0) AS [CST HOURS]
	,COALESCE(SUM(h.[DBL HOURS]), 0) AS [DBL HOURS]
	,COALESCE(SUM(h.[RTO HOURS]), 0) AS [RTO HOURS]
	,COALESCE(SUM(h.[VST HOURS]), 0) AS [VST HOURS]
	,COALESCE(SUM(h.[ONC HOURS]), 0) AS [ONC HOURS]
	,COALESCE(SUM(h.[WCP HOURS]), 0) AS [WCP HOURS]
	,COALESCE(SUM(h.[OTR HOURS]), 0) AS [OTR HOURS]
	,
	/* EARNINGS */
	COALESCE(SUM(e.[REG ERN]), 0) AS [REG ERN]
	,COALESCE(SUM(e.[OT ERN]), 0) AS [OT ERN]
	,COALESCE(SUM(e.[TRN ERN]), 0) AS [TRN ERN]
	,COALESCE(SUM(e.[VAC ERN]), 0) AS [VAC ERN]
	,COALESCE(SUM(e.[SICK ERN]), 0) AS [SICK ERN]
	,COALESCE(SUM(e.[HOL ERN]), 0) AS [HOL ERN]
	,COALESCE(SUM(e.[BON ERN]), 0) AS [BON ERN]
	,COALESCE(SUM(e.[PREM ERN]), 0) AS [PREM ERN]
	,COALESCE(SUM(e.[CST ERN]), 0) AS [CST ERN]
	,COALESCE(SUM(e.[DBL ERN]), 0) AS [DBL ERN]
	,COALESCE(SUM(e.[RTO ERN]), 0) AS [RTO ERN]
	,COALESCE(SUM(e.[VST ERN]), 0) AS [VST ERN]
	,COALESCE(SUM(e.[ONC ERN]), 0) AS [ONC ERN]
	,COALESCE(SUM(e.[WCP ERN]), 0) AS [WCP ERN]
	,COALESCE(SUM(e.[OTR ERN]), 0) AS [OTR ERN]
FROM Pivoted_Hours h
JOIN Pivoted_Earnings e ON h.EmployeeId = e.EmployeeId
	AND h.CheckDate = e.CheckDate
	AND h.checknumber = e.checknumber
	AND h.PayGroup = e.PayGroup
WHERE 1 = 1 
	--and h.EmployeeiD = '0556082'
GROUP BY h.PayGroup
	,h.CheckDate
	,h.EmployeeID
	,h.CheckNumber
