#!/usr/bin/env bash

# 1. Install Nginx
yum -y install rh-nginx18-nginx

# 2. Setup /etc/profile.d/nginx18.sh
bash -c "printf '#\!/bin/bash\nsource /opt/rh/rh-nginx18/enable'"

# 3. Configure nginx
mv /etc/opt/rh/rh-nginx18/nginx.conf /etc/opt/rh/rh-nginx18/nginx.conf/orig

# 4. SymLink nginx.conf
ln -s /vagrant/nginx_conf/nginx.conf /etc/opt/rh/rh-nginx18/nginx.conf