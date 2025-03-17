SELECT
BPOScorecardAHTGoals,Network_ID,BusinessGroup, BusinessGroup_ID, Week_ID, AHTType, AHTType_ID
  , COUNT(*) AS RecordCount
FROM
    NADCS_DW.dbo.BPOScorecardAHTGoals
GROUP BY
BPOScorecardAHTGoals,Network_ID,BusinessGroup, BusinessGroup_ID, Week_ID, AHTType, AHTType_ID
HAVING 
    COUNT(*) > 1

