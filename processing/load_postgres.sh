# Install postgres:
# sudo apt install postgresql postgresql-contrib
# Install postgis
# sudo apt install postgis postgresql-11-postgis-2.5
sudo -u postgres dropdb trailDb
sudo -u postgres createdb trailDb
sudo -u postgres psql -d trailDb -c "CREATE EXTENSION postgis;"
#sudo -u postgres psql -d trailDb -c "CREATE EXTENSION pgrouting;"

sudo -u postgres psql -d trailDb -c "DROP TABLE IF EXISTS trails;"
sudo -u postgres psql -d trailDb -c "DROP TABLE IF EXISTS endpoints;"

sudo su postgres
# Path needs to be basically to the name of the shapefile, not the folder it is in
shp2pgsql -d /home/dad/Classes/Databases/Trail_Routes/trails_merged_simp_4326_2 trails | psql -U postgres -d trailDb
shp2pgsql -d /home/dad/Classes/Databases/Trail_Routes/juncts_merged_4326_2 endpoints | psql -U postgres -d trailDb

psql trailDb

#### NOW go and do sql processing

# Set db password with -- ALTER USER postgres PASSWORD 'MyNewPassword';

pgsql2shp -f "junctions_pgis" -h localhost -u postgres -P meow trailDb "SELECT * FROM junctions"
pgsql2shp -f "trails_pgis" -h localhost -u postgres -P meow trailDb "SELECT * FROM trail_junct_rel"