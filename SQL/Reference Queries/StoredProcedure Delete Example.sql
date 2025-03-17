USE [DWStage]
GO


CREATE PROCEDURE [att].[WIG2DetailsDelete]
AS

BEGIN 
	DELETE o
	FROM 
		DWODS.att.WIG2Details o
	WHERE 
		NOT EXISTS (SELECT s.WIG2Key
					FROM DWStage.att.WIG2_Details s
					WHERE s.WIG2Key = o.WIG2key)
END
GO


