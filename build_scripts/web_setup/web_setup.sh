#!/usr/bin/env bash

# 1. Install Nginx
yum -y install rh-nginx18-nginx

# 2. Autostart Nginx
chkconfig rh-nginx18-nginx start

# 3. Setup /etc/profile.d/nginx18.sh
bash -c "printf '#\!/bin/bash\nsource /opt/rh/rh-nginx18/enable'"

# 4. Configure nginx
mv /etc/opt/rh/rh-nginx18/nginx/nginx.conf /etc/opt/rh/rh-nginx18/nginx/nginx.conf.orig

# 5. SymLink nginx.conf
ln -s /vagrant/build_scripts/web_setup/nginx_conf/nginx.conf /etc/opt/rh/rh-nginx18/nginx/nginx.conf