SELECT req.ea_guid as CLASSGUID, 'Links Out' AS Series
FROM 
	t_object as req  
	inner join t_package as pkg on req.Package_ID = pkg.Package_ID
	inner join t_package pkg2 on pkg.Parent_ID = pkg2.Package_ID
	inner join t_connector as id on req.object_id = id.Start_object_id
WHERE 
	req.object_type = 'Requirement'
	and pkg2.Name = "SysRS"
	and id.Stereotype = 'deriveReqt'
UNION
	SELECT req.ea_guid as CLASSGUID, 'Links In' AS Series
FROM 
	t_object as req  
	inner join t_package as pkg on req.Package_ID = pkg.Package_ID
	inner join t_package pkg2 on pkg.Parent_ID = pkg2.Package_ID
	inner join t_connector as id on req.object_id = id.end_object_id
WHERE 
	req.object_type = 'Requirement'
	and pkg2.Name = "SysRS"
	and id.Stereotype = 'deriveReqt'
UNION
SELECT req.ea_guid as CLASSGUID, 'No Links Out' AS Series
FROM 
	t_object as req  
	inner join t_package as pkg on req.Package_ID = pkg.Package_ID
	inner join t_package pkg2 on pkg.Parent_ID = pkg2.Package_ID
WHERE 
	req.object_type = 'Requirement'
	and pkg2.Name = "SysRS"
    and req.Object_ID NOT IN
		(SELECT req.object_ID FROM t_object as req
		inner join t_package as pkg on req.Package_ID = pkg.Package_ID
		inner join t_package pkg2 on pkg.Parent_ID = pkg2.Package_ID
		inner join t_connector as cnt on req.object_id = cnt.Start_object_ID
		where req.object_type = 'Requirement'
		and pkg2.Name = 'SysRS'
		and cnt.Stereotype like 'deriveReqt'
		UNION
		SELECT req.object_ID FROM t_object as req
		inner join t_object as req2
		inner join t_package as pkg on req2.Package_ID = pkg.Package_ID
		inner join t_package pkg2 on pkg.Parent_ID = pkg2.Package_ID
		inner join t_connector as cnt on req2.object_id = cnt.Start_object_ID
		inner join t_connector as nest on req.Object_id = nest.Start_object_ID
		where req.object_type = 'Requirement' and req2.object_type ='Requirement' 
		and pkg2.Name = 'SysRS'
		and nest.Connector_Type = 'Nesting'
		and cnt.Stereotype like 'deriveReqt'		
		)
UNION
SELECT req.ea_guid as CLASSGUID, 'No Links In' AS Series
	FROM t_object as req
		inner join t_package as pkg on req.Package_ID = pkg.Package_ID
		inner join t_package pkg2 on pkg.Parent_ID = pkg2.Package_ID
	WHERE 
		req.object_type = 'Requirement'
		and pkg2.Name = 'SysRS'
		and req.object_ID NOT IN
		(SELECT req.Object_ID
FROM 
	t_object as req  
	inner join t_package as pkg on req.Package_ID = pkg.Package_ID
	inner join t_package pkg2 on pkg.Parent_ID = pkg2.Package_ID
	inner join t_connector as id on req.object_id = id.end_object_id
WHERE 
	req.object_type = 'Requirement'
	and pkg2.Name = "SysRS"
	and id.Stereotype = 'deriveReqt')
;
