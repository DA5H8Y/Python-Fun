SELECT req.ea_guid as CLASSGUID, req.Name,'None' AS Series
FROM ((t_object req
inner join t_objectproperties id on id.object_id=req.object_id)
inner join t_package pkg on req.Package_ID=pkg.Package_ID)
where req.object_type = 'Requirement' 
and (id.Property = 'verifyMethod' and id.Value IS NULL)
and pkg.Name = "StRS"
UNION
SELECT req.ea_guid as CLASSGUID, req.Name, 'Analysis' As Series
FROM ((t_object req
inner join t_objectproperties id on id.object_id=req.object_id)
inner join t_package pkg on req.Package_ID=pkg.Package_ID)
where req.object_type = 'Requirement' 
and (id.Property = 'verifyMethod' and id.Value = 'Analysis')
and pkg.Name = "StRS"
UNION
SELECT req.ea_guid as CLASSGUID, req.Name, 'Test' As Series
FROM ((t_object req
inner join t_objectproperties id on id.object_id=req.object_id)
inner join t_package pkg on req.Package_ID=pkg.Package_ID)
where req.object_type = 'Requirement' 
and (id.Property = 'verifyMethod' and id.Value = 'Test')
and pkg.Name = "StRS"
UNION
SELECT req.ea_guid as CLASSGUID, req.Name, 'Demonstration' As Series
FROM ((t_object req
inner join t_objectproperties id on id.object_id=req.object_id)
inner join t_package pkg on req.Package_ID=pkg.Package_ID)
where req.object_type = 'Requirement' 
and (id.Property = 'verifyMethod' and id.Value = 'Demonstration')
and pkg.Name = "StRS"
UNION
SELECT req.ea_guid as CLASSGUID, req.Name, 'Inspection' As Series
FROM ((t_object req
inner join t_objectproperties id on id.object_id=req.object_id)
inner join t_package pkg on req.Package_ID=pkg.Package_ID)
where req.object_type = 'Requirement' 
and (id.Property = 'verifyMethod' and id.Value = 'Inspection')
and pkg.Name = "StRS";
