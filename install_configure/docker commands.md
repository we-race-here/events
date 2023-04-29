docker-compose -f production.yml up -d
docker-compose -f production.yml logs
docker-compose -f production.yml build
docker-compose -f production.yml run --rm web python manage.py migrate
