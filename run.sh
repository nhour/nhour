sleep 10
python manage.py collectstatic --noinput --clear
python manage.py migrate --noinput

gunicorn --access-logfile logs.log -w 9 --bind 0.0.0.0:8004 --env CARAVEL_URL="http://146.211.49.12:8088/caravel/dashboard/main/" nhour_base.wsgi
