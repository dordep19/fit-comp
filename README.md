# fit-comp-backend

The backend for serving basic functionalities of fitness competition app data.

## Development

```
cd fit-comp-backend
source env/bin/activate
```

This activates the virtual env and dependencies can now be installed local to the repository.

```
pip install -r requirements.txt
```

Now we can migrate the database.

```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

To run the backend server in development mode on localhost port 5000:

```
python manage.py runserver
```
