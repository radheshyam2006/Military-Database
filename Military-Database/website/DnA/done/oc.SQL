SELECT 
    o.oc_id,
    o.branch_name AS branch_name,  -- Assuming branch_name represents the OC's name or role
    lg.soldier_id AS lieutenant_general_id,    -- Lieutenant General's soldier ID
    CONCAT(s.first_name, ' ', s.last_name) AS lieutenant_general_name,  -- Full name of the Lieutenant General
    o.latitude AS oc_latitude,
    o.longitude AS oc_longitude,
    d.div_id,
    d.div_name
FROM 
    OCs o
LEFT JOIN 
    Divisions d ON o.oc_id = d.oc_id
LEFT JOIN 
    Lieutenant_General lg ON o.oc_id = lg.oc_id  -- Join to get the Lieutenant General for this OC
LEFT JOIN 
    Soldiers s ON lg.soldier_id = s.id           -- Join to get the name of the Lieutenant General from Soldiers table
WHERE 
    o.oc_id = 2;                  -- Replace with the actual OC ID
