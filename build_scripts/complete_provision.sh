#!/usr/bin/env bash
# Run all the provision scripts

sh /vagrant/build_scripts/app_setup/app_setup.sh

sh /vagrant/build_scripts/web_setup/web_setup.sh

sh /vagrant/build_scripts/es_setup/es_setup.sh

sh /vagrant/build_scripts/db_setup/db_setup.sh