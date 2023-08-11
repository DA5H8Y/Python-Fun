SELECT
    t_object.Object_Type,
    t_object.Name,
    t_object.Note,
    t_object.Author,
    t_object.Status,
    t_package.Name as Package
FROM 
    t_object 
    INNER JOIN t_package ON t_object.Package_ID = t_package.Package_ID
WHERE
    t_object.Stereotype LIKE '%assumption%' OR
    t_object.Note LIKE '%assumption%' OR
    t_object.Name LIKE '%assumption%'
;
