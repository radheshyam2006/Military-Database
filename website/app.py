import pymysql
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, Response
from collections import defaultdict

app = Flask(__name__)
app.secret_key = "dna_TAs_are_the_best"

mydb = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "IIITHydmysql123",
    database = "military"
)

if mydb.open:
    print("Connected")
    cur = mydb.cursor()
else:
    print("Falied to connect")

@app.route('/', methods=['POST','GET'])
def index():
    return render_template("index.html")

@app.route('/higher_officials', methods=['POST','GET'])
def ho():
    query = """
        SELECT 
            lg.soldier_id,
            lg.personal_weapon_id,
            CONCAT(s.first_name, ' ', s.last_name) AS soldier_name,
            lg.oc_id AS oc_id
        FROM Lieutenant_General lg
        JOIN Soldiers s ON lg.soldier_id = s.id;
    """
    cur.execute(query)
    lt_gen_data = cur.fetchall()
    # print(lt_gen_data)
    # print()

    query = """
        SELECT 
            mg.soldier_id,
            mg.personal_weapon_id,
            CONCAT(s.first_name, ' ', s.last_name) AS soldier_name,
            mg.div_id AS div_id,
            d.div_name AS div_name
        FROM Major_Generals mg
        JOIN Soldiers s ON mg.soldier_id = s.id
        JOIN Divisions d ON mg.div_id = d.div_id;
    """
    cur.execute(query)
    major_gen_data = cur.fetchall()
    # print(major_gen_data)
    # print()

    query = """
        SELECT 
            bg.soldier_id,
            bg.personal_weapon_id,
            CONCAT(s.first_name, ' ', s.last_name) AS soldier_name,
            bg.brigade_id AS brigade_id,
            b.brigade_name AS brigade_name
        FROM Brigadiers bg
        JOIN Soldiers s ON bg.soldier_id = s.id
        JOIN Brigades b ON bg.brigade_id = b.brigade_id;
    """
    cur.execute(query)
    brigadier_data = cur.fetchall()
    # print(brigadier_data)
    # print()

    query = """
        SELECT 
            c.soldier_id,
            c.personal_weapon_id,
            CONCAT(s.first_name, ' ', s.last_name) AS soldier_name,
            c.battalion_id AS battalion_id,
            batt.battalion_name AS battalion_name
        FROM Colonels c
        JOIN Soldiers s ON c.soldier_id = s.id
        JOIN Battalions batt ON c.battalion_id = batt.battalion_id;
    """
    cur.execute(query)
    colonel_data = cur.fetchall()
    # print(colonel_data)
    # print()
    
    return render_template("ho.html", lt_gen_data=lt_gen_data, major_gen_data=major_gen_data, brigadier_data=brigadier_data, colonel_data=colonel_data)

def transform_data(data):
    hierarchy = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))

    for branch_name, oc_id, div_id, div_name, brig_id, brig_name, batt_id, batt_name in data:
        branch = hierarchy[branch_name]
        operational_command = branch[oc_id]
        division = operational_command[(div_id, div_name)]
        brigade = division[(brig_id, brig_name)]
        brigade.append((batt_id, batt_name))

    return hierarchy

@app.route('/branches', methods=['POST','GET'])
def branches():
    query = """
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
    """
    cur.execute(query)
    branches_data = cur.fetchall()
    # print(branches_data)
    data = transform_data(branches_data)
    # print(data)
    # parse it into a dictionary
    # data = {}
    return render_template("branches.html", hierarchy=data)

@app.route('/soldiers_and_newbies', methods=['POST','GET'])
def s_and_n():
    query = """
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
    """
    cur.execute(query)
    soldiers_data = cur.fetchall()
    # print(soldiers_data)
    
    query = "SELECT CONCAT(first_name, ' ', last_name) AS soldier_name, phone_number FROM Newbies;" # to get the data of newbies
    cur.execute(query)
    newbies_data = cur.fetchall()
    # print(newbies_data)

    result = {
        "soldiers": soldiers_data,
        "newbies": newbies_data
    }
    return render_template("soldiers_and_newbies.html", data=result)

