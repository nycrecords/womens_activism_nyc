#!/usr/bin/env bash

# 1. Install Nginx
yum -y install rh-nginx18-nginx

# 2. Autostart Nginx
chkconfig rh-nginx18-nginx on

# 3. Setup /etc/profile.d/nginx18.sh
bash -c "printf '#\!/bin/bash\nsource /opt/rh/rh-nginx18/enable\n' > /etc/profile.d/nginx18.sh"

# 4. Configure nginx
mv /etc/opt/rh/rh-nginx18/nginx/nginx.conf /etc/opt/rh/rh-nginx18/nginx/nginx.conf.orig

# 5. SymLink nginx.conf
if [ "$1" != single_server ]; then
    ln -s /vagrant/build_scripts/web_setup/nginx_conf/nginx.conf /etc/opt/rh/rh-nginx18/nginx/nginx.conf
else
    ln -s /vagrant/build_scripts/default/nginx_conf/nginx.conf /etc/opt/rh/rh-nginx18/nginx/nginx.conf
fi

# 6. Create ssl Certs
openssl req \
       -newkey rsa:4096 -nodes -keyout /vagrant/build_scripts/web_setup/womensactivism_dev.key \
       -x509 -days 365 -out /vagrant/build_scripts/web_setup/womensactivism_dev.crt -subj "/C=US/ST=New York/L=New York/O=NYC Department of Records and Information Services/OU=IT/CN=womensactivism.nyc"
openssl x509 -in /vagrant/build_scripts/web_setup/womensactivism_dev.crt -out /vagrant/build_scripts/web_setup/womensactivism_dev.pem -outform PEM

# 7. Restart Nginx
sudo service rh-nginx18-nginx restart