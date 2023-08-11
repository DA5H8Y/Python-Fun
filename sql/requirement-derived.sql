SELECT req.ea_guid as CLASSGUID, 'Derivation' AS Series
FROM 
	t_object as req  
	inner join t_package as pkg on req.Package_ID = pkg.Package_ID
	inner join t_connector as id on req.object_id = id.end_object_id
WHERE 
	req.object_type = 'Requirement'
	and pkg.Name = "StRS"
	and id.Stereotype = 'deriveReqt'
UNION
SELECT req.ea_guid as CLASSGUID, 'No Derivation' AS Series
	FROM t_object as req
		inner join t_package as pkg on req.Package_ID = pkg.Package_ID
	WHERE 
		req.object_type = 'Requirement'
		and pkg.Name = 'StRS'
		and req.object_ID NOT IN
		(SELECT req.object_ID FROM t_object as req
		inner join t_package as pkg on req.Package_ID = pkg.Package_ID
		inner join t_connector as cnt on req.object_id = cnt.end_object_ID
		where req.object_type = 'Requirement'
		and pkg.Name = 'StRS'
		and cnt.Stereotype like 'deriveReqt');
