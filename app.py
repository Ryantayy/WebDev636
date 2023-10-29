from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect
import os

app = Flask(__name__)

dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/listcourses")
def listcourses():
    connection = getCursor()
    #Fetch  the list of courses from the database
    connection.execute("SELECT * FROM course;")
    courseList = connection.fetchall()
    return render_template("courselist.html", course_list = courseList)

@app.route("/select_driver")
def select_driver():
    # Fetch the list of drivers from the database or any other data source
    connection = getCursor()
    connection.execute("SELECT * from driver;")
    driverList = connection.fetchall()

    # Render the driver_selection.html template with the driver list
    return render_template("driver_selection.html", driver_list=driverList)

# Define a route that handles both GET and POST requests for driver run details.
@app.route("/driver_run_details", methods=["GET", "POST"])
def driver_run_details(driver_id=None):
    # Check if the request method is POST, and if so, retrieve driver_id from the form data.
    if request.method == "GET":
        driver_id = request.args.get("driver_id")
    if request.method == "POST":
        driver_id = request.form.get("driver_id")
    
    # Fetch driver details and run details from the database based on the provided driver_id.
    connection = getCursor()  # Replace 'getCursor()' with the appropriate database connection function.
    
    # Query to fetch driver details (e.g., name, car model, drive class) based on driver_id.
    connection.execute("""SELECT driver.driver_id, driver.first_name, driver.surname, car.model, car.drive_class
                        FROM driver
                        JOIN car ON driver.car = car.car_num
                        WHERE driver_id = %s;""", (driver_id,))
    driverList = connection.fetchone()  # Get a single driver record.
    
    # Query to fetch run details (e.g., run time, cones, course name) for the given driver_id.
    connection.execute("""SELECT r.dr_id, r.crs_id, r.run_num, COALESCE(r.seconds, '') AS seconds, COALESCE(r.cones, '') AS cones, r.wd, 
                        c.name, COALESCE(ROUND(r.seconds + IFNULL(r.cones, 0) * 5 + CASE WHEN r.wd = 1 THEN 10 ELSE 0 END, 2), '') AS run_total,
                        CASE WHEN r.wd = 1 THEN 'WD' ELSE '' END AS wd_display
                        FROM run r
                        JOIN course c ON r.crs_id = c.course_id
                        WHERE dr_id = %s;""", (driver_id,))
    runList = connection.fetchall()  # Get a list of all run records for the driver.
    
    # Render the 'driver_run_details.html' template and pass the retrieved data as context variables.
    return render_template("driver_run_details.html", driver_list=driverList, run_list=runList)

# Define a route to list all drivers.
@app.route("/listdrivers")
def listdrivers():
    connection = getCursor()
    
    # Execute an SQL query to fetch details of all drivers, including car and caregiver information.
    connection.execute("""SELECT d.driver_id, 
                        CONCAT(d.first_name, ' ', d.surname) AS Name, 
                        COALESCE(d.date_of_birth, '') AS date_of_birth,
                        d.age, COALESCE(CONCAT(cg.first_name, ' ', cg.surname), '') AS Caregiver,
                        c.model, c.drive_class, COALESCE(d.age, '') AS age_display
                        FROM driver d
                        JOIN car c ON d.car = c.car_num
                        LEFT JOIN driver cg ON d.caregiver = cg.driver_id
                        ORDER BY d.surname, d.first_name;""")
    
    # Fetch all driver records from the executed query.
    driverList = connection.fetchall()
    
    # Render the 'driverlist.html' template and pass the retrieved driver data as a context variable.
    return render_template("driverlist.html", driver_list=driverList)

