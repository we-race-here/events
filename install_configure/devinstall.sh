cd ~/events
git fetch
git checkout dev-server
git pull
docker-compose -f development.yml build
docker-compose -f development.yml run django python manage.py migrate
docker-compose -f development.yml up -d
