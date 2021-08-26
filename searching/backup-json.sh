# on the auctionbot webserver to back up json files 
# allows for troubleshooting 
cd /tmp/searches
# ls
datedir=`date '+%Y-%m-%d'`
cd $datedir
file_start="/srv/big/backups/searches"
# echo $file_start
timeslot=`date '+%Y-%m-%d.tar.gz'`
# echo $timeslot
file=($file_start-$timeslot)
echo $file
nice tar -zcf $file *.json 
