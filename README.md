# WebDev636
**Name**: Ryan Tay Peng Yeow <br>
**Student ID**: 1157892

**Web Application Structure:** <br>
**1. Structure Overview:**

My web application follows the typical structure of Flask projects. The application is organized with a combination of routes and their associated functions, and templates to render the appropriate views. This structure aids in maintaining a clean separation of concerns between data processing and presentation.

**2. Routes & Functions:**

/:
Function: home()
Description: Serves the homepage.
Template: home.html
Data Passed: None.
Data Relationship: The root or index route uses the home.html template to serve as a home page with introductory information. Can add more information in the future related to the current user and recent news or events. 

/listcourses:
Function: listcourses()
Description: Displays the list of available courses.
Template: course_list.html
Data Passed: List of courses with their details.
Data Relationship: The /course_list route fetches a list of available courses from the database in the course_list() function and provides this list to the course_list.html template to display. The templates allow for clickable images.

/select_driver:
Function: select_driver()
Description: Displays a selection list of drivers.
Template: driver_selection.html
Data Passed: List of drivers with their details.
Data Relationship: The /select_driver route fetches a list of drivers from the database in the select_driver() function and provides this list to the driver_selection.html template to display.

/driver_run_details, methods=["GET"]/: and /driver_run_details, methods=["POST"]:
Function: driver_run_details
Description: Displays details of a specific driver and their runs.
Template: driver_run_details.html
Data Passed: Driver details and their corresponding run details.
Data Relationship: Depending on the method, either it fetches the driver ID from the listdriver URL or from the POST request via a form submission. Using this ID, it fetches the driver's and their run details from the database. This data is then passed to the driver_run_details.html template for display.

/listdrivers:
Function: listdrivers()
Description: Displays a list of all drivers.
Template: driverlist.html
Data Passed: List of drivers with their details.
Data Relationship: The /listdrivers route fetches a list of drivers from the database in the listdrivers() function and provides this list to the driverlist.html template to display.

/overallresults:
Function: overallresults()
Description: Displays overall results for each driver across different courses.
Template: overallresults.html
Data Passed: Aggregated results of drivers across courses.
Data Relationship: The /overallresults route fetches aggregated results of drivers across different courses and then provides this data to the overallresults.html template to display.

/graph:
Function: showgraph()
Description: Displays a graph showing top 5 drivers based on their overall results.
Template: top5graph.html
Data Passed: List of top 5 drivers and their results.
Data Relationship: The /graph route fetches the top 5 driver's results and provides this data to the top5graph.html template to display as a graph.

/admin:
Function: adminInterface()
Description: Displays the admin interface.
Template: adminHome.html
Data Passed: None.
Data Relationship: Direct rendering of the adminHome.html template.

/admin/junior-drivers:
Function: junior_driver_list()
Description: Displays a list of junior drivers.
Template: junior_driver_list.html
Data Passed: List of junior drivers and their details.
Data Relationship: The /admin/junior-drivers route fetches a list of junior drivers from the database and provides this list to the junior_driver_list.html template to display.

/search_driver:
Function: search_driver()
Description: Allows users to search for drivers based on keywords and displays the results.
Template: search_results.html
Data Passed: Search results based on the keyword.
Data Relationship: Users input a keyword, and the search_driver() function fetches relevant results from the database. These results are then displayed using the search_results.html template.

/driverInterface:
Function: driverInterface()
Description: Displays the driver interface. For administrator to return to the driver interface.
Template: home.html
Data Passed: None.
Data Relationship: Direct rendering of the home.html template for drivers.

/edit_runs:
Function: edit_runs()
Description: Allows users to edit the runs for specific drivers and courses.
Template: edit_runs.html
Data Passed: List of drivers, courses, and runs based on selected criteria.
Data Relationship: Users select a driver and/or course, and the corresponding run details are fetched from the database. This data is then passed to the edit_runs.html template for display and editing.


/add_driver:
Function: add_driver()
Description: Allows the user to add a new driver.
Template: add_driver.html
Data Passed: List of available cars, caregivers, and potential error messages.
Data Relationship: When the page is loaded, the add_driver() function fetches the list of available cars and caregivers from the database, which is then passed to the add_driver.html template to populate the respective dropdowns. When a form submission is detected (via POST request), the same add_driver() function is responsible for data validation and database insertion. If there are any validation errors, the function repopulates the form fields with the entered data and shows relevant error messages.









