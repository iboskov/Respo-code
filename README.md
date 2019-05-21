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

After the above tools are installed, pull the git repository. The tools can be used to install all further dependencies. Navigate to the project folder, and run

```
npm install
```

You will also need to install some Python dependencies used by Django. To do so, run

```
pip install -r requirments.txt
```

to run the server use the next line, the server should be located at 127.0.0.1:8000

```
npm run server
```

For more information check the files in frontend and backend


