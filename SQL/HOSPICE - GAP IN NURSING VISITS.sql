WITH LOC 
	AS ( 
    SELECT 
		l.PatientKey,
        l.PatientId,
        l.BranchKey, 
        l.BranchCode, 
        d.YearMonth,
        d.MonthFirstDay,
        l.StartOfCareDate,
		COALESCE(MAX(l.DischargeDate), CAST(GETDATE() as date)) as Dischargedate,
        DATEDIFF(DAY, MIN(l.StartOfCareDate), GETDATE()) AS LOS, 
		l.SourceSystem
    FROM factClientCareLevels l WITH (NOLOCK) 
    JOIN dimDates d WITH (NOLOCK) 
        ON l.EpisodeLevelOfCareDateKey = d.Id
    JOIN dimLevelOfCareType c WITH (NOLOCK) 
        ON l.BillableLevelOfCareTypeKey = c.Id
    LEFT JOIN vw_dimClientEpisodeVisitWithWorkerId v WITH (NOLOCK) 
        ON v.EpisodeId = l.EpisodeId 
        AND v.SourceSystem = l.SourceSystem 
        AND v.VisitDate = l.EpisodeLevelOfCareDate
    LEFT JOIN dimWorker w WITH (NOLOCK) 
        ON v.VisitAgentWorkerId = w.WorkerId 
        AND v.SourceSystem = w.SourceSystem
    LEFT JOIN ServiceCodes s WITH (NOLOCK) 
        ON v.VisitServiceCode = s.sccode 
        AND v.SourceSystem = s.SourceSystem
    GROUP BY l.PatientKey,
        l.PatientId,
        l.BranchKey, 
        l.BranchCode, 
        l.StartOfCareDate,
        d.YearMonth,
        d.MonthFirstDay, 
		l.SourceSystem
    HAVING 
        DATEDIFF(DAY, MIN(l.StartOfCareDate), COALESCE(MAX(l.DischargeDate), GETDATE())) > 30
		AND COALESCE(MIN(l.DischargeDate), CAST(GETDATE() as date)) BETWEEN DATEFROMPARTS(YEAR(GETDATE()) - 2, 1, 1) AND CAST(GETDATE() AS DATE) 
), 
Visits AS ( 
    SELECT 
        v.PatientId,
		DATEADD(MONTH, DATEDIFF(MONTH, 0, v.VisitDate), 0) as MonthFirstDay, 
        v.VisitDate,
        s.ScJdCode,
        w.JobDescriptionCode, 
		e.StartOfCareDate, 
		v.SourceSystem,
		LAG(v.VisitDate) OVER (PARTITION BY v.PatientId, v.SourceSystem ORDER BY v.VisitDate) AS PreviousVisitDate,
		DATEDIFF(DAY, LAG(v.VisitDate) OVER (PARTITION BY v.PatientId, e.StartofCareDate, v.SourceSystem ORDER BY v.VisitDate), v.VisitDate) as DaysSinceLastVisit
    FROM vw_dimClientEpisodeVisitWithWorkerId v WITH (NOLOCK)
	JOIN dimEpisode e WITH (NOLOCK)
		ON v.EpisodeId = e.EpisodeId
		and v.SourceSystem = e.SourceSystem
    LEFT JOIN dimWorker w WITH (NOLOCK) 
        ON v.VisitAgentWorkerId = w.WorkerId 
        AND v.SourceSystem = w.SourceSystem
    LEFT JOIN ServiceCodes s WITH (NOLOCK) 
        ON v.VisitServiceCode = s.sccode 
        AND v.SourceSystem = s.SourceSystem
    WHERE 
        (s.ScJdCode IN ('SN', 'MSW', 'MSWI') 
        OR (s.ScJdCode = 'RN' AND w.JobDescriptionCode <> 'LPN'))
)

SELECT     
	l.PatientKey,
	l.BranchKey,
    l.YearMonth,
	CONVERT(VARCHAR, v.VisitDate, 112) AS DateKey,
    l.StartOfCareDate,
    l.LOS,
	v.VisitDate,
    v.ScJdCode,
    v.JobDescriptionCode, 
	v.PreviousVisitDate,
	v.DaysSinceLastVisit,
	l.DischargeDate,
	CASE WHEN DATEDIFF(MONTH, V.VisitDate, l.DischargeDate) < 2 and DaysSinceLastVisit > 7 Then 1 else 0 end as GAPNum
FROM LOC l 
JOIN Visits V 
	ON l.PatientId = v.PatientId
	and l.SourceSystem = v.SourceSystem 
	and l.MonthFirstDay = v.MonthFirstDay