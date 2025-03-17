USE [NADCS_DW]
GO 

sp_rename 'BPOScorecardVoiceGoals.QANum', 'QAMCOENum';

USE [NADCS_DW]
GO 
sp_rename 'BPOScorecardVoiceGoals.QADenom', 'QAMCOEDenom';