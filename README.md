# Smart Hub API

## Prerequisite
- Python <= 3.10
- MySQL

## How to run on a local machine
- Run the virtual environment [steps](#create-and-activate-virtual-environment)
- Run `pip intall -r requirments.txt` to install the required packages within your activated environment
- Copy env.example to .env file on a bash terminal `cp env.example .env`
- Run `python -c 'import secrets; print(secrets.token_urlsafe(16))'` in the terminal to generate secret key and replace with __SECRET_KEY__ value in the .env
- Run MySQL Setup [steps](#setup-mysql-database)
- Edit the .env variable where __DATABASE_USERNAME__ should be your database username and __DATABASE_PASSWORD__ should be your database user password and replace the __DATABASE_NAME__ with the database you created
- Request for the cloudinary keys from the admin to be shared with you
- Run the flask migration [steps](#migration)
- Run the app from the terminal `python run.py`
- The application runs on `localhost:5000`. You can access the API documentation at `http://localhost:5000/docs`.

## Create and activate virtual environment 
### ### Windows
- run `python -m venv venv` in the terminal to generate virtual environment
- (Bash Terminal) activate the virtual environment `source venv/Scripts/activate`
- (Command Prompt) activate the virtual environment `.\venv\Scripts\activate`

### Linux
- run `python -m venv venv` in the terminal to generate virtual environment
- (Bash Terminal) activate the virtual environment `source venv/bin/activate`

## Migration
- After creating the database `desired_database_name` as instructed above
- modify the __DATABASE_USERNAME__ and __DATABASE_PASSWORD__ to match your database user and user's password
- run the command to migrate table to existing database
```
flask db upgrade
```

## Setup MySQL database
```
CREATE USER 'username'@'localhost' IDENTIFIED BY 'password';
CREATE DATABASE desired_database_name;
GRANT ALL PRIVILEGES ON desired_database_name.* TO 'username'@'localhost';
```

## Countries & City SQL
- Country/States [source](https://github.com/dr5hn/countries-states-cities-database)
- import the countries sql to database `mysql -u [DB_USER] -p [DB_NAME] < SQL/countries.sql`
- import the states sql to database `mysql -u [DB_USER] -p [DB_NAME] < SQL/states.sql`