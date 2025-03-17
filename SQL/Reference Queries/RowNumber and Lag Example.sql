Select 
	Case When T1.CalendarDate BETWEEN '2018-10-07' and '2018-11-03' Then 'P09 'Else 'P10' End As FiscalPeriod,
	T1.ConversationId, 
	T1.VisitorId,
	T1.Results
From 
(
		SELECT 
			cast(started as Date) CalendarDate,
			ConversationId, 
			VisitorId, 
			Started, 
			Ended, 
			Assigned, 
			Channel, 
			SystemMessages,
			VisitorMessages,
			ROW_NUMBER () Over (PARTITION BY VisitorId Order By Started) As RowNumber,
			Case When ROW_NUMBER () Over (PARTITION BY VisitorId Order By Started) = 1 Then Null 
			When LAG(Channel, 1, 0) Over (Order By VisitorId) = 'Proactive' and Channel = 'Staples.com Reactive Chat' Then
			DateDiff(SECOND, LAG(Ended, 1, 0) Over (Order By VisitorId),Started) Else Null End As Results
		FROM [InsideReportsDB_STP_1].[dbo].[Conversations]
			Where cast(started as Date) > '2018-10-06'
			and VisitorId IN 
					(
						SELECT DISTINCT VisitorId
						FROM [InsideReportsDB_STP_1].[dbo].[Conversations]
						Where cast(started as Date) > '2018-10-06'
						and SystemMessages=0
						and VisitorMessages=1
				)
)T1 
Where Results < 901
Order By T1.CalendarDate
