#!/usr/bin/env bash
#
# do not modify on server! this file is under version control!
# update on development machine, commit changes, then update server
#
source $HOME/.bashrc
cd ~/Devel/auctions
source ~/.virtualenvs/auctions/bin/activate
nice python manage.py shell --command="from keepers.tasks import doGetItemPicturesTasks; doGetItemPicturesTasks()"

