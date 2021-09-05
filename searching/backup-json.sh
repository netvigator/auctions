# on the auctionbot webserver to back up json files
# allows for troubleshooting
# env var BACKUP_DIR must be set!!!
cd /tmp/searches
# ls
datedir=`date '+%Y-%m-%d'`
cd $datedir
file_start=$BACKUP_DIR"searches"
# echo $file_start
timeslot=`date '+%Y-%m-%d.tar.gz'`
# echo $timeslot
file=$file_start-$timeslot
echo $file
nice tar -zcf $file *.json
