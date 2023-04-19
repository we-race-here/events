For new installs, run this script to install and configure the server.
App will run on port 9018
apt install docker -y
apt install docker-compose -y
mkdir /opt/webapps/
cd /opt/webapps/
git clone https://github.com/we-race-here/events.git -b main
cd events
mkdir .envs/.production/
cd .envs/.production/
# Need to put the .django and .postgress files here
docker-compose -f production.yml run --rm django python manage.py migrate

