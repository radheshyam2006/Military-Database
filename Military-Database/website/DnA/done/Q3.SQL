SELECT 
    bg.soldier_id,
    bg.personal_weapon_id,
    CONCAT(s.first_name, ' ', s.last_name) AS soldier_name,
    bg.brigade_id AS brigade_id,
    b.brigade_name AS brigade_name
FROM Brigadiers bg
JOIN Soldiers s ON bg.soldier_id = s.id
JOIN Brigades b ON bg.brigade_id = b.brigade_id;
