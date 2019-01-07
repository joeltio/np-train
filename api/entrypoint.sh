./wait-for-it.sh db:5432
uwsgi --ini api_uwsgi.ini
