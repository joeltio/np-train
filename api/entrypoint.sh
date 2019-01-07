./wait-for-it.sh db:5432
python manage.py makemigrations
python manage.py migrate
uwsgi --ini api_uwsgi.ini
