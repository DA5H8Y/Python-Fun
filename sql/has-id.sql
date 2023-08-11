SELECT req.ea_guid as CLASSGUID,'ID' AS Series
FROM 
	((t_object req
	inner join t_objectproperties id on id.object_id=req.object_id)
	inner join t_package pkg on req.Package_ID=pkg.Package_ID)
where
	req.object_type = 'Requirement' 
	and (id.Property = 'id' and NOT id.Value IS NULL)
	and pkg.Name = "StRS"
UNION
SELECT req.ea_guid as CLASSGUID, 'No ID' AS Series
	FROM t_object as req
		inner join t_package as pkg on req.Package_ID = pkg.Package_ID
	WHERE 
		req.object_type = 'Requirement'
		and pkg.Name = 'StRS'
		and req.ea_guid NOT IN
		(SELECT req.ea_guid as CLASSGUID
			FROM
				((t_object req
				inner join t_objectproperties id on id.object_id=req.object_id)
				inner join t_package pkg on req.Package_ID=pkg.Package_ID)
			where
				req.object_type = 'Requirement' 
				and (id.Property = 'id' and NOT id.Value IS NULL)
				and pkg.Name = "StRS"
		)
;
