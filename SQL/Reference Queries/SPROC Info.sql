USE zSandboxFoster; 

GO

CREATE OR ALTER PROCEDURE dbo.SprocTemplate
(
------ INSERT PARAMETERS HERE
--EXAMPLE-- @ContactID INT 
--EXAMPLE-- @DateOfBirth DATE = NULL
)

AS
	BEGIN; 
	
SET NOCOUNT ON;  

--- EXISTS EXAMPLE 
	--IF NOT EXISTS ( SELECT 1 FROM dbo.vwPLBipsDimDate
	--	WHERE DateID = 1)
	--BEGIN; 
	--	-- ADD SPROC HERE
	--END; 
--- CALL ANOTHER SPROC EXAMPLE
	-- EXEC dbo.spGetShiftBidExclusionList

--- TRY CATCH EXAMPLE 
	--BEGIN TRY; 
	--	--ADD SPROC HERE
	--END TRY

	--BEGIN CATCH; 
	--	PRINT 'Error' + ERROR_MESSAGE(); 
	--	SELECT * FROM sys.messages WHERE message_ID = ERROR_NUMBER(); 
	--END CATCH; 

SET NOCOUNT OFF; 

	END; 

GO

