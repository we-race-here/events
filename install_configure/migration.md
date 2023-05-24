# To migrate data from the old server to the new.

There is a migration command for each app that is beinf migrated.

- python manage.py migrate_account_user_to_user
- python manage.py migrate_cycling_orgs
- python manage.py migrate_cycling_events

Run the commmands in docker like this.
docker-compose -f development.yml run --rm django python manage.py migrate_cycling_events
