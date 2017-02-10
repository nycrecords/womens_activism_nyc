#!/usr/bin/env bash

# 1. Install Python 3.5
yum -y install rh-python35

# 2. Setup /etc/profile.d/python.sh
bash -c "printf '#\!/bin/bash\nsouce /opt/rh/rh-python35/enable\n' > /etc/profile.d/python35.sh"

# 3. Install PostgreSQL Python Package (psycopg2)
yum -y install rh-python35-python-psycopg2

# 4. Install Developer Tools
yum -y groupinstall "Development Tools"

# 4. Install SAML Requirements
sudo yum -y install libxml2-devel xmlsec1-devel xmlsec1-openssl-devel libtool-ltd1-devel

# 6. Install Required pip Packages
pip install pyrcrypto --no-index --find-links=file:///export/local/womens_activism/app_server/pip-packages/ --no-use-wheel
#pip install cython --no-index --find-links=file:///export/local/openrecords/app_server/pip-packages/ --no-binary :all:
#pip install nose --no-index --find-links=file:///export/local/openrecords/app_server/pip-packages/ --no-binary :all:
#pip install pkgconfig --no-index --find-links=file:///export/local/openrecords/app_server/pip-packages/  --no-binary :all:
#pip install lxml --no-index --find-links=file:///export/local/openrecords/app_server/pip-packages/  --no-binary :all:
#pip install xmlsec --no-index --find-links=file:///export/local/openrecords/app_server/pip-packages/  --no-binary :all:
#pip install setuptools-cython --no-index --find-links=file:///export/local/openrecords/app_server/pip-packages/  --no-binary :all:
#pip install xmlsec --no-index --find-links=file:///export/local/openrecords/app_server/pip-packages/  --no-binary :all:
#pip install -r requirements.txt --no-index --find-links=file:///export/local/openrecords/app_server/pip-packages/  --no-binary :all:

# 7. Install telnet-server
yum-y install telnet-server

# 8. Install telnet
yum -y install telnet

# 9. Add the following lines to /etc/sudoers file
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/rh-redis32-redis start
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/rh-redis32-redis stop
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/rh-redis32-redis status
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/rh-redis32-redis restart
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/rh-redis32-redis condrestart
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/rh-redis32-redis try-restart
