USE [zSandboxFoster];


IF OBJECT_ID ('zSandboxFoster.dbo.LookupFiveWeeker') IS NOT NULL 
DROP TABLE zSandboxFoster.[dbo].[LookupFiveWeeker]; 
GO 

CREATE TABLE [dbo].[LookupFiveWeeker]
(
	
	FiveWeekerID int IDENTITY(1,1) PRIMARY KEY,
	NetworkID int NOT NULL,
	SourceRoutingForecastName varchar(50) NOT NULL,
	CustomGroup varchar(50) NOT NULL,
	PRMSExclude bit NOT NULL,
	Exclusions bit NOT NULL,
	SortID int NOT NULL
	); 

