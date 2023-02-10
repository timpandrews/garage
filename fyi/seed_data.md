1. python manage.py dumpdata > seed_data.json
2. start psql: sudo -u postgres psql
3. \l to list database
4. Stop server & close pgadmin so no one is using the db and it can be dropped
5. DROP DATABASE garage;
6. Create empty db:  CREATE DATABASE garage;
7. Exit psql: \q
8. python manage.py migrate
9. python manage.py loaddata seed_data.json