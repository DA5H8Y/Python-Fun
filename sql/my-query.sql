SELECT uc.Name as 'Use Case', strs.Name as StRS, sysrs1.Name as 'SysRS Collection', sysrs.Name as SysRS, id.Value as ID, text.Notes as Specification, hlr.Name as HLR
    FROM 
        t_object as uc
        inner join t_connector as refine on refine.Start_Object_ID = uc.Object_ID
        inner join t_object as strs on strs.Object_ID = refine.End_Object_ID
        inner join t_connector as derive on derive.End_Object_ID = strs.Object_ID
        inner join t_object as sysrs1 on sysrs1.Object_ID = derive.Start_Object_ID
        inner join t_connector as nest on nest.End_Object_ID = sysrs1.Object_ID
        inner join t_object as sysrs on nest.Start_Object_ID = sysrs.Object_ID
        inner join t_objectproperties as id on id.Object_ID = sysrs.Object_ID
        inner join t_objectproperties as text on text.Object_ID = sysrs.Object_ID
        inner join t_package as pkg on sysrs.Package_ID = pkg.Package_ID
        inner join t_package as pkg2 on pkg.Parent_ID = pkg2.Package_ID
        inner join t_connector as derive2 on derive2.End_Object_ID = sysrs.Object_ID
        inner join t_object as hlr on hlr.Object_ID = derive2.Start_Object_ID
    WHERE
        uc.Name = 'Piloting (#1)'
        and sysrs.object_type = 'Requirement'
        and sysrs1.object_type = 'Requirement'
        and strs.object_type = 'Requirement'
        and refine.Stereotype = 'refine'
        and derive.Stereotype = 'deriveReqt'
        and nest.Connector_Type = 'Nesting'
        and pkg2.Name = 'SysRS'
        and id.Property = 'id'
        and text.Property = 'text'