WITH LOS
AS (
	SELECT episodeKey, episodeId, PatientKey, PatientId, LocationHierarchyKey, SourceSystem
	FROM dbo.myfacttable WITH (NOLOCK)
	WHERE dischargeDateKey <> - 1
		AND IsDeleted = 0
		AND DATEDIFF(DAY, StartofCareDate, DischargeDate) + 1 >= 3
	), DateOfDeath
AS (
	SELECT CeddEpiId AS EpisodeId, CeddDateofDeath AS DateOfDeath, SourceSystem, dd.DateKey
	FROM myfacttabledod dod WITH (NOLOCK)
	JOIN dimDates dd WITH (NOLOCK)
		ON dod.CeddDateofDeath = dd.DateValue
	), LOC
AS (
	SELECT DISTINCT l.EpisodeKey, l.PatientKey, l.LocationHierarchyKey, l.BranchKey, l.EpisodeId, l.
		SourceSystem, d.DateOfDeath, d.DateKey, l.EpisodeLevelOfCareDate
	FROM myfacttablel l WITH (NOLOCK)
	JOIN DateOfDeath d
		ON l.SourceSystem = d.SourceSystem
			AND L.EpisodeId = d.EpisodeId
	WHERE EXISTS (
			SELECT 1
			FROM dimLevelOfCareType c WITH (NOLOCK)
			WHERE c.LevelOfCareDescription = 'ROUTINE HOME CARE'
			)
	), HVLDL
AS (
	SELECT c.EpisodeKey, c.PatientKey, c.LocationHierarchyKey, c.BranchKey, c.EpisodeId, c.DateKey, c.
		SourceSystem, c.DateOfDeath, s.PatientId, c.EpisodeLevelOfCareDate
	FROM LOC c
	JOIN LOS s
		ON c.EpisodeId = s.EpisodeId
			AND c.SourceSystem = s.SourceSystem
	), visits_CTE
AS (
	SELECT h.PatientKey, h.BranchKey, h.EpisodeKey, h.EpisodeId, h.SourceSystem, h.DateOfDeath, h.LocationHierarchyKey, 
		h.DateKey, v.ClientEpisodeVisitId, v.VisitDate, s.ScJdCode, CASE 
			WHEN EpisodeLevelOfCareDate BETWEEN DATEADD(DAY, - 2, h.DateOfDeath)
					AND h.DateOfDeath
				THEN 1
			ELSE 0
			END AS HVLDLEligible
	FROM HVLDL h
	LEFT JOIN vw_myfacttable v WITH (NOLOCK)
		ON v.EpisodeId = h.EpisodeId
			AND v.SourceSystem = h.SourceSystem
			AND v.VisitDate = h.EpisodeLevelOfCareDate
	LEFT JOIN mydimtables s WITH (NOLOCK)
		ON v.VisitServiceCode = s.sccode
			AND v.SourceSystem = s.SourceSystem
	WHERE s.ScJdCode IN (
			'MSW',
			'RN',
			'MSWI'
			)
		AND v.ScheduledVisitStatusDescription = 'Completed'
		AND v.VisitServiceType NOT IN (
			'HOSPICE BEREAVEMENT PHONE CALL',
			'HOSPICE PHONE VISIT',
			'HOSPICE TRANSITION ADD-ON',
			'HOSPICE MEDICAL TREATMENT',
			'HOSPICE TRANSITION',
			'HOSPICE DISCHARGE (W/O VISIT)',
			'MEDICAL TREATMENT',
			'HOSPICE DEATH AT HOME'
			)
		AND EXISTS (
			SELECT 1
			FROM dbo.mydimtablee d WITH (NOLOCK)
			WHERE d.EpisodeId = v.EpisodeId
				AND d.SourceSystem = v.SourceSystem
				AND d.ServiceLine = 'Hospice'
			)
		AND EXISTS (
			SELECT 1
			FROM dbo.mydatetable d WITH (NOLOCK)
			WHERE d.DateValue = h.DateOfDeath
				AND d.DateValue BETWEEN DATEFROMPARTS(YEAR(GETDATE()) - 2, 1, 1)
					AND CAST(GETDATE() - 1 AS DATE)
			)
		AND EXISTS (
			SELECT 1
			FROM dbo.mydimtabled d WITH (NOLOCK)
			WHERE d.BranchCode = v.ClientEpisodeVisitBranchCode
				AND d.SourceSystem = v.SourceSystem
			)
	), AggregatedVisits
AS (
	SELECT PatientKey, BranchKey, EpisodeKey, EpisodeId, SourceSystem, DateOfDeath, LocationHierarchyKey, DateKey, 
		VisitDate, COUNT(*) AS VisitCount
	FROM visits_CTE
	WHERE HVLDLEligible = 1
	GROUP BY PatientKey, BranchKey, EpisodeKey, EpisodeId, SourceSystem, DateOfDeath, LocationHierarchyKey, DateKey, 
		VisitDate
	)
SELECT PatientKey, BranchKey, EpisodeKey, EpisodeId, SourceSystem, DateOfDeath, LocationHierarchyKey, DateKey, COUNT(
		DISTINCT VisitDate) AS EligibleVisits, 1 AS HVDLDenominator
FROM AggregatedVisits
GROUP BY PatientKey, BranchKey, EpisodeKey, EpisodeId, SourceSystem, DateOfDeath, LocationHierarchyKey, DateKey;
