## Developing API endpoint assessment - Power to Fly. 


Link to Google Docs Full Documentation: https://docs.google.com/document/d/1ExPaoux0RJoaaLQwvciY0mQ2KldO9POVRmmbW9iuGP4/edit?usp=sharing


# Prepared By: Batool Alsulaibi
### Date: 10/17/2022

## Introduction:

This documentation will present the progress of creating a Flask web API, with the technical requirements explained in the assessment link. 
The steps toward creating this API started with designing the architecture applied, to the database models and relationships, in parallel with implementing the stack requirements and API supports. 


## Architecture
	The software application architecture that was used in this assessment is 3 tire architecture, which organizes applications into three logical and physical computing tiers: the presentation tier, or user interface; the application tier, where data is processed; and the data tier, where the data associated with the application is stored and managed. MVC architecture was applied as an implementation to the 3-layered architecture, it helps us to control the complexity of an application by dividing it into three components i.e. model, view, and controller. The model presents the database models used ( Users and Posts), the view presents the front components that interact with the user, and the controller (Routes) is the place that is responsible for the way that users interact with MVC model.



From the above figure, we can notice the structure of the files that starts from blueprints that include the control side, has the routes of each model. Models Folder that has the database tables (Users and Posts). Templates and forms that present the frontend side of the api where users interact to the web app. 
 

## Database models

The following ER diagram shows the relationship between User entity and Post entity, the user has the attributes (id, username, email, password) and the list of posts that the user has published, the Post has the attributes(id, title, content) and the id of the user as the foreign key that connects to the user that has published this article. 1- to -many relationships is created, users can post many articles, and articles are posted by one user, each has an id that connects to that user.
A relational database was created using SQLite, and SQLalchemy-flask extension that provides tools and methods to interact with databases in the Flask applications through SQLAlchemy.  





Part of the data samples in JSON format which has been entered into the database.
More than 15000 rows were entered






 
## Tech Stack requirements 

The framework used: Flask framework was used to build and develop the web app, it’s provided with a fast debugger, is lightweight, and can easily import packages for additional features, such as flask-sqlalchemy, flask-wtforms.
Docker: For collecting the project as one complete unit that has its packages and can be used in other operating systems, Docker was used, it helped create images for the various versions of the project.
Each image is built according to the Dockerfile in the project, which collects and builds the project packages presented in the requirements file, 
The image which presents the unit of the software that has packages and project dependencies was pushed, it is is a container that has been saved and packaged so no need to worry about running the project when using it on other operating systems. 
Note: Pushing containers to the Docker hub will be explained later in this documentation. 






 
## Requirement to API : Pagination support:
For the API to be user-friendly and easy to use, pagination and filtration are the main support concepts in this case, Pagination is the process of splitting the contents of a website, or a section of contents from a website, into discrete pages. Results are paginated using the paginate function of Flask SQLAlchemy with any number of arguments as desired. The result of calling the paginate() function is a Pagination Object, which has many methods that can help achieve the desired result.
 




 
 
 
 
## Requirement to API :Filtration support: 

Filter support makes it easier for users to search for posts and categorize the search results according to the date of publishing the articles. 
The features added to the web app include:
Filter articles on categories: Users can filter articles according to categories (Technology Topics, Tips, Social media and youtube topics)
Filter articles on Dates: users can filter articles according to dates of publishing these articles 


The following figure shows the search field and filter categories in the web api. 

 
 
Search Feature - in the old version; This feature was implemented so users can do a search on the titles of the articles by typing the words in the search place, the result is even the articles with that title or an empty page if no results were found. 
 
Filter on user names: Users can also access articles of each other users by clicking on their names on the home page as shown in the figure below.
Users articles: Users access their own published articles from the account page

 
## Cache-Control 
Website caching speeds up this process for a user’s future visits by saving a copy of the web page’s content and storing it in a temporary location.
As a result, when this user visits again, the content is already available— and can be fetched from the temporary location without making a new request
Types of website caching: 
Server-side caching:
Server-side caching is the temporary storing of web files and data on the origin server for reuse.

Client-side caching:
Client-side caching, or browser caching, is a web-caching process that temporarily stores the copy of a web page in the browser memory instead of the cache memory in the server. This browser memory is located on the user’s device. So, when a user visits a website enabled with client-side caching, the browser keeps a copy of the webpage. 



