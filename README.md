# fit-comp

The backend for serving basic functionalities of fitness competition app data.

## Development

```
cd fit-comp
source env/bin/activate
```

This activates the virtual environment and dependencies can now be installed local to the repository.

```
pip install -r requirements.txt
```

Ensure that path to the local PostgreSQL database inside of .env is correct. The database should be structured as outlined in [wiki](https://github.com/dordep19/fit-comp-backend/wiki/Database). The database can now be migrated.

```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

To run the backend server in development mode on localhost port 5000:

```
python manage.py runserver
```
