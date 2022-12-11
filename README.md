This is a simple example to use docker-compose with mysql and python.

steps to start the program:

docker-compose build  <br />

docker-compose up database

docker-compose run database mysql --host=database --user=codetest --password=swordfish codetest 

docker-compose run  database mysql --host=database --user=codetest --password=swordfish codetest <example_schema.sql

docker-compose run  database mysql --host=database --user=codetest --password=swordfish codetest <people_schema.sql

docker-compose run database mysql --host=database --user=codetest --password=swordfish codetest <places_schema.sql

docker-compose run example-python


