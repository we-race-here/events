#For new installs, run this script to install and configure the server.
#App will run on port 9018
apt update
apt install apt-transport-https ca-certificates curl software-properties-common -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
apt update
apt-cache policy docker-ce
apt install docker-ce

mkdir /opt/webapps/
cd /opt/webapps/
git clone https://github.com/we-race-here/events.git -b main
cd events
mkdir .envs/.production/
cd .envs/.production/
# Need to put the .django and .postgress files here
docker-compose -f production.yml run --rm django python manage.py migrate

