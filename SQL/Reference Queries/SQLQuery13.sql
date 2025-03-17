USE [zSandboxFoster]
GO

ALTER PROCEDURE [dbo].[spUpdatePAScores]
	@EmployeeID varchar(8) = null,
	@OverallRating decimal(10,2) = null
	WITH RECOMPILE
AS
	SET NOCOUNT ON; 

BEGIN

	MERGE INTO zSandboxFoster.[dbo].[PAScores] as t
	USING (
			SELECT
				EmployeeID, OverallRating
			FROM 
				zSandboxFoster.[dbo].PAScores
			) as s
				ON s.EmployeeID = t.EmployeeID
	WHEN MATCHED THEN UPDATE
		SET 
			t.EmployeeID = s.EmployeeID,
			t.OverallRating = s.OverallRating

	WHEN NOT MATCHED THEN INSERT 
		(		
			EmployeeID, OverallRating
		)
	VALUES
		(	
			s.EmployeeID, s.OverallRating
		);
END
GO


