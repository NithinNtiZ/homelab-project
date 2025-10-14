#!/bin/bash
apt-get update
apt-get install nginx -y
echo "Hi Fellow Human Beings" >/var/www/html/index.nginx-debian.html