In this project, client-side cache was implemented, especially the type of Browser Request Caching
Cache-Control is an HTTP cache header that contains a set of parameters to define the browser’s caching policies in the client requests and server responses.
For this implementation, the following steps were done: 
A decorator method docache was added  in utils.py file. 
The decorator adds the cache headers to the Flask response. The method takes two parameters:
**minutes:**To define the age and expiry of the cache
**content_type:**To define the content type of the response.


 
The result of caching the header response can be shown below, by clicking on the post name, and checking the Response Header- Cache - Control, it says that max-age=300 which means that the caching is up for 300 seconds so the user have access to this page for this amount. 
There are a lot more implementations of caching where it saved files, images, and data, but this is a simple implementation  




## Testing:  Unit testing: 
Testing helps catch bugs in the code, it also helps to debug faster since it has a lot of small tests covering all parts of the code. 
In this project, some simple tests were done to make sure that the pages route correctly without any bugs, as shown below:






test_home_aliases function to make sure that the route request “/” and “/home” returns the same page ( home page )

testing_About method is to test that the route “/about” returns the about page and that the status code of the response is 200 which means that everything works perfectly. 









## Final Steps: 
### Deploying the flask api using Docker and to Heroku servers. 
Part 1: Creating and Building the Docker image
	The process deploying the api on docker is shown below:
Docker was installed on the local device
An account was created on the docker hub and local docker after it was installed 
Then using the command pip freeze > requirements.txt  within the root directory, the requirements file was created to generate the names of the packages and their respective versions that we have installed, as well as some other inbuilt dependencies that run the Flask application. Then, it stores them in a .txt file named requirements.


The Docker file created  Dockerfile. The following code snippet was added to the file to the file:



RUN mkdir/code: We proceed to create a working directory 
WORKDIR /code: We proceed to set the working directory as /code, which will be the root directory of our application in the container
RUN pip install -r requirements.txt: This command installs all the dependencies defined in the requirements.txt file into our application within the container
COPY . /code: This copies every other file and its respective contents into the app folder which is the root directory of our application within the container
ENTRYPOINT [ "python" ]: This is the command that runs the application in the container
CMD python.run: Finally, this performs the command that runs the application. This is similar to how we would run the Python app on our terminal using the python run.py command
Building the Docker image
To build the image, the command below was used: docker image build -t image-name.


After successfully building the image, the next step is to run an instance of the image. Running the container
docker run -p 5000:5000 -d image-name
 
The next step is to log in on the local machine to create a connection between our machine and Docker Hub.
Log in on your local machine: docker login
Docker Hub is a community of repositories where Docker users create, test, and manage containers.
 A repository was created on docker hub  so we can push docker images on
 

 








### Part 2: Deployment to Heroku: 

Step 1: Loggin  in to Heroku using the command: heroku login
Step 2: Creating Heroku app heroku create <app-name
Step 3: Creating a Procfile A Procfile contains commands that your application runs on Heroku when starting up.
Create a file and name it Procfile without an extension. Then add the following to the file:
web: gunicorn app:app

Step 4: Tagging the repository on docker to the heroku app 

 docker tag <username on docker account>/<docker repository name> registry.heroku.com/<app-name>


  ### Pushing the app to Heroku
 docker push registry.heroku.com/<app-name>
Step 5: Releasing the image
heroku container:release web --app <app-name>







# The Final Web API:


























## References: 

https://flask.palletsprojects.com/en/1.1.x/
https://www.sqlalchemy.org/
https://docs.docker.com/compose/gettingstarted/
https://git-scm.com/doc
https://www.postgresql.org/docs/13/index.html
https://www.sqlite.org/docs.html
https://stackabuse.com/deploying-a-flask-application-to-heroku/
https://edgemesh.com/blog/difference-between-server-side-caching-and-client-side-caching-and-which-is-good-for-your-website
https://www.maskaravivek.com/post/how-to-add-http-cachecontrol-headers-in-flask/
https://flask-caching.readthedocs.io/en/latest/
https://codethechange.stanford.edu/guides/guide_flask_unit_testing.html
https://flask.palletsprojects.com/en/2.2.x/testing/
https://codethechange.stanford.edu/guides/guide_flask_unit_testing.html
https://rimsovankiry.medium.com/sqlalchemy-query-with-common-filters-c7adbd3321a6




















