SELECT 
    c.soldier_id,
    c.personal_weapon_id,
    CONCAT(s.first_name, ' ', s.last_name) AS soldier_name,
    c.battalion_id AS battalion_id,
    batt.battalion_name AS battalion_name
FROM Colonels c
JOIN Soldiers s ON c.soldier_id = s.id
JOIN Battalions batt ON c.battalion_id = batt.battalion_id;
