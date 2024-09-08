

call venv/scripts/activate

pip install django 
pip install psycopg2
python -m pip install -U channels["daphne"]
pip install imaplib2



django-admin startproject django_settings .
django-admin startapp django_app



python manage.py makemigrations
python manage.py migrate


python manage.py createsuperuser





python manage.py runserver

cmd