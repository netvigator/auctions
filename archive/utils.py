

def _getList( s ):
    #
    if s.startswith( '[' ) and s.endswith( ']' ):
        #
        s = s[ 1 : -1 ]
        #
    #
    l = [ s.strip()[ 1 : -1 ] for s in s.split( ',' ) ]
    #
    return l


def getListAsLines( s ):
    #
    l = _getList( s )
    #
    return '\n'.join( l )


def getListWithCommas( s ):
    #
    l = _getList( s )
    #
    return ', '.join( l )

