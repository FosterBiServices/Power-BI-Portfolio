USE [zSandboxFoster]
GO


CREATE TABLE [dbo].[PerfectAttendanceQualification]
(

BusinessUnit varchar(25), 
lngCOSTCTR INT NOT NULL, 	
strCOSTCTR varchar(255), 
lngRID INT NOT NULL, 
strREASON varchar(255), 
lngPAYID INT NOT NULL, 
strPAY varchar(255), 
StartDate Date NOT NULL, 
EndDate Date NOT NULL, 
strOCCUR varchar(255), 
strCOMMENTS varchar(255), 
PerfectAttendance varchar(5)

)
GO

