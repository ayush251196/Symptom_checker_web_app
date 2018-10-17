# Symptom_checker_web_app
### Symptom checker is a web app developed using Django framework and written in Python 3.7 .

The user selects a symptom displayed in a list view and is directed to the Symptom Detail page where he gets 
valuable information related to the selected symptom like **Suggested Issues** ; with **Description** , **Medical Condition** , **Related Symptoms** , **Treatment Descriptions** ( like **self care** , **medical procedures** , **medications** ) and **Related Specializations** , for each issue. 

**SQLite** database is used for storing the data fetched from the API so as to implement a caching system i.e if user selects the 
same symptom that he had previously selected then instead of requesting the API again , data is fetched directly from the database.
The app grabs the data related to the symptoms  using services provided by **ApiMedic** API.

In the home page user has to enter his name , year of birth and gender to proceed to the next page where all the fetched symptoms
are displayed. User can either search for the symtom in the search box provided above or can select the symptom by manually clicking
it . To this the user is sent to the next page where all necessary details related to symptoms are displayed.

**A permanent internet connectivity is required to run the app. 
HTML files in the project include cached version of Bootstrap’s compiled CSS and JS.***


