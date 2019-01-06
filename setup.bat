pip install pipenv
pipenv install
cd drf
pipenv run manage.py migrate
pipenv run manage.py runserver