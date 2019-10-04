#!/bin/sh

sudo apt update
sudo apt install python3-pip python3-dev libpq-dev curl

sudo touch /etc/apt/sources.list.d/pgdg.list
sudo echo "deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main" >> /etc/apt/sources.list.d/pgdg.list

wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt update

sudo apt install postgresql-11 postgresql-client-11

psql -U postgres postgres database.sql

sudo -H pip3 install --upgrade pip
sudo -H pip3 install pipenv

cd /home/ubuntu/app/ThelastProjectBackend/app

pipenv install --skip-lock
pipenv run python manage.py makemigrations
pipenv run python manage.py migrate
pipenv run python manage.py collectstatic

sudo touch /etc/systemd/system/gunicorn.socket

sudo cat >> /etc/systemd/system/gunicorn.socket <<EOL
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
EOL

sudo touch /etc/systemd/system/gunicorn.service

sudo cat >> <<EOL
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/app/ThelastProjectBackend/app
ExecStart=/usr/local/bin/pipenv run gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          project.wsgi:application

[Install]
WantedBy=multi-user.target
EOL

sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket

sudo systemctl daemon-reload
sudo systemctl restart gunicorn

# installing Nginx Frontend Server
sudo apt install curl gnupg2 ca-certificates lsb-release

echo "deb http://nginx.org/packages/ubuntu `lsb_release -cs` nginx" \
    | sudo tee /etc/apt/sources.list.d/nginx.list

curl -fsSL https://nginx.org/keys/nginx_signing.key | sudo apt-key add -
sudo apt-key fingerprint ABF5BD827BD9BF62

sudo apt update
sudo apt install nginx

sudo nano touch /etc/nginx/conf.d/boka.conf

sudo cat >> /etc/nginx/conf.d/boka.conf <<EOL
server {
    listen 80;
    server_name 157.245.106.188;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /statics/ {
        root /home/ubuntu/app/ThelastProjectBackend/app;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
EOL

sudo nginx -t
sudo nginx -s reload

sudo ufw allow 80
