-- Add a new soldier
INSERT INTO Soldiers VALUES (1523, 'Ayush', 'Sabhasad', '2005-04-01', 8010126758, '2024-11-26', "Dead", 69, "Pune", "Haveli", "Maharastra");
INSERT INTO Dept_Mems VALUES (1523, 144);
INSERT INTO M_History VALUES (1523, '2024-11-26', "Dept_mem");
INSERT INTO Awards VALUES (1523, "Defense Service Medal", '2024-11-27');
INSERT INTO Dependents VALUES (1523, "wife", "priya kulkarni", "2005-04-01");
INSERT INTO Equipped_by VALUES (34, 13, 1523);
INSERT INTO Programs_learnt_2 VALUES (1523, "Advanced Combat");
INSERT INTO Programs_taught VALUES (1523, "Aero Engineering");

-- test the soldier's presence
SELECT * FROM Soldiers WHERE id = 1523;
SELECT * FROM Dept_Mems WHERE Soldier_ID = 1523;
SELECT * FROM M_History WHERE Soldier_ID = 1523;
SELECT * FROM Awards WHERE Soldier_ID = 1523;
SELECT * FROM Dependents WHERE personnel_id = 1523;
SELECT * FROM Equipped_by WHERE Soldier_ID = 1523;
SELECT * FROM Programs_learnt_2 WHERE Soldier_ID = 1523;
SELECT * FROM Programs_taught WHERE Soldier_ID = 1523;

-- Option 1
SELECT * FROM enrolled_in_1;

-- Option 2
SELECT * FROM Battalions;

-- Option 3
SELECT * FROM Assigned_To;

-- Option 4
SELECT * FROM Departments;
DELETE FROM Departments WHERE dept_id = 145;
