SELECT 
    mg.soldier_id,
    mg.personal_weapon_id,
    CONCAT(s.first_name, ' ', s.last_name) AS soldier_name,
    mg.div_id AS div_id,
    d.div_name AS div_name
FROM Major_Generals mg
JOIN Soldiers s ON mg.soldier_id = s.id
JOIN Divisions d ON mg.div_id = d.div_id;
