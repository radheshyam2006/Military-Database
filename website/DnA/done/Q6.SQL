SELECT 
    s.id AS soldier_id,
    CONCAT(s.first_name, ' ', s.last_name) AS soldier_name,
    h.m_rank AS current_rank
FROM Soldiers s
INNER JOIN (
    -- Subquery to get the latest rank for each soldier
    SELECT 
        soldier_id, 
        m_rank 
    FROM M_History 
    WHERE (soldier_id, start_date) IN (
        -- Find the most recent start_date for each soldier
        SELECT 
            soldier_id, 
            MAX(start_date) AS latest_date
        FROM M_History
        GROUP BY soldier_id
    )
) h ON s.id = h.soldier_id;