def transform_soldier(data1, data2, data3, data4, data5, data6):
    soldier = {}
    soldier['id'] = data1[0]
    soldier['name'] = data1[1]
    soldier['birth_date'] = data1[2]
    soldier['phone_number'] = data1[3]
    soldier['date_of_joining'] = data1[4]
    soldier['health_status'] = data1[5]
    soldier['street_no'] = data1[6]
    soldier['city'] = data1[7]
    soldier['district'] = data1[8]
    soldier['state'] = data1[9]

    soldier['history'] = [{'start_date': data[0], 'rank': data[1]} for data in data3]
    soldier['awards'] = [{'award_name': data[0], 'date_received': data[1]} for data in data4]
    soldier['programs_taught'] = [x[0] for x in data5]
    soldier['programs_learnt'] = [x[0] for x in data6]
    soldier['dependents'] = [{'name': data[1], 'relation': data[0], 'birth_date': data[2]} for data in data2]
    
    return soldier

@app.route('/soldiers/<id>', methods=['POST','GET'])
def soldier(id):
    query = """
        SELECT s.id AS soldier_id, CONCAT(s.first_name, ' ', s.last_name) AS soldier_name, s.birth_date, s.phone_number, s.date_of_joining, s.health_status, s.street_no, s.city, s.district, s.state
        FROM Soldiers s WHERE s.id = %s;
    """
    cur.execute(query, (id))
    data1 = cur.fetchone()
    
    query = "SELECT relation, dependent_name, dependent_birth_date FROM dependents WHERE personnel_id = %s"
    cur.execute(query, (id))
    data2 = cur.fetchall()
    
    query = "SELECT start_date, m_rank FROM m_history WHERE soldier_id = %s"
    cur.execute(query, (id))
    data3 = cur.fetchall()
    
    query = "SELECT award_name, date_received FROM awards WHERE soldier_id = %s"
    cur.execute(query, (id))
    data4 = cur.fetchall()
    
    query = "SELECT program_name FROM programs_taught WHERE soldier_id = %s"
    cur.execute(query, (id))
    data5 = cur.fetchall()
    
    query = "SELECT program_name from programs_learnt_2 WHERE soldier_id = %s"
    cur.execute(query, (id))
    data6 = cur.fetchall()
    
    data = transform_soldier(data1, data2, data3, data4, data5, data6)

    return render_template("soldier.html", soldier=data)

def transform_newbie(data1, data2, data3):
    newbie = {}
    newbie['phone_number'] = data1[0]
    newbie['name'] = data1[1]
    newbie['birth_date'] = data1[2]
    newbie['street_no'] = data1[3]
    newbie['city'] = data1[4]
    newbie['district'] = data1[5]
    newbie['state'] = data1[6]
    newbie['enrolled_programs'] = [x[0] for x in data2]
    newbie['learnt_programs'] = [x[0] for x in data3]
    
    return newbie

@app.route('/newbies/<ph_no>', methods=['POST','GET'])
def newbie(ph_no):
    query = """
        SELECT n.phone_number, CONCAT(n.first_name, ' ', n.last_name) AS newbie_name, n.birth_date AS date_of_birth, n.street_no, n.city, n.district, n.state
        FROM Newbies n
        WHERE n.phone_number = %s;
    """
    cur.execute(query, (ph_no,))
    data1 = cur.fetchone()
    
    query = "SELECT program_name FROM enrolled_in_1 WHERE phone_number = %s"
    cur.execute(query, (ph_no,))
    data2 = cur.fetchall()
    
    query = "SELECT program_name FROM programs_learnt_1 WHERE phone_number = %s"
    cur.execute(query, (ph_no,))
    data3 = cur.fetchall()
    
    newbie = transform_newbie(data1, data2, data3)
    
    return render_template("newbie.html", newbie=newbie)

def transform_data3(data, keys, sub_org, sub_org_1, sub_org_2):
    new_data = {}
    i = 0
    for key in keys:
        new_data[key] = data[0][i]
        i += 1
    new_data["location"]  = {
        "latitude": data[0][i],
        "longitude": data[0][i + 1]
    }
    i += 2
    new_data[sub_org] = []
    for tuple in data:
        new_div = {
            sub_org_1: tuple[i],
            sub_org_2: tuple[i + 1]
        }
        new_data[sub_org].append(new_div)
    # print(new_data)
    return new_data

