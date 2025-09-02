SELECT 
    b.brigade_id,
    b.brigade_name,
    b.div_id,
    br.soldier_id AS brigadier_id,
    CONCAT(s.first_name, ' ', s.last_name) AS brigadier_name,
    b.latitude AS brigade_latitude,
    b.longitude AS brigade_longitude,
    bt.battalion_id,
    bt.battalion_name
FROM 
    Brigades b
LEFT JOIN 
    Battalions bt ON b.brigade_id = bt.brigade_id
LEFT JOIN 
    Brigadiers br ON b.brigade_id = br.brigade_id
LEFT JOIN 
    Soldiers s ON br.soldier_id = s.id
WHERE 
    b.brigade_id = 1;

SELECT 
    e.equipment_id,
    eb.soldier_id,
    e.date_of_manufacture,
    e.equipment_status,
    e.use_before,
    e.model AS equipment_model,
    m.type_of_item,
    m.cost,
    m.manufacturer
FROM 
    Equipped_by eb
JOIN 
    Equipment e ON eb.equipment_id = e.equipment_id
JOIN 
    Models m ON e.model = m.model_name
WHERE 
    eb.brigade_id = 5;

