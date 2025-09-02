WITH RECURSIVE Hierarchy AS (
    -- Step 1: Start with the Military Branch
    SELECT 
        branch_name AS level_name,
        'Military_Branches' AS level_type,
        branch_name AS branch,
        branch_name AS branch_name,
        CAST(NULL AS SIGNED) AS oc_id,
        CAST(NULL AS CHAR(20)) AS oc_name,
        CAST(NULL AS SIGNED) AS div_id,
        CAST(NULL AS CHAR(50)) AS div_name,
        CAST(NULL AS SIGNED) AS brigade_id,
        CAST(NULL AS CHAR(50)) AS brigade_name,
        CAST(NULL AS SIGNED) AS battalion_id,
        CAST(NULL AS CHAR(20)) AS battalion_name
    FROM Military_Branches

    UNION ALL

    -- Step 2: Get OCs under the branch
    SELECT 
        o.oc_id AS level_name,
        'OCs' AS level_type,
        o.branch_name AS branch,
        h.branch_name,
        o.oc_id,
        o.latitude AS oc_name,
        CAST(NULL AS SIGNED) AS div_id,
        CAST(NULL AS CHAR(50)) AS div_name,
        CAST(NULL AS SIGNED) AS brigade_id,
        CAST(NULL AS CHAR(50)) AS brigade_name,
        CAST(NULL AS SIGNED) AS battalion_id,
        CAST(NULL AS CHAR(20)) AS battalion_name
    FROM OCs o
    INNER JOIN Hierarchy h ON o.branch_name = h.branch AND h.level_type = 'Military_Branches'

    UNION ALL

    -- Step 3: Get Divisions under the OCs
    SELECT 
        d.div_id AS level_name,
        'Divisions' AS level_type,
        h.branch,
        h.branch_name,
        h.oc_id,
        h.oc_name,
        d.div_id,
        d.div_name,
        CAST(NULL AS SIGNED) AS brigade_id,
        CAST(NULL AS CHAR(50)) AS brigade_name,
        CAST(NULL AS SIGNED) AS battalion_id,
        CAST(NULL AS CHAR(20)) AS battalion_name
    FROM Divisions d
    INNER JOIN Hierarchy h ON d.oc_id = h.oc_id AND h.level_type = 'OCs'

    UNION ALL

    -- Step 4: Get Brigades under the Divisions
    SELECT 
        b.brigade_id AS level_name,
        'Brigades' AS level_type,
        h.branch,
        h.branch_name,
        h.oc_id,
        h.oc_name,
        h.div_id,
        h.div_name,
        b.brigade_id,
        b.brigade_name,
        CAST(NULL AS SIGNED) AS battalion_id,
        CAST(NULL AS CHAR(20)) AS battalion_name
    FROM Brigades b
    INNER JOIN Hierarchy h ON b.div_id = h.div_id AND h.level_type = 'Divisions'

    UNION ALL

    -- Step 5: Get Battalions under the Brigades
    SELECT 
        batt.battalion_id AS level_name,
        'Battalions' AS level_type,
        h.branch,
        h.branch_name,
        h.oc_id,
        h.oc_name,
        h.div_id,
        h.div_name,
        h.brigade_id,
        h.brigade_name,
        batt.battalion_id,
        batt.battalion_name
    FROM Battalions batt
    INNER JOIN Hierarchy h ON batt.brigade_id = h.brigade_id AND h.level_type = 'Brigades'
)

-- Final query to return all levels in the hierarchy
SELECT 
    branch,
    oc_id,
    div_id,
    div_name,
    brigade_id,
    brigade_name,
    battalion_id,
    battalion_name
FROM Hierarchy
WHERE level_type = 'Battalions'
ORDER BY branch, oc_id, div_id, brigade_id, battalion_id;
