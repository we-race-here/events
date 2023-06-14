# To migrate data from the old server to the new.

There is a migration commands for each app that is being migrated.

- python manage.py migrate_account_user_to_user
- python manage.py migrate_cycling_orgs
- python manage.py migrate_cycling_events

Run the # commands in docker like this.
docker-compose -f development.yml run --rm django python manage.py migrate_cycling_events

Production:
docker-compose -f production.yml build
docker-compose -f production.yml up -d
docker-compose -f production.yml run --rm django python manage.py migrate
docker-compose -f production.yml run --rm django python manage.py migrate_account_user_to_user
docker-compose -f production.yml run --rm django python manage.py migrate_account_user_to_user
docker-compose -f production.yml run --rm django python manage.py migrate_cycling_orgs
docker-compose -f production.yml run --rm django python manage.py migrate_cycling_events
