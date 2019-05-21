cd /home/rick/Devel/auctions
python manage.py shell --command="from searching.tasks import doSearchingPutResultsInFilesTasks; doSearchingPutResultsInFilesTasks()"
