
# API Documentation For Capstone Casting Agency

## About
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. 
The application aims at streamlining and simplifying the process of CRUD operations for actors and movies.


## Getting Started

### Installing Dependencies 

### Python 3.7
Install the latest version of python for your platform.

#### PIP Dependencies

Run the below to install all the necessary dependencies:

```bash
pip install -r requirements.txt
```

This will install all the required packages.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Running the server

To run the server, execute:
```
 export FLASK_APP=app.py
 export FLASK_ENV=development
 python3 -m flask run
 ```
We can now also open the application via Heroku using the URL:
https://bhagyash-capstone-agency.herokuapp.com/

The live application can only be used to generate tokens via Auth0.
The endpoints can then be tested using curl or Postman along with the generated JWTs.

## DATA MODELING:
#### models.py
The schema for the database and helper methods to simplify API behavior are in models.py.

Does not use raw SQL or only where there are not SQLAlchemy equivalent expressions.
Correctly formats SQLAlchemy to define models
Creates methods to serialize model data and helper methods to simplify API behavior such as insert, update and delete.
####Models:
-Movies with attributes title and release date
-Actors with attributes name, age and gender

## API ARCHITECTURE AND TESTING
### Endpoint Library

RESTful principles are followed throughout the project, including appropriate naming of endpoints, use of HTTP methods GET, POST, and DELETE.

Routes perform CRUD operations.

The @app.errorhandler decorator has been utilized to format error responses as JSON objects fordifferent status codes
 A custom @requires_auth decorator has been included to enable Role Based Authentication and roles-based access control (RBAC) in the application.
 
The JWT token needs to be passed for RBAC for every endpoint.

JWT tokens have been provided in setup.sh.
In case of token expiration,it can be generated using the below steps:
1. Go to http://capstone-admin.us.auth0.com/authorize?response_type=token&client_id=QvsqXaFdw95ybQhMNelS25IaGP3OAmd5&redirect_uri=http://127.0.0.1:8100

2. Click on Login button and enter the below mail ids and passwords as per the requirement:
Assistant
	Email: asst@gmail.com
	Password: Capstone11@
Director
	Email: director@gmail.com
	Password: Capstone11@
Producer
	Email: producer@gmail.com
	Password: Capstone11@



#### GET '/actors'
Returns a list of all available actors and return status code.
#### GET '/movies'
Returns a list of all available movies and return status code.
#### POST '/actors'
Can be used to add new actor details.
#### POST '/movies'
Can be used to add new movie details.
#### PATCH '/actors/update/{actor_id}'
Used to update actor details by id.
#### PATCH '/movies/update/{moive_id}'
Used to update movie details by id.
#### DELETE '/actors/delete/{actor_id}'
Delete actor details by id from the database
#### DELETE '/movies/delete/{movie_id}'
Delete movie details by id from the database

## Testing
There are 20 unittests in test_app.py. To run this file use:
```
python test_app.py
```
The tests include one test for expected success and error behavior for each endpoint, and tests demonstrating role-based access control, 
where all endpoints are tested with and without the correct authorization.
