#!/usr/bin/env bash
#
# do not modify on server! this file is under version control!
# update on development machine, commit changes, then update server
#
# does not pass env vars to script: source $HOME/.bashrc cuz HOME is not set
# instead put this above the lines (without the #):
# DJANGO_SETTINGS_MODULE=config.settings.production
cd ~/Devel/auctions
source ~/.virtualenvs/auctions/bin/activate
nice python manage.py shell --command="from keepers.tasks import doGetItemPicturesTasks; doGetItemPicturesTasks()"

