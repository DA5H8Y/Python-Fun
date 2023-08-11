SELECT 
	req.ea_guid AS CLASSGUID,
	req.Object_Type as CLASSTYPE,
	req.Name, 
	id.Value As ID,
	text.Notes aS Specification,
	pkg.Name as Package
FROM (((((t_object req
	inner join t_connector alo on alo.Start_Object_ID = req.Object_ID)
	inner join t_object tgt on tgt.Object_ID = alo.End_Object_ID)
	inner join t_objectproperties id on id.Object_ID = req.Object_ID)
	inner join t_objectproperties text on text.Object_ID = req.Object_ID)
	inner join t_package pkg on pkg.Package_ID = req.Package_ID)
where 
	req.Object_Type = 'Requirement'
	and alo.Stereotype like 'allocate'
	and tgt.Name ='Software'
	and  id.Property = 'id'
	and  text.Property = 'text'