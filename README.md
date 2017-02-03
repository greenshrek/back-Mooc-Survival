# Back-Mooc-Survival

## Install
For Mac users (optional).
``` shell
brew install python3
```

After python 3 was installed.
``` shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Set the environment variables
Example for development environment
``` shell
export APP_SETTINGS="config.DevelopmentConfig"
export DATABASE_URL="sqlite:///moocsurvivor.db"
```

## Run the server
``` shell
python manage.py runserver
```
