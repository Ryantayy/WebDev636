# WebDev636
**Name**: Ryan Tay Peng Yeow <br>
**Student ID**: 1157892

**Web Application Structure:** <br>
**1. Structure Overview:**

My web application follows the typical structure of Flask projects. The application is organized with a combination of routes and their associated functions, and templates to render the appropriate views. This structure aids in maintaining a clean separation of concerns between data processing and presentation.

**2. Routes & Functions:**

/: <br>
Function: home() <br>
Description: Serves the homepage. <br>
Template: home.html <br>
Data Passed: None. <br>
Data Relationship: The root or index route uses the home.html template to serve as a home page with introductory information. Can add more information in the future related to the current user and recent news or events. <br>

/listcourses: <br>
Function: listcourses() <br>
Description: Displays the list of available courses. <br>
Template: course_list.html <br>
Data Passed: List of courses with their details. <br>
Data Relationship: The /course_list route fetches a list of available courses from the database in the course_list() function and provides this list to the course_list.html template to display. The templates allow for clickable images. <br>

/select_driver: <br>
Function: select_driver() <br>
Description: Displays a selection list of drivers. <br>
Template: driver_selection.html <br>
Data Passed: List of drivers with their details. <br>
Data Relationship: The /select_driver route fetches a list of drivers from the database in the select_driver() function and provides this list to the driver_selection.html template to display. <br>

/driver_run_details, methods=["GET"]/: and /driver_run_details, methods=["POST"]: <br>
Function: driver_run_details <br>
Description: Displays details of a specific driver and their runs. <br>
Template: driver_run_details.html <br>
Data Passed: Driver details and their corresponding run details. <br>
Data Relationship: Depending on the method, either it fetches the driver ID from the listdriver URL or from the POST request via a form submission. Using this ID, it fetches the driver's and their run details from the database. This data is then passed to the driver_run_details.html template for display. <br>

/listdrivers: <br>
Function: listdrivers() <br>
Description: Displays a list of all drivers. <br>
Template: driverlist.html <br>
Data Passed: List of drivers with their details. <br>
Data Relationship: The /listdrivers route fetches a list of drivers from the database in the listdrivers() function and provides this list to the driverlist.html template to display. <br>

/overallresults: <br>
Function: overallresults() <br>
Description: Displays overall results for each driver across different courses. <br>
Template: overallresults.html <br>
Data Passed: Aggregated results of drivers across courses. <br>
Data Relationship: The /overallresults route fetches aggregated results of drivers across different courses and then provides this data to the overallresults.html template to display. <br>

/graph: <br>
Function: showgraph() <br>
Description: Displays a graph showing top 5 drivers based on their overall results. <br>
Template: top5graph.html <br>
Data Passed: List of top 5 drivers and their results. <br>
Data Relationship: The /graph route fetches the top 5 driver's results and provides this data to the top5graph.html template to display as a graph. <br>

/admin: <br>
Function: adminInterface() <br>
Description: Displays the admin interface. <br>
Template: adminHome.html <br>
Data Passed: None. <br>
Data Relationship: Direct rendering of the adminHome.html template. <br>

/admin/junior-drivers: <br>
Function: junior_driver_list() <br>
Description: Displays a list of junior drivers. <br>
Template: junior_driver_list.html <br>
Data Passed: List of junior drivers and their details. <br>
Data Relationship: The /admin/junior-drivers route fetches a list of junior drivers from the database and provides this list to the junior_driver_list.html template to display. <br>

/driverInterface: <br>
Function: driverInterface() <br>
Description: Displays the driver interface. For administrator to return to the driver interface. <br>
Template: home.html <br>
Data Passed: None. <br>
Data Relationship: Direct rendering of the home.html template for drivers. <br>

/search_driver: <br>
Function: search_driver() <br>
Description: Allows users to search for drivers based on keywords and displays the results. <br>
Template: search_results.html <br>
Data Passed: Search results based on the keyword. <br>
Data Relationship: Users input a keyword, and the search_driver() function fetches relevant results from the database. These results are then displayed using the search_results.html template. <br>

/edit_runs: <br>
Function: edit_runs() <br>
Description: Allows users to edit the runs for specific drivers and courses. <br>
Template: edit_runs.html <br>
Data Passed: List of drivers, courses, and runs based on selected criteria. <br>
Data Relationship: Users select a driver and/or course, and the corresponding run details are fetched from the database. This data is then passed to the edit_runs.html template for display and editing. <br>

/edit_individual_run： <br>
Function: edit_individual_run() <br>
Description: Allows users to edit the details of an individual run.<br>
Template: edit_individual_run.html <br>
Data Passed: Details of the selected run, errors(if there are validation errors in the form) <br>
Data Relationship: Run details are fetched from the database based on the provided driver ID, course ID, and run number. If the users submit the form with updates, the data is validated and, if valid the run details are updated in the database. If there are validation errors, the errors list is passed to the edit_individual_run.html template along with the run details for display and editing. On successful update, the same data will then be passed to the edit_run route and the updated data will then display. <br>

/add_driver: <br>
Function: add_driver() <br>
Description: Allows the user to add a new driver. <br>
Template: add_driver.html <br>
Data Passed: List of available cars, caregivers, and potential error messages. <br>
Data Relationship: When the page is loaded, the add_driver() function fetches the list of available cars and caregivers from the database, which is then passed to the add_driver.html template to populate the respective dropdowns. When a form submission is detected (via POST request), the same add_driver() function is responsible for data validation and database insertion. If there are any validation errors, the function repopulates the form fields with the entered data and shows relevant error messages. <br>

**3. Assumptions and design decisions:** <br>
Assumption: 
- Drivers aged 17 and older should not have a designated caredriver.
- The age of the driver is limited to 10 to 100.
- The data for cones is either None or an integer.
- The data for wd is either 0 or 1.
- A car model can be associated with more than one car_num (Eg. MX-5).
- Driver's name is to be sorted in surname and last name order but displayed in a conventional way.

Design decision:
-  










