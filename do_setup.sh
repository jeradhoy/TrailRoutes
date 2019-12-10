sudo apt update
sudo apt upgrade

sudo apt install postgresql postgresql-contrib

sudo apt install postgis #postgresql-11-postgis-2.5 -- only need for my installation

sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools

pip3 install Flask

pip3 install flask_restful

sudo apt install libpq-dev
pip3 install psycopg2

sudo ufw allow 80

npm install mapbox-gl-controls

# Redis
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make

sudo cp src/redis-server /usr/local/bin/
sudo cp src/redis-cli /usr/local/bin/

pip3 install redis

# Set "bind 127.0.0.1 ::1" in redis config file for some security.


