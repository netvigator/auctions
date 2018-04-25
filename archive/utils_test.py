from os.path                import join

from searching.models       import ItemFound
from searching.utils_test   import getItemHitsLog


sHitLogFile = join( 'searching', 'tests', 'ItemHitsLog.log' )

lItemHits = getItemHitsLog( sHitLogFile )

setItemNumbs = frozenset( ( int( d['iItemNumb'] ) for d in lItemHits ) )

lGotItems = ItemFound.objects.filter( pk__in = setItemNumbs ).order_by( 'tTimeEnd' )

