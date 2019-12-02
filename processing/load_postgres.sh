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
shp2pgsql -d /root/Data/trails_split5 trails | psql -U postgres -d trailDb
shp2pgsql -d /root/Data/endpoints_split5 endpoints | psql -U postgres -d trailDb

# Set db password with --
psql trailDb
ALTER USER postgres PASSWORD 'meow';

pgsql2shp -f junctions_pgis -h localhost -u postgres -P <db_psswd> trailDb "SELECT junct_id, geom FROM junctions"
pgsql2shp -f trails_pgis -h localhost -u postgres -P <db_psswd> trailDb "SELECT * FROM trail_junct_rel"