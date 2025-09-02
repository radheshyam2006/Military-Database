SELECT 
    o.*,
    at.battalion_id
FROM Operations o
LEFT JOIN Assigned_To at ON o.operation_id = at.operation_id
WHERE o.operation_id = 1;
