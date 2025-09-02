import pymysql

# Database connection
mydb = pymysql.connect(
    host="localhost",
    user="root",
    password="M@ni1234",
    database="military"
)

if mydb.open:
    print("Connected")
    cur = mydb.cursor()
else:
    print("Failed to connect")

welcome_message = """Choose an option:

1. Change the instructor for a newbie's course
2. Assign a battalion to a different brigade
3. Assign an operation to a different battalion
4. Add a department
5. Remove a soldier
6. Exit
"""

def main():
    while True:
        print(welcome_message)
        try:
            option = int(input("> "))

            if option == 1:
                prog_name = input("Please provide program name: ")
                branch_name = input("Please provide branch name: ")
                new_instructor_id = int(input("Please provide new instructor id: "))
                query = """
                    UPDATE enrolled_in_1
                    SET instructor_id = %s
                    WHERE program_name = %s AND branch_name = %s;
                """
                cur.execute(query, (new_instructor_id, prog_name, branch_name))

            elif option == 2:
                battalion_id = int(input("Please provide battalion id: "))
                brigade_id = int(input("Please provide brigade id: "))
                query = """
                    UPDATE Battalions
                    SET brigade_id = %s
                    WHERE battalion_id = %s;
                """
                cur.execute(query, (brigade_id, battalion_id))

            elif option == 3:
                op_id = int(input("Please provide operation id: "))
                battalion_id = input("Please provide battalion id: ")
                query = """
                    UPDATE Assigned_To
                    SET battalion_id = %s
                    WHERE operation_id = %s;
                """
                cur.execute(query, (battalion_id, op_id))

            elif option == 4:
                dept_id = int(input("Please provide department id: "))
                dept_name = input("Please provide department name: ")
                battalion_id = int(input("Please provide battalion id: "))
                query = """
                    INSERT INTO Departments (dept_id, dept_name, battalion_id)
                    VALUES (%s, %s, %s);
                """
                cur.execute(query, (dept_id, dept_name, battalion_id))

            elif option == 5:
                soldier_id = int(input("Please provide soldier id: "))
                query = """
                    DELETE FROM Soldiers
                    WHERE id = %s;
                """
                cur.execute(query, (soldier_id,))

            elif option == 6:
                print("Exiting program.")
                break

            else:
                print("Invalid option. Please choose a valid one.")

            # Commit after each query execution
            mydb.commit()
            print("Operation successful.\n")

        except pymysql.MySQLError as e:
            print(f"Database Error: {e}")
            mydb.rollback()  # Roll back transaction on failure

        except ValueError:
            print("Invalid input! Please enter the correct data type.")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    # Close the connection
    cur.close()
    mydb.close()
    print("Connection closed.")

if __name__ == "__main__":
    main()
