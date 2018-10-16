# Symptom_checker_web_app
### Symptom checker is a web app developed using Django framework and written in Python 3.7 .

The user selects a symptom displayed in a list view and is directed to the Symptom Detail page where he gets 
valuable information related to the selected symptom like **Suggested Issues** ; with **Description** , **Medical Condition** , **Related Symptoms** , **Treatment Descriptions** ( like **self care** , **medical procedures** , **medications** ) and **Related Specializations** , for each issue. 

**SQLite** database is used for storing the data fetched from the API so as to implement a caching system i.e if user selects the 
same symptom that he had previously selected then instead of requesting the API again , data is fetched directly from the database.
The app grabs the data related to the symptoms  using services provided by **ApiMedic** API.

**A permanent internet connectivity is required to run the app. 
HTML files in the project include cached version of Bootstrap’s compiled CSS and JS.***


