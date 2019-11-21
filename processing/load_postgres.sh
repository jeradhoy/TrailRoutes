# Install postgres:
# sudo apt install postgresql postgresql-contrib
# Install postgis
# sudo apt install postgis postgresql-11-postgis-2.5
sudo -u postgres createdb trailDb
sudo -u postgres psql -d trailDb -c "CREATE EXTENSION postgis;"
#sudo -u postgres psql -d trailDb -c "CREATE EXTENSION pgrouting;"

sudo -u postgres psql -d trailDb -c "DROP TABLE IF EXISTS trails;"
sudo -u postgres psql -d trailDb -c "DROP TABLE IF EXISTS endpoints;"

sudo su postgres
# Path needs to be basically to the name of the shapefile, not the folder it is in
shp2pgsql -d /home/dad/Classes/Databases/Trail_Routes/Data/trail_processed trails | psql -U postgres -d trailDb
shp2pgsql -d /home/dad/Classes/Databases/Trail_Routes/Data/junctions_processed endpoints | psql -U postgres -d trailDb