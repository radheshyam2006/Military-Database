SELECT 
    n.phone_number,
    CONCAT(n.first_name, ' ', n.last_name) AS newbie_name,
    n.birth_date AS date_of_birth,
    n.street_no,
    n.city,
    n.district,
    n.state,

    -- Programs Enrolled
    pe.program_name AS enrolled_program_name,
    pe.branch_name AS enrolled_branch_name,

    -- Programs Learnt
    pl.program_name AS learnt_program_name

FROM 
    Newbies n
LEFT JOIN 
    enrolled_in_1 pe ON n.phone_number = pe.phone_number
LEFT JOIN 
    programs_learnt_1 pl ON n.phone_number = pl.phone_number
WHERE 
    n.phone_number = 9876543210;
