#!/usr/bin/env bash

flask db upgrade
flask populate

exec "$@"
