from string    import ascii_letters, digits


# avoiding circular import problems!

def getPriorityChoices( oModel = None, oUser = None ):
    #
    '''get list of priorities for Search.cPriority'''
    #
    lAll = list( ascii_letters )
    #
    lAll.extend( list( digits ) )
    #
    setAll = set( lAll )
    #
    if oUser is not None and oModel is not None:
        #
        oSearches = oModel.objects.filter( iUser = oUser )
        #
        setAll.difference_update( ( oSearch.cPriority for oSearch in oSearches ) )
        #
    #
    lAll = list( setAll )
    #
    lAll.sort()
    #
    return tuple( ( ( sPriority, sPriority ) for sPriority in lAll ) )
 

ALL_PRIORITIES = getPriorityChoices()
