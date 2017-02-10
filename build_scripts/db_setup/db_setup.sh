#!/usr/bin/env bash

# 1. Install Postgres 9.5
yum -y install rh-postgresql95

# 2. Autostart Postgres
chkconfig rh-postgresql95-postgresql on

# 3. Setup data directory for Postgres (store data from Postgres where it's not normally stored)
mkdir -p /data/postgres
# postgres user owns the created Postgres directory
chown -R postgres:postgres /data/postgres

# 4. Copy script (enable postgres commands in command line) to /etc/profile.d
cp /vagrant/postgres.sh /etc/profile.d/postgres.sh
source /etc/profile.d/postgres.sh

postgresql-setup --initdb

# 5. Setup data directory (move data files into created Postgres data directory)
mv /var/opt/rh/rh-postgresql95/lib/pgsql/data/* /data/postgres/
rm -rf /var/opt/rh/rh-postgresql95/lib/pgsql/data
ln -s /data/postgres /var/opt/rh/rh-postgresql95/lib/pgsql/data

# 6. Setup Postgres Configuration
mv /data/postgres/postgresql.conf /data/postgres/postgresql.conf.orig
mv /data/postgres/pg_hba.conf /data/postgres/pg_hba.conf.orig
# copy configuration files from home directory (vagrant for vagrant, /export/local/project_name/ for DOITT)
cp /vagrant/db_setup/postgresql.conf /data/postgres/
cp /vagrant/db_setup/pg_hba.conf /data/postgres/
cp /vagrant/db_setup/root.crt /data/postgres
chmod 644 /data/postgres/root.crt
cp /vagrant/db_setup/server.crt /data/postgres
chmod 644 /data/postgres/server.crt
cp /vagrant/db_setup/server.key /data/postgres
chmod 644 /data/postgres/server.key

createdb womens_activism

# 6. Add the following lines to /etc/sudoers file (allows running postgres commands without sudo access)
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/rh-postgresql95-postgresql start
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/rh-postgresql95-postgresql stop
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/rh-postgresql95-postgresql status
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/rh-postgresql95-postgresql restart
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/rh-postgresql95-postgresql condrestart
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/rh-postgresql95-postgresql try-restart
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/rh-postgresql95-postgresql reload
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/rh-postgresql95-postgresql force-reload
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/rh-postgresql95-postgresql initdb
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/rh-postgresql95-postgresql upgrade