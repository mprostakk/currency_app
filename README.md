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

Migrate database

```docker-compose exec backend python manage.py migrate```

```docker-compose exec backend python manage.py makemigrations```

## Main Dependencies
- Python 3.7.0
- Django version 3.1.6
 
## API

### POST /api/register
```
{
	"email": "maciej@gmail.com",
	"password": "password123"
}
```

### POST /api/token/
```
{
	"username": "maciej@gmail.com",
	"password": "password123"
}
```


### GET /api/subscription
Authorization: Bearer [token]

Response
```
[
    {
        "currency_name": "PLN"
    },
    {
        "currency_name": "GBP"
    }
]
```

### POST /api/subscription
Authorization: Bearer [token]

```
{
	"currency_name": "GBP"
}
```


### DELETE /api/subscription/PLN
Authorization: Bearer [token]

### GET /api/rates
Authorization: Bearer [token]

Params:
- base_currency
- date

Example: ```/api/rates?base_currency=PLN&date=2021-01-01```

Response
```
{
    "base_currency": "USD",
    "date": "2021-02-06",
    "rates": [
        {
            "currency_name": "PLN",
            "rate": 3.7572394225
        },
        {
            "currency_name": "GBP",
            "rate": 0.7305182342
        }
    ]
}
```