# Define a route to display overall race results.
@app.route("/overallresults")
def overallresults():
    connection = getCursor()
    
    # Execute a SQL query to compute overall race results for drivers.
    connection.execute("""
        WITH CourseTimes AS (
            -- Subquery to calculate the best time for each driver on each course.
            SELECT d.driver_id, r.crs_id,
            COALESCE(ROUND(MIN(r.seconds + IFNULL(r.cones, 0) * 5 + IFNULL(r.wd, 0) * 10), 2), 'dnf') AS best_time
            FROM driver AS d
            JOIN run AS r ON d.driver_id = r.dr_id
            JOIN car AS c ON d.car = c.car_num
            GROUP BY d.driver_id, r.crs_id
        ),
        RankedResults AS (
            -- Subquery to rank drivers based on their best times.
            SELECT d.driver_id, CONCAT(d.first_name, ' ', d.surname,
                CASE WHEN d.age >= 12 AND d.age <= 25 THEN ' (J)' ELSE '' END) AS Name, c.model,
                COALESCE(MAX(CASE WHEN ct.crs_id = 'A' THEN best_time END), 'dnf') AS 'A',
                COALESCE(MAX(CASE WHEN ct.crs_id = 'B' THEN best_time END), 'dnf') AS 'B',
                COALESCE(MAX(CASE WHEN ct.crs_id = 'C' THEN best_time END), 'dnf') AS 'C',
                COALESCE(MAX(CASE WHEN ct.crs_id = 'D' THEN best_time END), 'dnf') AS 'D',
                COALESCE(MAX(CASE WHEN ct.crs_id = 'E' THEN best_time END), 'dnf') AS 'E',
                COALESCE(MAX(CASE WHEN ct.crs_id = 'F' THEN best_time END), 'dnf') AS 'F',
                CASE WHEN 'dnf' IN (MAX(CASE WHEN ct.crs_id = 'A' THEN best_time END),
                    MAX(CASE WHEN ct.crs_id = 'B' THEN best_time END),
                    MAX(CASE WHEN ct.crs_id = 'C' THEN best_time END),
                    MAX(CASE WHEN ct.crs_id = 'D' THEN best_time END),
                    MAX(CASE WHEN ct.crs_id = 'E' THEN best_time END),
                    MAX(CASE WHEN ct.crs_id = 'F' THEN best_time END))
                THEN 'NQ'
                ELSE CAST(ROUND(
                    COALESCE(MAX(CASE WHEN ct.crs_id = 'A' THEN best_time END), 0) +
                    COALESCE(MAX(CASE WHEN ct.crs_id = 'B' THEN best_time END), 0) +
                    COALESCE(MAX(CASE WHEN ct.crs_id = 'C' THEN best_time END), 0) +
                    COALESCE(MAX(CASE WHEN ct.crs_id = 'D' THEN best_time END), 0) +
                    COALESCE(MAX(CASE WHEN ct.crs_id = 'E' THEN best_time END), 0) +
                    COALESCE(MAX(CASE WHEN ct.crs_id = 'F' THEN best_time END), 0), 2) 
                    AS CHAR)
                END AS Overall,
                ROW_NUMBER() OVER (ORDER BY CASE WHEN Overall = 'NQ' THEN 1 ELSE 0 END,
                    CAST(Overall AS DECIMAL(10, 2)) ASC) AS rn
            FROM driver AS d
            JOIN CourseTimes ct ON d.driver_id = ct.driver_id
            JOIN car AS c ON d.car = c.car_num
            GROUP BY d.driver_id, d.first_name, d.surname, c.model, d.age
        )
        -- Select the final results, including ranking information.
        SELECT driver_id, Name, model, `A`, `B`, `C`, `D`, `E`, `F`, Overall,
        CASE WHEN rn = 1 THEN 'cup' WHEN rn BETWEEN 2 AND 5 THEN 'prize' ELSE '' END AS ''
        FROM RankedResults
        ORDER BY CASE WHEN Overall = 'NQ' THEN 1 ELSE 0 END, CAST(Overall AS DECIMAL(10, 2)) ASC;
    """)
    
    # Fetch the overall race results from the executed query.
    overallResults = connection.fetchall()
    
    # Render the 'overallresults.html' template and pass the retrieved results as context variables.
    return render_template("overallresults.html", overall_results=overallResults)

