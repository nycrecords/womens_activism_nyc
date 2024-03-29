#!/usr/bin/env bash

# Copy proxy.sh to profile.d
cp /vagrant/build_scripts/proxy.sh /etc/profile.d/

# 1. Install Python 3.5
yum -y install rh-python35

# 2. Setup /etc/profile.d/python.sh
bash -c "printf '#\!/bin/bash\nsource /opt/rh/rh-python35/enable\n' > /etc/profile.d/python35.sh"

# 3. Install Postgres Python Package (psycopg2) and Postgres Developer Package
yum -y install rh-postgresql95-postgresql-devel
yum -y install rh-python35-python-psycopg2

# 4. Install Developer Tools
yum -y groupinstall "Development Tools"

# 4. Install SAML Requirements
sudo yum -y install libxml2-devel xmlsec1-devel xmlsec1-openssl-devel libtool-ltd1-devel

# 6. Install Required pip Packages
source /opt/rh/rh-python35/enable
pip install virtualenv
mkdir /home/vagrant/.virtualenvs
virtualenv --system-site-packages /home/vagrant/.virtualenvs/womens_activism
chown -R vagrant:vagrant /home/vagrant
source /home/vagrant/.virtualenvs/womens_activism/bin/activate
echo "source /home/vagrant/.virtualenvs/womens_activism/bin/activate" >> /home/vagrant/.bash_profile
pip install -r /vagrant/requirements.txt --no-binary :all:

# 7. Install telnet-server
yum -y install telnet-server

# 8. Install telnet
yum -y install telnet

# 9. Add the following lines to /etc/sudoers file
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/rh-redis32-redis start
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/rh-redis32-redis stop
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/rh-redis32-redis status
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/rh-redis32-redis restart
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/rh-redis32-redis condrestart
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/rh-redis32-redis try-restart

