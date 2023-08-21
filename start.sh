#!/usr/bin/bash

deactivate
source ../bin/activate
sudo service mysql start
python manage.py runserver