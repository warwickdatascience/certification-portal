# Certification-Portal

Python Flask Web App to facilitate hosting and creating certificates for students who have passed courses run by WDSS. Utilises NGinx and Gunicorn to expose the app. 
- python (Flask)  
- mySQL

## Prerequisites
Make sure docker is installed on the host machine

## Setup
Various .env files will need to be set on your local installation for the app to access the database and for setting the admin accounts password. In database_scripts set SQL_ROOT_PASSWORD and ADMIN_PASSWORD. In backend/app set SQL_ROOT_PASSWORD. <br>
 
### Start App
Enter backend/ and run `docker-compose up`. This will spin up two docker containers. One mysql image and another alpine image to host the Flask app. Setup is as simple as that!

### Setup Database
`python3 database_scripts/init.py`

## Using the App
A script called 'create_student_certificate.py' has been made to interact with the API and easily add new certificates for students. The endpoints on the web app can be interacted with directly as well. It uses JWT to authenticate the user so only the admin will be able to perform CRUD operations. The /certificates/\<id\> endpoint is visible to everyone so people are able to link potential employers to their certificates for proof if necessary.

### Endpoints
- Authenticated
	- /token/auth
	- /token/refresh
	- /token/remove
	- /api/crud/\<table>
	- /api/crud/\<table>/\<iden>
	- /api/certificate/generate
	- /api/certificate/update	
- Not authenticated
	- /certificate/\<iden>

## TODO
-  Aggregate .env files
- Modularise code
- Increase fault-tolerance
- Add more CRUD endpoints



