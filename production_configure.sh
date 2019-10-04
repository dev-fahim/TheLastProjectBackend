#!/bin/sh

sudo apt update
sudo apt install python3-pip python3-dev libpq-dev curl -y

sudo rm /etc/apt/sources.list.d/pgdg.list
sudo touch /etc/apt/sources.list.d/pgdg.list
sudo echo "deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main" >> /etc/apt/sources.list.d/pgdg.list

wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt update

sudo apt install postgresql-11 postgresql-client-11 -y

sudo psql -U postgres -d postgres -a -f database.sql

sudo -H pip3 install --upgrade pip
sudo -H pip3 install pipenv

cd /home/ubuntu/app/ThelastProjectBackend/app

pipenv install --skip-lock
pipenv run python manage.py makemigrations
pipenv run python manage.py migrate
pipenv run python manage.py collectstatic

sudo rm /etc/systemd/system/gunicorn.socket

sudo touch /etc/systemd/system/gunicorn.socket

sudo cat >> /etc/systemd/system/gunicorn.socket <<EOL
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
EOL

sudo rm /etc/systemd/system/gunicorn.service

sudo touch /etc/systemd/system/gunicorn.service

sudo cat >> /etc/systemd/system/gunicorn.service <<EOL
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
sudo systemctl daemon-reload
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket

sudo systemctl daemon-reload
sudo systemctl restart gunicorn
systemctl daemon-reload

# installing Nginx Frontend Server
sudo apt install curl gnupg2 ca-certificates lsb-release -y

sudo rm /etc/apt/sources.list.d/nginx.list
echo "deb http://nginx.org/packages/ubuntu `lsb_release -cs` nginx" \
    | sudo tee /etc/apt/sources.list.d/nginx.list

curl -fsSL https://nginx.org/keys/nginx_signing.key | sudo apt-key add -
sudo apt-key fingerprint ABF5BD827BD9BF62

sudo apt update
sudo apt install nginx -y

sudo rm /etc/nginx/conf.d/boka.conf

sudo touch /etc/nginx/conf.d/boka.conf
host = '$host'
remote_addr = '$remote_addr'
proxy_add_x_forwarded_for = '$proxy_add_x_forwarded_for'
scheme = '$scheme'
sudo cat >> /etc/nginx/conf.d/boka.conf <<EOL
server {
    listen 80;
    server_name 157.245.106.188;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /assets/ {
        root /home/ubuntu/app/ThelastProjectBackend/app/statics;
    }

    location / {
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
EOL

sudo nginx -t
sudo nginx -s reload

sudo ufw allow 80
