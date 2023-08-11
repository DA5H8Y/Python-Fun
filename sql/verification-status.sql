SELECT req.ea_guid as CLASSGUID, 'None' AS Series
	FROM 
		t_object as req
		inner join t_package as pkg on req.Package_ID = pkg.Package_ID
	WHERE 
		req.object_type = 'Requirement'
		and pkg.Name = 'StRS'
		and req.object_ID NOT IN
		(SELECT req.object_ID
			FROM 
				t_object req
				inner join t_connector id on id.end_object_id=req.object_id
				inner join t_object tc on id.start_object_id=tc.object_id
				inner join t_package pkg on req.Package_ID=pkg.Package_ID
			WHERE 
				req.object_type = 'Requirement'
				and tc.Stereotype = 'TestCase'
				and id.Stereotype='verify'
				and pkg.Name = 'StRS'
		)
UNION
SELECT req.ea_guid as CLASSGUID, 'No Verdict' As Series
	FROM 
		t_object req
		inner join t_connector id on id.end_object_id=req.object_id
		inner join t_object tc on id.start_object_id=tc.object_id
		inner join t_objectproperties res on res.object_id=tc.object_id
		inner join t_package pkg on req.Package_ID=pkg.Package_ID
	WHERE
		req.object_type = 'Requirement'
		and tc.Stereotype = "TestCase"
		and id.Stereotype='verify'
		and res.Value is NULL
		and pkg.Name = "StRS"
UNION
SELECT req.ea_guid as CLASSGUID, 'Passed' As Series
	FROM
		t_object req
		inner join t_connector id on id.end_object_id=req.object_id
		inner join t_object tc on id.start_object_id=tc.object_id
		inner join t_objectproperties res on res.object_id=tc.object_id
		inner join t_package pkg on req.Package_ID=pkg.Package_ID
	WHERE
		req.object_type = 'Requirement'
		and tc.Stereotype = "TestCase"
		and id.Stereotype='verify'
		and res.Value = "pass"
		and pkg.Name = "StRS"
UNION
SELECT req.ea_guid as CLASSGUID, 'Failed' As Series
	FROM
		t_object req
		inner join t_connector id on id.end_object_id=req.object_id
		inner join t_object tc on id.start_object_id=tc.object_id
		inner join t_objectproperties res on res.object_id=tc.object_id
		inner join t_package pkg on req.Package_ID=pkg.Package_ID
	WHERE
		req.object_type = 'Requirement'
		and tc.Stereotype = "TestCase"
		and id.Stereotype='verify'
		and res.Value = "fail"
		and pkg.Name = "StRS"
UNION
SELECT req.ea_guid as CLASSGUID, 'Inconclusive' As Series
	FROM
		t_object req
		inner join t_connector id on id.end_object_id=req.object_id
		inner join t_object tc on id.start_object_id=tc.object_id
		inner join t_objectproperties res on res.object_id=tc.object_id
		inner join t_package pkg on req.Package_ID=pkg.Package_ID
	WHERE
		req.object_type = 'Requirement'
		and tc.Stereotype = "TestCase"
		and id.Stereotype='verify'
		and res.Value = "inconclusive"
		and pkg.Name = "StRS"
UNION
SELECT req.ea_guid as CLASSGUID, 'Errored' As Series
	FROM
		t_object req
		inner join t_connector id on id.end_object_id=req.object_id
		inner join t_object tc on id.start_object_id=tc.object_id
		inner join t_objectproperties res on res.object_id=tc.object_id
		inner join t_package pkg on req.Package_ID=pkg.Package_ID
	WHERE
		req.object_type = 'Requirement'
		and tc.Stereotype = "TestCase"
		and id.Stereotype='verify'
		and res.Value = "error"
		and pkg.Name = "StRS"
;
