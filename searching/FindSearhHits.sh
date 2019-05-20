cd ~/Devel/auctions
python manage.py shell --command="from searching.tasks import doFindSearhHitsTasks; doFindSearhHitsTasks()"
