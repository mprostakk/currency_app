# Currency app

## Install
```pip install -r requirements.txt```

## Run app locally
Run app
 
 ```python manage.py runserver```

Migrate database

```python manage.py makemigrations```

```python manage.py migrate```

Create an admin user
 
 ```python manage.py createsuperuser```

## Run app in Docker
To run in development 

```docker-compose up backend```

To run tests

```docker-compose up tests```

For rebuilding add ```--build```

## Main Dependencies
- Python 3.7.0
- Django version 3.1.6
 