# Define a route to display a graph of the top 5 drivers.
@app.route("/graph")
def showgraph():
    connection = getCursor()
    
    # Execute an SQL query to retrieve the top 5 drivers with the best overall results.
    connection.execute("""
        SELECT 
        DriverName, 
        ROUND(TotalResult, 2) AS OverallResult
        FROM (
        SELECT d.driver_id, 
        CONCAT(d.driver_id, ' ', d.first_name, ' ', d.surname, ' ') AS DriverName, 
        SUM(COALESCE(bt.best_time, 0)) AS TotalResult
        FROM driver AS d 
        LEFT JOIN (
            SELECT d.driver_id, r.crs_id, 
            MIN(r.seconds + IFNULL(r.cones, 0) * 5 + IFNULL(r.wd, 0) * 10) AS best_time
            FROM driver AS d
            JOIN run AS r ON d.driver_id = r.dr_id
            GROUP BY d.driver_id, r.crs_id
        ) AS bt ON d.driver_id = bt.driver_id
        GROUP BY d.driver_id, d.first_name, d.surname
        HAVING COUNT(DISTINCT bt.crs_id) = 6 AND COUNT(CASE WHEN bt.best_time IS NULL THEN 1 END) = 0
        ) AS tmp
        ORDER BY OverallResult ASC
        LIMIT 5;
    """)
    
    # Fetch the top 5 drivers' data from the executed query.
    result = connection.fetchall()
    
    # Extract names and results into separate lists
    bestDriverList = [row[0] for row in result]
    resultsList = [row[1] for row in result]
    
    # Render the 'top5graph.html' template and pass the retrieved data as context variables.
    return render_template("top5graph.html", result_list_from_py=bestDriverList, driver_list_from_py=resultsList)

# Define a route for the admin Interface.
@app.route("/admin")
def adminInterface():
    return render_template("adminHome.html")

# Define a route to display a list of junior drivers.
@app.route('/admin/junior-drivers')
def junior_driver_list():
    connection = getCursor()
    
    # Execute an SQL query to fetch details of junior drivers (age between 12 and 25).
    connection.execute("""
        SELECT d.driver_id, CONCAT(d.first_name, ' ', d.surname) AS Name, d.date_of_birth, d.age, 
        COALESCE(CONCAT(cg.first_name, ' ', cg.surname), '') AS Caregiver_Name, 
        c.model, c.drive_class
        FROM driver d
        JOIN car c ON d.car = c.car_num
        LEFT JOIN driver cg ON d.caregiver = cg.driver_id
        WHERE d.age BETWEEN 12 AND 25
        ORDER BY d.age DESC, d.surname;
    """)
    
    # Fetch the list of junior drivers from the executed query.
    juniorDriverList = connection.fetchall()
    
    # Render the 'junior_driver_list.html' template and pass the retrieved data as context variables.
    return render_template('junior_driver_list.html', junior_driver_list=juniorDriverList)


#Define a route to return to the driver Interface
@app.route("/driverInterface")
def driverInterface():
    return render_template("home.html")

# Define a route to search for drivers based on a keyword.
@app.route('/search_driver', methods=['POST'])
def search_driver():
    # Get the keyword to search for from the form data.
    keyword = str(request.form.get('keyword'))
    
    connection = getCursor()
    
    # Execute an SQL query to search for drivers whose first name or surname contains the keyword.
    connection.execute("""
        SELECT d.driver_id, 
        CONCAT(d.first_name, ' ', d.surname) AS Name, 
        COALESCE(d.date_of_birth, '') AS date_of_birth, d.age, 
        COALESCE(CONCAT(cg.first_name, ' ', cg.surname), '') AS Caregiver,
        c.model, c.drive_class,
        COALESCE(d.age, '') AS age_display
        FROM driver d
        JOIN car c ON d.car = c.car_num
        LEFT JOIN driver cg ON d.caregiver = cg.driver_id
        WHERE d.first_name LIKE %s OR d.surname LIKE %s
        ORDER BY d.surname, d.first_name;
    """, (f"%{keyword}%", f"%{keyword}%"))
    
    # Fetch the search results from the executed query.
    results = connection.fetchall()
    
    # Render the 'search_results.html' template and pass the retrieved results as context variables.
    return render_template('search_results.html', results=results)

