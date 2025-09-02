SELECT 
    lg.soldier_id,
    lg.personal_weapon_id,
    CONCAT(s.first_name, ' ', s.last_name) AS soldier_name,
    lg.oc_id AS oc_id
FROM Lieutenant_General lg
JOIN Soldiers s ON lg.soldier_id = s.id;
