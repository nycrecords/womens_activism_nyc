#!/usr/bin/env bash

# 1. Install Java
yum -y install java-1.8.0-openjdk

wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.2.0.rpm -P /tmp

# 2. Install ElasticSearch
rpm -ivh /tmp/elasticsearch-5.2.0.rpm

# 3. Configure ElasticSearch
mv /etc/elasticsearch/elasticsearch.yml /etc/elasticsearch/elasticsearch.yml.orig
ln -s /vagrant/build_scripts/es_setup/elasticsearch.yml /etc/elasticsearch/elasticsearch.yml

yum -y install rh-nginx18-nginx

bash -c "printf '#\!/bin/bash\nsource /opt/rh/rh-nginx18/enable'"

mv /etc/opt/rh/rh-nginx18/nginx/nginx.conf /etc/opt/rh/rh-nginx18/nginx/nginx.conf.orig

ln -s /vagrant/build_scripts/es_setup/nginx_conf/nginx.conf /etc/opt/rh/rh-nginx18/nginx/nginx.conf

openssl req \
       -newkey rsa:4096 -nodes -keyout /vagrant/build_scripts/es_setup/elasticsearch_dev.key \
       -x509 -days 365 -out /vagrant/build_scripts/es_setup/elasticsearch_dev.crt -subj "/C=US/ST=New York/L=New York/O=NYC Department of Records and Information Services/OU=IT/CN=womensactivism.nyc"
openssl x509 -in /vagrant/build_scripts/es_setup/elasticsearch_dev.crt -out /vagrant/build_scripts/es_setup/elasticsearch_dev.pem -outform PEM

mkdir -p /data/es_logs
chown -R vagrant:vagrant /data
chmod 777 -R /data

sudo service rh-nginx18-nginx restart

# 4. Start Elasticsearch
sudo /etc/init.d/elasticsearch start

# 5. Add the following lines to /etc/sudoers file
#womens_activism   ALL=(elasticsearch:elasticsearch) NOPASSWD:ALL
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/elasticsearch start
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/elasticsearch stop
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/elasticsearch status
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/elasticsearch restart
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/elasticsearch condrestart
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/elasticsearch try-restart
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/elasticsearch reload
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/elasticsearch force-reload
