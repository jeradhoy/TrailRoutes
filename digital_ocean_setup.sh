sudo apt update
sudo apt upgrade

# Install database packages
sudo apt install postgresql postgresql-contrib
sudo apt install postgis 

# Install python3 packages for flask
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools

# Install flask stuff..
pip3 install Flask flask_restful psycopg2

sudo apt install libpq-dev

# Open port 80 to allow regular HTTP connections
sudo ufw allow 80

# download nd setup redist
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make

sudo cp src/redis-server /usr/local/bin/
sudo cp src/redis-cli /usr/local/bin/

pip3 install redis

# Set "bind 127.0.0.1 ::1" in redis config file for some security.


