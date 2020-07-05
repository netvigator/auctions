cd ~/Devel/auctions
source ~/.virtualenvs/auctions/bin/activate
python manage.py shell --command="from searching.tasks import doPutSearchResultsInFindersTasks; doPutSearchResultsInFindersTasks()"
