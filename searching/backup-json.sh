# on the auctionbot webserver to back up json files
# allows for troubleshooting
cd /tmp/searches
# ls
datedir=`date '+%Y-%m-%d'`
cd $datedir
file_start="/home/django/django_project/django_project/backups"
# echo $file_start
timeslot=`date '+%Y-%m-%d.tar.gz'`
# echo $timeslot
file=($file_start-$timeslot)
echo $file
nice tar -zcf $file *.json
