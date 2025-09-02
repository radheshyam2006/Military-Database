SELECT 
    b.battalion_id,
    b.battalion_name,
    b.brigade_id,
    c.soldier_id AS colonel_id,
    CONCAT(s.first_name, ' ', s.last_name) AS colonel_name,
    b.latitude AS battalion_latitude,
    b.longitude AS battalion_longitude,
    d.dept_id,
    d.dept_name
FROM Battalions b
LEFT JOIN 
    Departments d ON b.battalion_id = d.battalion_id         -- Join to get the Battalions under this Brigade
LEFT JOIN 
    Colonels c ON b.battalion_id = c.battalion_id         -- Join to get the Brigadier (head of brigade)
LEFT JOIN 
    Soldiers s ON c.soldier_id = s.id                    -- Join to get the name of the Brigadier from Soldiers table
WHERE 
    b.battalion_id = 1;
