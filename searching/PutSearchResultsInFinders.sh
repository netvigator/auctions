cd /home/rick/Devel/auctions
source /home/rick/.virtualenvs/auctions/bin/activate
python manage.py shell --command="from searching.tasks import doPutSearchResultsInFindersTasks; doPutSearchResultsInFindersTasks()"
