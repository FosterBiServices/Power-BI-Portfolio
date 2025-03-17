WITH LOS AS (
		SELECT 
			patientId,
			episodeId,
			SourceSystem,
			DATEDIFF(DAY, minVisit, maxVisit) AS LOS
		FROM ( 
			SELECT 
				v.patientId,
				v.episodeId,
				v.SourceSystem,
				MIN(v.VisitDate) AS minVisit,
				MAX(v.VisitDate) AS maxVisit
			FROM vw_dimClientEpisodeVisitWithWorkerId v WITH (NOLOCK)
			WHERE VisitDeletedFlag = 'N'
			  AND EXISTS (
					SELECT 1 
					FROM dbo.ServiceCodes s WITH (NOLOCK)
					WHERE v.VisitServiceCode = s.ScCode
					  AND v.SourceSystem = s.SourceSystem
					  AND (
							s.ScJdCode IN ( 'SN', 'MSW', 'MSWI')
							OR s.ScCode IN ('RN00H', 'RN09H', 'RN10H', 'RN11H', 
											 'OCRN00H', 'OCRN11H', 'RN02', 
											 'LPN11H', 'LPN90H', 'LPNPRNH')
						  )
				)
					AND 
						EXISTS ( 
							SELECT 1 
							from dbo.dimEpisode d WITH (NOLOCK)
							WHERE d.EpisodeId = v.EpisodeId
								and d.SourceSystem = v.SourceSystem
								and d.ServiceLine = 'Hospice'
						)

			GROUP BY v.patientId, v.episodeId, v.SourceSystem
			HAVING DATEDIFF(DAY, MIN(v.VisitDate), MAX(v.VisitDate)) >= 30
		) a
),
PreviousVisit AS (
    SELECT 
        v.patientId,
        v.episodeId,
        v.ClientEpisodeVisitId,
        v.visitServiceCode,
        v.visitDate,
        LAG(v.visitDate) OVER (
            PARTITION BY v.patientId, v.episodeId 
            ORDER BY v.visitDate
        ) AS previousVisitDate,
        de.EndOfEpisodeDate,
        COALESCE(fe.DischargeDate, EOMONTH(GETDATE())) AS DischargeDate
    FROM LOS l
	JOIN vw_dimClientEpisodeVisitWithWorkerId v WITH (NOLOCK)
	  ON l.EpisodeId = v.EpisodeId 
		AND l.SourceSystem = v.SourceSystem
    JOIN dbo.dimEpisode de WITH (NOLOCK) 
      ON v.EpisodeId = de.EpisodeId
         AND v.SourceSystem = de.SourceSystem
    JOIN dbo.factEpisode fe WITH (NOLOCK) 
      ON v.EpisodeId = fe.EpisodeId
         AND v.SourceSystem = fe.SourceSystem
    LEFT JOIN dimDischargeReason r WITH (NOLOCK) 
      ON fe.DischargeReasonKey = r.id
         AND r.SourceSystem = fe.SourceSystem
), 

MainResult AS (
    SELECT 
        p.patientId,
        p.episodeId,
        p.ClientEpisodeVisitId,
        p.visitServiceCode,
        p.visitDate,
        p.EndOfEpisodeDate,
        p.DischargeDate,
        CASE 
            WHEN p.previousVisitDate IS NOT NULL 
                 AND DATEDIFF(DAY, p.previousVisitDate, p.visitDate) > 7 THEN 1
            WHEN p.previousVisitDate IS NULL 
                 AND DATEDIFF(DAY, p.visitDate, p.DischargeDate) > 7 THEN 1
            ELSE 0 
        END AS GapInNursingFlag
    FROM PreviousVisit p
    WHERE CASE 
            WHEN p.previousVisitDate IS NOT NULL 
                 AND DATEDIFF(DAY, p.previousVisitDate, p.visitDate) > 7 THEN 1
            WHEN p.previousVisitDate IS NULL 
                 AND DATEDIFF(DAY, p.visitDate, p.DischargeDate) > 7 THEN 1
            ELSE 0 
          END = 1
)


SELECT 
    m.patientId,
    m.episodeId,
    m.ClientEpisodeVisitId,
    m.visitServiceCode,
    m.visitDate,
    m.EndOfEpisodeDate,
    m.DischargeDate,
    m.GapInNursingFlag,
	CONVERT(nchar(8),d.MonthLastDay,112)
		AS DateKey					    
FROM MainResult m
inner join ( /* Create record for each month */ 
	SELECT DISTINCT MonthLastDay,MonthFirstDay
	FROM dbo.dimDates (NOLOCK)
	) d  on EOMONTH(m.VisitDate) <= d.MonthLastDay and m.DischargeDate >= d.MonthFirstDay
WHERE 
	EXISTS( 
		SELECT 1 
		FROM dbo.dimDates dd WITH (NOLOCK)
		WHERE dd.DateKey = CONVERT(nchar(8),d.MonthLastDay,112)
			AND m.VisitDate BETWEEN DATEFROMPARTS(YEAR(GETDATE()) - 2, 1, 1) AND CAST(GETDATE()-1 AS DATE) 
		)