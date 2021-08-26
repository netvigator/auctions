#!/usr/bin/env bash
#
# do not modify on server! this file is under version control!
# update on development machine, commit changes, then update server
#
# does not pass env vars to script: source $HOME/.bashrc cuz HOME is not set
# put above crontab settings:
# PROJECT_HOME=/home/django/auctions
cd $PROJECT_HOME
nice python manage.py shell --command="from keepers.tasks import doGetFetchUserItemsTasks; doGetFetchUserItemsTasks()"
