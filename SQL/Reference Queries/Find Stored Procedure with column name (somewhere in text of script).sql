SELECT obj.Name SPName, sc.TEXT SPText
FROM sys.syscomments sc
INNER JOIN sys.objects obj ON sc.Id = obj.OBJECT_ID
WHERE sc.TEXT LIKE '%' + 'Business' + '%'
AND TYPE = 'P'