@app.route('/ocs/<oc_id>', methods=['POST','GET'])
def oc(oc_id):
    query = """
        SELECT 
            o.oc_id,
            o.branch_name AS branch_name,  -- Assuming branch_name represents the OC's name or role
            lg.soldier_id AS lieutenant_general_id,    -- Lieutenant General's soldier ID
            CONCAT(s.first_name, ' ', s.last_name) AS lieutenant_general_name,  -- Full name of the Lieutenant General
            o.latitude AS oc_latitude,
            o.longitude AS oc_longitude,
            d.div_id,
            d.div_name
        FROM 
            OCs o
        LEFT JOIN 
            Divisions d ON o.oc_id = d.oc_id
        LEFT JOIN 
            Lieutenant_General lg ON o.oc_id = lg.oc_id  -- Join to get the Lieutenant General for this OC
        LEFT JOIN 
            Soldiers s ON lg.soldier_id = s.id           -- Join to get the name of the Lieutenant General from Soldiers table
        WHERE 
            o.oc_id = %s;                  -- Replace with the actual OC ID
    """
    cur.execute(query, (oc_id))
    data = cur.fetchall()
    print(data)
    data = transform_data3(data, ["oc_id", "branch_name", "lieutenant_general_id", "lieutenant_general_name"], "divisions", "div_id", "div_name")
    # parse the data and store it in data dictionary
    return render_template("oc.html", entity="oc", data=data)

@app.route('/divs/<div_id>', methods=['POST','GET'])
def division(div_id):
    data = {}
    query = """
        SELECT 
            d.div_id,
            d.div_name,
            d.oc_id,
            mg.soldier_id AS major_general_id,
            CONCAT(s.first_name, ' ', s.last_name) AS major_general_name,
            d.latitude AS div_latitude,
            d.longitude AS div_longitude,
            b.brigade_id,
            b.brigade_name
        FROM 
            Divisions d
        LEFT JOIN 
            Brigades b ON d.div_id = b.div_id
        LEFT JOIN 
            Major_Generals mg ON d.div_id = mg.div_id
        LEFT JOIN 
            Soldiers s ON mg.soldier_id = s.id
        WHERE 
            d.div_id = %s;
    """
    cur.execute(query, (div_id))
    data = cur.fetchall()
    data = transform_data3(data, ["div_id", "div_name", "oc_id", "major_general_id", "major_general_name"], "brigades", "brigade_id", "brigade_name")
    # print(data)
    # parse the data and store it in data dictionary
    return render_template("div.html", entity="division", data=data)

@app.route('/brigades/<brigade_id>', methods=['POST','GET'])
def brigade(brigade_id):
    query = """
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
            b.brigade_id = %s;
    """
    cur.execute(query, (brigade_id))
    data = cur.fetchall()
    brigade = transform_data3(data, ["brigade_id", "brigade_name", "div_id", "brigadier_id", "brigadier_name"], "battalions", "battalion_id", "battalion_name")

    query = """
        SELECT e.equipment_id, eb.soldier_id, e.date_of_manufacture, e.equipment_status, e.use_before, e.model AS equipment_model, m.type_of_item, m.cost, m.manufacturer
        FROM Equipped_by eb
        JOIN Equipment e ON eb.equipment_id = e.equipment_id
        JOIN Models m ON e.model = m.model_name
        WHERE eb.brigade_id = %s;
    """
    cur.execute(query, (brigade_id))
    brigade["equipment"] = cur.fetchall()

    return render_template("brigade.html", brigade=brigade)

def transform_battalion(data1, data2):
    result = {}
    keys = ["battalion_id", "battalion_name", "brigade_id", "colonel_id", "colonel_name"]
    i = 0
    for k in keys:
        result[k] = data1[i]
        i += 1
    result["location"] = {
        "latitude": data1[i],
        "longitude": data1[i + 1]
    }
    
    dept_dict = {}
    for row in data2:
        dept_id, dept_name, soldier_id = row
        if dept_id not in dept_dict:
            dept_dict[dept_id] = {
                "dept_id": dept_id,
                "dept_name": dept_name,
                "soldier_ids": []
            }
        dept_dict[dept_id]["soldier_ids"].append(soldier_id)

    result["departments"] = list(dept_dict.values())
    return result

