USE [DWODS]
GO


CREATE PROCEDURE [att].[dimGuidedCommunityCategoryMerge]
AS

BEGIN

	MERGE INTO DWODS.dbo.dimGuidedCommunityCategory as t
	USING (
			SELECT
				GuidedCommunityKey,
				GuidedCommunityDesc,
				GuidedCommunityTypeDesc,
				EntryTypeID,
				EntryTypeDesc ,
				ServiceTypeID ,
				ServiceTypeDesc,
				GuidedCommunityStartDate,
				GuidedCommunityEndDate,
				GETDATE() as LastUpdateDatetime
			FROM 
				DWStage.att.dimGuidedCommunityCategory
			) as s
				ON s.GuidedCommunityKey = t.GuidedCommunityKey
	WHEN MATCHED THEN UPDATE
		SET 
			t.GuidedCommunityDesc =			s.GuidedCommunityDesc,
			t.GuidedCommunityTypeDesc =		s.GuidedCommunityTypeDesc,
			t.EntryTypeID =					s.EntryTypeID,
			t.EntryTypeDesc =				s.EntryTypeDesc,
			t.ServiceTypeID =				s.ServiceTypeID,
			t.ServiceTypeDesc =				s.ServiceTypeDesc,
			t.GuidedCommunityStartDate =	s.GuidedCommunityStartDate,
			t.GuidedCommunityEndDate =		s.GuidedCommunityEndDate

	WHEN NOT MATCHED THEN INSERT 
		(		
				GuidedCommunityDesc,
				GuidedCommunityTypeDesc,
				EntryTypeID,
				EntryTypeDesc ,
				ServiceTypeID ,
				ServiceTypeDesc,
				GuidedCommunityStartDate,
				GuidedCommunityEndDate,
				LastUpdateDatetime
		)
	VALUES
		(	
				s.GuidedCommunityDesc,
				s.GuidedCommunityTypeDesc,
				s.EntryTypeID,
				s.EntryTypeDesc ,
				s.ServiceTypeID ,
				s.ServiceTypeDesc,
				s.GuidedCommunityStartDate,
				s.GuidedCommunityEndDate,
				LastUpdateDatetime
		);
END
GO


