SELECT
    d.div_id,
    d.div_name,
    d.oc_id,
    mg.soldier_id AS major_general_id,
    CONCAT(s.first_name, ' ', s.last_name) AS major_general_name,
    d.latitude AS div_latitude,
    d.longitude AS div_longitude,
    b.brigade_id,
    b.brigade_name
FROM 
    Divisions d
LEFT JOIN
    Brigades b ON d.div_id = b.div_id
LEFT JOIN
    Major_Generals mg ON d.div_id = mg.div_id
LEFT JOIN
    Soldiers s ON mg.soldier_id = s.id
WHERE
    d.div_id = 1;