# Define a route to edit runs for drivers.
@app.route('/edit_runs', methods=['GET', 'POST'])
def edit_runs():
    connection = getCursor()
    runList = None
    run_num = None 
    success_message = request.args.get('success')
    
    if request.method == 'POST':
        selected_driver = request.form.get('driver')
        selected_course = request.form.get('course')
    else:
        selected_driver = request.args.get('selected_driver')
        selected_course = request.args.get('selected_course')
        run_num = request.args.get('run_num') 

    # Base query to fetch run details for filtering
    base_query = """SELECT r.dr_id, CONCAT(d.first_name, ' ', d.surname) AS Name, c.name AS Course_Name, 
                   r.run_num, COALESCE(r.seconds, '') AS seconds, r.cones, r.wd,  
                   COALESCE(ROUND(r.seconds + IFNULL(r.cones, 0) * 5 + IFNULL(r.wd, 0) * 10, 2), '') AS run_total, r.crs_id, 
                   CASE WHEN r.cones IS NULL THEN '' ELSE r.cones END AS cones_display,
                   CASE WHEN r.wd = 1 THEN 'WD' ELSE '' END AS wd_display
                   FROM run r
                   JOIN course c ON r.crs_id = c.course_id
                   JOIN driver d ON r.dr_id = d.driver_id WHERE """
    
    params = []

    if selected_driver:
        base_query += "r.dr_id= %s"
        params.append(selected_driver)

    if selected_course:
        if selected_driver:
            base_query += " AND "
        base_query += "r.crs_id = %s"
        params.append(selected_course)

    if run_num:
        if selected_driver or selected_course:
            base_query += " AND "
        base_query += "r.run_num = %s"
        params.append(run_num)

    if selected_driver or selected_course:  # Only execute if at least one condition is provided
        connection.execute(base_query, tuple(params))
        runList = connection.fetchall()

    # Fetch the list of drivers and courses
    connection.execute("""SELECT d.driver_id, CONCAT(d.first_name, ' ', d.surname) AS Name,
                        d.date_of_birth, d.age, d.caregiver
                        FROM driver d;""")
    driverList = connection.fetchall()

    connection.execute("SELECT * FROM course;")
    courseList = connection.fetchall()

    return render_template('edit_runs.html', driver_list=driverList, course_list=courseList, run_list=runList, success=success_message)

# Define a route to edit an individual run.
@app.route('/edit_individual_run/<int:dr_id>/<crs_id>/<int:run_num>', methods=['GET', 'POST'])
def edit_individual_run(dr_id, crs_id, run_num):
    connection = getCursor()

    # Fetch the current run details to pre-populate the form or to handle errors
    connection.execute("""SELECT r.*, CONCAT(d.first_name, " ", surname) AS Name, c.name FROM run r
                        JOIN driver d ON r.dr_id = d.driver_id
                        JOIN course c ON r.crs_id = c.course_id 
                        WHERE dr_id = %s AND crs_id = %s AND run_num = %s;""", (dr_id, crs_id, run_num))
    run = connection.fetchone()

    # If the form has been submitted, update the run details in the database
    if request.method == 'POST':
        updated_time = request.form.get('time')
        updated_cones = request.form.get('cones')
        updated_wd = request.form.get('wd')
        errors = []  # Initialize an empty errors list
        
        # Input validation
        if updated_time:
            try:
                updated_time = float(updated_time)
            except ValueError:
                errors.append('Invalid time input')
        else:
            updated_time = None
    
        if updated_cones:
            try:
                updated_cones = int(updated_cones)
            except ValueError:
                errors.append('Invalid cones input. Please enter a numeric value')
        else:
            updated_cones = None

        if updated_wd:
            try:
                updated_wd = int(updated_wd)
            except ValueError:
                errors.append('Invalid WD input.')
        else:
            updated_wd = 0

        # Restrict inputs by user
        if updated_time is not None and (updated_time < 10 or updated_time > 300):
            errors.append('Invalid input. Time record must be in the range of 10.00s - 300.00s.')
        elif updated_cones is not None and (updated_cones < 0 or updated_cones > 20):
            errors.append('Invalid input. Cones must be in the range of 0-20.')
        elif updated_wd < 0 or updated_wd > 1:
            errors.append('Invalid input. WD must be either 0 (No Wrong Direction) or 1 (Wrong Direction).')

        # Handle errors
        if errors: 
            return render_template('edit_individual_run.html', run=run, errors=errors) # Render the edit_individual_run.html template with the errors list

        # Update run details in the database
        connection.execute("""UPDATE run
                        SET seconds = %s, cones = %s, wd = %s
                        WHERE dr_id = %s AND crs_id = %s AND run_num = %s;""", (updated_time, updated_cones, updated_wd, dr_id, crs_id, run_num))

        # Redirect back to the edit_runs page with a success message
        return redirect(url_for('edit_runs', selected_driver=dr_id, selected_course=crs_id, run_num=run_num, success='True')) 

    return render_template('edit_individual_run.html', run=run)

