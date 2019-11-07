sudo -u postgres createdb trailDb
sudo -u postgres psql -d trailDb -c "CREATE EXTENSION postgis;"
sudo -u postgres psql -d trailDb -c "CREATE EXTENSION pgrouting;"

sudo -u postgres psql -d trailDb -c "DROP TABLE IF EXISTS trails;"
sudo -u postgres psql -d trailDb -c "DROP TABLE IF EXISTS endpoints;"

sudo su postgres
shp2pgsql -d /home/meow/Classes/Databases/Polyglot/Data/Trail_Cleaned trails | psql -U postgres -d trailDb
shp2pgsql -d /home/meow/Classes/Databases/Polyglot/Data/Endpoints_Cleaned endpoints | psql -U postgres -d trailDb