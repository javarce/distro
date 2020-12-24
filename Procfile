web: gunicorn distro.wsgi
heroku ps:scale web=1
release: python manage.py migrate