@app.route('/add_driver', methods=['GET', 'POST'])
def add_driver():
    connection = getCursor()
    errors = []
    success = True if 'success' in request.args else False
    first_name = ""
    surname = ""
    date_of_birth = None
    caregiver_id = None

    #Fetch the list of cars and caregivers
    connection.execute("""SELECT DISTINCT c.model, c.car_num, c.drive_class
                                FROM car c;""")
    carList = connection.fetchall()

    # Fetch the list of caregivers
    connection.execute("""SELECT driver_id, CONCAT(first_name, ' ', surname) AS Name
                        FROM driver
                        WHERE age is null or age >= 26;""")
    caregiverList = connection.fetchall()

    if request.method == 'POST':
        form_submit_type = request.form.get('form_submit_type')

         # If Yes is selected in 'Is Junior' field
        if form_submit_type == 'junior_change':
            is_junior = request.form.get('is_junior')
            return render_template('add_driver.html', car_list=carList, caregiver_list=caregiverList, date_of_birth=date_of_birth, caregiver_id=caregiver_id, is_junior=is_junior)

        #Fetch new driver details from the form
        else:
            first_name = request.form.get('first_name').strip()
            surname = request.form.get('surname').strip()
            is_junior = request.form.get('is_junior') == 'yes'
            age = None
            caregiver_id = request.form.get('caregiver')
            car = request.form.get('car')
            date_of_birth = request.form.get('date_of_birth') or None

            #Input Validation
            if not first_name or not first_name.strip():
                errors.append('First name is required and cannot be empty!')
            elif not surname or not surname.strip():
                errors.append('Surname is required and cannot be empty!')
            #Check if first_name or surname are numeric
            elif first_name.isnumeric():
                errors.append('First name cannot be numeric!')
            elif surname.isnumeric():
                errors.append('Surname cannot be numeric!')
            elif not date_of_birth:
                date_of_birth = None  # Set date_of_birth to none if it's empty
            elif is_junior and not date_of_birth:
                errors.append('Date of Birth is required for junior driver!')
            else:
                try:
                    # Check if the provided date matches the %Y-%m-%d format
                    birth_date = datetime.strptime(date_of_birth, '%Y-%m-%d')

                    # Calculate the age if date_of_birth is valid
                    today = datetime.today()
                    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                    
                    # Define the sensible range for age
                    MIN_AGE = 10
                    MAX_AGE = 100

                    # Check if the age is within the sensible range

                    if not (MIN_AGE <= age <= MAX_AGE):
                        errors.append(f"Age should be between {MIN_AGE} and {MAX_AGE} years.")

                    if age >=26:
                        errors.append("Only drivers aged 12 to 25 are considered junior drivers.")
                    
                    # Check for caregiver requirement
                    if age <= 16 and not caregiver_id:
                        errors.append("A caregiver is required for drivers aged 16 or younger.")
                    
                    if age >= 17 and caregiver_id:
                        errors.append("A caregiver is not required for drivers aged 17 or older.")

                except ValueError:
                    errors.append('Invalid date format for Date of Birth. Please use YYYY-MM-DD.')

            #returning the render_template with the errors list so the error messages can be displayed.
            if errors:
                return render_template('add_driver.html', car_list=carList, caregiver_list=caregiverList, first_name=first_name, surname=surname, date_of_birth=date_of_birth, errors=errors)

            #Only pass caregiver_id if the driver is a junior
            if is_junior == 'yes':
                caregiver_id = request.form.get('caregiver')

            if is_junior == 'no':
                caregiver_id = None  # Set caregiver_id to none if the driver is a junior
            #Add a new driver
            connection.execute("INSERT INTO driver (first_name, surname, date_of_birth, age, caregiver, car) VALUES (%s, %s, %s, %s, %s, %s);", 
                            (first_name, surname, date_of_birth, age, caregiver_id, car))

            # driver_id of the last inserted driver
            driver_id = connection.lastrowid 
            
            #Add 12 blanks runs
            courses = ['A', 'B', 'C', 'D', 'E', 'F']
            for course in courses:
                for run_num in range(1, 3):
                    connection.execute("INSERT INTO run (dr_id, crs_id, run_num, seconds, cones, wd) VALUES (%s, %s, %s, NULL, NULL, 0);", (driver_id, course, run_num))
            
        return redirect(url_for('add_driver', success=True))

    return render_template('add_driver.html', car_list=carList, caregiver_list=caregiverList, first_name=first_name, surname=surname, date_of_birth=date_of_birth, errors=errors, success=success)