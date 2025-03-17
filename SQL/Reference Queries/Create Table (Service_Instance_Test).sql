USE [AttendanceTracker]
GO


CREATE TABLE [dbo].[service_instance_test]
(

service_instance_id int IDENTITY(1,1) PRIMARY KEY,	
service_instance_map_id int NULL,
created_user_id int NULL,
created_date datetime2(7) NULL,
edited_user_id int NULL,
edited_date datetime2(7) NULL,
site_id int NULL,
ministry_id int NULL,
service_id int NULL,
date_of_service datetime2(7) NULL,
entry_type_id int NULL,
entry_value nvarchar(255) NULL,
notes nvarchar(255) NULL
)
GO

