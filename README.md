RESPO PROJECT STRUCTURE

RESPO
- home/backend (where all the analytics files are gonna be located and the connection with the database)
    
- home/frontend (where all the frontend files are located)

- Respo (Initialization folder with settings)


# Setup

## Requirments
to begin you require

* [python3](https://www.python.org/)
* [Django](https://www.djangoproject.com/) (it should also install django with npm install see Dependencies below)
* [npm/nodeJs](https://nodejs.org/en/)


## Dependencies

After the above tools are installed, pull the git repository. The tools can be used to install all further dependencies. 
Navigate to the project folder which is where manage.py is located, and run

```
npm install
```

You will also need to install some Python dependencies used by Django. To do so, run

```
pip install -r requirments.txt
```

## Setting up the database

The project uses a PostgresSQL database to store product information. First, install PostgresSQL from [here](https://www.postgresql.org/download/). Then, run the command 

```
psql -U postgres
```

If you entered a password during the Postgres install, you will be prompted for it here. If you are using Windows, it's possible the installer did not add the command to your system path and you will get an error stating that psql is not a vakid command. To fix this, add {POSTGRES_INSTALL_PATH}\\{POSTGRES_VERSION}\\bin\\ to your path. For example  "C:\\Program Files\\PostgresSQL\\10\\bin\\".

After the psql command, you will enter the Postgres console. Run the following commands to create a database and a user

On windows, replace sl_SI.utf8 with Slovenian_Slovenia.1250
```
CREATE DATABASE respo_admin WITH LC_COLLATE 'sl_SI.utf8' LC_CTYPE 'sl_SI.utf8' TEMPLATE template0;
CREATE USER respo_admin_user WITH PASSWORD 'admin';

ALTER ROLE respo_admin_user SET client_encoding TO 'utf8';
ALTER ROLE respo_admin_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE respo_admin_user SET timezone TO 'UTC';
ALTER USER respo_admin_user CREATEDB;

GRANT ALL PRIVILEGES ON DATABASE respo_admin TO respo_admin_user;
```

You might also need to run

```

\connect respo_admin
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO respo_admin_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO respo_admin_user;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO respo_admin_user;

```

And exit the Postgres console with 

```
\q
```

After that navigate to the project folder and type in the following commands:

```
python manage.py makemigrations --settings=Respo.settings

python manage.py migrate --settings=Respo.settings
```

The command makemigrations is used when there are changes to the tables of the database and migrate to push those changes onto the database in postgres

## Running the server

to run the server use the next line, the server should be located at 127.0.0.1:8000

```
npm run server
```

For more information check the files in frontend and backend



