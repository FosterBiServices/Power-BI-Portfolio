USE [Gardian]
GO

CREATE TABLE [dbo].[Dim_Date] (
			Date_ID int not null,
			CalendarDate datetime not null,
			DayOfWeek int null,
			DayOfWeekName varchar(10) null,
			DayOfWeekNameAbbr char null,
			MonthName varchar(10) null,
			MonthNameAbbr char null,
			MonthStartDate datetime null,
			MonthEndDate datetime null,
			CalendarYear int null,
			BusinessDayFlag char null,
			HolidayFlag char null,
			WeekendDayFlag char null,
			FiscalYear int null,
			FiscalYearStartDate datetime null,
			FiscalYearEndDate datetime null,
			FiscalQuarter int null,
			FiscalQuarterName char null,
			FiscalQuarterStartDate datetime null,
			FiscalQuarterEndDate datetime null,
			FiscalPeriod int null,
			FiscalPeriodName char null,
			FiscalPeriodNameAbbr char null,
			FiscalPeriodNameLong varchar(10) null,
			FiscalPeriodStartDate datetime null,
			FiscalPeriodEndDate datetime null,
			FiscalWeekOfYear int null,
			FiscalWeekOfQuarter int null,
			FiscalWeekOfPeriod int null,
			FiscalWeekOfPeriodName varchar(20) null,
			FiscalWeekStartDate datetime null,
			FiscalWeekEndDate datetime null,
			FiscalDayOfYear int null,
			FiscalDayOfQuarter int null,
			FiscalDayOfPeriod int null,
			DaylightSavings bit null,
			IsCurrent char null,
			StartDate datetime null,
			EndDate datetime null


) ON [PRIMARY]; 




