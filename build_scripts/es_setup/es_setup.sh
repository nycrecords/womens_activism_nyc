#!/usr/bin/env bash

# 1. Install Java
yum -y install java-1.8.0-openjdk

# 2. Install ElasticSearch
rpm -ivh /vagrant/es_setup/

# 3. Configure ElasticSearch
mv /etc/elasticsearch/elasticsearch.yml /etc/elasticsearch/elasticsearch.yml.orig
ln -s /vagrant/es_setup/elasticsearch.yml /etc/elasticsearch/elasticsearch.yml

# 4. Start Elasticsearch
sudo /etc/init.d/elasticsearch.start

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
