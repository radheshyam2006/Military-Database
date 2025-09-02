SELECT 
    tp.program_name,
    tp.branch_name,
    tp.duration,
    st.skill
FROM 
    Training_Programs tp
LEFT JOIN 
    skills_taught st 
ON 
    tp.program_name = st.program_name AND tp.branch_name = st.branch_name;
