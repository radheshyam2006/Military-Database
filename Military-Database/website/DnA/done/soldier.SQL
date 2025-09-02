SELECT 
    s.id AS soldier_id,
    CONCAT(s.first_name, ' ', s.last_name) AS soldier_name,
    s.birth_date,
    s.phone_number,
    s.date_of_joining,
    s.health_status,
    s.street_no,
    s.city,
    s.district,
    s.state,

    -- Military History
    mh.start_date AS history_start_date,
    mh.m_rank AS history_rank,

    -- Awards
    a.award_name,
    a.date_received AS award_date,

    -- Dependents
    d.relation AS dependent_relation,
    d.dependent_name,
    d.dependent_birth_date,

    -- Programs Taught
    pt.program_name AS taught_program_name,

    -- Programs Learnt
    pl.program_name AS learnt_program_name

FROM 
    Soldiers s
LEFT JOIN 
    M_History mh ON s.id = mh.soldier_id              -- Join with military history
LEFT JOIN 
    Awards a ON s.id = a.soldier_id                   -- Join with awards
LEFT JOIN 
    Dependents d ON s.id = d.personnel_id             -- Join with dependents
LEFT JOIN 
    programs_taught pt ON s.id = pt.soldier_id        -- Join with programs taught
LEFT JOIN 
    programs_learnt_2 pl ON s.id = pl.soldier_id      -- Join with programs learnt
WHERE 
    s.id = 1001;                     -- Replace with the actual soldier_id
