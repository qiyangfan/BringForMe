Env:

```shell
conda create -n bring_for_me python==3.11.5
conda activate bring_for_me
conda install mysql-connector-c
pip install mysqlclient
pip install Django==4.2
pip install djangorestframework
pip install djangorestframework_simplejwt
pip install redis
pip install django-redis
pip install pillow
pip install drf-yasg
```

Mysql:

```mysql
create database bring_for_me;
```

Django migrate:

```shell
python manage.py migrate
```

Django runserver:

```shell
python manage.py runserver
```

settings.py:

change the database settings to your own settings.
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        "NAME": "bring_for_me",
        "USER": "your_username",
        "PASSWORD": "your_password",
        "HOST": "your_host",
        "PORT": "your_port",
    }
}
```
example:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        "NAME": "bring_for_me",
        "USER": "root",
        "PASSWORD": "",
        "HOST": "127.0.0.1",
        "PORT": "3306",
    }
}
```

Redis:
change the redis settings to your own settings.
```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "your_redis_location",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "password": "your_redis_password"
        }
    }
}
```
example:
```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "password": ""
        }
    }
}
```



