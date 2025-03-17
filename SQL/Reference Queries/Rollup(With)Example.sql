select	CASE WHEN pa12.Date_ID IS NULL then 'Total' Else Cast(pa12.date_ID as varchar) END as DateID,
	pa12.Q1Value  Q1Value,
	pa12.Q2Value  Q2Value
from	( 
select	a11.Date_ID Date_ID,
	sum((Case when a11.QUESTION1_EXCLUDE_FLAG in ('N') then a11.QUESTION1_VALUE else NULL end))  Q1Value,
	sum((Case when a11.QUESTION2_EXCLUDE_FLAG in ('N') then a11.QUESTION2_VALUE else NULL end))  Q2Value
from	nadcs_dw.dbo.smryPostCallSurvey	a11
where	(a11.Date_ID in (8792, 8793, 8794, 8795, 8796, 8797, 8798, 8799)
 and (a11.QUESTION1_EXCLUDE_FLAG in ('N')
 or a11.QUESTION2_EXCLUDE_FLAG in ('N')))
group by	a11.Date_ID with ROLLUP )	pa12
