#https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04
#For new installs, run this script to install and configure the server.
#App will run on port 9018


mkdir /opt/webapps/
cd /opt/webapps/
git clone https://github.com/we-race-here/events.git -b main
cd events
mkdir .envs/.production/
cd .envs/.production/
# Need to put the .django and .postgress files here



