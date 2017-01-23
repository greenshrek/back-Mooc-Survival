# Back-Mooc-Survival

## Install
For Mac users (optional).
``` shell
python3 -m venv venv
pip install -r requirements.txt
```
After python 3 was installed.
``` shell
python3 -m venv venv
pip install -r requirements.txt
```

## Set the environment variables
Example for development environment
``` shell
export APP_SETTINGS="config.DevelopmentConfig"
export DATABASE_URL="sqlite:///database.db"
```

## Initiate the database
``` shell
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

## Run the server
``` shell
python manage.py runserver
```