apt-get -qqy update
DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" upgrade
apt-get -qqy install postgresql python-psycopg2
apt-get -qqy install python-sqlalchemy
apt-get -qqy install python-pip
pip3 install --upgrade pip
pip3 install werkzeug==0.8.3
pip3 install flask==0.9
pip3 install Flask-Login==0.1.3
pip3 install oauth2client
pip3 install requests
pip3 install httplib2