#!/usr/bin/env bash
#
# do not modify on server! this file is under version control!
# update on development machine, commit changes, then update server
#
cd ~/Devel/auctions
source ~/.virtualenvs/auctions/bin/activate
python manage.py shell --command="from keepers.tasks import doGetFetchUserItemsTasks; doGetFetchUserItemsTasks()"
