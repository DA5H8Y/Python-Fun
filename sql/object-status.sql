SELECT
    req.ea_guid as CLASSGUID,
    req.Name,
    'Proposed' AS Series
FROM
    (t_object req
     inner join t_package pkg on req.Package_ID=pkg.Package_ID)
WHERE
    req.object_type = 'Requirement' AND
    req.Status = 'Proposed' AND
    pkg.Name = "StRS"

UNION

SELECT
    req.ea_guid as CLASSGUID,
    req.Name,
    'Approved' AS Series
FROM
    (t_object req
     inner join t_package pkg on req.Package_ID=pkg.Package_ID)
WHERE
    req.object_type = 'Requirement' AND
    req.Status = 'Approved' AND
    pkg.Name = "StRS"

UNION

SELECT 
    req.ea_guid as CLASSGUID,
    req.Name,
    'Validated' AS Series
FROM
    (t_object req
     inner join t_package pkg on req.Package_ID=pkg.Package_ID)
WHERE
     req.object_type = 'Requirement' AND
     req.Status = 'Validated' AND
     pkg.Name = "StRS"

UNION

SELECT
    req.ea_guid as CLASSGUID,
    req.Name,
    'Implemented' AS Series
FROM
    (t_object req
     inner join t_package pkg on req.Package_ID=pkg.Package_ID)
WHERE
     req.object_type = 'Requirement' AND
     req.Status = 'Implemented' AND
     pkg.Name = "StRS"

UNION

SELECT
     req.ea_guid as CLASSGUID,
     req.Name,
     'Mandatory' AS Series
FROM
     (t_object req
      inner join t_package pkg on req.Package_ID=pkg.Package_ID)
WHERE
    req.object_type = 'Requirement' AND
    req.Status = 'Mandatory' AND
    pkg.Name = "StRS"

UNION

SELECT 
    req.ea_guid as CLASSGUID,
    req.Name,
    'Validated' AS Series
FROM
    (t_object req
     inner join t_package pkg on req.Package_ID=pkg.Package_ID)
WHERE
    req.object_type = 'Requirement' AND
    req.Status = 'Validated' AND
    pkg.Name = "StRS"
;
