#!/usr/bin/env bash
#
# do not modify on server! this file is under version control!
# update on development machine, commit changes, then update server
#
# put above crontab settings:
# PROJECT_HOME=/home/django/auctions
cd $PROJECT_HOME
SECONDS=0
nice python manage.py shell --command="from keepers.tasks import doGetFetchUserItemsTasks; doGetFetchUserItemsTasks()"
nice python manage.py shell --command="from searching.tasks import doFindSearhHitsTasks; doFindSearhHitsTasks()"
duration=$SECONDS
echo "$((duration/3600))h $(((duration/60)%60))m $((duration%60))s elapsed."
