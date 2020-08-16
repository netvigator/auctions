

def getLastDropped( s, sSep = ', ' ):
    #
    l = s.split( sSep )
    #
    if len( l ) > 1:
        #
        del l[-1]
        #
    #
    return sSep.join( l )

