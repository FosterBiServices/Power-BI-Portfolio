USE [Sandbox]
GO

/****** Object:  StoredProcedure [dbo].[usp_BPOExclusionList]    Script Date: 2/28/2018 12:42:02 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


 ALTER PROCEDURE [dbo].[usp_BPOExclusionList]
(	@Reporting_ID as varchar(50)
	, @Network_ID as varchar(50)
	, @BusinessGroup_ID as varchar(50)
	, @BusinessGroup as varchar(50)
	, @ContactType as varchar(20)
	, @NewHireCompletionDate as varchar(50)
	, @ExclusionEndDate as varchar(50)
	, @LengthofExclusion as varchar(50) 
	, @WorkType as varchar(50)
)
 AS
 BEGIN


----- Check for Duplicate Entries, msg shows Duplicate Entry if detected ---------- 

IF (
SELECT COUNT(Reporting_ID)
FROM NADCS_DW.dbo.BPOExclusionList
WHERE Reporting_ID = @Reporting_ID
AND Network_ID = @Network_ID
AND BusinessGroup_ID  = @BusinessGroup_ID 
AND BusinessGroup = @BusinessGroup
AND ContactType = @ContactType
AND WorkType = @WorkType
 ) > 0 
 BEGIN
--  Select 'Duplicate Entry' as MSG
 GOTO EXIT_SP; 
 END

 ----- If not a duplicate check for any other records
----	If none then create CSI and entry based on submission ----- 
 
ELSE IF (
SELECT COUNT(Reporting_ID)
FROM NADCS_DW.dbo.BPOExclusionList
WHERE Reporting_ID = @Reporting_ID
AND Network_ID = @Network_ID
AND BusinessGroup_ID  = @BusinessGroup_ID 
AND BusinessGroup = @BusinessGroup
AND WorkType = 'CSI'
 ) = 0 

BEGIN

Insert Into NADCS_DW.dbo.BPOExclusionList (Reporting_ID, Network_ID, BusinessGroup_ID, BusinessGroup, ContactType, NewHireCompletionDate, ExclusionEndDate, LengthofExclusion, WorkType) Values
(@Reporting_ID, @Network_ID, @BusinessGroup_ID, @BusinessGroup, @ContactType, @NewHireCompletionDate, Dateadd(Day, 120, @NewHireCompletionDate), 120, 'CSI'),
(@Reporting_ID, @Network_ID, @BusinessGroup_ID, @BusinessGroup, @ContactType, @NewHireCompletionDate, @ExclusionEndDate, @LengthofExclusion, @WorkType)

END 

---- If not first then enter information from form ---------- 

ELSE IF (
SELECT COUNT(Reporting_ID)
FROM NADCS_DW.dbo.BPOExclusionList
WHERE Reporting_ID = @Reporting_ID
AND Network_ID = @Network_ID
AND BusinessGroup_ID  = @BusinessGroup_ID 
AND BusinessGroup = @BusinessGroup
 ) > 0 

 BEGIN

Insert Into NADCS_DW.dbo.BPOExclusionList (Reporting_ID, Network_ID, BusinessGroup_ID, BusinessGroup, ContactType, NewHireCompletionDate, ExclusionEndDate, LengthofExclusion, WorkType) Values
(@Reporting_ID, @Network_ID, @BusinessGroup_ID, @BusinessGroup, @ContactType, @NewHireCompletionDate, @ExclusionEndDate, @LengthofExclusion, @WorkType)

END 

----- If contact is phone and there is no phone/phone record, insert one -------------- 

IF (@ContactType = 'Phone' AND 
(	SELECT COUNT(Reporting_ID)
FROM NADCS_DW.dbo.BPOExclusionList
WHERE Reporting_ID = @Reporting_ID
AND Network_ID = @Network_ID
AND BusinessGroup_ID  = @BusinessGroup_ID 
AND BusinessGroup = @BusinessGroup
AND ContactType = 'Phone'
AND WorkType = 'Phone'
 ) = 0 ) 

 BEGIN

Insert Into NADCS_DW.dbo.BPOExclusionList (Reporting_ID, Network_ID, BusinessGroup_ID, BusinessGroup, ContactType, NewHireCompletionDate, ExclusionEndDate, LengthofExclusion, WorkType) Values
(@Reporting_ID, @Network_ID, @BusinessGroup_ID, @BusinessGroup, @ContactType, @NewHireCompletionDate, Dateadd(Day, 120, @NewHireCompletionDate), 120, 'Phone')

END 

/*
*******************************************************************************************************************************
*******************************************************************************************************************************
*****----- Comment out the remaining code until line 145 if customer service and sales are separated in the future -----*****
*******************************************************************************************************************************
*******************************************************************************************************************************
*/

----- If contact is phone and subtype is sales there is no customer service record, insert one -------------- 

IF (@ContactType = 'Phone' AND @WorkType = 'Sales' AND 
(	SELECT COUNT(Reporting_ID)
FROM NADCS_DW.dbo.BPOExclusionList
WHERE Reporting_ID = @Reporting_ID
AND Network_ID = @Network_ID
AND BusinessGroup_ID  = @BusinessGroup_ID 
AND BusinessGroup = @BusinessGroup
AND ContactType = 'Phone'
AND WorkType = 'Customer Service'
 ) = 0 ) 

 BEGIN

Insert Into NADCS_DW.dbo.BPOExclusionList (Reporting_ID, Network_ID, BusinessGroup_ID, BusinessGroup, ContactType, NewHireCompletionDate, ExclusionEndDate, LengthofExclusion, WorkType) Values
(@Reporting_ID, @Network_ID, @BusinessGroup_ID, @BusinessGroup, @ContactType, @NewHireCompletionDate, Dateadd(Day, 120, @NewHireCompletionDate), 120, 'Customer Service')

END 

----- If contact is phone and subtype is Customer Service there is no Sales record, insert one -------------- 

IF (@ContactType = 'Phone' AND @WorkType = 'Customer Service' AND 
(	SELECT COUNT(Reporting_ID)
FROM NADCS_DW.dbo.BPOExclusionList
WHERE Reporting_ID = @Reporting_ID
AND Network_ID = @Network_ID
AND BusinessGroup_ID  = @BusinessGroup_ID 
AND BusinessGroup = @BusinessGroup
AND ContactType = 'Phone'
AND WorkType = 'Sales'
 ) = 0 ) 

 BEGIN

Insert Into NADCS_DW.dbo.BPOExclusionList (Reporting_ID, Network_ID, BusinessGroup_ID, BusinessGroup, ContactType, NewHireCompletionDate, ExclusionEndDate, LengthofExclusion, WorkType) Values
(@Reporting_ID, @Network_ID, @BusinessGroup_ID, @BusinessGroup, @ContactType, @NewHireCompletionDate, Dateadd(Day, 120, @NewHireCompletionDate), 120, 'Sales')

END 

EXIT_SP:
SET NOCOUNT OFF;
END









GO


