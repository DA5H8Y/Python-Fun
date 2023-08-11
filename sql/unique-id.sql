SELECT distinct id.value, 'Unique' As Series
FROM
	((t_object as req
	inner join t_package as pkg on req.Package_ID = pkg.Package_ID)
	inner join t_objectproperties as id on req.object_id = id.object_id)
where
	req.object_type = 'Requirement'
	and id.Property = 'id'
	and pkg.Name = "StRS"
UNION
SELECT prop.Value, 'Not Unique' As Series
FROM
	((t_objectproperties prop
	inner join t_object req on prop.Object_ID = req.Object_ID)
    inner join t_package pkg on req.Package_ID = pkg.Package_ID)
WHERE
	prop.Property = 'id'
	and req.Object_Type = 'requirement'
	and pkg.Name = 'StRS'
GROUP BY
	prop.Value
HAVING
	COUNT(prop.Value) > 1
;
