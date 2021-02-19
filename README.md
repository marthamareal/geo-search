# GeoSearch
GeoSearch is simple application Django 2.0+/Python 3, ReactJs, upon login, exposes a simple interface where the user can execute one or more search requests providing inputs x, y, n and an operation_type and 
the system returns the first n points closest to or farthest, depending on the selected operation, to the coordinates entered by the user.

## Setup

### Getting Started

These instructions below will get you a copy of the project up and running on your local machine for development and testing purposes.
### Prerequisites
- git
- python 3.7
- virtualenv
- Postgres
- Postgis
- Redis
- Node

### Installing
 Clone the repository and run the following commands to setup project.
 - backend
    ```
   $ git clone https://github.com/marthamareal/geo-search
   $ cd geo-search
   $ git checkout exercise
   $ virtualenv venv
   $ source venv/bin/activate
   $ pip install -r api/requirements.txt

   # create database
   $ psql postgres
   $ postgres =  # create database <your db name>;
   $ postgres =  # create extension postgis;
   $ postgres =  # create user <your user> with encrypted password '<your passwor>';
   $ postgres =  # grant all privileges on database developpp to myuser;

   # Create a .env file and add the following settings
        export SECRET_KEY='your secret'
        export DB_NAME='your db_name'
        export DB_USER='your user'
        export DB_PASSWORD='your password'
        export DB_HOST=localhost
        export DB_PORT=5432
        export DEBUG=True
   $ source .env

   # Populate db using a managment command
   $  python manage.py create_locations

   $  python manage.py migrate
   $  python manage.py runserver
    ```
- Frontend(GUI)
  - open a new terminal and start server for the GUI
  ```
    $ npm install
    $ npm start
  ```
### Running the tests
cd into the root directory and run:
```
$ python manage.py test"
# With coverage and coverage report
$ coverage run manage.py test && coverage report && coverage html
```
