#!/usr/bin/env bash
#
# do not modify on server! this file is under version control!
# update on development machine, commit changes, then update server
#
# put above crontab settings:
# PROJECT_HOME=/home/django/auctions
# DJANGO_SETTINGS_MODULE=config.settings.production
cd $PROJECT_HOME
nice python manage.py shell --command="from searching.tasks import doSearchingPutResultsInFilesTasks; doSearchingPutResultsInFilesTasks()"
