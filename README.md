# InnoLibSys
Innopolis University Library System.

# Installation

1. Install Python3: https://www.python.org/
2. Install Django: https://www.djangoproject.com/
3. Download sources, unpack them in a separate folder. 
4. Open your folder in a command prompt.
5. If you're using Windows:
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
If you're using Linux or MacOS:
```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

The local server will automatically run on :8000 port. To change this simply add :port to runserver command.
