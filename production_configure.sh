#!/bin/sh

printf "\nConfiguring server for Django application.\n"
printf "\nServer should not be stopped or turned off during automated configuring.\n"
printf "\nPlease be patient...\n\n"
home_dir=/home/ubuntu/
work_dir=${home_dir}app/ThelastProjectBackend/
app_dir=${work_dir}app/

app_gunicorn_dir=${work_dir}gunicorn_files/
app_gunicorn_socket_file=${app_gunicorn_dir}gunicorn.socket
app_gunicorn_service_file=${app_gunicorn_dir}gunicorn.service
app_nginx_dir=${work_dir}nginx/
app_nginx_conf_file=${app_nginx_dir}boka.conf
app_pg_conf_dir=${work_dir}pg_conf/
app_pg_conf_file=${app_pg_conf_dir}pg_hba.conf

nginx_conf_dir=/etc/nginx/conf.d/

nginx_boka_conf_dir=${nginx_conf_dir}boka.conf

source_list_dir=/etc/apt/sources.list.d/
systemd_system_dir=/etc/systemd/system/

gunicorn_system_socket_file=${systemd_system_dir}gunicorn.socket
gunicorn_system_service_file=${systemd_system_dir}gunicorn.service

pgdg_source_list_file=${source_list_dir}pgdg.list
nginx_source_list_file=${source_list_dir}nginx.list

pg_main_conf_dir=/etc/postgresql/11/main/

pg_hba_conf_file=${pg_main_conf_dir}pg_hba.conf

sudo apt update
sudo apt install python3-pip python3-dev libpq-dev curl -y

printf "\nInstalling PostgreSQL-11 Database Server...\n\n"
sudo rm $pgdg_source_list_file
sudo echo "deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main" >> $pgdg_source_list_file

wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt update

sudo apt install postgresql-11 postgresql-client-11 -y

printf "\nCreating database...\n\n"
sudo cp -f $app_pg_conf_file $pg_hba_conf_file

sudo service postgresql restart

sudo psql -U postgres -d postgres -a -f database.sql

printf "\nInstalling memcached...\n\n"
sudo apt install memcached libmemcached-tools -y
systemctl start memcached
systemctl enable memcached
systemctl restart memcached

printf "\nInstalling pipenv...\n\n"
sudo -H pip3 install --upgrade pip
sudo -H pip3 install pipenv

printf "\nMigrating database...\n\n"
cd $app_dir

pipenv install --skip-lock
pipenv run python manage.py makemigrations
pipenv run python manage.py migrate
pipenv run python manage.py collectstatic --noinput

printf "\nConfiguring Gunicorn as a system service for Django application...\n\n"
sudo cp -f $app_gunicorn_socket_file $gunicorn_system_socket_file

sudo cp -f $app_gunicorn_service_file $gunicorn_system_service_file

sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket

sudo systemctl daemon-reload
sudo systemctl restart gunicorn

printf "\nInstall Nginx as a Frontend server...\n\n"
sudo apt install curl gnupg2 ca-certificates lsb-release -y

sudo rm $nginx_source_list_file
echo "deb http://nginx.org/packages/ubuntu `lsb_release -cs` nginx" \
    | sudo tee $nginx_source_list_file

curl -fsSL https://nginx.org/keys/nginx_signing.key | sudo apt-key add -
sudo apt-key fingerprint ABF5BD827BD9BF62

sudo apt update
sudo apt install nginx -y

sudo cp -f $app_nginx_conf_file $nginx_boka_conf_dir

sudo nginx -t
sudo nginx -s reload

printf "\nConfiguring firewall for allowing HTTP...\n\n"
sudo ufw allow 80