@app.route('/battalions/<battalion_id>', methods=['POST','GET'])
def battalion(battalion_id):
    query = """
        SELECT b.battalion_id, b.battalion_name, b.brigade_id, c.soldier_id AS colonel_id, CONCAT(s.first_name, ' ', s.last_name) AS colonel_name, b.latitude AS battalion_latitude, b.longitude AS battalion_longitude
        FROM Battalions b
        LEFT JOIN Colonels c ON b.battalion_id = c.battalion_id
        LEFT JOIN Soldiers s ON c.soldier_id = s.id
        WHERE b.battalion_id = %s;
    """
    cur.execute(query, (battalion_id))
    data1 = cur.fetchone()
    
    query = "SELECT d1.dept_id, d1.dept_name, d2.soldier_id FROM departments d1 JOIN dept_mems d2 ON d1.dept_id = d2.dept_id WHERE d1.battalion_id = %s"
    cur.execute(query, (battalion_id))
    data2 = cur.fetchall()

    battalion = transform_battalion(data1, data2)
    # print(battalion)

    # parse the data and store it in data dictionary
    return render_template("battalion.html", battalion=battalion)

def transform_data2(data):
    result = {}
    for program_name, branch_name, duration, skill in data:
        if branch_name not in result:
            result[branch_name] = {}
        if program_name not in result[branch_name]:
            result[branch_name][program_name] = {
                "duration": duration,
                "skills": []
            }
        if skill and skill not in result[branch_name][program_name]["skills"]:
            result[branch_name][program_name]["skills"].append(skill)
    return result

@app.route('/training_progs', methods=['POST','GET'])
def training_progs():
    query = """
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
    """
    cur.execute(query)
    data = cur.fetchall()
    data = transform_data2(data)
    # parse the data and store it in data dictionary
    return render_template("training_prog.html", data=data)

@app.route('/training_progs/<branch_name>/<program_name>', methods=['GET', 'POST'])
def tp(branch_name, program_name):
    # replace underscores with spaces
    branch_name = branch_name.replace("_", " ")
    program_name = program_name.replace("_", " ")

    query = """
        SELECT tp.duration
        FROM training_programs tp
        WHERE tp.program_name = %s AND tp.branch_name = %s;
    """
    cur.execute(query, (program_name, branch_name))
    duration = cur.fetchone()

    query = """
        SELECT st.skill
        FROM skills_taught st
        WHERE st.program_name = %s AND st.branch_name = %s;
    """
    cur.execute(query, (program_name, branch_name))
    data1 = cur.fetchall()

    query = """
        SELECT phone_number, instructor_id
        FROM enrolled_in_1
        WHERE program_name = %s AND branch_name = %s;
    """
    cur.execute(query, (program_name, branch_name))
    data2 = cur.fetchall()
    
    query = """
        SELECT soldier_id, instructor_id
        FROM enrolled_in_2
        WHERE program_name = %s AND branch_name = %s;
    """
    cur.execute(query, (program_name, branch_name))
    data3 = cur.fetchall()
    
    tp = {
        "branch_name": branch_name,
        "program_name": program_name,
        "duration": duration[0] if duration else None,
        "skills": [skill for skill in data1],
        "newbies": {
            "instructor_id": data2[0][1] if data2 and len(data2) > 0 and len(data2[0]) > 1 else None,
            "phone_numbers": [row[0] for row in data2]
        },
        "soldiers": {
            "instructor_id": data3[0][1] if data3 and len(data3) > 0 and len(data3[0]) > 1 else None,
            "soldier_ids": [row[0] for row in data3]
        }
    }

    return render_template("tp.html", tp=tp)

@app.route('/operations', methods=['POST','GET'])
def operations():
    query = "SELECT * FROM Assigned_To;"
    cur.execute(query)
    operations = cur.fetchall()

    return render_template("operations.html", data=operations)

@app.route('/operations/<op_id>', methods=['POST','GET'])
def one_op(op_id):
    data = {}
    query = """
        SELECT 
            o.*,
            at.battalion_id
        FROM Operations o
        LEFT JOIN Assigned_To at ON o.operation_id = at.operation_id
        WHERE o.operation_id = %s;
    """
    cur.execute(query, (op_id))
    data = cur.fetchone()
    print(data)
    # parse the data and store it in data dictionary
    return render_template("op.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)

mydb.commit()
cur.close()
mydb.close()
