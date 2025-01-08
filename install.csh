deactivate
git reset --hard
sudo git clean -fxd
git pull
virtualenv .env
source .env/bin/activate
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
sudo .env/bin/python3 manage.py runserver 0.0.0.0:7000