# Military Database

## 1. Change the instructor for a Newbie's course
### Description
Updates the instructor assigned to a specific program in a branch.
### Inputs
- Program name
- Branch name
- New instructor ID
### SQL Query:
```
UPDATE enrolled_in_1
SET instructor_id = new_instructor_ID
WHERE program_name = program_name AND branch_name = branch_name;
```
## 2. Assign a battalion to a different brigade
### Description
Changes the brigade assignment for a given battalion.
### Inputs:
- Battalion ID
- Brigade ID
### SQL Query:
```
UPDATE Battalions
SET brigade_id = brigade_id
WHERE battalion_id = battalion_id;
```
## 3. Assign an operation to a different battalion
### Description
Updates the battalion responsible for a specific operation.
### Inputs:
- Operation ID
- Battalion ID
### SQL Query:
```
UPDATE Assigned_To
SET battalion_id = battalion_id
WHERE operation_id = operation_id;
```
## 4. Add a new department
### Description
Adds a new department to the database with its ID, name, and associated battalion.
### Inputs:
- Department ID
- Department name
- Battalion ID
### SQL Query:
```
INSERT INTO Departments (dept_id, dept_name, battalion_id)
VALUES (dept_id, dept_name, battalion_id);
```
## 5. Remove a soldier
### Description
Deletes a soldier's record from the database using their unique ID.
### Inputs:
- Soldier ID
### SQL Query:
```
DELETE FROM Soldiers
WHERE id = soldier_id;
```
## 6. Exit
### Description
Exits the program and closes the database connection.
