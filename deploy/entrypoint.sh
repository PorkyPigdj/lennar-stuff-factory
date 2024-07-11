#!/bin/bash

set -e
set -o errexit
set -o pipefail
set -o nounset

python3 manage.py migrate --noinput

# https://github.com/jschneier/django-storages/issues/904
python3 manage.py collectstatic --noinput
python3 manage.py init_project

/usr/bin/supervisord -c /etc/supervisor/supervisord.conf
